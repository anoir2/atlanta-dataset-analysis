from dataclasses import dataclass
from typing import Union, Dict

from arcgis.widgets import MapView
from bokeh.plotting import Figure
from enum import Enum


class ResultType(Enum):
    BOKEH_PLOT = "bokeh_plot"
    ARC_GIS_MAP = "arc_gis_map"

@dataclass(frozen=True)
class ResultArcGIS:
    map: MapView
    mapAttribute: Dict[str, str]

@dataclass(frozen=True)
class ResultUnit:
    data: Union[Figure, ResultArcGIS]
    fileName: str
    type: ResultType
