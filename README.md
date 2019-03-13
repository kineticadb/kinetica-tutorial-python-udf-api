# Kinetica Python UDF API Tutorial #

This project contains the **7.0** version of the **Python UDF API Tutorial**.

This guide exists on-line at:  [Kinetica Python UDF API Tutorial](http://www.kinetica.com/docs/udf/python/tutorial.html)

More information can be found at:  [Kinetica Documentation](http://www.kinetica.com/docs/index.html)

-----

The following guide provides step-by-step instructions to get started writing
and running UDFs in *Python*. This particular example is a simple distributed
*UDF* that copies data from one table to another using a CSV configuration file
to determine from which processing node to copy data. Note that only copying
data from some processing nodes typically would not have "real" applications and
this exercise is purely to demonstrate the many facets of the *UDF* API.

## Contents

* [References](#references)
* [Prerequisites](#prerequisites)
* [API Download and Installation](#api-download-and-installation)
* [Development](#development)
* [Deployment](#deployment)
* [Execution Detail](#execution-detail)


## References

* [Python UDF Reference](https://www.kinetica.com/docs/udf/python/writing.html)
  -- detailed description of the entire *UDF* API
* [Running UDFs](https://www.kinetica.com/docs/udf/python/running.html)
  -- detailed description on running *Python* UDFs
* [Example UDFs](https://www.kinetica.com/docs/udf/python/examples.html)
  -- example *UDFs* written in *Python*


## Prerequisites

The general prerequisites for using *UDFs* in *Kinetica* can be found on
the [UDF Implementation](https://www.kinetica.com/docs/udf/index.html) page.


### Data Files

There are four files associated with the *Python UDF* tutorial:

* an initialization script, ``udf_tc_py_init.py``, that creates the input and
  output tables
* a UDF, ``udf_tc_py_proc.py``, that contains a table copying example
* an execute script, ``udf_tc_py_exec.py`` that creates the proc and executes
  it
* a CSV input file, ``rank_tom.csv``


## API Download and Installation

The *Python UDF* tutorial requires local access to the *Python UDF* tutorial
repository, native *Python* API, and the *Python UDF* API, and the native
*Python* API must be installed. Installing the native *Python* API requires
either *Python* 2.7 (or greater) or ``pip``.

**NOTE:** The locations of ``python`` and ``pip`` should be placed in the
   ``PATH`` environment variable. If they are not, you'll need to use
   the full path to the ``python`` and ``pip`` executables in the
   relevant instructions below. Also, administrative access will most likely be
   required when installing the *Python* packages.

In the desired directory, run the following but be sure to replace
``kinetica-version`` with the name of the installed Kinetica version, e.g.,
``v7.0``:

    git clone -b release/<kinetica-version> --single-branch https://github.com/kineticadb/kinetica-tutorial-python-udf-api.git

In the same directory, run the following but be sure to replace
``kinetica-version`` with the name of the installed Kinetica version, e.g.,
``v7.0``:

    git clone -b release/<kinetica-version> --single-branch https://github.com/kineticadb/kinetica-udf-api-python.git

In the same directory, run the following but be sure to replace
``kinetica-version`` with the name of the installed Kinetica version, e.g.,
``v7.0``:

    git clone -b release/<kinetica-version> --single-branch https://github.com/kineticadb/kinetica-api-python.git

Change directory into the newly downloaded native *Python* API repository:

    cd kinetica-api-python/

In the root directory of the repository, install the Kinetica API:

    sudo python setup.py install

Back out one directory level:

    cd ..


## Development

Refer to the [Python UDF API Reference](https://www.kinetica.com/docs/udf/python/writing.html)
page to begin writing your own *UDF(s)* or use the *UDF* already provided with
the *Python UDF* tutorial repository. The steps below outline using the
[UDF Simulator](https://www.kinetica.com/docs/udf/simulating_udfs.html) with
the *UDF* included with the *Python UDF* tutorial repository.

Add the *Python UDF* API directory to the ``PYTHONPATH``:

    export PYTHONPATH=$PYTHONPATH:$(cd kinetica-udf-api-python;pwd)

Change directory into the newly downloaded *Python UDF* tutorial repository:

    cd kinetica-tutorial-python-udf-api/

Run the *UDF* initialization script, specifying the database host and optional
port (if non-default):

    python udf_tc_py_init.py <kinetica-host> [<kinetica-port> [<kinetica-user> <kinetica-pass>]]

In the native *Python* API directory, run the *UDF* simulator with the
following options, ensuring you replace the *Kinetica* URL and port with
the appropriate values.  Username & password can be specified, if your
instance requires authentication:

    python ../kinetica-api-python/examples/udfsim.py execute -d \
         -i udf_tc_py_in_table -o udf_tc_py_out_table \
         -K http://<kinetica-host>:<kinetica-port> \
         [-U <kinetica-user> -P <kinetica-pass>]

For instance:

    python ../kinetica-api-python/examples/udfsim.py execute -d \
         -i udf_tc_py_in_table -o udf_tc_py_out_table \
         -K http://127.0.0.1:9191 \
         -U admin -P admin123

Copy & execute the ``export`` command output by the previous command; this
will prepare the execution environment for simulating the UDF:

    export KINETICA_PCF=/tmp/udf-sim-control-files/kinetica-udf-sim-icf-xMGW32

**Important:**  The ``export`` command shown above is an *example* of what
      the ``udfsim.py`` script will output--it should **not** be copied to the
      terminal in which this example is being run.  Make sure to copy & execute
      the **actual** command output by ``udfsim.py`` in the previous step.

Run the *UDF*:

    python udf_tc_py_proc.py

Output the results to *Kinetica* (use the dry run flag ``-d`` to avoid
writing to *Kinetica*), ensuring you replace the *Kinetica* URL and port with
the appropriate values. The ``results`` map will be returned (even if there's
nothing in it) as well as the amount of records that were (or will be in the
case of a dry run) added to the given output table:

    python ../kinetica-api-python/examples/udfsim.py output \
         -K http://<kinetica-host>:<kinetica-port> \
         [-U <kinetica-user> -P <kinetica-pass>]

For instance:

    python ../kinetica-api-python/examples/udfsim.py output \
         -K http://127.0.0.1:9191 \
         -U admin -P admin123

This should output the following:

    No results
    Output:

    udf_tc_py_out_table: 10000 records

Clean the control files output by the *UDF* simulator:

    python ../kinetica-api-python/examples/udfsim.py clean

**Important:**  The ``clean`` command is only necessary if data was output
      to *Kinetica*; otherwise, the *UDF* simulator can be re-run as many
      times as desired without having to clean the output files and enter
      another export command.


## Deployment

If satisfied after testing your *UDF* with the *UDF* simulator, the *UDF* can
be created and executed using the official *UDF* endpoints: ``/create/proc``
and ``/execute/proc`` (respectively).

Optionally, run the *UDF* init script to reset the example tables:

    python udf_tc_py_init.py <kinetica-host> [<kinetica-port> [<kinetica-user> <kinetica-pass>]]

Run the *UDF* execute script:

    python udf_tc_py_exec.py <kinetica-host> [<kinetica-port> [<kinetica-user> <kinetica-pass>]]


## Execution Detail

While the table copy *UDF* can run against multiple tables, the example run
will use a single table, ``udf_tc_py_in_table``, as input and a similar table,
``udf_tc_py_out_table``, for output.

The input table will contain one *int16* column (``id``) and two *float*
columns (``x`` and ``y``). The ``id`` column will be an ordered integer field,
with the first row containing ``1``, the second row containing ``2``, etc. Both
*float* columns will contain 10,000 pairs of randomly-generated numbers. The
output table will also contain one *int16* column (``id``) and two *float*
columns (``a`` and ``b``).

The *UDF* will first read from a given CSV file to determine from which
processing node container and processing node to copy data:

    rank_num,tom_num
    1,0
    2,0

The ``tom_num`` column values refer to the processing node that contains the
many shards of data inside the database. The ``rank_num`` column values refer
to the processing node container that holds the processing nodes for the
database. For example, the given CSV file determines that the data from
``udf_tc_py_in_table`` on processing node container ``1``, processing node ``0``
and processing node container ``2``, processing node ``0`` will be copied to
``udf_tc_py_out_table``.

Once the *UDF* is executed, a *UDF* instance (OS process) is spun up for each
processing node to execute the given code against its assigned processing node.
The *UDF* then determines if the processing node container/processing node pair
it's currently running on matches one of the pairs of values in the CSV file. If
there is a match, the *UDF* will loop through the input tables, match the output
tables' size to the input tables', and copy the appropriate data from the input
tables to the output tables. If there isn't a match, the code will complete.


### Initialization (udf_tc_py_init.py)

To interact with *Kinetica*, you must first instantiate an object of the
``GPUdb`` class while providing the connection URL, including the host and port
of the database server.

```python
h_db = GPUdb(host=db_host, port=db_port, username=db_user, password=db_pass)
```

The input table is created.

```python
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
```

Next, sample data is generated and inserted into the new input table:

```python
records = []
for val in range(1, MAX_RECORDS+1):
    records.append([val, random.gauss(1, 1), random.gauss(1, 2)])
input_table_obj.insert_records(records)
```

Lastly, an output table is created with a schema that is similar to the input
table.

```python
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
```


### UDF (udf_tc_py_proc.py)

First, the file gets a handle to the ``ProcData()`` class:

```python
proc_data = ProcData()
```

Then, the CSV file mentioned in [Data Files](#data-files) is read (skipping the
header). For each row in the file, set each row's first value as ``rank_num``;
set each row's second value as ``tom_num``.

```python
rank_tom_info = csv.reader(open("rank_tom.csv"))
rank_tom_info.next()
for row in rank_tom_info:
    rank_num = row[0]
    tom_num = row[1]
```

Determine if the rank and tom number found in the request info map pointing to
the current instance of the UDF matches the values in the CSV file:

```python
if (proc_data.request_info["rank_number"] == rank_num and
        proc_data.request_info["tom_number"] == tom_num):
```

For each input and output table found in the ``input_data`` and ``output_data``
objects (respectively), set the output tables' size to the input tables' size.

```python
for in_table, out_table in zip(
        proc_data.input_data, proc_data.output_data):
    out_table.size = in_table.size
```

For each input column in the input table(s) and for each output column in the
output table(s), copy the input columns' values to the output columns.

```python
for in_column, out_column in zip(in_table, out_table):
    out_column.extend(in_column)
```

If no matches were found, finish processing.

```python
else:
    print "No rank or tom matches; exiting"
```

Call ``complete()`` to tell *Kinetica* the proc code is finished.

```python
# Inform Kinetica that the proc has finished successfully
proc_data.complete()
```


### Execution (udf_tc_py_exec.py)

To interact with *Kinetica*, you must first instantiate an object of the
``GPUdb`` class while providing the connection URL, including the host and port
of the database server. Ensure the host address and port are correct for your
setup.

```python
h_db = GPUdb(host=db_host, port=db_port, username=db_user, password=db_pass)
```

To upload the ``udf_tc_py_proc.py`` and ``rank_tom.csv`` files to *Kinetica*,
they will first need to be read in as bytes and added to a file data map:

```python
file_names = (csv_file_name, proc_file_name)
files = {}
for file_name in file_names:
    with open(file_name, 'rb') as file:
        files[file_name] = file.read()
```

After the files are placed in a data map, the distributed ``udf_tc_py_proc``
proc can be created in *Kinetica* and the files associated with it. Note the
proc requires the proper ``command`` and ``args`` to execute the proc, in this
case, the assembled command line would be ``python udf_tc_py_proc.py``:

```python
response = h_db.create_proc(
    proc_name=proc_name,
    execution_mode="distributed",
    files=files,
    command="python",
    args=[proc_file_name],
    options={}
)
```

Finally, after the proc is created, it can be executed. The input table
and output table created in `Initialization (udf_tc_py_init.py)`_ are passed in
here.

```python
response = h_db.execute_proc(
    proc_name=proc_name,
    params={},
    bin_params={},
    input_table_names=[INPUT_TABLE],
    input_column_names={},
    output_table_names=[OUTPUT_TABLE],
    options={}
)
```
