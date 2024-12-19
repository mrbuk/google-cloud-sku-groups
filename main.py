import functions_framework
from flask import abort, Response
import requests
import json
from bs4 import BeautifulSoup

@functions_framework.http
def transform(request):
  # set CORS headers for the preflight request
  if request.method == 'OPTIONS':
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600'
    }

    return ('', 204, headers)

  # Set CORS headers for the main request
  request_json = request.get_json(silent=True)
  request_args = request.args

  if request_json and 'sku_group' in request_json:
    sku_group = request_json['sku_group']
  elif request_args and 'sku_group' in request_args:
    sku_group = request_args['sku_group']
  else:
    return abort(400)

  r = Response(convert_sku_to_jsonl(sku_group), mimetype="application/jsonl")
  return (r, { 'Access-Control-Allow-Origin': '*' })

# e.g url = "https://cloud.google.com/skus/sku-groups/gen-ai"
def convert_sku_to_jsonl(sku_group):
  url = "https://cloud.google.com/skus/sku-groups/{}".format(sku_group)
  page = requests.get(url)
  soup = BeautifulSoup(page.content, "html.parser")
  rows = soup.find(id="gc-wrapper").find_all("tr")

  all = []
  for row in rows:
          service_name, sku_name, sku_id, date_added = list(map(lambda cell: cell.text.strip(), row))
          yield json.dumps({ 'sku_id': sku_id, 'sku_name': sku_name, 'date_added': date_added}) + "\n"

