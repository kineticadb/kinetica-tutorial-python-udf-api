import argparse
import gpudb
import random
import sys

SCHEMA = 'tutorial_udf_python'
INPUT_TABLE = SCHEMA + '.udf_tc_py_in_table'
OUTPUT_TABLE = SCHEMA + '.udf_tc_py_out_table'
MAX_RECORDS = 10000

OPTION_NO_CREATE_ERROR = {"no_error_if_exists": "true"}


def python_tc_udf_init():

    print("")
    print("PYTHON UDF TABLE COPY INITIALIZATION")
    print("====================================")
    print("")

    # Create the Python UDF tutorial schema, if it doesn't exist
    kinetica.create_schema(SCHEMA, options=OPTION_NO_CREATE_ERROR)

    # Create input data table
    columns = [
        ["id", "int", "int16", "primary_key"],
        ["x", "float"],
        ["y", "float"]
    ]

    if kinetica.has_table(table_name=INPUT_TABLE)['table_exists']:
        kinetica.clear_table(table_name=INPUT_TABLE)

    input_table_obj = gpudb.GPUdbTable(
        _type=columns,
        name=INPUT_TABLE,
        db=kinetica
    )

    print("Input table successfully created: ")
    print(input_table_obj)

    records = []
    for val in range(1, MAX_RECORDS+1):
        records.append([val, random.gauss(1, 1), random.gauss(1, 2)])
    input_table_obj.insert_records(records)

    print("Number of records inserted into the input table: {}".format(
        input_table_obj.size()))

    # Create output data table
    columns = [
        ["id", "int", "int16", "primary_key"],
        ["a", "float"],
        ["b", "float"]
    ]

    if kinetica.has_table(table_name=OUTPUT_TABLE)['table_exists']:
        kinetica.clear_table(table_name=OUTPUT_TABLE)

    output_table_obj = gpudb.GPUdbTable(
        _type=columns,
        name=OUTPUT_TABLE,
        db=kinetica
    )

    print("")
    print("Output table successfully created: ")
    print(output_table_obj)
    print("")

# end python_tc_udf_init()


if __name__ == '__main__':

    # Set up args
    parser = argparse.ArgumentParser(
        description='Initialize tables for Python UDF table copy example.')
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
    python_tc_udf_init()
