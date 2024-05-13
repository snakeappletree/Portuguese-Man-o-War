import sys
from read_fasta import read_fasta
import numpy as np
def fff(seqfile, match, mismatch, indel, see=False):
    seqs = read_fasta(seqfile)
    seq1 = seqs[0]
    seq2 = seqs[1]
    m = len(seq1)
    n = len(seq2)

    # Initialize variables to track maximum score, its position, and alignment sequences
    max_score = 0
    max_pos = (0, 0)

    # Initialize two rows for scoring
    curr_row = np.zeros(n + 1, dtype=int)
    prev_row = np.zeros(n + 1, dtype=int)
    score_row = []

    # Debugging output: Print scores of cells around the maximum score position
    print("Scores of cells around the maximum score position:")
    for i in range(max_pos[0] - 1, max_pos[0] + 2):
        for j in range(max_pos[1] - 1, max_pos[1] + 2):
            print(f"({i},{j}): {curr_row[j]}")

    for i in range(1, m + 1):
        for j in range(1, n + 1):

            # Calculate scores for diagonal, up, and left movements
            diag = prev_row[j - 1] + (match if seq1[i - 1] == seq2[j - 1] else mismatch)
            up = prev_row[j] + indel
            left = curr_row[j - 1] + indel

            # Update current row with the maximum score
            curr_row[j] = max(0,diag, up, left)
            
            # Update maximum score and position
            if curr_row[j] > max_score:
                max_score = curr_row[j]
                max_pos = (i, j)
                

        # Swap current and previous rows
        prev_row, curr_row = curr_row, prev_row

    # Debugging output: Print maximum score and position
    print("Maximum Score:", max_score)
    print("Maximum Position:", max_pos)
   
    # Perform traceback for the best local alignment
    i, j = max_pos
    aligns = []
    while True:
        print("i:",i,"j:",j)
        align_seq1 = ""
        align_seq2 = ""
        if curr_row[j]==0 or i==j:
            break
    
        while (i > 0 or j > 0 )and i!=j and curr_row[j] !=0:
            print("curr_row[j]:",curr_row[j])
            print("i:",i,"j:",j)

            # Determine the operation (match/mismatch, insertion, deletion)
            if curr_row[j] == prev_row[j-1] + (match if seq1[i-1] == seq2[j-1] else mismatch):
                print("match/mismatch")
                align_seq2 = seq2[j-1] + align_seq2
                align_seq1 = seq1[i-1] + align_seq1
                i = i-1
                j = j-1
            elif curr_row[j] == prev_row[j] + indel:
                print("insertion")
                align_seq1 = seq1[i-1] + align_seq1
                align_seq2 = "-" + align_seq2
                i = i-1
            elif curr_row[j] == curr_row[j - 1] - indel:
                print("deletion")
                align_seq1 = "-" + align_seq1
                align_seq2 = seq2[j-1] + align_seq2
                j = j-1

            # Update curr_row[j] within the loop
            curr_row[j] = max(prev_row[j - 1] + 
                (match if seq1[i-1] == seq2[j-1] else mismatch),
                    prev_row[j] + indel,curr_row[j - 1] + indel)
               
        # Store the alignment found during this iteration
        aligns.append((align_seq1, align_seq2))

    # Reverse the alignment sequences since they were built from the end
    aligns = [(align_seq1[::-1], align_seq2[::-1]) for align_seq1, align_seq2 in aligns]    

    # Debugging output: Print alignment sequences
    print("Alignment Sequence 1:", aligns[0][0])
    print("Alignment Sequence 2:", aligns[0][1])

    # Debugging output: Print input sequences
    print("Sequence 1:", seq1)
    print("Sequence 2:", seq2)

    # Print or return alignment information
    if see:
        return max_score, len(aligns[0][0]), aligns[0][0], aligns[0][1]
    else:
        return max_score, len(aligns[0][0]), "", ""
if __name__ == "__main__":
    if len(sys.argv) < 7:
        print("Format: python locAL.py <seqfile> -m <match> -s <mismatch> -d <indel> -a(optional)")
        sys.exit(1)
    seqfile = sys.argv[1]
    match = float(sys.argv[sys.argv.index('-m') + 1])
    mismatch = float(sys.argv[sys.argv.index('-s') + 1])
    indel = float(sys.argv[sys.argv.index('-d') + 1])
    see = '-a' in sys.argv
    align_score, align_len, align_seq1, align_seq2 = fff(seqfile, match, mismatch, indel, see)
    print("Score of the best local-alignment:", align_score)
    print("Length of the best local-alignment:", align_len)
    if see:
        print("the alignment:")
        print(align_seq1)
        print(align_seq2)


