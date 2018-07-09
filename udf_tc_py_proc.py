################################################################################
#                                                                              #
# Kinetica UDF Table Copy Example                                              #
# ---------------------------------------------------------------------------- #
# This UDF first compares the given CSV file's rank and tom number values to   #
# the ranks and toms processing the UDF. If the values in the CSV file match   #
# the ranks and toms found in the request info map, the associated data with   #
# the matching rank/tom is copied from the input table to the output table.    #
#                                                                              #
################################################################################

from kinetica_proc import ProcData
import csv


# Instantiate a handle to the ProcData() class
proc_data = ProcData()

# Read the CSV file (skipping the header) and assign each row's first value as
# its "rank_num" and each row's second value as its "tom_num"
rank_tom_info = csv.reader(open("rank_tom.csv"))
rank_tom_info.next()
for row in rank_tom_info:
    rank_num = row[0]
    tom_num = row[1]

    # If the rank and tom number found in the request info map matches the
    # rank_num and tom_num values from the CSV file, continue
    if (proc_data.request_info["rank_number"] == rank_num and
            proc_data.request_info["tom_number"] == tom_num):

        # Loop through input and output tables (assume the same number)
        for in_table, out_table in zip(
                proc_data.input_data, proc_data.output_data):
            out_table.size = in_table.size

            # Loop through columns in the input and output tables (assume the
            # same number and types)
            for in_column, out_column in zip(in_table, out_table):
                out_column.extend(in_column)

        break;

# If no matches exist, don't copy any values
else:
    print "No rank or tom matches; exiting"

# Inform Kinetica that the proc has finished successfully
proc_data.complete()
