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



def process_amplitude_file (filename) -> (int, dict, dict, int) :
    """
    Processes an input amplitude file, and calculates the probability of each measurement
    from the amplitudes. From the probabilities, it then calculates the frequency of occurance
    of each measurement.

    Parameters:
        filename(str)       - The input amplitude file.

    Returns:
        totalSamples(int)   - Total number of samples in the input file.
        measfreq(dict)      - dictionary of measurement and its frequency
        meassampl(dict)     - dictionary of measurement and the corresponding probability
        num_qubits(int)     - The total number of qubits (n) corresponding to the input amplitude file.

    Exceptions:
        None.

    """

    input_file = open(filename, 'r')
    
    measfreq = {}
    measampl = {}

    totalSamples = 0
    
    # Using for loop
    for line in input_file:
        items = line.strip().split()
        # Access the three items
        item1, item2, item3 = items[0], items[1], items[2]
        Y = complex(float(item2), float(item3))
        YY = abs(Y)**2
        
        if item1 not in measfreq:
            measfreq[item1] = 0
            measampl[item1] = YY
        measfreq[item1] += 1

        totalSamples += 1
    
    # Close input file
    input_file.close()

    first_key = next(iter(measfreq))

    num_qubits = len(first_key)
    
    return totalSamples, measfreq,  measampl, num_qubits



def f_xeb(counts, probs, n) ->float :
    """
    Calculates the linear cross-entropy benchmark (XEB) from the measurement frequencies
    and probabilities determined from the method process_amplitude_file.

    Parameters:
        counts(dict)    - Dictionary of amplitudes (key) and frequencies of each amplitude (value).
        probs(dict)     - Dictionary of amplitudes (key) and amplitudes of each amplitude (value).
        n(int)          - Total number of qubits.

    Returns:
        calculated f_xeb value (float)

    Exceptions:
        None.

    """
    total_samples = 0
    avg_prob = 0

    for key, val in counts.items():
        avg_prob += counts[key] * probs[key]
        total_samples += counts[key]

    calc_f_xeb = ((2**n) * (avg_prob / total_samples) )   - 1
    
    return calc_f_xeb