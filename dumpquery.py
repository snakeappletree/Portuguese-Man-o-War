import argparse
import hashlib

def parse_arguments():
    parser = argparse.ArgumentParser(description="K-mer counting tool")
    subparsers = parser.add_subparsers(dest="command")

    # Dump subcommand
    dump_parser = subparsers.add_parser("dump", help="Dump k-mers and their counts")
    dump_parser.add_argument("input_file", type=str, help="Input file containing k-mers and counts")
    dump_parser.add_argument("output_file", type=str, help="Output FASTA file")
    dump_parser.add_argument("-L", "--low", type=int, default=1, help="Minimum count of k-mers to include")
    dump_parser.add_argument("-U", "--high", type=int, default=float('inf'), help="Maximum count of k-mers to include")

    # Query subcommand
    query_parser = subparsers.add_parser("query", help="Query k-mers and their counts")
    query_parser.add_argument("input_file", type=str, help="Input file containing k-mers and counts")
    query_parser.add_argument("-s", "--sequence_files", action="append", help="FASTA files to read sequences from")

    return parser.parse_args()

def read_kmers(file_path):
    kmers = {}
    with open(file_path, 'r') as file:
        for line in file:
            kmer, count = line.strip().split()
            kmers[kmer] = int(count)
    return kmers

def filter_kmers(kmers, low, high):
    return {kmer: count for kmer, count in kmers.items() if low <= count <= high}

def hash_kmer(kmer):
    return int(hashlib.md5(kmer.encode()).hexdigest(), 16)

def sort_kmers(kmers):
    return sorted(kmers.items(), key=lambda x: hash_kmer(x[0]))

def output_kmers_to_fasta(kmers, output_file):
    with open(output_file, 'w') as file:
        for kmer, count in kmers.items():
            file.write(f">{count}\n{kmer}\n")

def read_sequences_from_fasta(file_path):
    sequences = []
    with open(file_path, 'r') as file:
        sequence = ''
        for line in file:
            if line.startswith('>'):
                if sequence:
                    sequences.append(sequence)
                    sequence = ''
            else:
                sequence += line.strip()
        if sequence:
            sequences.append(sequence)
    return sequences

def query_kmers(kmers_dict, query_kmers):
    results = {kmer: kmers_dict.get(kmer, 0) for kmer in query_kmers}
    return results

def main():
    args = parse_arguments()

    if args.command == "dump":
        kmers = read_kmers(args.input_file)
        filtered_kmers = filter_kmers(kmers, args.low, args.high)
        sorted_kmers = sort_kmers(filtered_kmers)
        output_kmers_to_fasta(dict(sorted_kmers), args.output_file)
    
    elif args.command == "query":
        kmers = read_kmers(args.input_file)
        
        if args.sequence_files:
            query_kmers_set = set()
            for seq_file in args.sequence_files:
                sequences = read_sequences_from_fasta(seq_file)
                for seq in sequences:
                    for i in range(len(seq) - len(next(iter(kmers))) + 1):
                        query_kmers_set.add(seq[i:i+len(next(iter(kmers)))])
            query_results = query_kmers(kmers, query_kmers_set)

            for kmer, count in query_results.items():
                print(f"{kmer}: {count}")

if __name__ == "__main__":
    main()
