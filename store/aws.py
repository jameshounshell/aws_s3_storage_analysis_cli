import boto3


class AWS:
    def __init__(self, profile="default", region="us-east-1"):
        self.profile = profile
        self.region = region
