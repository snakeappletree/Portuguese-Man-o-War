import sys
import argparse
from __init__ import countm, dumpquerym, histom, randomDNAm

def parse_arguments():
   parser = argparse.ArgumentParser(description="PortugueseManoWar Command-Line Interface")
   parser.add_argument("command", nargs="?", choices=["count", "dumpquery", "histo", "randomDNA"], help="Select command")
   parser.add_argument("args", nargs="*", help="Arguments for the selected command")
   return parser.parse_args()

def main():
   args = parse_arguments()

   # If -h is present as the first argument, display available commands
   if len(sys.argv) > 1 and sys.argv[1] == "-h":
      print("Available commands:")
      print("count: Count k-mers in a DNA sequence")
      print("dumpquery: Dump or query k-mers and their counts")
      print("histo: Plot histogram of k-mer counts")
      print("randomDNA: Generate random DNA sequences")
      return
   
   if args.command == "count":
      countm(args.args)
   elif args.command == "dumpquery":
      dumpquerym(args.args)
   elif args.command == "histo":
      histom(args.args)
   elif args.command == "randomDNA":
      randomDNAm(args.args)
   else:
      print("Invalid command")

if __name__ == "__main__":
    main()