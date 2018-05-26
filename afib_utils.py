import wfdb as wf
import numpy as np
from glob import glob
from matplotlib import pyplot as plt
import re, os, shutil


def get_records():
    """ Get paths for data in data/ directory """

    # There are 3 files for each record
    # *.atr is one of them
    paths = glob('data/*.hea')

    # Get rid of the extension
    paths = [path[:-4] for path in paths]
    paths.sort()

    return paths


def extract_afib_records(records): 
    """ Extracts all p records, dividing them into 
        two groups - one with afib and one without """ 
    afib = []
    afib_cont = []
    
    regular = []
    regular_cont = []

    for r in records:
        has_p = re.search(r'[p]', r)
        has_c = re.search(r'[c]', r)
        afib_match = re.search(r'[p].[2,4,6,8]', r)
        afib_tens = re.search(r'[p][1,2,3,4,5][0]', r)
        
        if has_p:
            if afib_match or afib_tens:
                if has_c:
                    afib_cont.append(r)
                else: 
                    afib.append(r)
            
            elif has_c:
                regular_cont.append(r)
            else:
                regular.append(r)
    
    return afib, afib_cont, regular, regular_cont


def extract_test_records(records): 
    """ Extracts all n records """ 
    test = []
    test_cont = []

    for r in records:
        match = re.search(r'[n]', r)
        has_c = re.search(r'[c]', r)
        if match:
            if has_c:
                test_cont.append(r)
            else:
                test.append(r)
    
    return test, test_cont


def plot_ekg(record_path): 
    record = wf.rdrecord(record_path) 
    chid = 0
    data = record.p_signal
    channel = data[:, chid]

    print('ECG channel type:', record.sig_name[chid])

    # Plot only the first 2000 samples
    howmany = 100

    # Calculate time values in seconds
    times = np.arange(howmany, dtype = 'float') / record.fs

    plt.plot(times, channel[ : howmany])
    plt.xlabel('Time [s]')
    plt.show()
    
def make_data_dirs(records, dir_names):
    ''' makes separate data directories for series of records
    records: list of lists containing the datafiles that will go into dir
    dir_names: the names of the directories to be created
    '''
    assert(len(records) == len(dir_names))
    
    EXTENSIONS = ['.dat', '.hea', '.qrs']
    os.chdir(os.getcwd())
    print(os.getcwd())
                  
    for i, directory in enumerate(dir_names):        
        if not os.path.exists(directory):
            os.mkdir(directory)
            for rec in records[i]:
                for ex in EXTENSIONS:
                    shutil.copy(rec+ex, directory)  
    