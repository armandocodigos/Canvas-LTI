"""
Configuration file for flask sample application
"""
import os

# enable CSRF
WTF_CSRF_ENABLED = True

# secret key for authentication
SECRET_KEY = 'MY_SECRET_KEY'

# Specify your tool's consumer_key and secret_key combination here
PYLTI_CONFIG = {
    "consumers": {
        "MY_CONSUMER_KEY": {
            "secret": 'MY_SECRET_KEY',
        }
    }
}