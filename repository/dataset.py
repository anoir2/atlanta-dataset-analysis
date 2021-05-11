import json
import requests

from typing import List
from model import DatasetModel
from abc import ABCMeta, abstractmethod
from exception import DataNotFoundError, UnexpectedDatasetFormatError


class DatasetRepository(metaclass=ABCMeta):
    @abstractmethod
    def findAll(self) -> List[DatasetModel]:
        pass


class LocalDatasetRepository(DatasetRepository):
    def __init__(self, filePath):
        self.filePath = filePath

    def findAll(self) -> List[DatasetModel]:
        datasetFilePointer = open(self.filePath, 'r')

        try:
            datasetFile = datasetFilePointer.read()
            datasetJson = json.loads(datasetFile)
            datasetModels = DatasetModel.from_list_dict(datasetJson)
        except FileNotFoundError:
            raise DataNotFoundError
        except KeyError:
            raise UnexpectedDatasetFormatError

        return datasetModels


class RemoteDatasetRepository(DatasetRepository):
    def __init__(self, fileURI):
        self._fileURI = fileURI

    def findAll(self) -> List[DatasetModel]:
        try:
            datasetContent = requests.get(self._fileURI).content
            datasetJSON = json.loads(datasetContent)
            datasetModels = DatasetModel.from_list_dict(datasetJSON)
        except RuntimeError:
            raise DataNotFoundError
        except KeyError:
            raise UnexpectedDatasetFormatError

        return datasetModels
