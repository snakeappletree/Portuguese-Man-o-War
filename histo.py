import argparse
import matplotlib.pyplot as plt

def read_count_file(file):
   counts = {}
   with open(file, 'r') as f:
      for line in f:
         hash_val, count = line.strip().split(': ')
         count_str = count.split(',')[1].strip()
         count_val = int(count_str.strip(')'))
         counts[hash_val] = count_val
   return counts

def plot_histogram(counts, low, high, incr):
   bins = range(low, high + incr, incr)
   plt.hist(counts.values(), bins=bins, color='green', edgecolor='black')
   plt.xlabel('Count')
   plt.ylabel('Frequency')
   plt.title('Histogram of K-mer Counts')
   plt.grid(True)
   plt.show()

def main():
   parse = argparse.ArgumentParser(description='Plot histogram of k-mer counts')
   parse.add_argument('input_file', type=str, help='Path to the input file containing k-mer counts')
   parse.add_argument('-l', '--low', type=int, default=0, help='Low count bucket value')
   parse.add_argument('-h', '--high', type=int, default=100, help='High count bucket value')
   parse.add_argument('-i', '--incr', type=int, default=10, help='Increment for bucket value')
   args = parse.parse_args()
   counts = read_count_file(args.input_file)
   plot_histogram(counts, args.low, args.high, args.incr)

if __name__ == "__main__":
   main()