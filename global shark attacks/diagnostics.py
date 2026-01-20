import sys
import os

filepath = r'e:\programming\data science\global shark attacks\test_result.txt'
with open(filepath, 'w') as f:
    f.write(f'Python version: {sys.version}\n')
    f.write(f'Current Dir: {os.getcwd()}\n')
    try:
        import pandas as pd
        f.write(f'Pandas version: {pd.__version__}\n')
    except ImportError:
        f.write('Pandas not found\n')
