from pyspark.sql import DataFrame as SparkDataFrame
from pyspark.sql.functions import (
    to_timestamp,
    dayofweek,
    pandas_udf,
    hour,
    col,
    expr,
    sum,
    avg,
    count,
    lit,
)

import pandas as pd
import holidays


class GroupsReportProvider:
    """
    This class contains table processing methods for taxi rides.
    Based on this data management will decide in which region it makes sense to add more family cars (e.g. vans), and at what time they are mostly requested.
    """

    @staticmethod
    @pandas_udf("boolean")
    def is_holiday(dates: pd.Series) -> pd.Series:
        us_holidays = holidays.US()
        return dates.apply(lambda _date: _date in us_holidays)

    @staticmethod
    def get_only_group_trips(trips: SparkDataFrame) -> SparkDataFrame:
        """
        Filters out all trips where are <=3 passengers.
        Returns filtered trips by condition.
        """
        return trips.where("passenger_count is not null and passenger_count >= 3")

    @staticmethod
    def add_pickup_info(trips: SparkDataFrame) -> SparkDataFrame:
        result = (
            trips.withColumn("pickup_dttm", to_timestamp("tpep_pickup_datetime"))
            .withColumn("pickup_day_of_week", dayofweek("pickup_dttm"))
            .withColumn("pickup_hour_of_day", hour("pickup_dttm"))
        )
        return result

    def add_holiday_info(trips: SparkDataFrame) -> SparkDataFrame:
        result = trips.withColumn(
            "pickup_is_holiday", GroupsReportProvider.is_holiday(col("pickup_dttm"))
        )
        return result

    def prepare_report(trips: SparkDataFrame) -> SparkDataFrame:
        result = (
            trips.withColumn("pickup_month", expr("date_trunc('month', pickup_dttm)"))
            .groupBy(
                "pickup_month",
                "pickup_day_of_week",
                "pickup_hour_of_day",
                "pickup_is_holiday",
            )
            .agg(
                count(lit(1)).alias("num_trips"),
                sum("total_amount").alias("total_amount"),
                avg("trip_distance").alias("avg_trip_distance"),
            )
        )
        return result
