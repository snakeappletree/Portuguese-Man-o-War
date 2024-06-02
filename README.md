# Large Sequence K-mer Counting

This tool is used to count k-mers in large sequences of DNA similar to the well-known program jellyfish (seen in Lab 2, Part 1).
The tool operates using the external library mmh3 for efficient hashing for k-mer storage.
The tool contains the following submethods:

## Count: Counts all k-mers in the sequence
Arguments:
 - -k: K-mer length
 - -s: Hash table size
 - -t: Number of threads to run the tool
 - -C: Count forward and reverse of sequence as the same
 - file: Input file

## Histo: Computes a histogram of k-mer occurences
Arguments:
- input_file: The input file
- -L: Low count bucket value
- -H: High count bucket value
- -i: Increment for bucket value

## Dump: Outputs all k-mer counts
Arguments: 
- input_file: Input file containing k-mers and counts
- -c, --column: Output in column format
- -L, --low: Minimum count of k-mers to include (Default = 1)
- -U, --high: Maximum count of k-mers to include (Default = inf)

## Query: Queries the counts for a specific k-mer
Arguments:
- input_file: Input file containing k-mers and counts
- kmers: K-mers to query
- -s, --sequence_files: FASTA or FASTQ files to read sequences from

### randomDNA : optional bonus tool to generate data for testing main tool
Arguments:
- num_seq: number of sequences to generate
- seq_len: length of the sequences to generate
- outfile: the file to save these generated sequences to
- uno_prob: probability of generating a single sequence, basically output similar to sample_DNA.txt
