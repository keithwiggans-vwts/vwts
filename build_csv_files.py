# we're going to iterate through the dict
# for each file that endswith the dict key, we yield a row with data and delimiters
# The function return a list of rows to be printed to a file

import argparse
import os

from dicts_to_parse import tceq_objects_nor_txt
from tqdm import tqdm

delimiter="|"
suffix=".txt"
prefix="ihw_dump_"
invalid_starting_words=['Starting...',]
default_path=os.getcwd()

def build_rows_from_text(input_dir, output_dir, table_name):
  """
  Takes input file and writes to output file using specified delimiter.
  table_dict is a single table dictionary containing column/tuple/single combinations
  Example:
    table_name : {
        column_1 : (1, 5),
        column_2 : (6, 8),
        column_3 : (9),
        }
  """
  # Check input file to see if exists
  if os.path.isfile(os.path.join(input_dir, f"{prefix}{table_name}{suffix}")):
    input_file=os.path.join(input_dir, f"{prefix}{table_name}{suffix}")
  elif os.path.isfile(os.path.join(input_dir, f"{table_name}{suffix}")):
    input_file=os.path.join(input_dir, f"{table_name}{suffix}")
  else:
    return

  output_file=os.path.join(output_dir, f"{table_name}.csv")

  def process_file_line(line):
    for col in tceq_objects_nor_txt[table_name]:
      srt_end = tceq_objects_nor_txt[table_name][col]
      if type(srt_end) == tuple:
        srt = srt_end[0] - 1
        end = srt_end[1]
      else:
        srt = srt_end - 1
        end = srt_end
      yield line[srt:end].strip().replace("|", " ").replace('"', "")

  with open(input_file, "r") as in_file, open(output_file, "w") as out_file:
    headers=[h.lower() for h in tceq_objects_nor_txt[table_name].keys()]
    out_file.write(delimiter.join(headers) + "\n")
    for line in tqdm(in_file):
      # check for invalid starting words
      for w in invalid_starting_words:
        if line.startswith(w):
          continue
      # split line according to dicts_to_parse
      data_list = process_file_line(line)
      out_file.write(delimiter.join(data_list) + "\n")

def main():
  parser = argparse.ArgumentParser(description="Generate CSV files to load into PGRES")
  parser.add_argument("-i", "--input_dir", type=str, default=os.path.join(default_path, "raw"), help="Path to raw data")
  parser.add_argument("-o", "--output_dir", type=str, default=os.path.join(default_path, "csv"), help="Path to output directory")
  args = parser.parse_args()

  # Write csv files to output director
  for tbl in tceq_objects_nor_txt:
    print(f"\n{tbl}")
    build_rows_from_text(args.input_dir, args.output_dir, tbl)

if __name__ == "__main__":
  main()
