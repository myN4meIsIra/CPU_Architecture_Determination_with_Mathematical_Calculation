# fingerprint data analyzer
"""
    analyze the data, generate visuals, and help lead to conclusions
"""

import time
import os
import csv
import json
import matplotlib.pyplot as plt
import numpy as np
import mplcursors


# Directory containing the fingerprint data files
data_directory = "python scripts/fingerprint_results"
aggregate_fingerprint_data_filename = "python scripts/aggregate_fingerprint_data.json"
aggregate_system_data_filename = "python scripts/aggregate_system_data.json"
inconsistant_rows_filename = "python scripts/inconsistent_rows.json"

# read txt
"""
read and return the data for a .txt file
returns array of directories
"""
def read_txt(directory, filename):
    print(f"Reading {filename}")

    with open(f"{directory}/{filename}", mode='r') as txtfile:
        reader = txtfile.readlines()
        system_information = {
            'OS Type' : reader[0].split(":")[-1].lower().strip(),
            'OS Type (User Input)' : reader[1].split(":")[-1].lower().strip().strip("\n"),
            'Running on VM' : reader[2].split(":")[-1].lower().strip(),
            'CPU Info' : reader[3].split(":")[-1].lower().strip(),
            'CPU Info (User Input)' : reader[4].split(":")[-1].lower().strip(),
            'CPU Generation (User Input)' : reader[5].split(":")[-1].lower().strip(),
            'Script Hash' : reader[6].split(":")[-1].strip("\n").strip(' '),
            'UUID' : reader[7].split(":")[-1].strip("\n").strip(' ')
        }
    return system_information



# read csv
"""
read and return the data for a .csv file
returns array of dictionaries
"""
def read_csv(directory, filename):
    print(f"Reading {filename}")

    # get uuid from filename 
    uuid = filename.split('_')[-1].split('.')[0]
    
    data = []
    with open(f"{directory}/{filename}", mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            fingerprint = {
                'UUID': uuid,
                'i': int(row['i']),
                'sin_value': row['sin_value'],
                'sin_elapsed': row['sin_elapsed'],
                'cos_value': row['cos_value'],
                'cos_elapsed': row['cos_elapsed'],
                'e_value': row['e_value'],
                'e_elapsed': row['e_elapsed'],
                'log_value': row['log_value'],
                'log_elapsed': row['log_elapsed'],
            }
            data.append(fingerprint)
    return data



# aggregate 
""" 
aggregate all the data files into a single, large file
"""
def aggregate():
    
    # pull the data from all those files in the directory
    print(f"files in {data_directory}: {os.listdir('.')}")

    aggregate_csv_data = []
    aggregate_txt_data = []

    for filename in os.listdir(data_directory):
        # for the CSV files, which hold the fingerprint data
        if filename.endswith(".csv"):
            csv_data = read_csv(data_directory, filename)
            aggregate_csv_data.append(csv_data)
          

        # for the .txt files, which hold the system data
        if filename.endswith(".txt"):
            txt_data = read_txt(data_directory, filename)
            aggregate_txt_data.append(txt_data)

    # clear aggregate files if they already exist
    if(os.path.exists(aggregate_fingerprint_data_filename)):
        os.remove(aggregate_fingerprint_data_filename)
    if(os.path.exists(aggregate_system_data_filename)):
        os.remove(aggregate_system_data_filename)



    # write each line of the aggregate_csv_data 
    with open(aggregate_fingerprint_data_filename, mode='a') as aggregate_fingerprint_data_file:
        data_line = json.dumps(aggregate_csv_data[0], indent=4)
        aggregate_fingerprint_data_file.write("["+data_line+",")

        for line in aggregate_csv_data[1:-2]:
            #print(f"{line}\n\n")
            data_line = json.dumps(line, indent=4)
            aggregate_fingerprint_data_file.write(data_line+",")

        data_line = json.dumps(aggregate_csv_data[-1], indent=4)
        aggregate_fingerprint_data_file.write(data_line+"]")
            

    # write each line of the aggregate_txt_data
    with open(aggregate_system_data_filename, mode='a') as aggregate_system_data_file:
        data_line = json.dumps(aggregate_txt_data[0], indent=4).strip('\n')         
        aggregate_system_data_file.write('['+data_line+',')

        for line in aggregate_txt_data[1:-2]:
            data_line = json.dumps(line, indent=4)         
            aggregate_system_data_file.write(data_line+',')

        data_line = json.dumps(aggregate_txt_data[-1], indent=4)         
        aggregate_system_data_file.write(data_line+']')

    return 1



# analyze
"""
    analyze the aggregated data files, searching for instances where the recorded values differ
"""
def analyze():
    # Load the aggregate data file
    with open(aggregate_fingerprint_data_filename, 'r') as f:
        data = json.load(f)  # List of lists of dicts, one list per UUID

    # Load the system data file and build a UUID -> system info mapping
    with open(aggregate_system_data_filename, 'r') as sys_f:
        system_data = json.load(sys_f)
    uuid_to_sysinfo = {entry['UUID']: entry for entry in system_data}

    # Flatten data: each entry is a dict with UUID, i, and values
    all_records = []
    for uuid_records in data:
        all_records.extend(uuid_records)

    # Group by iteration
    from collections import defaultdict
    grouped = defaultdict(list)
    for record in all_records:
        grouped[record['i']].append(record)

   # For each iteration, check for differing values
    functions = ['sin_value', 'cos_value', 'e_value', 'log_value']
    inconsistent_rows = []
    for i, records in grouped.items():
        for func in functions:
            values = {}
            sysinfos = {}
            for rec in records:
                uuid = rec['UUID']
                values[uuid] = rec[func]
                sysinfos[uuid] = uuid_to_sysinfo.get(uuid, {})
            unique_vals = set(values.values())
            if len(unique_vals) > 1:
                print(f"Iteration i={i}, function {func} has differing values:")
                for uuid, val in values.items():
                    print(f"  UUID {uuid}: {val}")
                    print(f"    System Info: {sysinfos[uuid]}")
                # Save inconsistent row data with system info
                inconsistent_rows.append({
                    'iteration': i,
                    'function': func,
                    'values': values,
                    'system_info': sysinfos
                })

    # Export inconsistent rows to a JSON file
    with open(inconsistant_rows_filename, "w") as out_f:
        json.dump(inconsistent_rows, out_f, indent=4)


import mplcursors

def visualize():
    # Load the aggregate data file
    with open(aggregate_fingerprint_data_filename, 'r') as f:
        data = json.load(f)

    # Flatten data
    all_records = []
    for uuid_records in data:
        all_records.extend(uuid_records)

    # Group by iteration
    from collections import defaultdict
    grouped = defaultdict(list)
    for record in all_records:
        grouped[record['i']].append(record)

    functions = ['sin_value', 'cos_value', 'e_value', 'log_value']
    iterations = sorted(grouped.keys())

    for func in functions:
        inconsistencies = []
        uuids_per_inconsistency = []
        i_vals = []

        for i in iterations:
            records = grouped[i]
            values = {}
            for rec in records:
                values[rec['UUID']] = rec[func]
            unique_vals = set(values.values())
            if len(unique_vals) > 1:
                inconsistencies.append(1)
                uuids_per_inconsistency.append(list(values.keys()))
            else:
                inconsistencies.append(0)
                uuids_per_inconsistency.append([])
            i_vals.append(i)

        plt.figure(figsize=(12, 2))
        scatter = plt.scatter(i_vals, [1]*len(i_vals), c=inconsistencies, cmap='Reds', marker='s', s=100)
        plt.xlabel('Iteration (i)')
        plt.yticks([1], [func])
        plt.title(f'Inconsistencies for {func}')
        plt.grid(True)
        plt.tight_layout()

        # Add interactive hover showing i, UUIDs, and function name
        cursor = mplcursors.cursor(scatter, hover=True)
        @cursor.connect("add")
        def on_add(sel):
            idx = sel.index
            if inconsistencies[idx]:
                sel.annotation.set_text(
                    f"Iteration: {i_vals[idx]}\n"
                    f"Function: {func}\n"
                    f"UUIDs: {', '.join(uuids_per_inconsistency[idx])}"
                )
            else:
                sel.annotation.set_text(
                    f"Iteration: {i_vals[idx]}\n"
                    f"Function: {func}\n"
                    f"No inconsistency"
                )

    plt.show()                                                  



# main function
"""
    main function
"""
def main_function():
    print(f"Aggregating data files...")
    aggregate()

    print(f"Analyzing aggregated data file...")
    analyze()
    
    print(f"Generating visualization...")
    visualize()
    return 1



if __name__ == "__main__":
    main_function()
