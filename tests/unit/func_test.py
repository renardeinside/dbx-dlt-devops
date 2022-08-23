from pyspark.sql import SparkSession
import pandas as pd 

def test_chain(spark: SparkSession):

    from dbx_dlt_devops.filters import GroupsReportProvider
    trips = spark.createDataFrame([
        (None, pd.to_datetime("2019-12-01T00:00:00.000+0000").to_pydatetime(), 100.0, 9.0),
        (2, pd.to_datetime("2019-12-01T00:00:00.000+0000").to_pydatetime(), 100.0, 9.0),
        (3, pd.to_datetime("2019-12-01T00:00:00.000+0000").to_pydatetime(), 100.0, 9.0),
        (3, pd.to_datetime("2019-12-20T00:00:00.000+0000").to_pydatetime(), 100.0, 9.0),
    ]).toDF("passenger_count", "tpep_pickup_datetime", "total_amount", "trip_distance")

    group_trips = GroupsReportProvider.get_only_group_trips(trips)
    assert group_trips.count() == 2

    with_pickup_info = GroupsReportProvider.add_pickup_info(group_trips)

    assert "pickup_dttm" in with_pickup_info.columns
    assert "pickup_day_of_week" in with_pickup_info.columns
    assert "pickup_hour_of_day" in with_pickup_info.columns

    with_holiday_info = GroupsReportProvider.add_holiday_info(with_pickup_info)

    assert "pickup_is_holiday" in with_holiday_info.columns

    report = GroupsReportProvider.prepare_report(with_holiday_info)

    assert report.count() == 2
    assert report.where("avg_trip_distance is null").count() == 0
    
    report.show()
