from typing import List

from model import DatasetModel
from repository.dataset import DatasetRepository


class DatasetRepositoryMock(DatasetRepository):
    def findAll(self) -> List[DatasetModel]:
        pass
