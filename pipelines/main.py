# Databricks notebook source
# DBTITLE 1,Install package
# MAGIC %pip install /dbfs/packages/dbx_dlt_devops-0.0.1-py3-none-any.whl

# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC ## Main DLT pipeline which prepares the tables

# COMMAND ----------

from pyspark.sql.functions import *
from pyspark.sql.types import *
from dbx_dlt_devops.filters import GroupsReportProvider

# COMMAND ----------

import dlt

# COMMAND ----------

data_schema = "DOLocationID BIGINT,PULocationID BIGINT,RatecodeID BIGINT,VendorID BIGINT,congestion_surcharge DOUBLE,extra DOUBLE,fare_amount DOUBLE,improvement_surcharge DOUBLE,mta_tax DOUBLE,passenger_count BIGINT,payment_type BIGINT,store_and_fwd_flag STRING,tip_amount DOUBLE,tolls_amount DOUBLE,total_amount DOUBLE,tpep_dropoff_datetime STRING,tpep_pickup_datetime STRING,trip_distance DOUBLE,pep_pickup_date_txt DATE"
source_path = "/databricks-datasets/nyctaxi/sample/json/"


# COMMAND ----------


@dlt.table(comment="Raw trips data without any additional transformations")
def trips_raw():
    return spark.read.format("json").load(source_path)


# COMMAND ----------


@dlt.table(comment="Only trips which are considered as a group (3 or more passangers)")
def group_trips():
    return GroupsReportProvider.get_only_group_trips(dlt.read("trips_raw"))


# COMMAND ----------


@dlt.view(comment="Group trips extended with pickup information")
def group_trips_with_pickup_info():
    return GroupsReportProvider.add_pickup_info(dlt.read("group_trips"))


# COMMAND ----------


@dlt.view(
    comment="Group trips extended with pickup information and holiday information"
)
def group_trips_with_pickup_and_holiday_info():
    return GroupsReportProvider.add_holiday_info(
        dlt.read("group_trips_with_pickup_info")
    )


# COMMAND ----------


@dlt.table(
    comment="High level report on the group trips usage, by month, with information per hour. Holidays are also available for analysis"
)
def prepare_report():
    return GroupsReportProvider.add_holiday_info(
        dlt.read("group_trips_with_pickup_and_holiday_info")
    )
