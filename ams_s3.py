import boto3
import json


class Aws:
    def __init__(self):
        self.s3 = boto3.client(
            's3',
            aws_access_key_id='AKIAYKAKMRRSIKGPTGO2',
            aws_secret_access_key='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'
        )
        self.bucket_name = 'bangapp'
        self.bucket_policy = {
            'Version': '2012-10-17',
            'Statement': [{
                'Sid': 'AddPerm',
                'Effect': 'Allow',
                'Principal': '*',
                'Action': ['s3:GetObject'],
                'Resource': f'arn:aws:s3:::{self.bucket_name}/*'
            }]
        }
        self.bucket_policy = json.dumps(self.bucket_policy)
        self.bucket_location = self.s3.get_bucket_location(Bucket=self.bucket_name)

    def upload_file(self, path):
        self.s3.upload_file(path, self.bucket_name, path)
        return self.get_url(path)

    def set_public(self):
        self.s3.put_bucket_policy(Bucket=self.bucket_name, Policy=self.bucket_policy)

    def get_url(self, path):
        return "https://s3-{0}.amazonaws.com/{1}/{2}".format(
            self.bucket_location['LocationConstraint'], self.bucket_name, path
        )