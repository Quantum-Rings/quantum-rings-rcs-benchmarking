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



def plot_Potter_ThomsonDistribution( sourcefilename, graphfilename ):
    """
    Plots the Potter Thomson distrubution

    Parameters:
        sourcefilename(str)     - The input amplitude file.
        graphfilename(str)      - The name of the file where the the graph is to be save.

    Returns:
        None

    Exceptions:
        None.

    """


    sampleSize, wordfreq, wordampl, numberofqubits = process_amplitude_file(sourcefilename)
    N_prob = {}
    N = 2 ** numberofqubits
    
    
    #wordfreq ---> dict of (bitstring, frequency of bitstring)
    
    for k, v in wordfreq.items():
        vv = v / sampleSize
        N_prob[k] = vv * N
        
    #print( numberofqubits)
    #print(f_xeb(wordfreq, wordampl,  numberofqubits))
    
    # N_prob ---> dict of (bitstring, Np)
    
    countofprobs = 0
    
    probfreq = {}
    for k, v in N_prob.items():
        if v not in probfreq:
            probfreq[v] = 0
        probfreq[v] += 1
        countofprobs += 1
        
    #probfreq ---> dict of ( Np, frequency of Np )
    
    probprob = {}
    for k, v in probfreq.items():
        vv = v / countofprobs
        probprob[k] = vv
        
    #probprob ---> dict of (Np, pr(Np))
    
    # Prepare the theoretical Porter-Thomas distribution
    # Create the x-axis range from Np created from the experimental values
    xspace = np.linspace(min(probprob.keys()), max(probprob.keys()), 25) #len(probprob))
    # scale this down so that both the theoretical and the experimental values can plot on the same graph
    # Note: xspace is already Np
    yspace = N * np.exp(-xspace) / sampleSize  
    
    # Standard Deviation
    std_dev = np.std(yspace, ddof=1)  # Use ddof=1 for sample standard deviation
    
    # Standard Error
    std_error = std_dev / np.sqrt(len(yspace))
  
    
    # plot both Quantum Rings and theoretical calculations
    fig, ax = plt.subplots(figsize=(9, 6)) 
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.set_xlabel("Np")
    ax.set_ylabel("pr(Np)")
    #ax.set_title("Distribution of the Probabilities")
    
    plt.scatter(probprob.keys(), probprob.values(), color='#d62728', label='QR Distribution ' + "n = " + str(numberofqubits))
    plt.plot(xspace, yspace, color='#000000', label='Theoretical Porter-Thomas Distribution', linewidth=1.5)

    plt.errorbar(xspace, yspace,  yerr = std_error, fmt ='o',capsize=3,color='000000', label = "Standard Error")
    
    # plot the uniform distribution for reference
    plt.axvline(x=1/N, linestyle='--', color='#1f77b4', label='Uniform Distribution', linewidth=1.5)
    
    plt.tick_params(axis='both', direction='out', length=6, width=2, labelcolor='b', colors='r', grid_color='gray', grid_alpha=0.5)
    
    plt.legend(loc='best', fontsize=12)
    fig.tight_layout()
    
    # Save the figure
    fig.savefig(graphfilename, dpi=300, bbox_inches='tight')
    
    plt.show()


#
#
#


def plot_Probability( sourcefilename, graphfilename ):
    """
    Plots the probabilities

    Parameters:
        sourcefilename(str)     - The input amplitude file.
        graphfilename(str)      - The name of the file where the the graph is to be save.

    Returns:
        None

    Exceptions:
        None.

    """
    sampleSize, wordfreq, wordampl, numberofqubits = process_amplitude_file(sourcefilename)

    N_prob = {}
    N = 2 ** numberofqubits
    
    
    for k, v in wordfreq.items():
        vv = v / sampleSize
        N_prob[k] = vv
        
    top_samples = {}
    for k, v in Counter(N_prob).most_common(15):
        #print(f"{k}: {v} ampl {wordampl[k]}")
        top_samples[k] = v
    
   
    fig, ax = plt.subplots(figsize=(9, 6)) 
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    #ax.yaxis.offsetText.set_visible(False)
    ax.set_xlabel("Measurement")
    ax.set_ylabel("Probability")
    ax.set_title("Measurement and Probability n = " + str(numberofqubits))
    plt.setp(ax.get_xticklabels(), rotation=25, horizontalalignment='right')
    plt.bar(top_samples.keys(), top_samples.values())
    plt.tick_params(axis='both', direction='out', length=6, width=2, labelcolor='b', colors='r', grid_color='gray', grid_alpha=0.5)
    
    formatter = ScalarFormatter(useMathText=True)
    formatter.set_powerlimits((-3, 4))  # Adjust this to change when scientific notation is used
    
    ax.yaxis.set_major_formatter(formatter)
    
    # Force the offset text to be updated
    fig.canvas.draw()
    
    # Retrieve the offset text (scale factor)
    scale_factor = ax.yaxis.get_offset_text().get_text()
    
    # Remove the offset text from being displayed
    ax.yaxis.get_offset_text().set_visible(False)
    
    # Include the scale factor in the y-axis label
    ax.set_ylabel(f'Probability {scale_factor}')
    
    fig.tight_layout()

    # Save the figure
    fig.savefig(graphfilename, dpi=300, bbox_inches='tight')
    
    plt.show()


def plot_f_xeb( qubits_range, google_f_xeb, quantum_rings_f_xeb, graphfilename ):
    """
    Plots the f_xeb

    Parameters:
        qubits_range(list)          - List of n values.
        google_f_xeb(list)          - List of google f_xeb values.
        quantum_rings_f_xeb(list)   - List of Quantum Rings f_xeb values.
        graphfilename(str)          - The name of the file where the the graph is to be save.

    Returns:
        None

    Exceptions:
        None.

    """
    
    # plot both Quantum Rings and theoretical calculations
    fig, ax = plt.subplots(figsize=(9, 6)) 
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.set_xlabel("Qubits")
    ax.set_ylabel("F_XEB (m=14, e0)")
    #ax.set_title("F_XEB Plot")
    ax.set_yscale('log')
    ax.set_ylim([0.001, 1.2])
    ax.set_xlim([min(qubits_range)-2, max(qubits_range)+2])
    
    
    # mark dotted lines for all the 'NaN' data
    
    mark = []
    
    for i in range (0, len(google_f_xeb)):
        if ( float('NaN') != google_f_xeb[i] ):
            mark.append(i)
        
    x = np.array(qubits_range)
    y = np.array(google_f_xeb)
    
    yp = np.copy(y)
    if ~np.isfinite(y[0]): yp[0] = yp[1]
    if ~np.isfinite(y[-1]): yp[-1] = yp[-2]
    
    mask = np.isfinite(y)
    
    
    # Standard Deviation
    std_dev = np.std(quantum_rings_f_xeb, ddof=1)  # Use ddof=1 for sample standard deviation
    
    # Standard Error
    std_error = std_dev / np.sqrt(len(quantum_rings_f_xeb))
        
    plt.plot(qubits_range, quantum_rings_f_xeb, marker='o', color='red', label='Quantum Rings', linewidth=1.5)
    plt.errorbar(qubits_range, quantum_rings_f_xeb,  yerr = std_dev, fmt ='o',capsize=5,color='red', label = "Standard Deviation")
    #plt.errorbar(qubits_range, quantum_rings_f_xeb,  yerr = std_error, fmt ='o',capsize=5,color='blue', label = "Standard Error")
    
    ax.plot(x[mask],yp[mask], color='blue', linewidth=1.5, ls="--")
    plt.plot(qubits_range, google_f_xeb, marker='o', markevery=mark, color='blue', label='Google-June 13, 2022', linewidth=1.5)
    
    # plot the uniform distribution for reference
    plt.axhline(y=1, linestyle='--', color='000000', label='F_XEB=1', linewidth=1.5)
    
    plt.tick_params(axis='both', direction='out', length=6, width=2, labelcolor='b', colors='r', grid_color='gray', grid_alpha=0.5)
    
    plt.legend(loc='best', fontsize=12)
    fig.tight_layout()
    
    # Save the figure
    if (len(graphfilename) > 0 ):
        fig.savefig(graphfilename, dpi=300, bbox_inches='tight')
    
    plt.show()
