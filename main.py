#restAPI
import json
from flask import Flask, request, jsonify
#docx libs
from pdf2docx import Converter
#get data from url
import requests
# file_uploader.py MinIO Python SDK example
from minio import Minio
from minio.error import S3Error

app = Flask(__name__)

pdf_file = 'DHK.pdf'
docx_file = 'DHK.docx'

#minio 
minio_access_key = "minioadmin"
minio_secret_key = "minioadmin"
minio_endpoint = "Minio:9000"
minio_region = "us-east-1"
minio_bucket_name = "default"
minio_content_type = "application/docx"

def upload_docx(filepath, source_file):
    # Create a client with the MinIO server playground, its access key
    # and secret key.
    client = Minio(minio_endpoint,
        access_key=minio_access_key,
        secret_key=minio_secret_key,
        region=minio_region
    )

    # Upload the file, renaming it in the process
    client.fput_object(
        minio_bucket_name, filepath, source_file, minio_content_type
    )   
    print(
        source_file, "successfully uploaded as object",
        filepath, "to bucket", minio_bucket_name,
    )

@app.route('/pdf2docx', methods=['POST'])
# body: url,filepath
def generate_docx():
    request_dictionary = json.loads(request.data)
    url = request_dictionary['url']
    filepath = request_dictionary['filepath']
    new_filepath = filepath.replace(".pdf", ".docx")

    response_from_url = requests.get(url)

    with open(pdf_file,"wb") as output_file:
        output_file.write(response_from_url.content)

    cv= Converter(pdf_file)
    cv.convert(docx_file)
    cv.close()

    upload_docx(new_filepath, docx_file)

    return jsonify({"filepath": new_filepath})

app.run(debug=True)
