import pandas as pd
from sqlalchemy import create_engine
import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='export_all_to_s3.log'
)
logger = logging.getLogger(__name__)

def get_db_engine():
    """Create and return SQLAlchemy engine for PostgreSQL."""
    try:
        load_dotenv()
        connection_string = os.getenv('DATABASE_URL', '')
        logger.info("Connecting to PostgreSQL database...")
        return create_engine(connection_string)
    except Exception as e:
        logger.error(f"Failed to create database engine: {str(e)}")
        raise

def get_s3_client():
    """Initialize and return boto3 S3 client."""
    try:
        logger.info("Initializing S3 client...")
        return boto3.client('s3')
    except Exception as e:
        logger.error(f"Failed to initialize S3 client: {str(e)}")
        raise

def validate_s3_bucket(s3_client, bucket):
    """Check if S3 bucket exists and is accessible."""
    try:
        s3_client.head_bucket(Bucket=bucket)
        logger.info(f"Bucket {bucket} is accessible.")
    except ClientError as e:
        logger.error(f"Bucket {bucket} does not exist or is inaccessible: {e}")
        raise

def export_table_to_s3(engine, s3_client, table_name, query, s3_bucket, s3_path):
    """Export a table to S3 as Parquet with error handling."""
    try:
        logger.info(f"Executing query for table {table_name}...")
        df = pd.read_sql(query, engine)
        
        if df.empty:
            logger.info(f"No new or updated records found for {table_name}.")
            return False

        logger.info(f"Writing {len(df)} records from {table_name} to s3://{s3_bucket}/{s3_path}...")
        df.to_parquet(f's3://{s3_bucket}/{s3_path}', index=False, engine='pyarrow')
        logger.info(f"Export completed successfully for {table_name}.")
        return True
    except Exception as e:
        logger.error(f"Error exporting {table_name} to S3: {str(e)}")
        raise

def export_all_to_s3():
    """Export all tables to S3 with incremental logic."""
    try:
        # Initialize resources
        s3_bucket = os.getenv('S3_BUCKET', 'your-bucket')
        s3_client = get_s3_client()
        validate_s3_bucket(s3_client, s3_bucket)
        engine = get_db_engine()

        # Define export configurations
        tables = [
            {
                'name': 'users',
                'query': """
                    SELECT id, username, email, full_name, created_at, last_login
                    FROM users
                    WHERE created_at >= NOW() - INTERVAL '1 day'
                       OR last_login >= NOW() - INTERVAL '1 day'
                       OR created_at IS NULL
                       OR last_login IS NULL
                """,
                's3_path': f'raw/users/{datetime.now().strftime("%Y%m%d_%H%M%S")}.parquet'
            },
            {
                'name': 'sports',
                'query': """
                    SELECT id, name, description, created_at
                    FROM sports
                    WHERE created_at >= NOW() - INTERVAL '1 day'
                       OR created_at IS NULL
                """,
                's3_path': f'raw/sports/{datetime.now().strftime("%Y%m%d_%H%M%S")}.parquet'
            },
            {
                'name': 'categories',
                'query': """
                    SELECT id, name, description, sport_id, created_at
                    FROM categories
                    WHERE created_at >= NOW() - INTERVAL '1 day'
                       OR created_at IS NULL
                """,
                's3_path': f'raw/categories/{datetime.now().strftime("%Y%m%d_%H%M%S")}.parquet'
            },
            {
                'name': 'questions',
                'query': """
                    SELECT id, text, question_type, difficulty, options, 
                           correct_answer, explanation, category_id, created_at
                    FROM questions
                    WHERE created_at >= NOW() - INTERVAL '1 day'
                       OR created_at IS NULL
                """,
                's3_path': f'raw/questions/{datetime.now().strftime("%Y%m%d_%H%M%S")}.parquet'
            },
            {
                'name': 'quizzes',
                'query': """
                    SELECT id, user_id, category_id, difficulty, score, 
                           total_questions, time_taken, completed_at
                    FROM quizzes
                    WHERE completed_at >= NOW() - INTERVAL '1 day'
                       OR completed_at IS NULL
                """,
                's3_path': f'raw/quizzes/{datetime.now().strftime("%Y%m%d_%H%M%S")}.parquet'
            },
            {
                'name': 'quiz_answers',
                'query': """
                    SELECT id, quiz_id, question_id, user_answer, is_correct, time_taken
                    FROM quiz_answers
                    WHERE EXISTS (
                        SELECT 1 FROM quizzes q 
                        WHERE q.id = quiz_answers.quiz_id 
                        AND (q.completed_at >= NOW() - INTERVAL '1 day' OR q.completed_at IS NULL)
                    )
                """,
                's3_path': f'raw/quiz_answers/{datetime.now().strftime("%Y%m%d_%H%M%S")}.parquet'
            }
        ]

        # Export each table
        for table in tables:
            export_table_to_s3(
                engine=engine,
                s3_client=s3_client,
                table_name=table['name'],
                query=table['query'],
                s3_bucket=s3_bucket,
                s3_path=table['s3_path']
            )

        logger.info("All tables exported successfully.")

    except Exception as e:
        logger.error(f"Failed to export all tables: {str(e)}")
        raise
    finally:
        engine.dispose()
        logger.info("Database connection closed.")

if __name__ == '__main__':
    export_all_to_s3()