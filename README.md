# dbx-dlt-devops

Please replace all occurancies of `itrusov-az-dbx` with your profile name.

## Local environment setup

1. Instantiate a local Python environment via a tool of your choice. This example is based on `conda`, but you can use any environment management tool:
```bash
conda create -n dbx_dlt_devops python=3.9
conda activate dbx_dlt_devops
```

2. If you don't have JDK installed on your local machine, install it (in this example we use `conda`-based installation):
```bash
conda install -c conda-forge openjdk=11.0.15
```

3. Install project in a dev mode (this will also install dev requirements):
```bash
pip install -e ".[dev]"
```

## Running unit tests

For unit testing, please use `pytest`:
```
pytest tests/unit --cov
```

Please check the directory `tests/unit` for more details on how to use unit tests.
In the `tests/unit/conftest.py` you'll also find useful testing primitives, such as local Spark instance with Delta support, local MLflow and DBUtils fixture.

## Syncronizing with notebooks

1. Create user repo `dbx-dlt-devops`

2. Run this command to start one-directional sync between local machine and user repo in Databricks:
```
dbx sync repo -d dbx-dlt-devops --profile=YOUR-PROFILE
```