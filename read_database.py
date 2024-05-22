# Read database file
def read_database(file_path):
   database = ""
   with open(file_path, "r") as dna_file:
      for line in dna_file:
         if line.startswith('>') == False: 
            database +=line.strip()
      return database
