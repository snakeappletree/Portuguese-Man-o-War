import mmh3
import argparse
import threading
#from collections import defaultdict < potentially currently i store them as hashvalues

# Read database file
def read_database(file_name):
   database = ""
   with open(file_name, "r") as dna_file:
      for line in dna_file:
         if line.startswith('>') == False: 
            database +=line.strip()
      return database

# Count unique kmers
def count(kmer_len,table_size,threads,output,file,c=False):
   database = read_database(file)
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
               kmer_count[hash_value][1] += 1
            else:
               if elements >= table_size:
                  return  # Stop processing if table size limit reached
               kmer_count[hash_value] = (kmer,1)
               elements += 1

   chunk_size = len(database) // threads
   threads_list = []
   for i in range(threads):
      start = i * chunk_size
      end = (i + 1) * chunk_size if i < threads - 1 else len(database)
      thread = threading.Thread(target=count_chunk, args=(database[start:end],))
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

   num_kmers=count(args.m,args.s, args.t,args.o,args.file,args.C)
   print(num_kmers)

if __name__ == "__main__":
   main()