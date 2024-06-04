# Large Sequence K-mer Counting

This tool is used to count k-mers in large sequences of DNA similar to the well-known program jellyfish (seen in Lab 2, Part 1).
The tool operates using the external library mmh3 for efficient hashing for k-mer storage.
The tool contains the following submethods:
## Main: acts primative help function and allows users to know all other functions calls that can be made. basically our -h help command our only actual properly working one 
## Count: Counts all k-mers in the sequence
Arguments:
 - -m: K-mer length  (default = 21)
 - -s: Hash table size (default = 1000000)
 - -t: Number of threads to run the tool (default = 4)
 - -o: outputfile of user choice 
 - file: Input file
 - -C: Count forward and reverse of sequence as the same (default = false, i.e. not present no '-C' typed)

for some reason the usage prints it in a way that implies file as last argument even though this is not how it is set up. I would change code to match usage but it refuses to accept anything but -c as pylance does not like "Non-default argument follows default argument" so the printed usage is misleading but don't know how to fix it. this is why i usually define my own arg parcers
usage should be -h, -m kmer_len , -s table_size , -t threads , -o output, file, -C

## Histo: Computes a histogram of k-mer occurences
Arguments:
- input_file: The input file
- -L: Low count bucket value (default=0)
- -H: High count bucket value (default=100)
- -i: Increment for bucket value (default=10)

again like in case of count it is not reflecting accurately so I guess just know order is same as seen in readme for all modules. assume items that are not labeled like -item expect no prefix identifier. ex : the input file just type the file don't type "input_file" before it. 
again this is why I usually use my own parcers as I can make it work exactly as I want.
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
- num_seq: number of sequences to generate (default = 21)
- seq_len: length of the sequences to generate (default = 200)
- outfile: the file to save these generated sequences to
- uno_prob: probability of generating a single sequence, basically output similar to sample_DNA.txt (default = 0.5)

for giving arguments just give in order seen here if i want say 50 sequces of len 100 nt to outfile called bat.txt with uno_prob of 50% I will type python randomDNA.py 50 100 bat.txt 0.5
if users desire I will change it to be similar to rest. this is a module unique from jellyfish so did not try to follow jellyfish's convention on this one, probably should have said something my bad
