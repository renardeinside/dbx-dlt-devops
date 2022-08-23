.PHONY = build 

build:
	rm -rf dist
	pip wheel -e ".[dev]" -w dist --no-deps

upload:
	databricks --profile=itrusov-az-dbx fs cp \
		--overwrite \
		dist/dbx_dlt_devops-0.0.1-py3-none-any.whl \
		dbfs:/packages/dbx_dlt_devops-0.0.1-py3-none-any.whl

prepare-workspace:
	databricks repos create \
		--profile=itrusov-az-dbx \
		 --url https://github.com/renardeinside/dbx-dlt-devops.git \
		 --provider github --path /Repos/Staging/dbx-dlt-devops

update-repo:
	databricks repos update \
		--profile=itrusov-az-dbx \
		--path=/Repos/Staging/dbx-dlt-devops --branch=main 

prepare-packages-folder:
	databricks --profile=itrusov-az-dbx fs mkdirs dbfs:/packages


deploy: prepare-packages-folder build upload
	echo "Deployment done"
	


