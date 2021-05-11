import json
import unittest
from unittest.mock import MagicMock

from exception import DataNotFoundError, UnexpectedDatasetFormatError
from model import DatasetModel
from service.read_dataset import ReadDataset
from test import mock


class MyTestCase(unittest.TestCase):
    def testDatasetShouldHaveZeroElement(self):
        listValues = []
        repository = givenDatasetRepositoryThatReturnValuesList(listValues)
        service = givenReadDatasetService(repository)

        result = whenReadDataGetAllAvailableData(service)

        expected = []
        thenDatasetListIsEqualToExpected(self, expected, result)
        thenDatasetListHasNElements(self, 0, result)

    def testDatasetShouldHaveTwoElement(self):
        listValues = givenDatasetListWithTwoElement()
        repository = givenDatasetRepositoryThatReturnValuesList(listValues)
        service = givenReadDatasetService(repository)

        result = whenReadDataGetAllAvailableData(service)

        expected = givenDatasetListWithTwoElement()
        thenDatasetListIsEqualToExpected(self, expected, result)
        thenDatasetListHasNElements(self, 2, result)

    def testDatasetExceptionThrowingDataNotFoundError(self):
        repository = givenDatasetRepositoryThatThrowError(DataNotFoundError)
        service = givenReadDatasetService(repository)

        thenExpectedExceptionIsRaised(self, DataNotFoundError, whenReadDataGetAllAvailableData, service)

    def testDatasetExceptionThrowingUnexpectedDatasetFormatError(self):
        repository = givenDatasetRepositoryThatThrowError(UnexpectedDatasetFormatError)
        service = givenReadDatasetService(repository)

        thenExpectedExceptionIsRaised(self, UnexpectedDatasetFormatError, whenReadDataGetAllAvailableData, service)


# ********************************************** #
# ****************    GIVEN    ***************** #
# ********************************************** #

def givenReadDatasetService(repository):
    service = ReadDataset(repository)
    return service


def givenDatasetRepositoryThatThrowError(exception):
    repository = mock.DatasetRepositoryMock()
    repository.findAll = MagicMock(side_effect=exception)
    return repository


def givenDatasetRepositoryThatReturnValuesList(returnListValues):
    repository = mock.DatasetRepositoryMock()
    repository.findAll = MagicMock(return_value=returnListValues)
    return repository


def givenDataModelList(givenJson):
    listValues = DatasetModel.from_list_dict(givenJson)
    return listValues


def givenDatasetListWithTwoElement():
    jsonValues = json.loads('['
                            '{'
                            '"occur_time": "05:00:00",'
                            '"occur_date":"12/31/2017", '
                            '"crime_type":"LARCENY-FROM VEHICLE", '
                            '"avg_day": "Sun" ,'
                            '"neighborhood": "Wildwood (NPU-C)", '
                            '"location": "2020 HOWELL MILL RD NW @PUBLIX - HOWELL", '
                            '"x": -84.413470000000004, '
                            '"y": 33.810220000000001'
                            '}, '
                            '{'
                            '"occur_time": "05:00:00",'
                            '"occur_date":"12/31/2017", '
                            '"crime_type":"LARCENY-FROM VEHICLE", '
                            '"avg_day": "Sun" ,'
                            '"neighborhood": "Wildwood (NPU-C)", '
                            '"location": "2020 HOWELL MILL RD NW @PUBLIX - HOWELL", '
                            '"x": -84.413470000000004,'
                            '"y": 33.810220000000001'
                            '}'  
                            ']')
    return givenDataModelList(jsonValues)


# ********************************************** #
# ****************    WHEN    ****************** #
# ********************************************** #

def whenReadDataGetAllAvailableData(service):
    result = service.getAllData()
    return result


# ********************************************** #
# ****************    THEN    ****************** #
# ********************************************** #

def thenDatasetListIsEqualToExpected(testObj, expected, result):
    testObj.assertEqual(expected, result)


def thenDatasetListHasNElements(testObj, elementNumber, result):
    testObj.assertEqual(elementNumber, len(result))


def thenExpectedExceptionIsRaised(testObj, expected, actual, *args):
    testObj.assertRaises(expected, actual, *args)


if __name__ == '__main__':
    unittest.main()
