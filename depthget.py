#!/usr/bin/env python
import pandas as pd
import os
import argparse
import sys
import glob
import subprocess
import shutil

# Version
_verion_= "0.1"

# Argparse Setup
parser = argparse.ArgumentParser(description="Parses bam files to extract information about individual base coverage.")
parser.add_argument("-i", "--input", required=True, help="Path to directory containing snippy subdirectories.")
parser.add_argument("-l", "--length", required=True, type=int, help="Length of reference genome in base pairs")
parser.add_argument("-o", "--output", required=True, help="Output path.")
args = parser.parse_args()

# Welcome
print()
print('###################')
print('Welcome to DepthGet!')
print('###################')

# Directory orientation
invoked_from = os.getcwd()
os.chdir(args.input)
snippy_directories = os.getcwd()
os.chdir(invoked_from)
if not os.path.exists(args.output):
    os.makedirs(args.output)
os.chdir(args.output)
output_directory = os.getcwd()

# Create temporary directory
temp_path = (output_directory + '/temp')
if not os.path.exists(temp_path):
    os.makedirs(temp_path)
os.chdir(temp_path)
temp_dir = os.getcwd()
os.chdir(invoked_from)

# List comprehension
snippy = glob.glob(os.path.join(snippy_directories, "*", ""))
sample_names = [x.replace((snippy_directories), '').replace('/','') for x in snippy]
bam_files = [x + 'snps.bam' for x in snippy]
depth_files = [temp_dir + '/' + x + '.tsv' for x in sample_names]

# Depth calculation
print()
print('Commencing depth-getting...')
print()
for bam, tsv in zip(bam_files, depth_files):
    print('Writing sample depth to:', tsv)
    samtools = ['samtools', 'depth', '-a', bam]
    with open(tsv, "wb") as outfile:
        subprocess.call(samtools, stdout=outfile)


# TSV Processing
print()
print('Successfully depth-got!')
print()
print('Commencing tsv processing...')
final = (output_directory + '/output.csv')
numbers = (temp_dir + '/numbers.csv')
with open(numbers, 'w') as num:
    for i in range(1, args.length):
        num.write('%s,\n'%i)
    num.close
df = pd.read_csv(numbers, header=None)
df.columns = ['Position', 'Remove']
df = df.drop(columns=['Remove'])
for tsv_in, sample in zip(depth_files, sample_names):
    print('Parsing', sample)
    temp_df = pd.read_csv(tsv_in, sep='\t', header=None)
    temp_df.columns = ['ref', 'pos', sample]
    df[sample] = temp_df[sample]
print()
print('Saving final output to:', final)
df.to_csv(final, index=False)
print()
print('Done!')
print()
print('Removing temporary directory...')
shutil.rmtree(temp_dir)

# Thank you, come again.
print()
print()
print('Author: www.github.com/stevenjdunn')
print()
print()
print('###################')
print('DepthGet Completed!')
print('###################')
