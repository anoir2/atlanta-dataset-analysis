from typing import Dict

from model.export_result import ResultUnit
from repository.export_result import ExportResultRepository


class ExportResultRepositoryMock(ExportResultRepository):
    def save(self, elements: Dict[str, ResultUnit]) -> None:
        pass
