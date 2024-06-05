def read_fasta(file_path):
    seqs = []
    with open(file_path, 'r') as file:
        seq = []  # Initialize an empty list to store each sequence
        for line in file:
            line = line.strip()
            if line.startswith('@') or line.startswith('>'):
                if seq:  # If there's a sequence in progress, append it to seqs
                    seqs.append(''.join(seq))
                    seq = []  # Reset seq to start storing a new sequence
            else:
                seq.append(line)  # Append the current line to the sequence
        if seq:  # If there's a sequence left after the loop ends, append it to seqs
            seqs.append(''.join(seq))
    return seqs