import random
import argparse

#To build the specified number of sequences of the specified length
def build_seq(num_seq, seq_len, uno_prob):
   seqs = []
   nt = ['A', 'C', 'G', 'T'] # could add 'U' for RNA but ehh maybe some other time
   if random.random() < uno_prob:
      seq = ''.join(random.choices(nt, k=num_seq * seq_len))
      for i in range(0, len(seq), seq_len):
         seqs.append(seq[i:i+seq_len])
   else:
      for _ in range(num_seq):
         seq = ''.join(random.choices(nt, k=seq_len))
         seqs.append(seq)
   return seqs

#To write the sequences made from calling build_seq(arguments) to the file specified
def write_fasta(seqs, filename):
   with open(filename, 'w') as f:
      for i, seq in enumerate(seqs):
         f.write(f">seq{i+1}\n")
         f.write(f"{seq}\n")

def main():
   # Add arguments
   parse = argparse.ArgumentParser(description='generate random fasta file for purpose of testing')
   parse.add_argument('num_seq', type=int, default=21, help="number of sequences to generate")
   parse.add_argument('seq_len', type=int, default=200, help="length of the sequences to generate")
   parse.add_argument('outfile', type=str, help="the file to save these generated sequences to")
   parse.add_argument('uno_prob', type=float, default=0.5, help="probability of generating a single sequence")
   # Parse arguments
   args = parse.parse_args()
   # Generate random sequences
   seqs = build_seq(args.num_seq, args.seq_len, args.uno_prob)
   # Write sequences to file
   write_fasta(seqs, args.outfile)
   print(f"Random DNA sequences generated and saved to {args.outfile}")

if __name__ == "__main__":
   main()