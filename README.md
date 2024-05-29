# Large Sequence K-mer Counting

This tool is used to count k-mers in large sequences of DNA similar to the well-known program jellyfish (seen in Lab 2, Part 1).
The tool operates using the external library mmh3 for efficient hashing for k-mer storage.
The tool contains the following submethods:

## Count: Counts all k-mers in the sequence
Arguments:
 - -k: K-mer length
 - -s: Hash table size
 - -t: Number of threads to run the tool
 - -C: Ignore directionality modifier
 - file: Input file

## Histo: Computes a histogram of k-mer occurences
Arguments:
- input_file: the input file

## Dump: Outputs all k-mer counts
//TODO

## Query: Queries the counts for a specific k-mer
//TODO
