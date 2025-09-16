from dagster import asset
from dagster_aws.redshift import RedshiftClientResource
import os
from datetime import datetime

@asset
def load_to_redshift(redshift: RedshiftClientResource):
    s3_bucket = os.getenv('S3_BUCKET', 'your-bucket')
    tables = [
        {'name': 'users', 's3_path': f'raw/users/{datetime.now().strftime("%Y%m%d_%H%M%S")}.parquet'},
        {'name': 'sports', 's3_path': f'raw/sports/{datetime.now().strftime("%Y%m%d_%H%M%S")}.parquet'},
        {'name': 'categories', 's3_path': f'raw/categories/{datetime.now().strftime("%Y%m%d_%H%M%S")}.parquet'},
        {'name': 'questions', 's3_path': f'raw/questions/{datetime.now().strftime("%Y%m%d_%H%M%S")}.parquet'},
        {'name': 'quizzes', 's3_path': f'raw/quizzes/{datetime.now().strftime("%Y%m%d_%H%M%S")}.parquet'},
        {'name': 'quiz_answers', 's3_path': f'raw/quiz_answers/{datetime.now().strftime("%Y%m%d_%H%M%S")}.parquet'},
    ]

    for table in tables:
        query = f"""
        COPY {table['name']} FROM 's3://{s3_bucket}/{table['s3_path']}'
        IAM_ROLE 'arn:aws:iam::your-account:role/RedshiftRole'
        FORMAT AS PARQUET;
        """
        redshift.get_client().execute_query(query)