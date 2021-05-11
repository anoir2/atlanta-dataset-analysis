from exception import UnitOfWorkEmptyError
from model.export_result import ResultUnit
from repository.export_result import ExportResultUnitOfWork


class ExportResultService:
    _unitOfWork: ExportResultUnitOfWork

    def __init__(self, unitOfWork: ExportResultUnitOfWork):
        self._unitOfWork = unitOfWork

    def addElementToExport(self, element: ResultUnit):
        self._unitOfWork.add(element)

    def completeExportProcess(self):
        if self._unitOfWork.isEmpty():
            raise UnitOfWorkEmptyError
        self._unitOfWork.complete()
