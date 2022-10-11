# Databricks notebook source
# Defining variables for the pathes of source data that has been created in the previous notebook and for the tables that will be created as a result of the DLT pipeline

TABLE_PATH = spark.conf.get("TABLE_PATH")
STORAGE_PATH = spark.conf.get("STORAGE_PATH")

# COMMAND ----------

# Declare event_logs table as a read from the STORAGE_PATH and sort by timestamp
import dlt
from pyspark.sql.functions import desc, col

@dlt.table(
 name="event_logs",
 comment="The raw event logs relating to our DLT pipeline",
 path=f"{TABLE_PATH}/event_logs/"
)
def event_logs():
    return # Fill in

# COMMAND ----------

# Declare audit_logs table which is a silver table by reading from the event_logs table with the below crtiteria
#  - all the record where event_type is user_action
#  - the audit_logs table should have the following schema (id, timestamp, user_name, action, details)
@dlt.table(
 name="audit_logs",
 comment="Audit logs relating to our DLT pipeline",
 path=f"{TABLE_PATH}/audit_logs/"
)
def audit_logs():
    return (
    dlt.read("event_logs").where("event_type = 'user_action'")
      .selectExpr("id", "timestamp", "details:user_action:user_name", "details:user_action:action", "details")
      .orderBy(desc("timestamp"))
    )
