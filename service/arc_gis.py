from typing import Type, List

from arcgis.features import Feature, FeatureSet, FeatureCollection
from arcgis.gis import GIS, Layer
from arcgis.widgets import MapView
from arcgis.geometry import Point

from exception import DatasetEmptyError


class ArcGISService:
    ATLANTA_ARCGIS_CITY_NAME = "Atlanta"
    ATLANTA_NEIGHBORHOOD_ID = "96c978163d7647f0aec469a80c25c720"

    _gisRepository: GIS
    _neighborhoodLayer: Layer
    _use_cache: bool

    def __init__(self, gisRepository: GIS, use_cache=False):
        self._gisRepository = gisRepository
        self._use_cache = use_cache
        self._neighborhoodLayer = None

    def getCrimesMapByFelonyType(self, dataframe, symbol):
        xCoordList: List[float] = dataframe['x']
        yCoordList: List[float] = dataframe['y']
        if len(xCoordList) == 0 or len(xCoordList) != len(yCoordList):
            raise DatasetEmptyError

        pointList = [Point({"x": xCoordList[index], "y": yCoordList[index]}) for index in range(len(xCoordList))]
        featureSet = self.__getPointFeatureSet(pointList)

        crime_map = self.__getAtlantaMapWithNeighborhoodMap()
        crime_map.add_layer(FeatureCollection.from_featureset(featureSet, symbol=symbol))

        crime_map.draw(
            featureSet,
            symbol=symbol
        )

        return crime_map

    def __getAtlantaMapWithNeighborhoodMap(self) -> Type[MapView]:
        gisMap = self._gisRepository.map(ArcGISService.ATLANTA_ARCGIS_CITY_NAME)
        gisMap.add_layer(self.__getAtlantaNeighborHoodLayer())
        return gisMap

    def __getAtlantaNeighborHoodLayer(self) -> Type[Layer]:
        if self._neighborhoodLayer is not None and self._use_cache:
            return self._neighborhoodLayer
        search_results = self._gisRepository.content.get(ArcGISService.ATLANTA_NEIGHBORHOOD_ID)
        lay_one = search_results.layers[1]
        self._neighborhoodLayer = lay_one

        return lay_one

    def __getPointFeatureSet(self, points: List[Point]) -> FeatureSet:
        featureList = [Feature(point) for point in points]

        return FeatureSet(featureList,
                          geometry_type="esriGeometryMultipoint",
                          spatial_reference={'wkid': 4326})


class ArcGISPointStyle:
    RED_POINT = {"angle": 0, "xoffset": 0, "yoffset": 0, "type": "esriPMS",
                 "url": "http://static.arcgis.com/images/Symbols/Basic/RedSphere.png", "contentType": "image/png",
                 "width": 24, "height": 24}
    GREEN_POINT = {"angle": 0, "xoffset": 0, "yoffset": 0, "type": "esriPMS",
                   "url": "http://static.arcgis.com/images/Symbols/Basic/GreenSphere.png", "contentType": "image/png",
                   "width": 24, "height": 24}

    PURPLE_POINT = {"angle": 0, "xoffset": 0, "yoffset": 0, "type": "esriPMS",
                    "url": "http://static.arcgis.com/images/Symbols/Basic/PurpleSphere.png", "contentType": "image/png",
                    "width": 24, "height": 24}
