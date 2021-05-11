from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class DatasetModel:
    crime_type: str
    occur_date: str
    occur_time: str
    avg_day: str
    neighborhood: str
    location: str
    x: float
    y: float

    @staticmethod
    def from_dict(element: dict):
        crime_type = element["crime_type"]
        occur_date = datetime.strptime(element["occur_date"], '%m/%d/%Y').strftime('%Y-%m-%d')
        occur_time = element["occur_time"]
        avg_day = element["avg_day"]
        neighborhood = element["neighborhood"]
        location = element["location"]
        x = element["x"]
        y = element["y"]
        return DatasetModel(crime_type, occur_date, occur_time, avg_day, neighborhood, location, x, y)

    @staticmethod
    def from_list_dict(elements: list) -> list:
        return list(map(DatasetModel.from_dict, elements))

    def to_dict(self):
        return vars(self)
