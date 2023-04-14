import os

# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

# Define the database - we are working with
SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
                                os.getenv("GENOPATHS_DB_USER", "genopaths"),
                                os.getenv("GENOPATHS_DB_PASS", "genopaths"),
                                os.getenv("GENOPATHS_DB_HOST", "localhost"),
                                os.getenv("GENOPATHS_DB_PORT", "5432"),
                                os.getenv("GENOPATHS_DB_NAME", "genopaths"),
                            )

DATABASE_CONNECT_OPTIONS = {}
