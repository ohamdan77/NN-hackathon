%md
# Distributed Forecasting with Prophet, Spark, Delta & MLflow

<img src = "https://raw.githubusercontent.com/rafaelvp-db/distributed-forecasting/master/img/disttributed_forecasting1.png" />

### Context

* This project contains code for training, tracking and deploying a **distributed sales forecasting model**, using **Prophet, Spark, Delta & MLflow**.

* It also features distributed inference of previously trained models using **Spark and Pandas UDFs**.

* **Fine-grained** forecasting models are trained for multiple **store** and **product** combinations. For this example, we train more than 500 different models, while tracking each of the training runs as well as the resulting validation metrics into MLflow.

* Finally, a **custom PyFunc** model is created, allowing users to seamlessly run distributed inference in order to obtain fine-grained forecasting at scale leveraging the models that were trained and registered in MLflow in the previous step.

## High Level Architecture

<img src="https://raw.githubusercontent.com/rafaelvp-db/distributed-forecasting/master/img/dist_forecasting2.png" />

# DBX Instructions

Note: DBX support is still in progress.

## Local environment setup

1. Instantiate a local Python environment via a tool of your choice. This example is based on `conda`, but you can use any environment management tool:
```bash
conda create -n nn_forecasting python=3.9
conda activate nn_forecasting
```

2. If you don't have JDK installed on your local machine, install it (in this example we use `conda`-based installation):
```bash
conda install -c conda-forge openjdk=11.0.15
```

3. Install project locally (this will also install dev requirements):
```bash
pip install -e ".[local,test]"
```

## Running unit tests

For unit testing, please use `pytest`:
```
pytest tests/unit --cov
```

Please check the directory `tests/unit` for more details on how to use unit tests.
In the `tests/unit/conftest.py` you'll also find useful testing primitives, such as local Spark instance with Delta support, local MLflow and DBUtils fixture.

## Running integration tests

There are two options for running integration tests:

- On an all-purpose cluster via `dbx execute`
- On a job cluster via `dbx launch`

For quicker startup of the job clusters we recommend using instance pools ([AWS](https://docs.databricks.com/clusters/instance-pools/index.html), [Azure](https://docs.microsoft.com/en-us/azure/databricks/clusters/instance-