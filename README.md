# CPU Fingerprinting Tool

### In Using Floating Point Operations to Fingerprint CPU Architectures

*By Ira Garrett*

*Master's Student in Cybersecurity at Hood College*


This tool is part of the data-gathering phase of a research project, with the purpose and intention to fingerprint your CPU Architecture by performing mathematical operations and recording the results.  


## How It Works

- The script runs several mathematical functions (`sin`, `cos`, `e^x`, `log`) for increasing values of `i`, from 0 to 10,000.
- It records both the result and the time taken for each calculation, which are the data necessary for the application of this research and data relavent in simple side-channel attacks, respectively.
- The process repeats for thousands of iterations to collect a detailed fingerprint (10,000 to be exact).
- System information and a hash of the script are saved for integrity and research accuracy. I want to ensure that the data comes from the original script, so the hashing algorithm is present to ensure data-generation integrity.


## Usage

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


## Notes
- **Library Requirements**

    This script uses the following Python libraries:
    - time
    - math
    - platform
    - csv
    - hashlib
    - os

    Some (though not all) of these libraries may need to be installed explicitly before the script can work.
    And they may be installed from the terminal using `pip3 install <library_name>`

- **Do not modify or delete the generated files.**  
  Accurate data is essential for research, and a hash code is incorperated in the `fingerprinting.py` script, to help ensure script integrity.
- If you encounter any issues, contact `garrnic3@isu.edu`.


## License

This tool is for research and educational use only.
But, if you are polite about it and don't do anything rude or bad, then I have no problem with the use of part or all of this script.

---

Thank you for helping with this research!!!