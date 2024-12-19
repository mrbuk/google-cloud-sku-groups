# google-cloud-sku-groups

Deploy as a Cloud Function to export Google Cloud SKU Group as JSONL. This data can then be used in other tools like [DuckDB](shell.duckdb.org)

	CREATE TABLE skus_edp_24 AS SELECT * FROM read_json_auto('https://my-fucntion.cloudfunctions.net/sku-to-json?sku_group=cloud-enterprise-2024');
