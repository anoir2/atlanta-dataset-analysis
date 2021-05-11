from typing import List
from model import DatasetModel
from repository.dataset import DatasetRepository


class ReadDataset:
    def __init__(self, repository: DatasetRepository):
        self.repository = repository

    def getAllData(self) -> List[DatasetModel]:
        return self.repository.findAll()
