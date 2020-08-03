import argparse
import gpudb
import sys

SCHEMA = 'tutorial_udf_python'
INPUT_TABLE = SCHEMA + '.udf_tc_py_in_table'
OUTPUT_TABLE = SCHEMA + '.udf_tc_py_out_table'

proc_name = 'udf_tc_py_proc'
proc_file_name = proc_name + '.py'
csv_file_name = 'rank_tom.csv'


def python_tc_udf_exec():

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

    # Remove proc if it exists from a prior registration
    if kinetica.has_proc(proc_name=proc_name)["proc_exists"]:
        kinetica.delete_proc(proc_name=proc_name)

    print("Registering distributed proc...")
    response = kinetica.create_proc(
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
    response = kinetica.execute_proc(
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
    print("Check the system log or 'gpudb-proc.log' for execution information")
    print("")

# end python_tc_udf_exec()


if __name__ == '__main__':

    # Set up args
    parser = argparse.ArgumentParser(
        description='Execute the table copy Python UDF example.')
    parser.add_argument('--host', default='127.0.0.1',
                        help='Kinetica host to run example against')
    parser.add_argument('--username', default='',
                        help='Username of user to run example with')
    parser.add_argument('--password', default='', help='Password of user')

    args = parser.parse_args()

    # Establish connection with a locally-running instance of Kinetica
    kinetica = gpudb.GPUdb(host=['http://' + args.host + ':9191'],
                           username=args.username, password=args.password)

    # Execute defined functions
    python_tc_udf_exec()
