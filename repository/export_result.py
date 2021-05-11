import os
from typing import Dict, Any
from abc import ABCMeta, abstractmethod
from arcgis.widgets import MapView
from bokeh.io import save, reset_output
from bokeh.plotting import Figure
from pandas_bokeh import output_file
from model.export_result import ResultUnit


class ExportResultRepository(metaclass=ABCMeta):
    @abstractmethod
    def save(self, elements: Dict[str, ResultUnit]) -> None:
        pass


class ExportResultUnitOfWork:
    _result: Dict[str, ResultUnit]
    _repository: ExportResultRepository

    def __init__(self, repository: ExportResultRepository):
        self._result = dict()
        self._repository = repository

    def add(self, resultUnit: ResultUnit) -> None:
        key = resultUnit.fileName
        self._result[key] = resultUnit

    def complete(self) -> None:
        self._repository.save(self._result)
        self._result = dict()

    def isEmpty(self) -> bool:
        return len(self._result.keys()) == 0


class LocalSaveFactory:
    def arc_gis_map(self, path: str, arcGisMap: MapView):
        arcGisMap.export_to_html(path)

    def bokeh_plot(self, path: str, plot: Figure):
        output_file(path)
        save(plot)
        reset_output()


class LocalExportResultRepository(ExportResultRepository):
    _basePath: str
    _saveMethod: Any

    def __init__(self, basePath, saveMethod):
        self._basePath = basePath
        self._saveMethod = saveMethod

    def save(self, elements: Dict[str, ResultUnit]) -> None:
        for _, element in elements.items():
            file_path = os.path.join(self._basePath, element.fileName)
            saveMethodName = element.type.value
            saveMethod = getattr(self._saveMethod, saveMethodName, None)
            if saveMethod is None:
                raise NotImplementedError("Method {} not implemented".format(saveMethodName))

            saveMethod(file_path, element.data)

