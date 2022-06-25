import os
import csv
import json 
from sre_constants import ANY
from typing import List

"""
Class used for reading dataset from csv file, sample filtering and mapping to objects.

Decoupled from the dataset sample format.

To use it:
    * Instantiate DatasetManager().
    * Call its setup() method.
    * Call its getDatasetObjects() to get dataset rows mapped to objects.
"""
class DatasetManager:
    def __init__(self, path, invalids) -> None:
        self.__datasetPath = path
        self.__invalids = invalids

    class DatasetRow:
        def __init__(self, props) -> None:
            for key in props:
                self.__setattr__(key, ANY)
        
        def __setitem__(self, key, value):
            setattr(self, key, value)

        def __getitem__(self, key):
            return getattr(self, key)


    # Dataset's directory absolute path.
    __datasetPath = ""

    # Invalid value to be used for sample filtering.
    __invalids = []

    # Dynamic list of attributes read from dataset and used to create DatasetRow class.
    __attributes = []

    # List of all absolute paths for all dataset files.
    __datasetFilesPaths = []
    
    # List of json objects read from the dataset.
    __csvRows = []

    # List of DatasetRow (converted list of json objects).
    __datasetObjects = []

    # Counter for invalid number of samples.
    __invalidRowCount = 0

    """
    Find all dataset samples' absolute paths.
    """
    def  __findDatasetAbsPaths(self):
        for root, dirs, files in os.walk(self.__datasetPath):
            for file in files:
                # Find dataset files:
                if (file.find(".csv") > -1):
                    path = f"{root}/{file}"
                    self.__datasetFilesPaths.append(os.path.abspath(path))
    # print(_findDatasetAbsPaths.__doc__)

    """
    Open all dataset files and load its data.
    """
    def __loadDataset(self):
        for filePath in self.__datasetFilesPaths:
            path = os.path.abspath(filePath)
            with open(path, newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    jsonRow = ",".join(row)
                    # Convert to json format:
                    jsonRow = jsonRow.replace("'", "\"")
                    
                    # Exclude invalid samples:
                    for invalid in self.__invalids:
                        if (jsonRow.find(invalid) == -1):
                            # print(jsonRow)
                            jsonObj = json.loads(jsonRow)
                            self.__csvRows.append(jsonObj)
                        else:
                            self.__invalidRowCount += 1

    def __loadAttributes(self):
        for row in self.__csvRows:
            for key in row:
                self.__attributes.append(key)
            break

    """
    Convert all jsons to objects.
    """
    def __convertJsonsToObjects(self):
        for row in self.__csvRows:
            dataRow = self.DatasetRow(self.__attributes)
            for attr in self.__attributes:
                dataRow[attr] = row[attr]
            self.__datasetObjects.append(dataRow)

    """
    Print total, valid and invalid number of results.
    """
    def __printStatus(self, skip):
        if (not skip):
            for row in self.__csvRows:
                print(row)
        print(f"Dataset attributes: {self.__attributes}")
        print(f"Total number of samples: {self.__csvRows.__len__() + self.__invalidRowCount}")
        print(f"VALID: {self.__csvRows.__len__()}")
        print(f"INVALID: {self.__invalidRowCount}")

        # PRINT_TOTAL()
        # PRINT_VALID(self.__csvRows.__len__())
        # PRINT_INVALID(self.__invalidRowCount)

    """
    Method for reading dataset from csv, filtering and json to object conversion.
    """
    def setup(self, skip = True):
        self.__findDatasetAbsPaths()
        self.__loadDataset()
        self.__loadAttributes()
        self.__convertJsonsToObjects()
        self.__printStatus(skip)

    """
    Getter for converted dataset objects.
    """
    def getDatasetObjects(self) -> List[DatasetRow]: 
        return self.__datasetObjects