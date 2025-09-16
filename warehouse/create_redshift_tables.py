import os
from dotenv import load_dotenv
import logging
import psycopg2
from psycopg2 import sql

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='create_redshift_tables.log'
)
logger = logging.getLogger(__name__)

