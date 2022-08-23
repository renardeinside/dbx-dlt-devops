# Databricks notebook source
# MAGIC %md
# MAGIC 
# MAGIC # This notebook is used for exploration and dev purposes

# COMMAND ----------

# MAGIC %pip install holidays

# COMMAND ----------

# MAGIC %load_ext autoreload
# MAGIC %autoreload 2

# COMMAND ----------

from pathlib import Path
import sys

project_root = Path(".").absolute().parent
print(f"appending the main project code from {project_root}")
sys.path.append(project_root)


# COMMAND ----------

data_schema = "DOLocationID BIGINT,PULocationID BIGINT,RatecodeID BIGINT,VendorID BIGINT,congestion_surcharge DOUBLE,extra DOUBLE,fare_amount DOUBLE,improvement_surcharge DOUBLE,mta_tax DOUBLE,passenger_count BIGINT,payment_type BIGINT,store_and_fwd_flag STRING,tip_amount DOUBLE,tolls_amount DOUBLE,total_amount DOUBLE,tpep_dropoff_datetime STRING,tpep_pickup_datetime STRING,trip_distance DOUBLE,pep_pickup_date_txt DATE"

# COMMAND ----------

from dbx_dlt_devops.filters import GroupsReportProvider

# COMMAND ----------

all_trips = (
    spark.read.format("json")
    .option("inferSchema", False)
    .option("schema", data_schema)
    .load("/databricks-datasets/nyctaxi/sample/json/")
)

# COMMAND ----------

display(all_trips)

# COMMAND ----------

s1 = GroupsReportProvider.get_only_group_trips(all_trips)
s2 = GroupsReportProvider.add_pickup_info(s1)
s3 = GroupsReportProvider.add_holiday_info(s2)
s4 = GroupsReportProvider.prepare_report(s3)

display(s4)
