from dbx_dlt_devops.filters import GroupsReportProvider
from pyspark.sql import SparkSession
import pandas as pd 

def test_chain(spark: SparkSession):
    trips = spark.createDataFrame([
        (1, pd.to_datetime())
    ]).toDF("passenger_count", "tpep_pickup_datetime", "total_amount", "trip_distance")
    GroupsReportProvider.get_only_group_trips()