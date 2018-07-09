import sys
import random
from gpudb import GPUdb, GPUdbTable

INPUT_TABLE = 'udf_tc_py_in_table'
OUTPUT_TABLE = 'udf_tc_py_out_table'
MAX_RECORDS = 10000


db_host = sys.argv[1] if len(sys.argv) > 1 else '127.0.0.1'
db_port = sys.argv[2] if len(sys.argv) > 2 else '9191'
db_user = sys.argv[3] if len(sys.argv) > 3 else ''
db_pass = sys.argv[4] if len(sys.argv) > 4 else ''


print("")
print("PYTHON UDF TABLE COPY INITIALIZATION")
print("====================================")
print("")

# Connect to Kinetica
h_db = GPUdb(host=db_host, port=db_port, username=db_user, password=db_pass)

# Create input data table
columns = [
    ["id", "int", "int16", "primary_key"],
    ["x", "float"],
    ["y", "float"]
]

if h_db.has_table(table_name=INPUT_TABLE)['table_exists']:
    h_db.clear_table(table_name=INPUT_TABLE)

input_table_obj = GPUdbTable(
    _type=columns,
    name=INPUT_TABLE,
    db=h_db
)

print("Input table successfully created: ")
print(input_table_obj)

records = []
for val in range(1, MAX_RECORDS+1):
    records.append([val, random.gauss(1, 1), random.gauss(1, 2)])
input_table_obj.insert_records(records)

print("Number of records inserted into the input table: {}".format(input_table_obj.size()))

# Create output data table
columns = [
    ["id", "int", "int16", "primary_key"],
    ["a", "float"],
    ["b", "float"]
]

if h_db.has_table(table_name=OUTPUT_TABLE)['table_exists']:
    h_db.clear_table(table_name=OUTPUT_TABLE)

output_table_obj = GPUdbTable(
    _type=columns,
    name=OUTPUT_TABLE,
    db=h_db
)

print("")
print("Output table successfully created: ")
print(output_table_obj)
print("")
