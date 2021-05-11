import json
import unittest
from unittest.mock import MagicMock

from exception import DataNotFoundError, UnexpectedDatasetFormatError, DatasetEmptyError
from model import DatasetModel
from service.extract_dataset import ExtractDataFromDataset
from service.read_dataset import ReadDataset
from test import mock


class MyTestCase(unittest.TestCase):
    def testExtractDatasetServiceWithCorrectData(self):
        elements = givenDatasetListWithTwoElement()

        extractService = whenServiceIsInstanciated(elements)

        thenServiceIsCreatedCorrectly(self, extractService)

    def testExtractDatasetServiceWithEmptyListValue(self):
        elements = []

        thenExpectedExceptionIsRaised(self, DatasetEmptyError, whenServiceIsInstanciated, elements)

    def testExtractDatasetServiceWithNoneValue(self):
        elements = None

        thenExpectedExceptionIsRaised(self, DataNotFoundError, whenServiceIsInstanciated, elements)

# ********************************************** #
# ****************    GIVEN    ***************** #
# ********************************************** #


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


def givenExtractDatasetService(elements):
    return ExtractDataFromDataset(elements)


# ********************************************** #
# ****************    WHEN    ****************** #
# ********************************************** #


def whenServiceIsInstanciated(elements):
    return givenExtractDatasetService(elements)


# ********************************************** #
# ****************    THEN    ****************** #
# ********************************************** #

def thenServiceIsCreatedCorrectly(testObj, extractService):
    testObj.assertIsNotNone(extractService)


def thenExpectedExceptionIsRaised(testObj, expected, actual, *args):
    testObj.assertRaises(expected, actual, *args)

if __name__ == '__main__':
    unittest.main()
