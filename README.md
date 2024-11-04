# Cross-Entropy Benchmarking on the Quantum Rings SDK

Folder Organization
--------------------

    [root]
       ├── src                                             <- Source code folder 
       |    ├── Quantum Rings SDK - Sycamore Circuit.py    <- The main Python file which executes the Sycamore circuits
       |    ├── fxeb_calculation.py                        <- Python code containing routines to calculate linear F_XEB
       |    ├── graphing_functions.py                      <- Python code containing graphing functions   
       ├── README.md                                       <- This file
       ├── amplitudes                                      <- Look here for more information on from where to download the amplitude files from Quantum Rings experiments
                            
--------------------

## STEP 1 Download Google Dryad Repository

Download the Data files dated June 13, 2022, from [DRYAD](https://doi.org/10.5061/dryad.k6t1rj8).
Expand the 'tar.gz' files
Retain the QASM files with the pattern `circuit_n*_m14_s*_e0_pEFGH.qasm` and the amplitude files with the pattern `amplitudes_n*_m14_s*_e0_pEFGH.txt`
You may discard the rest of the files.
To keep everything well organized, you can store the QASM files and amplitude files in a folder structure like this:

    [dryad]
       ├── qasm                                             <- Google provided QASM files
       ├── amplitudes                                       <- All the amplitude files provided by Google

--------------------

## STEP 2 Install Quantum Rings SDK

Signup and create your Quantum Rings account at [SIGNUP](https://quantumrings.com/). Follow the onscreen instructions to activate your account and obtain the license keys.
Install the SDK as outlined in [INSTALL SDK](https://quantumrings.com/doc/Installation.html).

## STEP 3 Execute the Sycamore circuits

Download the Python source code outlined in `Folder Organization.` Edit the following two lines the file `Quantum Rings SDK - Sycamore Circuit.py` to reflect the folder path
where you have downloaded the dryad repository as explianed in Step 2. Depending upon your platform -- Windows or linux --- use appropriate folder seperators --  `\\` or `/`.

```
qasm_path = "C:\\Users\\vkasi\\Desktop\\Sycamore\\June-13-2022\\QASM Files\\"
log_path = "C:\\FXEBTests\\QuantumRings\\"
```

From your Python command prompt, execute the following command:

```
python "Quantum Rings SDK - Sycamore Circuit.py"
```

Once prompted, enter the value for `n` to select the qubit size for the circuits you want to run. 
Note that, depending upon your system configuration, it may take sometime. Hang tight!!

> ⚠️**IMPORTANT**
> Quantum Rings SDK version 0.6.0 or later is required to generate amplitudes. You can check your SDK version by typing the following code in the commmand line.
> ```
> print(QuantumRingsLib.__version__)
> ```


## STEP 4 Plot the f_xeb values obtained

You can use the following lines of code to generate the f_xeb graph. Be sure to replace with your data! and use appropriate folder seperator in the image file path!!
Note that the 'NaN' values are the circuits for which amplitudes are not provided by Google.

```
from fxeb_calculation import plot_f_xeb

qubits_range = [12,14,16,18,20,22,24,26,28,30,32,34,36,38,39,40,41,42,43,44,45,46,47,48,49,50,51,53]

# Replace the following with your data!
quantum_rings_f_xeb = [0.6482126191,0.6060935058,0.6688798281,0.6701486739,0.6239790610,0.6691315513,0.6275010378,0.6586183194,
                       0.6266498558,0.7045217950,0.7702898257,0.6894628052,0.7329588928,0.6307282078,0.6166113934,0.6676224862,
                       0.6876358129,0.7207449382,0.6258813506,0.7405889928,0.7286001290,0.6594373156,0.6279716700,0.7553807635,
                       0.6575359697,0.7349589604,0.7068855806,0.6225257618]

google_f_xeb = [0.3701487273, 0.3298103449, 0.2721089653, 0.2442371206, 0.2184211384, 0.165036218, 0.1407034141, 0.1141170845,
                0.09490405143, 0.0822755337, 0.07126891799, 0.05855909273, 0.05195515039, 0.04188335939, 0.03291150865, float('NaN'), 
                float('NaN'), float('NaN'), float('NaN'), float('NaN'), float('NaN'), float('NaN'), float('NaN'), float('NaN'), float('NaN'),
                float('NaN'), float('NaN'),
                0.007406441391]


imagefile = 'C:\\FXEBTests\\f_xeb_m14_e0.svg'

plot_f_xeb(qubits_range, google_f_xeb, quantum_rings_f_xeb, imagefile)
```

--------------------
<div align="center"> &copy; 2024 Quantum Rings Inc. All Rights Reserved. </div>
   
   
  


