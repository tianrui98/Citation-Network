#%% Set-up
import sys, os
#%% Set-up
import pathlib
from datetime import datetime
import warnings
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')

date = datetime.now().strftime("%d_%m_%Y_%H%M")

# sys.path.append(os.path.abspath(os.path.join('..', 'lib')))
#set the working directory to the folder containing the current script
pathlib.Path(__file__).parent.absolute()
#all outputs will be saved to the current folder
save_path = 'test/test_output/'+ date

if not os.path.exists(save_path):
    os.makedirs(save_path)

#%%$ Run main functions in sequence
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))

from lib.flow import *

if __name__ == "__main__":
    RunAll (save_path)
