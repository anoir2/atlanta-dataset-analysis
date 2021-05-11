import unittest
from unittest.mock import MagicMock
from exception.dataset_empty import DatasetEmptyError
from service.arc_gis import ArcGISService
from test import mock


class MyTestCase(unittest.TestCase):
    def testGetMapByFelonyOneTimeWithANonEmptyDataframe(self):
        useCache = False
        mapView = givenMapView()
        layerList = [mock.Layer(), mock.Layer()]
        search_result = givenSearchResultWithLayers(layerList)
        gisRepository = givenGISRepository(mapView, search_result)
        dataframe = givenPopulatedDataframe()
        gisService = givenGISService(gisRepository, useCache)

        whenGetCrimesMapByFelonyIsCalled(dataframe, gisService)

        thenMapView_drawIsCalledNTimes(self, mapView, 1)
        thenMapView_add_layerIsCalledNTimes(self, mapView, 2)
        thenGisRepository_mapIsCalledNTimesWithAtlantaCityName(self, gisRepository, 1)
        thenGisRepository_content_getIsCalledNTimes(self, gisRepository, 1)

    def testGetMapByFelonyOneTimeWithAEmptyDataframe(self):
        useCache = False
        mapView = givenMapView()
        layerList = [mock.Layer(), mock.Layer()]
        search_result = givenSearchResultWithLayers(layerList)
        gisRepository = givenGISRepository(mapView, search_result)
        dataframe = {"x": [], "y": []}
        gisService = givenGISService(gisRepository, useCache)

        thenExpectedExceptionIsRaised(self, DatasetEmptyError, whenGetCrimesMapByFelonyIsCalled, dataframe, gisService)

    def testGetMapByFelonyTwoTimesWithoutCache(self):
        useCache = False
        mapView = givenMapView()
        layerList = [mock.Layer(), mock.Layer()]
        search_result = givenSearchResultWithLayers(layerList)
        gisRepository = givenGISRepository(mapView, search_result)
        dataframe = givenPopulatedDataframe()
        gisService = givenGISService(gisRepository, useCache)

        whenGetCrimesMapByFelonyIsCalled(dataframe, gisService)
        whenGetCrimesMapByFelonyIsCalled(dataframe, gisService)

        thenMapView_drawIsCalledNTimes(self, mapView, 2)
        thenMapView_add_layerIsCalledNTimes(self, mapView, 4)
        thenGisRepository_mapIsCalledNTimesWithAtlantaCityName(self, gisRepository, 2)
        thenGisRepository_content_getIsCalledNTimes(self, gisRepository, 2)

    def testGetMapByFelonyTwoTimesWithCache(self):
        useCache = True
        mapView = givenMapView()
        layerList = [mock.Layer(), mock.Layer()]
        search_result = givenSearchResultWithLayers(layerList)
        gisRepository = givenGISRepository(mapView, search_result)
        dataframe = givenPopulatedDataframe()
        gisService = givenGISService(gisRepository, useCache)

        whenGetCrimesMapByFelonyIsCalled(dataframe, gisService)
        whenGetCrimesMapByFelonyIsCalled(dataframe, gisService)

        thenMapView_drawIsCalledNTimes(self, mapView, 2)
        thenMapView_add_layerIsCalledNTimes(self, mapView, 4)
        thenGisRepository_mapIsCalledNTimesWithAtlantaCityName(self, gisRepository, 2)
        thenGisRepository_content_getIsCalledNTimes(self, gisRepository, 1)


# ********************************************** #
# ****************    GIVEN    ***************** #
# ********************************************** #

def givenGISService(gisRepository, useCache):
    gisService = ArcGISService(gisRepository, use_cache=useCache)
    return gisService


def givenPopulatedDataframe():
    return {"x": [12.23, 10.45], "y": [8.98, -1.33]}


def givenSearchResultWithLayers(layerList):
    search_result = MagicMock()
    search_result.layers = layerList
    return search_result


def givenGISRepository(mapView, search_result):
    gisRepository = mock.GIS()
    gisRepository.map = MagicMock(return_value=mapView)
    gisRepository.content.get = MagicMock(return_value=search_result)
    return gisRepository


def givenMapView():
    mapView = mock.MapView()
    mapView.add_layer = MagicMock()
    mapView.draw = MagicMock()
    return mapView


# ********************************************** #
# ****************    WHEN    ****************** #
# ********************************************** #

def whenGetCrimesMapByFelonyIsCalled(dataframe, gisService):
    gisService.getCrimesMapByFelonyType(dataframe, None)


# ********************************************** #
# ****************    THEN    ****************** #
# ********************************************** #

def thenGisRepository_content_getIsCalledNTimes(testObj, gisRepository, nCall):
    testObj.assertEqual(nCall, gisRepository.content.get.call_count)


def thenGisRepository_mapIsCalledNTimesWithAtlantaCityName(testObj, gisRepository, nCall):
    gisRepository.map.assert_called_with(ArcGISService.ATLANTA_ARCGIS_CITY_NAME)
    testObj.assertEqual(nCall, gisRepository.map.call_count)


def thenMapView_add_layerIsCalledNTimes(testObj, mapView, nCall):
    testObj.assertEqual(nCall, mapView.add_layer.call_count)


def thenMapView_drawIsCalledNTimes(testObj, mapView, nCall):
    testObj.assertEqual(nCall, mapView.draw.call_count)

def thenExpectedExceptionIsRaised(testObj, expected, actual, *args):
    testObj.assertRaises(expected, actual, *args)