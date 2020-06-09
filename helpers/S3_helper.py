import boto3

s3 = boto3.resource('s3')


def upload_file_to_S3(filename, key, bucket_name):
    s3.Bucket(bucket_name).upload_file(filename, key)

