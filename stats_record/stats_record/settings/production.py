from .base import *
import dj_database_url

DATABASE_URL = os.environ.get('DATABASE_URL')

DATABASES = {
    'default': dj_database_url.config(
        # Replace this value with your local database's connection string.
        default='{DATABASE_URL}',
        conn_max_age=600
    )
}