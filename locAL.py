import sys
from read_fasta import read_fasta
import numpy as np
#honestly surprised this was enough to get an answer for prob 4 
#this was a pain to code at least 8 hrs on doing this over and over
#to make faster and this make randomDNA faster had to consort chatGPT,
#learned about something called pool which should speed this up. cuz otherwise 5 min by original program
#this exsists for sake of comparison as what I came up with
def locAL(seqfile,match,mismatch,indel,see = False):
   #print("running")
   seqs = read_fasta(seqfile)
   seq1 = seqs[0]
   seq2 = seqs[1]
   #print("seq1:",seq1)
   #print("seq2:",seq2)
   m = len(seq1)
   n = len(seq2)
   #print("m:",m)
   #print("n:",n)
   scoring = np.zeros((m + 1, n + 1),dtype=int)
   max_score = 0
   max_pos = (0,0)
   align_seq1 = ""
   align_seq2 = ""
   
   diag_score = np.zeros((m+1, n+1), dtype=int)
   up_score = np.zeros((m+1, n+1), dtype=int)
   L_score = np.zeros((m+1, n+1), dtype=int)

   for i in range(1,m+1):
      #print("for i:",i)
      for j in range(1,n+1):
         #print("for j:",j)
         if seq1[i-1]==seq2[j-1]:
            score = match
         else:
            score = mismatch
         
         diag_score[i][j] = scoring[i - 1][j-1] + score
         up_score[i][j] = scoring[i - 1][j] + indel
         L_score[i][j] = scoring[i][j-1] + indel

         scoring[i,j] = max(0,diag_score[i,j],up_score[i,j],L_score[i,j])

         #print(f"i: {i}, j: {j}, scoring[i, j]: {scoring[i, j]}")

         if scoring[i,j] > max_score:
            max_score = scoring[i][j]
            max_pos = (i,j)
         
   i,j = max_pos
   while(i > 0 and j > 0) and scoring[i,j] != 0:
      #if i == 1: print("while reached")
      if scoring[i][j] == diag_score[i][j]:
         print('diag')
         align_seq1 += seq1[i-1]
         align_seq2 += seq2[j-1]
         i -= 1
         j -= 1
      elif scoring[i][j] == up_score[i][j]:
         print('up')
         align_seq1 += seq1[i-1]
         align_seq2 += '-'
         i -= 1
      elif scoring[i][j] == L_score[i][j]:
         print('left')
         align_seq1 += '-'
         align_seq2 += seq2[j-1]
         j -= 1
   print("Alignment Sequence 1:", align_seq1)
   print("Alignment Sequence 2:", align_seq2)
   print("Sequence 1:", seq1)
   print("Sequence 2:", seq2)
   if see:
      #print("Score of the best local-alignment:", max_score)
      #print("Length of the best local-alignment:", len(align_seq1))
      #print("the alignment:")
      #print(align_seq1)
      #print(align_seq2)
      return max_score, len(align_seq1), align_seq1, align_seq2
   else:
      #print("Score of the best local-alignment:", max_score)
      #print("Length of the best local-alignment:", len(align_seq1))
      return max_score, len(align_seq1),"",""

if __name__ == "__main__":
   if len(sys.argv) < 7:
      print("Format: python locAL.py <seqfile> -m <match> -s <mismatch> -d <indel> -a(optional)")
      sys.exit(1)
   seqfile = sys.argv[1]
   match = float(sys.argv[sys.argv.index('-m') + 1])
   mismatch = float(sys.argv[sys.argv.index('-s') + 1])
   indel = float(sys.argv[sys.argv.index('-d') + 1])
   see = '-a' in sys.argv
   align_score, align_len, align_seq1, align_seq2 = locAL(seqfile, match, mismatch, indel, see)
   #locAL(seqfile, match, mismatch, indel, see)
   print("Score of the best local-alignment:", align_score)
   print("Length of the best local-alignment:", align_len)
   if see:
      print("the alignment:")
      print(align_seq1)
      print(align_seq2)

