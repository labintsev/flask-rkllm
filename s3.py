
"""Upload selected files to S3 storage"""
import argparse
from dotenv import dotenv_values
import boto3

env = dotenv_values('.env')
BUCKET_NAME = 'labintsev'


def main(args):
    client = boto3.client(
        's3',
        endpoint_url='https://storage.yandexcloud.net',
        aws_access_key_id=env['KEY_ID'],
        aws_secret_access_key=env['API_KEY']
    )

    if len(args.upload) == 0:
        print("No files selected for upload")
    
    for file_path in args.upload:
        print(f'Start upload {file_path}')
        object_name = file_path
        client.upload_file(file_path, BUCKET_NAME, object_name)

    if len(args.download) == 0:
        print("No files selected for download")

    for file_path in args.download:
        print(f'Start download {file_path}')
        object_name = file_path
        client.download_file(Bucket=BUCKET_NAME, 
                            Key=object_name, 
                            Filename=file_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--upload', nargs='+',
                        help='Local data files to upload to S3 storage',
                        default=[])
    parser.add_argument('-d', '--download', nargs='+',
                        help='Remote file names to download from S3 storage',
                        default=[])
    args = parser.parse_args()
    main(args)
