WORKSPACE_URL = https://adb-3867452311804142.2.azuredatabricks.net

build:
	pip wheel -e ".[dev]" -w dist --no-dep

upload:
	databricks --profile=itrusov-az-dbx fs cp \
		--overwrite \
		dist/dbx_dlt_devops-0.0.1-py3-none-any.whl \
		dbfs:/packages/dbx_dlt_devops-0.0.1-py3-none-any.whl

prepare-packages-folder:
	databricks --profile=itrusov-az-dbx fs mkdirs dbfs:/packages


deploy: prepare-packages-folder build upload
	echo "Deployment done"
	

