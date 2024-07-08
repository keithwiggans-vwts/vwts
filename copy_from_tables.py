import argparse
import os

from dicts_to_parse import tceq_objects_nor_txt

delimiter="|"
default_path=os.getcwd()

def copy_from_files(table_dict, input_dir):
  """
  Contents of csv files are copied to their respective tables
  """
  table_names = table_dict.keys()
  for tbl in table_names:
    yield (
      f"TRUNCATE TABLE {tbl};"
      f"COPY {tbl} FROM '{os.path.join(input_dir, tbl)}.csv' "
      f"WITH (FORMAT 'csv', DELIMITER '{delimiter}', HEADER MATCH, ESCAPE '\\');"
    )

def main():
  parser = argparse.ArgumentParser(description="Generate CREATE TABLE statements")
  parser.add_argument("-i", "--input_dir", type=str, default=os.path.join(default_path, "csv"), help="Path to csv data")
  parser.add_argument("-o", "--output_file", type=str, default="pgres_copy_tables.sql", help="Path to output sql file")
  args = parser.parse_args()

  copy_from_generator = copy_from_files(tceq_objects_nor_txt, args.input_dir)

  # Write statements to output file
  with open(args.output_file, "w") as f:
    f.write("\n".join(copy_from_generator))
  print(f"COPY table_name FROM statements written to: {args.output_file}")

if __name__ == "__main__":
  main()
