import sys
from gpudb import GPUdb

INPUT_TABLE = 'udf_tc_py_in_table'
OUTPUT_TABLE = 'udf_tc_py_out_table'

proc_name = 'udf_tc_py_proc'
proc_file_name = proc_name + '.py'
csv_file_name = 'rank_tom.csv'


db_host = sys.argv[1] if len(sys.argv) > 1 else '127.0.0.1'
db_port = sys.argv[2] if len(sys.argv) > 2 else '9191'
db_user = sys.argv[3] if len(sys.argv) > 3 else ''
db_pass = sys.argv[4] if len(sys.argv) > 4 else ''


print("")
print("PYTHON UDF TABLE COPY EXECUTION")
print("===============================")

print("")
print("Reading in the 'udf_tc_py_proc.py' and 'rank_tom.csv' files as bytes...")
print("")

file_names = (csv_file_name, proc_file_name)
files = {}
for file_name in file_names:
    with open(file_name, 'rb') as file:
        files[file_name] = file.read()

# Connect to Kinetica
h_db = GPUdb(host=db_host, port=db_port, username=db_user, password=db_pass)


# Remove proc if it exists from a prior registration
if h_db.has_proc(proc_name=proc_name)["proc_exists"]:
    h_db.delete_proc(proc_name=proc_name)


print("Registering distributed proc...")
response = h_db.create_proc(
    proc_name=proc_name,
    execution_mode="distributed",
    files=files,
    command="python",
    args=[proc_file_name],
    options={}
)
print("Proc created successfully:")
print(response)
print("")

print("Executing proc...")
response = h_db.execute_proc(
    proc_name=proc_name,
    params={},
    bin_params={},
    input_table_names=[INPUT_TABLE],
    input_column_names={},
    output_table_names=[OUTPUT_TABLE],
    options={}
)
print("Proc executed successfully:")
print(response)
print("Check 'gpudb.log' or 'gpudb-proc.log' for execution information")
print("")
