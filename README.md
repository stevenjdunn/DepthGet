# DepthGet

Ridiculously niche use-case. Produces a file containing all base positions and their respective coverage from a group of Snippy subdirectories.

## Requirements
- Python3
- Samtools
- Pandas

### How
depthget.py -i directory_containing_snippy_output -l length_of_ref_genome_in_bp -o output_directory

### Quirks
You can't invoke it from the input directory. It's probably also best to put your output directory outside of the input directory. ¯\\_(ツ)_/¯

### Why?
So we can get information on gene coverage from a very large genomic dataset. 
