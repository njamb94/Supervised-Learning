import os

# Model attributes
_DEVICE = 'device'
_HUMIDITY = 'humidity'
_TEMP = 'temperature'
_EXP = 'experiment'
_TIME = 'time'

DATASET_ATR = [
    _DEVICE,
    _HUMIDITY,
    _TEMP,
    _EXP,
    _TIME
]

# Dataset location
_DATASET_DIR = "dataset"
_path = os.path.abspath(_DATASET_DIR)
DATASET_PATH = f"{_path}"

# Dataset invalid value
DATASET_INVALID = ["None"]

# Dataset results (print)
_DATASET_PRINT = lambda text, value: f"{text}:{value}"
PRINT_TOTAL = lambda total: print(_DATASET_PRINT("Total number of samples", total))
PRINT_VALID = lambda valid: print(_DATASET_PRINT("VALID", valid))
PRINT_INVALID = lambda invalid: print(_DATASET_PRINT("INVALID", invalid))
