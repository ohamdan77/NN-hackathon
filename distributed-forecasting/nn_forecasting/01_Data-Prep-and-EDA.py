# Databricks notebook source
# MAGIC %md-sandbox
# MAGIC ## Download Data and Import into Workspace
# MAGIC 
# MAGIC For our training dataset, we will make use of 5-years of store-item unit sales data for 50 items across 10 different stores.  This data set is publicly available as part of a past Kaggle competition and can be downloaded [here](https://www.kaggle.com/c/demand-forecasting-kernels-only/data). 
# MAGIC 
# MAGIC Once downloaded, we can uzip the *train.csv.zip* file and upload the decompressed CSV to the DBFS root using the file import steps documented [here](https://docs.databricks.com/data/tables.html#create-table-ui). 
# MAGIC 
# MAGIC ![Upload Train](https://files.training.databricks.com/images/upload_train.png)
# MAGIC 
# MAGIC 1. Click **Data** on the sidebar
# MAGIC 2. Click **Add Data** in the top right of the blade that opens
# MAGIC 3. Add `<your initials>/demand` to the target directory
# MAGIC 4. Use the **Files** box to upload your train.csv file
# MAGIC 5. Once the upload is complete, you'll see a green check mark next to the path this file uploaded to. Make sure your `rawDataPath` variable in the following cell is updated to match this path.
# MAGIC 
# MAGIC <img alt="Caution" title="Caution" style="vertical-align: text-bottom; position: relative; height:1.3em; top:0.0em" src="https://files.training.databricks.com/static/images/icon-warning.svg"/> When performing the file import, you don't need to select the *Create Table with UI* or the *Create Table in Notebook* options to complete the import process.

# COMMAND ----------

rawDataPath = "/FileStore/tables/foo/demand/train.csv"

# COMMAND ----------

import re

import logging
logging.getLogger('py4j').setLevel(logging.ERROR)

username = (sc._jvm.com.databricks.logging.AttributionContext.current().tags().get(
  sc._jvm.com.databricks.logging.BaseTagDefinitions.TAG_USER()).x())

userhome = f"dbfs:/user/{username}"

database = f"""{re.sub("[^a-zA-Z0-9]", "_", username)}_demand_db"""

spark.sql(f"CREATE DATABASE IF NOT EXISTS {database}")

spark.sql(f"USE {database}");

# COMMAND ----------

# MAGIC %md
# MAGIC ## Examine the Data
# MAGIC 
# MAGIC The dataset from which we wish to generate our forecasts consists of daily sales data for 50 products across 10 store locations for a 5 year period:

# COMMAND ----------

spark.sql("DROP TABLE IF EXISTS sales-raw")
rawSchema = """
  date DATE,
  store INT,
  item INT,
  sales INT"""

sales = (spark.read
  .format("csv") 
  .option("header", True) 
  .schema(rawSchema)
  .load(rawDataPath))

sales.write.saveAsTable("sales-raw")

# show data
display(spark.read.table("sales-raw"))

# COMMAND ----------

# MAGIC %md As is typical when performing forecasting, we will want to examine the data for trends and seasonality, at both the yearly and weekly levels:

# COMMAND ----------

# DBTITLE 1,View Yearly Trends
# MAGIC %sql
# MAGIC 
# MAGIC SELECT
# MAGIC   year(date) as year, 
# MAGIC   sum(sales) as sales
# MAGIC FROM sales-raw
# MAGIC GROUP BY year(date)
# MAGIC ORDER BY year;

# COMMAND ----------

# DBTITLE 1,View Monthly Trends
# MAGIC %sql
# MAGIC 
# MAGIC SELECT 
# MAGIC   TRUNC(date, 'MM') as month,
# MAGIC   SUM(sales) as sales
# MAGIC FROM sales-raw
# MAGIC GROUP BY TRUNC(date, 'MM')
# MAGIC ORDER BY month;

# COMMAND ----------

# DBTITLE 1,View Weekday Trends
# MAGIC %sql
# MAGIC 
# MAGIC SELECT
# MAGIC   YEAR(date) as year,
# MAGIC   extract(dayofweek from date) as weekday,
# MAGIC   AVG(sales) as sales
# MAGIC FROM (
# MAGIC   SELECT 
# MAGIC     date,
# MAGIC     SUM(sales) as sales
# MAGIC   FROM sales-raw
# MAGIC   GROUP BY date
# MAGIC  ) x
# MAGIC GROUP BY year, weekday
# MAGIC ORDER BY year, weekday;

# COMMAND ----------

# MAGIC %md
# MAGIC ## Hackathon exercise:
# MAGIC 
# MAGIC 
# MAGIC 
# MAGIC * Do some additional Data Exploration
# MAGIC * Try to train a facbook prophet model for 30 days demand forecasting for every item in every store
# MAGIC * Use automl to create a forecasting training experiment
# MAGIC * Explore the result of your experiment
# MAGIC * Register the best model to mlflow model registery
# MAGIC * Load the model from the registery and use it for inference
