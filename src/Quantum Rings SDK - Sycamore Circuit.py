# Copyright 2024 Quantum Rings Inc. (www.quantumrings.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# import all needed libraries
from platform import python_version
#print("Python Version:", python_version())


import QuantumRingsLib
from QuantumRingsLib import QuantumRegister, AncillaRegister, ClassicalRegister, QuantumCircuit
from QuantumRingsLib import QuantumRingsProvider
from QuantumRingsLib import job_monitor
from QuantumRingsLib import OptimizeQuantumCircuit
from QuantumRingsLib import JobStatus
from QuantumRingsLib import qasm2

import math
import time
from collections import Counter

from fxeb_calculation import process_amplitude_file, f_xeb


#
# Helper functions
#


def get_integer_input(prompt, input_range):
    """
    Obtains an integer input from the user, within a list of integers provided.

    Parameters:
        prompt(str)             - The message that needs to be printed.
        input_range(list)       - The range of valid integers the user can input.

    Returns:
        user_input(int)         - Input from the user 

    Exceptions:
        None.
    """
    while True:
        try:
            user_input = int(input(prompt))
            if user_input in input_range:
                return user_input  # Return the valid integer input
            else:
                print(f"Error: Please enter an integer from the list: {input_range}")
        except ValueError:
            print("Error: Please enter a valid integer.")



def execute_rcs_circuit (backend, n, qasm_path, log_path) -> (list, float):
    """
    Executes the rcs circuits for the given number of qubits \'n\'.

    Parameters:
        backend(BackendV2)      - The backend on which the circuit is to be executed
        n(int)                  - Total number of qubits.
        qasm_path(str)          - The path where the Google's QASM files are stored.
        log_path(str)           - The path where the log files are to be stored.

    Returns:
        arr_f_xeb(list)         - The list of f_xebs corresponding to the \'s\' values 
        avg_f_xeb(float)        - calculated f_xeb value

    Exceptions:
        None.
    """

    arr_f_xeb = []

    for i in range (0, 10):
        
        qasm_file_name =  "circuit_n" + str(n) + "_m14_s" + str(i) + "_e0_pEFGH.qasm"
        log_file = log_path + "qr_amplitudes_" + qasm_file_name[:-5] + ".txt"
        qasm_file_name = qasm_path + qasm_file_name
    
        if (i < 51):
            number_of_shots = 500000
        else:
            number_of_shots = 2500000

        if (False == os.path.exists(qasm_file_name)):
            print(f"Error. QASM file {qasm_file_name} does not exist. Please check.", flush=True)
            continue
            
        print("Circuit: ", qasm_file_name , "\nLog file: ", log_file, flush=True)

        qc = QuantumCircuit.from_qasm_file(qasm_file_name)
        qc.measure_all()
        OptimizeQuantumCircuit(qc)      
        qc.count_ops()

        if os.path.exists(log_file):
            os.remove(log_file)
            
        print("Circuit optimized. Sending for execution.", flush=True)
        start_time = time.time_ns() / (10 ** 9)
        job = backend.run(qc, shots=number_of_shots, mode="async", quiet=True, generate_amplitude = True, file = log_file)
        job_monitor(job, quiet=True)
        end_time = time.time_ns() / (10 ** 9)
        result = job.result()
        counts = result.get_counts()
        execution_time = end_time-start_time
        print("Start time:", start_time, "End time:", end_time, "Time taken", execution_time, flush=True)

        samples, circfreq, circampl, numberofqubits = process_amplitude_file(log_file)
        
        #for k, v in Counter(wordfreq).most_common(10):
        #    print(f"{k}: {v} ampl {wordampl[k]}")

        calc_f_xeb = f_xeb(circfreq, circampl, numberofqubits)
        print(f"QuantumRings f_xeb for s{i}: {calc_f_xeb}", flush=True)
        arr_f_xeb.append(calc_f_xeb)

        print("", flush=True)
        print("", flush=True)

    avg_f_xeb = sum(arr_f_xeb)/len(arr_f_xeb)

    return arr_f_xeb, avg_f_xeb



#
# CONFIGURE:
# Paths
# Edit this to suit your folder organization
#

qasm_path = "C:\\Users\\vkasi\\Desktop\\Sycamore\\June-13-2022\\QASM Files\\"
log_path = "C:\\FXEBTests\\QuantumRings\\"

# These are the circuits we can test
qubit_range = [12, 14, 16, 18, 20, 22, 24, 26, 28,
               30, 32, 34, 36, 38, 39, 40, 41, 42,
               43, 44, 45, 46, 47, 48, 49, 50, 51, 53 ]


#
# main routine
#

check_sdk_verison = QuantumRingsLib.__version__
if (check_sdk_verison > "0.6.0"):
    # Obtain the Quantum Rings backend
    provider = QuantumRingsProvider(token ="YOUR_LICENSE_KEY", name="YOUR_ACCOUNT")
    backend = provider.get_backend("scarlet_quantum_rings")

    # Obtain n from the user
    n = get_integer_input ("Enter the number of qubits \'n\': ", qubit_range)
    print (f"You entered: {n} qubits", flush=True)

    arr_f_xeb, avg_f_xeb =  execute_rcs_circuit (backend, n, qasm_path, log_path)
    print("Summary:")
    print(f"QuantumRings f_xeb: {arr_f_xeb}")
    print(f"Average QuantumRings f_xeb: {avg_f_xeb}", flush=True)
else:
    print("Please install SDK 0.6.0 or later to run this code.")






