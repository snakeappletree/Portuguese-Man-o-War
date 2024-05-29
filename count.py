import mmh3
import argparse
import threading
from read_database import read_database
from read_fasta import read_fasta

# To determine if use read_fasta or read_database
def Format(file_path):
   with open(file_path, 'r') as file:
      count = 0
      for line in file:
         if line.startswith(">"):
            count +=1
            if count > 1:
               reader = "read_fasta"
               return reader
      if count == 1:
         reader = "read_database"
         return reader

# Count unique kmers
def count(kmer_len,table_size,threads,output,file,c=False):
   file_format = Format(file)
   if file_format == 'read_database':
      data = read_database(file)
   elif file_format == 'read_fasta':
      data = ''.join(read_fasta(file))
   else:
      raise ValueError("Unable to determine file format.")
   kmer_count={}
   elements=0
   lock = threading.Lock()
   def write_out(kmer_count,output):
      with open(output, 'w') as f:
         for hash_value, (seq, freq) in kmer_count.items():
            f.write(f"{hash_value}: ({seq}, {freq})\n")

   def count_chunk(chunk):
      nonlocal kmer_count, elements
      for i in range(len(chunk) - kmer_len + 1):
         kmer = chunk[i:i+kmer_len]
         hash_value = mmh3.hash(kmer)
         if c:
            rev_hash_value = mmh3.hash(kmer[::-1])
            hash_value = min(hash_value, rev_hash_value)
         with lock:
            if hash_value in kmer_count:
               D_kmer = list(kmer_count[hash_value])
               D_kmer[1] += 1  # Increment frequency
               kmer_count[hash_value] = tuple(D_kmer)  # Convert back to tuple
            else:
               if elements >= table_size:
                  return  # Stop processing if table size limit reached
               #print(f"New k-mer: {kmer}, Hash: {hash_value}")
               kmer_count[hash_value] = (kmer,1)
               elements += 1

   chunk_size = len(data) // threads
   threads_list = []
   for i in range(threads):
      start = i * chunk_size
      end = (i + 1) * chunk_size if i < threads - 1 else len(data)
      thread = threading.Thread(target=count_chunk, args=(data[start:end],))
      thread.start()
      threads_list.append(thread)

   for thread in threads_list:
      thread.join()
   write_out(kmer_count,output)
   return kmer_count

def main():

   # Add arguments
   parse = argparse.ArgumentParser(description='Count k-mers in a DNA sequence.')
   parse.add_argument('-m',metavar='kmer_len',type=int,default=21,help="length of k-mers (default:21)")
   parse.add_argument('-s',metavar='table_size',type=int,default=1000000,help="number of elements in hash table (default:1000000)")
   parse.add_argument('-t',metavar='threads',type=int,default=4,help="number of threads to use (default:4)")
   parse.add_argument('-o',metavar='output',type=str,help="output file containing DNA sequences" )
   parse.add_argument('file', type=str, help="input file containing DNA sequence")
   parse.add_argument('-C', action='store_true', help="count with forward and reverse kmers as same")

   # Parse arguments
   args = parse.parse_args()

   count(args.m,args.s, args.t,args.o,args.file,args.C)

   #num_kmers=count(args.m,args.s, args.t,args.o,args.file,args.C)
   #print(num_kmers)

if __name__ == "__main__":
   main()