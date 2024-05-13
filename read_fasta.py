def read_fasta(file_path):
   seqs = []
   with open(file_path, 'r') as file:
      seq = []
      for line in file:
         line = line.strip()
         if line.startswith('>'):
            if seq:
               seqs.append(''.join(seq))  
            seq = []
         else:
            seq.append(line.strip())
      if seq:
         seqs.append(''.join(seq))
   return seqs