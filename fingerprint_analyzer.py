# fingerprint analyzer
"""
given a directory of csv files and text files, analyze the fingerprints and identify trends
"""


import csv
import os   
import time
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import mplcursors  # Add this import


aggregate_data_filename = "python scripts/aggregate_data.csv"


# handle txt file
"""
    Read the system information text files
"""
def handle_txt_file(file_path):
    """
    Read a text file and extract system information.
    """
    sys_info = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        system_info = {}
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                system_info[key.strip()] = value.strip()
                sys_info.append((key.strip(), value.strip()))
    return sys_info



# handle csv file
"""
    Read the fingerprint data from the inputted csv
"""
def handle_csv_file(file_path):
    """
    Read a CSV file and extract fingerprint data.
    """
    sys_data = []
    with open(file_path, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            fingerprint = {
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
            sys_data.append(fingerprint)
    return sys_data



# aggregate data
"""
        The aggregate data file will have headers for each of the main fields, present in the data. 
        However, when each new file is read through, it will be appended to the list of headers, 
        following a general format as below:

        v = value of the sin, cos, e, log fingerprint for the i-th iteration
        e = elapsed time for the calculation of the fingerprint for the i-th iteration
        
        i,v+uuid[0],e+uuid[0],...,v+uuid[1],e+uuid[1],...,v+uuid[n],e+uuid[n]

        It is going to be a very slow operation, but will allow for relatively fast analysis of the aggregated data.
"""
def aggregate_data(sys_info, sys_data, uuids):

    # pull the uuid from the sys_info 
    uuid = sys_info[-1][1]  

    # Build new headers, following the format a_<uuid>, b_<uuid>, etc.>
    base_keys = list(sys_data[0].keys())[1:]  # skip 'i'
    fieldnames = ['i'] + [f"{key}_{u}" for u in uuids for key in base_keys]

    # Read existing data, and load it into a list, which is going to be updated with new data and rewritten
    if os.path.exists(aggregate_data_filename):
        with open(aggregate_data_filename, mode='r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            existing_data = [row for row in reader]
    else:
        existing_data = []

    # Build a mapping from i to row for fast lookup
    data_map = {int(row['i']): row for row in existing_data}

    # Update or add new columns for this UUID
    for entry in sys_data:
        i_val = entry['i']
        if i_val not in data_map:
            # Create a new row with only 'i'
            data_map[i_val] = {'i': i_val}
        # Add new columns for this UUID
        for key in base_keys:
            data_map[i_val][f"{key}_{uuid}"] = entry[key]

    # Write back all rows with updated headers and data
    with open(aggregate_data_filename, mode='w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i_val in sorted(data_map.keys()):
            writer.writerow(data_map[i_val])



# analyze data
"""
    Analyze the aggregated data and identify trends
"""
def analyze_data():
    """
    Identify when and which UUIDs have differing values for each metric at each iteration.
    """
    if not os.path.exists(aggregate_data_filename):
        print("No aggregate data file found. Please run the fingerprint collection first.")
        return


    data = []

    # puls the data and pushes it into the data dictionary array
    with open(aggregate_data_filename, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
    
        print(f"fieldnames {reader.fieldnames}")

        for row in reader:
            row_data = {"i": int(row['i']), "sin": {}, "cos": {}, "e": {}, "log": {}}
            for key in row.keys():
                if key.startswith('sin_value_'):
                    uuid = key.split('_')[-1]
                    val = row[key]
                    row_data['sin'].setdefault(val, []).append(uuid)
                elif key.startswith('cos_value_'):
                    uuid = key.split('_')[-1]
                    val = row[key]
                    row_data['cos'].setdefault(val, []).append(uuid)
                elif key.startswith('e_value_'):
                    uuid = key.split('_')[-1]
                    val = row[key]
                    row_data['e'].setdefault(val, []).append(uuid)
                elif key.startswith('log_value_'):
                    uuid = key.split('_')[-1]
                    val = row[key]
                    row_data['log'].setdefault(val, []).append(uuid)
            data.append(row_data)
                    

    
    # for each i, perform checks      
    unique_data = []  
    for row in data:
        unique_row_data = {"i": row["i"], "sin": [], "sin_uuids": [], "cos": [], "cos_uuids": [], "e": [], "e_uuids": [], "log": [], "log_uuids": []}

        # For each metric, collect unique values and their associated UUIDs
        for metric in ['sin', 'cos', 'e', 'log']:
            value_to_uuids = row[metric]  # {value: [uuid1, uuid2, ...]}
            unique_values = list(value_to_uuids.keys())
            unique_row_data[metric] = unique_values
            # Store a list of lists: each inner list is the UUIDs for a unique value
            unique_row_data[f"{metric}_uuids"] = [uuids for uuids in value_to_uuids.values()]

        unique_data.append(unique_row_data)

    print(f"unique rows: {unique_data}")

    # generate graphical plot of unique data
    metrics = ['sin', 'cos', 'e', 'log']
    for metric in metrics:
        x_vals = []
        y_vals = []
        hover_texts = []
        colors = []

        for row in unique_data:
            i = row['i']
            values = row[metric]
            uuids_per_value = row[f"{metric}_uuids"]
            highlight = len(values) > 1  # True if multiple unique values
            for val, uuids in zip(values, uuids_per_value):
                try:
                    y_val = float(val)
                except ValueError:
                    continue
                x_vals.append(i)
                y_vals.append(y_val)
                hover_texts.append(f"i={i}\nValue={val}\nUUIDs: {', '.join(uuids)}")
                colors.append('red' if highlight else 'blue')  # Red for multiple, blue for single

        plt.figure(figsize=(15, 8))
        scatter = plt.scatter(x_vals, y_vals, c=colors, marker='o')
        plt.xlabel('Iteration (i)')
        plt.ylabel(f'{metric.title()} Value')
        plt.title(f'Unique {metric.title()} Values per Iteration\n(Red: Multiple Unique Values)')
        plt.grid(True)
        plt.tight_layout()

        # Add interactive hover showing all unique values and UUIDs for this iteration
        cursor = mplcursors.cursor(scatter, hover=True)
        @cursor.connect("add")
        def on_add(sel):
            idx = sel.index
            i_hover = x_vals[idx]
            # Find the row in unique_data for this iteration
            row = next(r for r in unique_data if r['i'] == i_hover)
            values = row[metric]
            uuids_per_value = row[f"{metric}_uuids"]
            info = [f"Value: {v}\nUUIDs: {', '.join(u)}" for v, u in zip(values, uuids_per_value)]
            sel.annotation.set_text(f"i={i_hover}\n" + "\n\n".join(info))

    plt.show()
    

# main function
"""
    Main function to analyze fingerprints and trends
"""
def main():
    
    # Directory containing the fingerprint files
    directory = "python scripts/fingerprint_results"
    
    # List to hold all fingerprints
    fingerprints = []
    
    uuids = []

    # pull the data from all those files in the directory
    print(f"files: {os.listdir('.')}")
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):

            # for the CSV files, which hold the fingerprint data
            sys_data = handle_csv_file(os.path.join(directory, filename))

            # for the TXT files, which hold the system information
            uuid = filename.split('_')[-1].split('.')[0]  # Extract UUID from filename
            uuids.append(uuid)  # add the UUID to the list
            sys_info = handle_txt_file(os.path.join(directory, f"system_info_{uuid}.txt"))
    
            # add the data to the aggregate data file
            print(f"Agregating data for UUID: {uuid}")
            aggregate_data(sys_info, sys_data, uuids)

    # analyze the data
    print("Analyzing Data")
    analyze_data()

if __name__ == "__main__":
    print("Startin fingerprint analysis...")
    main()