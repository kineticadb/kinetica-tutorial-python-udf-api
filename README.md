<h3 align="center" style="margin:0px">
	<img width="200" src="https://2wz2rk1b7g6s3mm3mk3dj0lh-wpengine.netdna-ssl.com/wp-content/uploads/2018/08/kinetica_logo.svg" alt="Kinetica Logo"/>
</h3>
<h5 align="center" style="margin:0px">
	<a href="https://www.kinetica.com/">Website</a>
	|
	<a href="https://docs.kinetica.com/7.2/">Docs</a>
	|
	<a href="https://docs.kinetica.com/7.2/api/">API Docs</a>
	|
	<a href="https://join.slack.com/t/kinetica-community/shared_invite/zt-1bt9x3mvr-uMKrXlSDXfy3oU~sKi84qg">Community Slack</a>   
</h5>
<p align = "center">
	<img src="https://img.shields.io/badge/tested-=v7.2.0-green"></img>
	<img src="https://img.shields.io/badge/time-15 mins-blue"></img>
</p>

# Kinetica Python UDF API Tutorial #

This project contains the **7.2** version of the **Python UDF API Tutorial**.

This guide exists on-line at:  [Kinetica Python UDF API Tutorial](https://docs.kinetica.com/7.2/guides/udf_python_guide/)

More information can be found at:  [Kinetica Documentation](https://docs.kinetica.com/7.2/)

-----

The following guide provides step-by-step instructions to get started writing
and running UDFs in Python. This example is a simple distributed UDF that copies
data from one table to another using a CSV configuration file to determine on
which processing node(s) data will be copied.

Standard (non-replicated) tables have their data distributed across all
processing nodes, while replicated tables have all of their data on every
processing node.  In this example, we'll use a standard table and copy only the
portions of its data that reside on the nodes named in the CSV file.

Note that only copying data from some processing nodes typically would not have
"real" applications and this exercise is purely to demonstrate the many facets
of the UDF API.

## Contents

* [References](#references)
* [Prerequisites](#prerequisites)
* [API Download and Installation](#api-download-and-installation)
* [Development](#development)
* [Deployment](#deployment)
* [UDF Detail](#udf-detail)


## References

* [Python UDF Reference](https://docs.kinetica.com/7.2/udf/python/writing/)
  -- detailed description of the entire UDF API
* [Running UDFs](https://docs.kinetica.com/7.2/udf/python/running/)
  -- detailed description on running Python UDFs
* [Example UDFs](https://docs.kinetica.com/7.2/udf/python/examples/)
  -- example UDFs written in Python


## Prerequisites

The general prerequisites for using UDFs in Kinetica can be found on the
[UDF Implementation](https://docs.kinetica.com/7.2/udf/) page.


### Program Files

There are three files associated with the Python UDF tutorial:

* A UDF management program,
  [udf_tc_py_manager.py](table-copy/udf_tc_py_manager.py),
  written using the Python API, which creates the input & output tables, and
  creates the UDF and executes it.
* A UDF,
  [udf_tc_py_proc.py](table-copy/udf_tc_py_proc.py),
  written using the Python UDF API, which contains a table copying example.
* A CSV input file,
  [rank_tom.csv](table-copy/rank_tom.csv), used to
  identify which processing nodes should copy data.


## API Download and Installation

The Python UDF tutorial requires local access to the Python UDF API & tutorial
repositories and the Python API. The native Python API is also used to run the
UDF simulator (details found in [Development](#development)).

* In the desired directory, run the following to download the Kinetica Python
  UDF tutorial repository:

      git clone -b release/v7.2 --single-branch https://github.com/kineticadb/kinetica-tutorial-python-udf-api.git

* In the same directory, run the following to download the Kinetica Python UDF
  API repository:

      git clone -b release/v7.2 --single-branch https://github.com/kineticadb/kinetica-udf-api-python.git

* In the same directory, run the following to download the Kinetica Python API
  repository:

      git clone -b release/v7.2 --single-branch https://github.com/kineticadb/kinetica-api-python.git

* Install the ``pandas`` Python library:

      pip3 install pandas

* Change directory into the newly downloaded native *Python* API repository:

      cd kinetica-api-python/

* In the root directory of the repository, install the Kinetica API:

      sudo python3 setup.py install

* Change directory into the UDF tutorial root:

      cd ..

* Add the Python UDF API directory to the ``PYTHONPATH``:

      export PYTHONPATH=$PYTHONPATH:$(cd kinetica-udf-api-python;pwd)


## Development

The steps below outline using the
[UDF Simulator](https://docs.kinetica.com/7.2/udf/simulating_udfs/),
included with the Python API. The UDF Simulator simulates the mechanics of
[execute_proc()](https://docs.kinetica.com/7.2/api/python/?source/gpudb.html#gpudb.GPUdb.execute_proc)
without actually calling it in the database; this is useful for developing UDFs
piece-by-piece and test incrementally, avoiding memory ramifications for the
database.

* Ensure that the Python UDF API directory is in the ``PYTHONPATH``.

* Change directory into the newly downloaded Python UDF tutorial repository:

      cd kinetica-tutorial-python-udf-api/table-copy

* Run the UDF manager script with the ``init`` option, specifying the database
  URL and a username & password:

      python3 udf_tc_py_manager.py init <url> <username> <password>

* In the native Python API directory, run the UDF Simulator in ``execute``
  mode with the following options to simulate running the UDF:
   
      python3 ../../kinetica-api-python/examples/udfsim.py execute -d \
         -i [<schema>.]<input-table> -o [<schema>.]<output-table> \
         -K <url> -U <username> -P <password>

  Where:

  * ``-i`` - schema-qualified UDF input table
  * ``-o`` - schema-qualified UDF output table
  * ``-K`` - Kinetica URL
  * ``-U`` - Kinetica username
  * ``-P`` - Kinetica password 

  For instance:

      python3 ../../kinetica-api-python/examples/udfsim.py execute -d \
         -i udf_tc_py_in_table -o udf_tc_py_out_table \
         -K http://127.0.0.1:9191 -U admin -P admin123

* Copy & execute the ``export`` command output by the previous command; this
  will prepare the execution environment for simulating the UDF:

      export KINETICA_PCF=/tmp/udf-sim-control-files/kinetica-udf-sim-icf-xMGW32

  **IMPORTANT:**
      The ``export`` command shown above is an *example* of what the
      ``udfsim.py`` script will output--it should **not** be copied to the
      terminal in which this example is being run.  Make sure to copy & execute
      the **actual** command output by ``udfsim.py`` in the previous step.

* Run the UDF:

      python3 udf_tc_py_proc.py

* Run the UDF Simulator in ``output`` mode to output the results to
  Kinetica (use the dry run flag ``-d`` to avoid writing to Kinetica),
  The ``results`` map will be returned (even if there's nothing in it) as well
  as the number of records that were (or will be in the case of a dry run)
  added to the given output table:

      python3 ../../kinetica-api-python/examples/udfsim.py output \
         -K <url> -U <username> -P <password>

  For instance:

      python3 ../../kinetica-api-python/examples/udfsim.py output \
         -K http://127.0.0.1:9191 -U admin -P admin123

  This should output the following:

      No results
      Output:

      udf_tc_py_out_table: 10000 records

* Clean the control files output by the UDF Simulator:

      python3 ../../kinetica-api-python/examples/udfsim.py clean

  **IMPORTANT:**
      The ``clean`` command is only necessary if data was output to Kinetica;
      otherwise, the UDF Simulator can be re-run as many times as desired
      without having to clean the output files and enter another export command.


## Deployment

The UDF can be created and executed using the UDF functions:
[create_proc()](https://docs.kinetica.com/7.2/api/python/?source/gpudb.html#gpudb.GPUdb.create_proc)
and
[execute_proc()](https://docs.kinetica.com/7.2/api/python/?source/gpudb.html#gpudb.GPUdb.execute_proc)
(respectively).

* Run the UDF manager script with the ``init`` option to reset the example
  tables:

      python3 udf_tc_py_manager.py init <url> <username> <password>

* Run the UDF manager script with the ``exec`` option to run the example:

      python3 udf_tc_py_manager.py exec <url> <username> <password>

* Verify the results, using a SQL client (KiSQL), Kinetica Workbench, or other:

  * The ``udf_tc_py_in_table`` table is created in the user's default schema
    (``ki_home``, unless a different one was assigned during account creation)
  * A matching ``udf_tc_py_out_table`` table is created in the same schema
  * The ``udf_tc_py_in_table`` contains 10,000 records of random data
  * The ``udf_tc_py_out_table`` contains the correct amount of copied data
    from ``udf_tc_py_in_table``.
     
    On single-node installations, as is the case with *Developer Edition*, all
    data should be copied.  This is because single-node instances have a
    default configuration of 2 worker ranks with one TOM each, and the
    ``rank_tom.csv`` configuration file contains a reference to rank 1/TOM 0
    and rank 2/TOM 0, effectively naming both data TOMs to copy data from.
     
    In larger cluster configurations, only a fraction of the data in the input
    table will be stored on those two TOMs; so, the output table will contain
    that same fraction of the input table's data.
     
    The database logs should also show the portion of the data being copied:
     
        Copying <5071> records on rank/TOM <1/0> from <ki_home.udf_tc_py_in_table> to <ki_home.udf_tc_py_out_table>
        Copying <4929> records on rank/TOM <2/0> from <ki_home.udf_tc_py_in_table> to <ki_home.udf_tc_py_out_table>


## UDF Detail

As mentioned previously, this section details a simple distributed UDF that
copies data from one table to another. While the table copy UDF can run
against multiple tables, the example run will use a single table,
``udf_tc_py_in_table``, as input and a similar table,
``udf_tc_py_out_table``, for output.

The input table will contain one *int16* column (``id``) and two *float*
columns (``x`` and ``y``). The ``id`` column will be an ordered integer field,
with the first row containing ``1``, the second row containing ``2``, etc. Both
*float* columns will contain 10,000 pairs of randomly-generated numbers:

    +------+-----------+-----------+
    | id   | x         | y         |
    +======+===========+===========+
    | 1    | 2.57434   | -3.357401 |
    +------+-----------+-----------+
    | 2    | 0.0996761 | 5.375546  |
    +------+-----------+-----------+
    | ...  | ...       | ...       |
    +------+-----------+-----------+

The output table will also contain one *int16* column (``id``) and two *float*
columns (``a`` and ``b``). No data is inserted:

    +------+-----------+-----------+
    | id   | a         | b         |
    +======+===========+===========+
    |      |           |           |
    +------+-----------+-----------+

The UDF will first read from a given CSV file to determine from which
processing node container (*rank*) and processing node (*TOM*) to copy data:

    rank_num,tom_num
    1,0
    2,0

The ``tom_num`` column values refer to processing nodes that contain the many
shards of data inside the database. The ``rank_num`` column values refer to
processing node containers that hold the processing nodes for the database. For
example, the given CSV file determines that the data from ``udf_tc_py_in_table``
on processing node container ``1``, processing node ``0`` and processing node
container ``2``, processing node ``0`` will be copied to ``udf_tc_py_out_table``
on those same nodes.

Once the UDF is executed, a UDF instance (OS process) is spun up for each
processing node to execute the UDF code against its assigned processing node's
data.  Each UDF process then determines if its corresponding processing node
container/processing node pair matches one of the pairs of values in the CSV
file. If there is a match, the UDF process will loop through the given input
tables and copy the data contained in that processing node from the input tables
to the output tables. If there isn't a match, no data will be copied by that
process.


### Initialization (udf_tc_py_manager.py init)

The *init* option invokes the ``init()`` function in the
``udf_tc_py_manager.py`` script.  This function will create the input table for
the UDF to copy data from and the output table to copy data to. Sample data will
also be generated and inserted into the input table.

To interact with Kinetica, you must first instantiate an object of the
``GPUdb`` class while providing the connection URL and username & password to
use for logging in. This database object is later passed to the ``init()`` and
``exec()`` methods:

```python
kinetica = gpudb.GPUdb(host=[args.url], username=args.username, password=args.password)
```

The input table is created.

```python
columns = [
    ["id", "int", "int16", "primary_key"],
    ["x", "float"],
    ["y", "float"]
]

if kinetica.has_table(table_name=input_table)['table_exists']:
    kinetica.clear_table(table_name=input_table)

input_table_obj = gpudb.GPUdbTable(
    _type = columns,
    name = input_table,
    db = kinetica
)
```

Next, sample data is generated and inserted into the new input table:

```python
records = []
for val in range(1, MAX_RECORDS+1):
    records.append([val, random.gauss(1, 1), random.gauss(1, 2)])
input_table_obj.insert_records(records)
```

Lastly, an output table is created with a schema that is similar to the input
table but is removed first if it already exists.

```python
columns = [
    ["id", "int", "int16", "primary_key"],
    ["a", "float"],
    ["b", "float"]
]

if kinetica.has_table(table_name=output_table)['table_exists']:
    kinetica.clear_table(table_name=output_table)

output_table_obj = gpudb.GPUdbTable(
    _type = columns,
    name = output_table,
    db = kinetica
)
```


### UDF (udf_tc_py_proc.py)

The ``udf_tc_py_proc.py`` script is the UDF itself.  It does the work of copying
the input table data to the output table, based on the ranks & TOMs specified in
the given CSV file.

First, instantiate a handle to the ``ProcData()`` class:

```python
proc_data = ProcData()
```

Retrieve the rank/TOM pair for this UDF process instance from the request info
map:

```python
proc_rank_num = proc_data.request_info["rank_number"]
proc_tom_num = proc_data.request_info["tom_number"]
```

Then, the CSV file mentioned in [Program Files](#program-files) is read
(skipping the header):

```python
rank_tom_info = csv.reader(open("rank_tom.csv"))
next(rank_tom_info)
```

Compare the rank and TOM of the current UDF instance's processing node to each
rank/TOM pair in the file to determine if the current UDF instance should copy
the data on its corresponding processing node:

```python
for row in rank_tom_info:
    rank_num = row[0]
    tom_num = row[1]

    if (proc_rank_num == rank_num and proc_tom_num == tom_num):
```

For each input and output table found in the ``input_data`` and ``output_data``
objects (respectively), set the output tables' size to the input tables' size.
This will allocate enough memory to copy all input records to the output
table:

```python
for in_table, out_table in zip(
        proc_data.input_data, proc_data.output_data):
    out_table.size = in_table.size
```

For each input column in the input table(s), copy the input columns' values to
the corresponding output table columns:

```python
for in_column, out_column in zip(in_table, out_table):
    out_column.extend(in_column)
```

Call ``complete()`` to tell Kinetica the UDF is finished.

```python
proc_data.complete()
```


### Execution (udf_tc_py_exec.py)

The *exec* option invokes the ``exec()`` function in the
``udf_tc_py_manager.py`` script.  This function will read files in as bytes,
create a UDF, and upload the files to the database. The function will then
execute the UDF.

To upload the ``udf_tc_py_proc.py`` and ``rank_tom.csv`` files to Kinetica,
they will first need to be read in as bytes and added to a file data map:

```python
file_names = (CSV_FILE_NAME, PROC_FILE_NAME)
files = {}
for file_name in file_names:
    with open(file_name, 'rb') as file:
        files[file_name] = file.read()
```

After the files are placed in a data map, the distributed ``udf_tc_py_proc``
UDF can be created in Kinetica and the files can be associated with it:

```python
response = kinetica.create_proc(
    proc_name = PROC_NAME,
    execution_mode = "distributed",
    files = files,
    command = "python",
    args = [PROC_FILE_NAME],
    options = {}
)
```

Finally, after the UDF is created, it can be executed. The input & output tables
created in the [Initialization](#initialization-udf_tc_py_managerpy-init) section are passed
in here:

```python
response = kinetica.execute_proc(
    proc_name = PROC_NAME,
    params = {},
    bin_params = {},
    input_table_names = [input_table],
    input_column_names = {},
    output_table_names = [output_table],
    options = {}
)
```


## Support

For bugs, please submit an
[issue on Github](https://github.com/kineticadb/kinetica-udf-api-python/issues).

For support, you can post on
[stackoverflow](https://stackoverflow.com/questions/tagged/kinetica) under the
``kinetica`` tag or
[Slack](https://join.slack.com/t/kinetica-community/shared_invite/zt-1bt9x3mvr-uMKrXlSDXfy3oU~sKi84qg).


## Contact Us

* Ask a question on Slack:
  [Slack](https://join.slack.com/t/kinetica-community/shared_invite/zt-1bt9x3mvr-uMKrXlSDXfy3oU~sKi84qg)
* Follow on GitHub:
  [Follow @kineticadb](https://github.com/kineticadb) 
* Email us:  <support@kinetica.com>
* Visit:  <https://www.kinetica.com/contact/>
