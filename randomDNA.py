import sys
import random
import matplotlib.pyplot as plot
from locAL import locAL
import os

# ok so after running a computer for 2 nights suddenly nothing worked until i changed my original code weird
# now it processes even slower :(
def build_seq(num_seq, seq_len):
   #print("built")
   seqs = []
   # could make nt for prokary and eukary so one with T one with U
   nt = ['A','C','G','T']
   for _ in range(num_seq):
      seq =''.join(random.choices(nt, k=seq_len))
      seqs.append(seq)
   return seqs

def Expected_align_lens(x):
   return sum(x)/len(x)

def get_freq(seqs):
   #print("frequencies computed")
   freq = {}
   nts = 0
   for seq in seqs:
      for nt in seq:
         freq[nt] = freq.get(nt,0) + 1
         nts += 1
   nt_freq = {}
   for nt, num in freq.items():
      nt_freq[nt] = num/nts
   return nt_freq

#geeksforgeeks.org
def write_fasta(seqs, filename):
   with open(filename, 'w') as f:
      for i, seq in enumerate(seqs):
         f.write(f">seq{i+1}\n")
         f.write(f"{seq}\n")
#from jupyter notebook for CSE 185
def histo(lens, name, save=False):
   plot.hist(lens, bins=max(1, len(lens)//10))
   plot.xlabel("length of local alignment")
   plot.ylabel("frequency")
   plot.title(name)
   if save:
        save_dir = "plots"
        if not os.path.exists(save_dir):
         os.mkdir(save_dir)
        save_path = os.path.join(save_dir, f"{name}.png")
        plot.savefig(save_path)
        plot.show()
        plot.close()
   else:
      plot.show()
      plot.close()

#this will take an extremely extremely long time unless i can find a way to do it using multiple cores
#not going to write results of using it to file as then can't see if it is still running or not,
#my print statements is the only way to know it is running as it is very very very slooooow
# function. I let it run overnight and it was still not done just to warn you.
# maybe i made it harder than need be, so far approaching 24hrs of running  :(
# ok now simplifying it greatly can't wait another week 
def plot_mean(temps):
   means = []
   vals = [-100,-10,-1,0]
   for val in vals:
      aligns = []
      count = 0
      for file in temps:
         count +=1
         align = locAL(file, 1, 7*val, val/2)
         aligns.append(align[1])
         print("processed",count)
      mean = Expected_align_lens(aligns)
      means.append(mean)
   histo(means, "Mean alignment lengths for various parameter settings", save=True)
   for file in temps:
      os.remove(file)
# note the graphing will take like a minute so just press enter to not graph
#delete the fastas generated to still have space
def randomDNA(num_seq,seq_len):
   seqs = build_seq(num_seq*2,seq_len)
   freqs = get_freq(seqs)
   #print("freqs:",freqs)
   count = 0
   aligns = []
   temp_files = []
   for i in range(0,num_seq*2,2):
      temp_file = f"seq_{i//2}.fasta"
      print(f"sequence {i}:\n{seqs[i]}")
      print(f"sequence {i+1}:\n{seqs[i+1]}")
      if i+1 < num_seq*2:
         write_fasta([seqs[i], seqs[i+1]], temp_file)
         temp_files.append(temp_file)
   print("freqs:",freqs)
   plot = input("Type 'm' if you wish to plot mean values of lP(n): ")
   if plot == "m":
      print("type 'y' for yes or 'n' for no")
      #final warning in case m was typed by accident
      confirm = input("this will take a long time do you still wish to proceed?:")
      if confirm == 'y':
         print("ok, ...., you were warned")
         plot_mean(temp_files)
      elif confirm == 'n':
         for file in temp_files:
            os.remove(file)
   else:
      asked = 1
      while(asked <= 2):
         #print("running?")
         #print("asked:",asked)
         if(input("Type 'd' to delete temporary files:") == "d"):
            break
         count = 0
         aligns.clear()
         if input(f"Type 'p' if you wish to plot parameter {asked}:\n") =="p":
            print("now using locAL, provide -m -s -d")
            m = float(input("-m:"))
            print(m)
            s = float(input("-s:"))
            print(s)
            d = float(input("-d:"))
            print(d)
            for file in temp_files:
               #print("count:",count)
               #print("in for loop")
               count +=1
               #print("count:",count)
               align = locAL(file, m, s, d)
               #print("a")
               aligns.append(align[1])
            # to tell it is still doing something 
               print("processed",count)
            histo(aligns, f"P{asked}", save=True)
            P = Expected_align_lens(aligns)
            print(f"Expected alignment length for P{asked}:",P)
         asked +=1
      for file in temp_files:
         os.remove(file)
   
if __name__ == "__main__":
   print("sys.argv:", sys.argv)
   if len(sys.argv) < 3:
      print("Format: python randomDNA.py <num of seqs> <len of seqs>")
      sys.exit(1)
   num_seq = int(sys.argv[1])
   seq_len = int(sys.argv[2])
   randomDNA(num_seq,seq_len)