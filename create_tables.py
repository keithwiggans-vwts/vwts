import argparse

from dicts_to_parse import tceq_objects_nor_txt

def create_tables_tceq(table_dict):
  """
  Returns a list of create table statements to be written to a separate file.
  Each key within the dictionary references a table in the TCEQ PARIS IHW.
  The key value is the name of the table.
  Each key has it's own dictionary keyed on the column names.
  Each column name has a tuple value providing the start/end column number of that field.
  Example:
    tables : {
        table_1 : {
            column_1 : (<start number>, <end number>),
            column_2 : (<start number>, <end number>),
            },
        }
  """
  for table in table_dict:
    columns = []
    for column in table_dict[table]:
      col_lengths = table_dict[table][column]
      if type(col_lengths) is tuple:
        if len(col_lengths) > 1:
          col_length = 1 + (col_lengths[1] - col_lengths[0])
          if col_length == 0:
            col_length = 1
          assert col_length > 0, f"{table}, {column} is an invalid length"
        else:
          col_length = col_lengths[0]
      else:
        col_length = 1
      columns.append(f"{column.lower()} varchar({col_length})")
    yield (
      f"DROP TABLE IF EXISTS {table};"
      f"CREATE TABLE {table} ({','.join(columns)});"
      )

def main():
  parser = argparse.ArgumentParser(description="Generate CREATE TABLE statements")
  parser.add_argument("-o", "--output_file", type=str, default="pgres_create_tables.sql", help="Path to output sql file")
  args = parser.parse_args()

  # Generate CREATE TABLE statements
  create_statements_generator = create_tables_tceq(tceq_objects_nor_txt)

  # Write statements to output file
  with open(args.output_file, "w") as f:
    f.write("\n".join(create_statements_generator))
  print(f"CREATE TABLE statements written to: {args.output_file}")

if __name__ == "__main__":
  main()
