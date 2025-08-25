# fingerprinting.py
"""
    This script is designed to fingerprint the CPU of the system it is run on
    by performing mathematical operations and collecting data on the resultant values. 
    It is designed to be run in a controlled environment for research purposes, 
    and for the combination and analysis of the data collected from multiple systems to be used
    to determine variations in computations performed by differnt CPU architectures.

    Please be nice and do not change the code, or delete the files that are generated.
    I am trying to do research here, and I need the data to be accurate.
    There are integrity checks in place to ensure that the script has not been tampered with,
    but we all now that it is possible to bypass these checks and falsify data. 
    So please, be nice. 

    Thank you <3
        ~ Ira Garrett 
        Master's Student in Cybersecurity at Hood College
        Email: garrnic3@isu.edu
"""



import time
import math
import platform
import csv

# for hashing the script itself for integrity check
import hashlib
import os


# self hash
"""
    Calculate the SHA-256 hash of the current script file for integrity checking
"""
def self_hash():
    # Get the path to the current script (relative to its own location)
    script_path = os.path.join(os.path.dirname(__file__), os.path.basename(__file__))
    
    with open(script_path, "rb") as f:
        content = f.read()
    
    return hashlib.sha256(content).hexdigest()



# test for bit overflow
"""
 test if the system can handle the various operations based on i without overflow
"""
def test_for_bit_overflow(i, operation): 
    try:
        # Check if the system can handle the operation without overflow
        if operation == "sin": bits_sin = math.sin(10**i * math.pi)
        elif operation == "cos": bits_cos = math.cos(10**i * math.pi)
        elif operation == "e": bits_e = math.e ** i
        elif operation == "log": bits_log = math.log10(10**(i*-1))
        elif operation == "cosh": bits_cosh = math.cosh(i)
        elif operation == "tan": bits_tan = math.tan(-1*10**i)
        else: raise ValueError("Invalid operation specified.")
    except Exception as e:
        """print(f"(Anticipated) Error at i={i}, and proper handling occured. "
              "This error probably occured because of the float accuracy operations, which is expected "
              f"Stopping further calculations for {operation}.")
        """
        return True
    
    return False



#sin fingerprint
"""
 calculate sin(10^i * pi) fingerprint
"""
def sin_fingerprint(i):
    start = time.time()
    val = math.sin(10** i * math.pi)
    elapsed = time.time() - start
    
    return {i:[val, elapsed]}



# cos fingerprint
"""
calculate cos(10^i * pi) fingerprint
"""
def cos_fingerprint(i):
    start = time.time()
    val = math.cos(10** i * math.pi)
    elapsed = time.time() - start
    
    return {i:[val, elapsed]}



# e fingerprint
"""
 calculate e^x fingerprint
"""
def e_fingerprint(i):
    start = time.time()
    val = math.e ** (i)
    elapsed = time.time() - start
    
    return {i:[val, elapsed]}



# log fingerprint
"""
calculate log(10^-i) fingerprint
"""
def log_fingerprint(i):
    start = time.time()
    val = math.log10(10**(i*-1))
    #print(f"Calculating log for i={i} \t val = {val}")
    elapsed = time.time() - start
    
    return {i:[val, elapsed]}



# cosh fingerprint
"""
calculate cosh(i)
"""
def cosh_fingerprint(i):
    start = time.time()
    val = math.cosh(i)
    elapsed = time.time() - start
    
    return {i:[val, elapsed]}



# tan fingerprint
"""
calculate tan(-1*10^i)
"""
def tan_fingerprint(i):
    start = time.time()
    val = math.tan(-1*10**i)
    elapsed = time.time() - start
    
    return {i:[val, elapsed]}



# fingerprint cpu
"""
    Perform the fingerprinting process for the CPU by iterating through a range of values
    and collecting the results of the various mathematical operations.
"""
def fingerprint_cpu():
    results = [[],[],[],[],[],[]]

    iterations = 10000
    for i in range(iterations):
        if not test_for_bit_overflow(i, "sin"): results[0].append(sin_fingerprint(i))
        else: results[0].append({i: ["Overflow", "N/A"]})

        if not test_for_bit_overflow(i, "cos"): results[1].append(cos_fingerprint(i))
        else: results[1].append({i: ["Overflow", "N/A"]})

        if not test_for_bit_overflow(i, "e"): results[2].append(e_fingerprint(i))
        else: results[2].append({i: ["Overflow", "N/A"]})

        if not test_for_bit_overflow(i, "log"): results[3].append(log_fingerprint(i))
        else: results[3].append({i: ["Overflow", "N/A"]})

        if not test_for_bit_overflow(i, "cosh"): results[4].append(cosh_fingerprint(i))
        else: results[4].append({i: ["Overflow", "N/A"]})

        if not test_for_bit_overflow(i, "tan"): results[5].append(tan_fingerprint(i))
        else: results[5].append({i: ["Overflow", "N/A"]})

        print(f"Progress: {i+1}/iterations", end='\r')

    return results



# main function to run/command the fingerprinting process
"""
 main script
"""
if __name__ == "__main__":
    print("Welcome to the CPU Fingerprinting Tool!")

    # get system information
    """ this is the meta-data of the system that is being fingerprinted, so that the data can be matched and analyzed later """
    while True:
        # get OS type
        try:
            os_type = platform.system()
        except Exception as e:
            print(f"Error determining OS type: {e}")
            os_type = "Unknown"
        os_type_from_user = input(f"What type of Operating System are you using? (e.g., Windows, Linux, macOS): ").strip()


        # determine if running off a VM, etc.
        while True:
            vm_check = input("Are you running this on a virtual machine? (yes/no): ").strip().lower()
            if vm_check in ['yes', 'no']:
                break
            print("Please answer with 'yes' or 'no'.")

        # fingerprint CPU
        try:
            cpu_info = platform.processor()
        except Exception as e:
            print(f"Error retrieving CPU information: {e}")
            cpu_info = "Unknown"
        cpu_info_from_user = input("What type of CPU are you using? (e.g., Intel, AMD): ").strip()

        # CPU generation
        cpu_generation_from_user = input("What generation is your CPU? (e.g., 10th, 11th, etc.) -- type \"IDK\" if you do not know --: ").strip()
        

        # Confirm system information
        print(f"\n\n\n****** Please look over this information, for research accuracy purposes ******\n"
              f"Detected OS Type: {os_type}\n"
              f"OS Type (That You Typed In): {os_type_from_user}\n"
              f"Are you running on a VM?: {vm_check}\n"
              f"Detected CPU Info: {cpu_info} \n"
              f"CPU Info (That You Typed In): {cpu_info_from_user}\n"
              f"CPU Generation (That You Typed In): {cpu_generation_from_user}\n")
        currect_system_info = input("Is this correct? (yes/no): ").strip().lower()
        if currect_system_info == 'yes':
            break
        else:
            print("Please re-enter the information.")

    # Perform fingerprinting
    print("Starting fingerprinting process...")
    time.sleep(1)  # Simulate some delay for user experience

    # call the fingerprinting function
    results = fingerprint_cpu()

    print("Fingerprinting completed.")
    print("Thank you for using the CPU fingerprinting tool! Saving results...")
    time.sleep(1)  # Simulate some delay for user experience


    # try and load the system information and calculation data into a file
    try:
        # Generate a unique identifier for the results
        import uuid
        uuid = str(uuid.uuid4())
        print(f"Generated UUID for this session: {uuid}\n")
        time.sleep(1)  # Simulate some delay for user experience

        # Hash the script for integrity check
        """ I beg you, please do not be mean and delete, change, or do something funny with the data files. 
            I am trying to do research here, and I need the data to be accurate.
            We're all in the CS, IT, or Cyber field, and I know full well that you are quite capable of understanding
            and changing this code. I know that full well. And I know that like any good volunteer runnign someone
            else's code on their system, you are reading through it to see what it does before running it.
            Please... please don't be mean.
            Thank you <3 
        """
        self_hash = self_hash()

        # Save results to a file or database as needed
        with open(f"system_info_{uuid}.txt", "w") as file:
            file.write(f"OS Type: {os_type}\n")
            file.write(f"OS Type (User Input): {os_type_from_user}\n")
            file.write(f"Running on VM: {vm_check}\n")
            file.write(f"CPU Info: {cpu_info}\n")
            file.write(f"CPU Info (User Input): {cpu_info_from_user}\n")
            file.write(f"CPU Generation (User Input): {cpu_generation_from_user}\n")
            file.write(f"Script Hash: {self_hash}\n")
            file.write(f"Results UUID: {uuid}\n")
        time.sleep(1)  # Simulate some delay for user experience


        # Save results of data collection to a CSV file
        with open(f"fingerprint_results_{uuid}.csv", "w", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["i", "sin_value", "sin_elapsed",
                                                    "cos_value", "cos_elapsed",
                                                    "e_value", "e_elapsed",
                                                    "log_value", "log_elapsed"])
            writer.writeheader()
            for i in range(len(results[0])):
                writer.writerow({
                    "i": i,
                    "sin_value": results[0][i][i][0],
                    "sin_elapsed": results[0][i][i][1],
                    "cos_value": results[1][i][i][0],
                    "cos_elapsed": results[1][i][i][1],
                    "e_value": results[2][i][i][0],
                    "e_elapsed": results[2][i][i][1],
                    "log_value": results[3][i][i][0],
                    "log_elapsed": results[3][i][i][1]
                })

    
    except Exception as e:  
        print(f"An error occurred while saving results: {e}")
        print("Please try again or contact me at garrnic3@isu.edu if the issue persists.")
        exit(1)    


    print("Results saved successfully.")
    time.sleep(1)  # Simulate some delay for user experience

    print("Thank you so much for using this CPU fingerprinting tool! \n" \
    "I am very grateful for your time and effort in helping me to gather data\n"
    f"Please email the resulting files \"{file.name}\" and \"{csvfile.name}\" to me at garrnic3@isu.edu\n")
    print("Have a great day!")

