import pandas as pd
from typing import List
from pandas import DataFrame
from exception import DataNotFoundError, DatasetEmptyError
from model import DatasetModel


class ExtractDataFromDataset:
    _datasetValues: List[DatasetModel]
    _datasetDictValues: List[dict]
    _dataFrame: DataFrame

    def __init__(self, datasetValues: List[DatasetModel]):
        if datasetValues is None:
            raise DataNotFoundError
        elif len(datasetValues) == 0:
            raise DatasetEmptyError

        self._datasetValues = datasetValues
        self._datasetDictValues = [model.to_dict() for model in datasetValues]
        self._dataFrame = pd.DataFrame.from_records(self._datasetDictValues)

    def getAllCrimesCountByDateDataframe(self):
        df = self.__getDataFrameClone()
        df.occur_date = pd.to_datetime(df['occur_date'])
        return df.groupby('occur_date')['occur_date'].count()

    def getAllCrimesCountByTypeDataframe(self):
        df = self.__getDataFrameClone()
        return df.groupby('crime_type')['crime_type'] \
            .count() \
            .sort_values()

    def getAllCrimesCountByDayDataframe(self):
        df = self.__getDataFrameClone()
        return df.groupby('avg_day')['avg_day'] \
            .count() \
            .sort_values()

    def getAllTop50NeighborhoodWithMostCrimesCountDataframe(self):
        df = self.__getDataFrameClone()
        return df.groupby('neighborhood')['neighborhood'] \
            .count() \
            .reset_index(name='Frequency') \
            .sort_values(ascending=False, by="Frequency") \
            .head(50) \
            .sort_values(ascending=True, by="Frequency")

    def getAllTop50NeighborhoodWithLessCrimesCountDataframe(self):
        df = self.__getDataFrameClone()
        return df.groupby('neighborhood')['neighborhood'] \
            .count() \
            .reset_index(name='Frequency') \
            .sort_values(ascending=True, by="Frequency") \
            .head(50) \
            .sort_values(ascending=False, by="Frequency")

    def getAllCrimesCountGroupByDayAndFelony(self):
        def updateDataStructureAndTranspose(groupElem):
            values = [row['count'] for _, row in groupElem.iterrows()]
            groupKey = groupElem.head(1)['avg_day'].to_numpy()[0]
            return pd.DataFrame.from_records({groupKey: values},
                                             index=groupElem['crime_type'].unique().tolist()).transpose()

        df = self.__getDataFrameClone()

        return df.value_counts(subset=['avg_day', 'crime_type']) \
            .reset_index(name='count') \
            .groupby('avg_day') \
            .apply(updateDataStructureAndTranspose) \
            .reset_index(level='avg_day', drop=True)

    def getAllCrimeByFelony(self, felony: str):
        df = self.__getDataFrameClone()

        return df.where(df['crime_type'] == felony).dropna().reset_index()

    def __getDataFrameClone(self):
        return self._dataFrame.copy()

