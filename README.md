# CPU Architecture Fingerprint Analyzer

### By Ira Garrett  
*Master's student in Cybersecurity at Hood College*  
Email: garrnic3@isu.edu

This tool analyzes and visualizes floating-point computation fingerprints from multiple CPUs.  
It helps researchers identify differences in mathematical results and timing across architectures.
There are two main parts: `fingerprint.py` and the companion analyzing script `fingerprint_data_and_elapsed_time_analyzer.py`.

---

## What Does It Do?
### Data Collector
The script runs several mathematical functions (`sin`, `cos`, `e^x`, `log`) for increasing values of `i`, from 0 to 10,000. It records both the result and the time taken for each calculation, which are the data necessary for the application of this research and data relavent in simple side-channel attacks, respectively.

The process repeats for thousands of iterations to collect a detailed fingerprint (10,000 to be exact).

System information and a hash of the script are saved for integrity and research accuracy. I want to ensure that the data comes from the original script, so the hashing algorithm is present to ensure data-generation integrity.


### Data Analyzer
The Analyzer script consists of a three-step process of combining the results of multiple runs of the data collection script, analyzing all of them together.The three steps are shown and described below:

**Aggregate:** fingerprint data and system info from multiple machines are automatically saved in the `fingerprint.py` script with UUIDs to distinguish them. These various scripts are brought together into aggregate data files.

**Analyze:** where different CPUs (UUIDs) produce different results or elapsed times for mathematical functions (`sin`, `cos`, `e`, `log`), the aggregated files are analyzed to identify where these inconsistencies occur.

**Visualize:** taking the lists of inconsistencies, they are visually plotted and graphed, showing when and which CPUs differ.

---

## How To Use
### `fingerprint.py`

1. **Run the script:**  
   Open a terminal and run:
   ```
   python3 fingerprinting.py
   ```
   or run the `fingerprinting.py` file some other way.

2. **Answer the prompts:**  
   - Enter your operating system, CPU type, generation, and whether you are running on a virtual machine.
   - Review and confirm your system information.

3. **Wait for fingerprinting to complete:**  
   - The script will run for several minutes, showing progress as it collects data.

4. **Results:**  
   - Two files are generated:
     - `system_info_<UUID>.txt` — contains your system details and script hash, which are used to match trends in data.
     - `fingerprint_results_<UUID>.csv` — contains the fingerprint data, which is the more important part of the result set.

5. **Send your results:**  
   - Email both files to the researcher (me) at `garrnic3@isu.edu`.

### `fingerprint_data_and_elapsed_time_analyzer.py`

1. **Prepare Data**
   - Place all fingerprint CSV files and system info TXT files in the `python scripts/fingerprint_results` directory.

2. **Run the Analyzer**
   - Open a terminal and run:
     ```
     python fingerprint_data_and_elapsed_time_analyzer.py
     ```
     or execute the script some other way.

   - The script will:
     - Aggregate all data files.
     - Analyze for inconsistencies.
     - Generate interactive visualizations.

3. **View Results**
   - Inconsistencies are saved to `python scripts/inconsistent_rows.json`.
   - Visualizations pop up showing where and when CPUs differ, and can be saved individually.

---

## Features of analyzer script

- **Checks both values and elapsed times** for each function.
- **Connects system info** to each UUID for deeper analysis.
- **Interactive plots**: Hover to see iteration, function, and UUIDs involved in inconsistencies.
- **Limits x-axis** to avoid overflow/underflow in plots.

---

## Requirements

- Python 3.x

Install missing libraries with:
```
pip3 install <library_name>
```

This script uses the following Python libraries:
   - `time`
   - `math`
   - `platform`
   - `csv`
   - `hashlib`
   - `os`
   - `matplotlib`
   - `mplcursors`
   - `numpy`


   Some (though not all) of these libraries may need to be installed explicitly before the script can work.


---

## Notes

Accurate data is essential for research, and a hash code is incorperated in the `fingerprinting.py` script, to help ensure script integrity.
- If you encounter any issues, contact `garrnic3@isu.edu`.

---

## License

This tool is for research and educational use only.
But, if you are polite about it and don't do anything rude or bad, then I have no problem with the use of part or all of this script. I think it's super cool, so I hope that you do too.

---

Thank you for helping with this research!!!