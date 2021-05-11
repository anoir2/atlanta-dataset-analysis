import unittest
from unittest.mock import MagicMock
from exception import UnitOfWorkEmptyError
from model.export_result import ResultUnit, ResultType
from repository.export_result import ExportResultUnitOfWork
from service.export_file import ExportResultService
from test import mock


class MyTestCase(unittest.TestCase):
    def testWithElementsToExport(self):
        exportRepository = givenExportResultRepository()
        exportUnitOfWork = givenExportResultUnitOfWork(exportRepository)
        exportService = givenExportResultService(exportUnitOfWork)
        resultUnitOne = ResultUnit(MagicMock(), "file-name-1", ResultType.BOKEH_PLOT)
        resultUnitTwo = ResultUnit(MagicMock(), "file-name-2", ResultType.BOKEH_PLOT)

        whenAddElementIntoUnitOfWork(exportService, resultUnitOne)
        whenAddElementIntoUnitOfWork(exportService, resultUnitTwo)
        whenCompleteExportProcessIsCalled(exportService)

        expectedResultList = {"file-name-1": resultUnitOne, "file-name-2": resultUnitTwo}
        thenRepositorySaveIsCalledOnce(self, exportRepository)
        thenRepositorySaveIsCalledWithResultListAsArgument(self, exportRepository, expectedResultList)

    def testWithElementsToExportWithFirstElementOverride(self):
        exportRepository = givenExportResultRepository()
        exportUnitOfWork = givenExportResultUnitOfWork(exportRepository)
        exportService = givenExportResultService(exportUnitOfWork)
        resultUnitOne = ResultUnit(MagicMock(), "file-name-1", ResultType.BOKEH_PLOT)
        resultUnitTwo = ResultUnit(MagicMock(), "file-name-2", ResultType.BOKEH_PLOT)
        resultUnitOneOverride = ResultUnit(MagicMock(), "file-name-1", ResultType.ARC_GIS_MAP)

        whenAddElementIntoUnitOfWork(exportService, resultUnitOne)
        whenAddElementIntoUnitOfWork(exportService, resultUnitTwo)
        whenAddElementIntoUnitOfWork(exportService, resultUnitOneOverride)
        whenCompleteExportProcessIsCalled(exportService)

        expectedResultList = {"file-name-1": resultUnitOneOverride, "file-name-2": resultUnitTwo}
        thenRepositorySaveIsCalledOnce(self, exportRepository)
        thenRepositorySaveIsCalledWithResultListAsArgument(self, exportRepository, expectedResultList)

    def testWithNoElementToExport(self):
        exportRepository = givenExportResultRepository()
        exportUnitOfWork = givenExportResultUnitOfWork(exportRepository)
        exportService = givenExportResultService(exportUnitOfWork)

        thenExpectedExceptionIsRaised(self, UnitOfWorkEmptyError, whenCompleteExportProcessIsCalled, exportService)


# ********************************************** #
# ****************    GIVEN    ***************** #
# ********************************************** #


def givenExportResultUnitOfWork(exportRepository):
    return ExportResultUnitOfWork(exportRepository)


def givenExportResultRepository():
    repository = mock.ExportResultRepositoryMock()
    repository.save = MagicMock()

    return repository


def givenExportResultService(exportUnitOfWork):
    return ExportResultService(exportUnitOfWork)


# ********************************************** #
# ****************    WHEN    ****************** #
# ********************************************** #


def whenAddElementIntoUnitOfWork(exportService: ExportResultService, element):
    exportService.addElementToExport(element)


def whenCompleteExportProcessIsCalled(exportService):
    exportService.completeExportProcess()


# ********************************************** #
# ****************    THEN    ****************** #
# ********************************************** #


def thenExpectedExceptionIsRaised(testObj, expected, actual, *args):
    testObj.assertRaises(expected, actual, *args)


def thenRepositorySaveIsCalledOnce(testObj, exportRepository):
    testObj.assertEqual(exportRepository.save.call_count, 1)


def thenRepositorySaveIsCalledWithResultListAsArgument(testObj, exportRepository, resultList):
    exportRepository.save.assert_called_with(resultList)