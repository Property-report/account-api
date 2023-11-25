import os


def convert_to_bool(value):
    if value == "True":
        return True
    elif value == "False":
        return False


APP_NAME = os.environ['APP_NAME']
APM_ENABLED = convert_to_bool(os.environ['APM_ENABLED'])

AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY']
AWS_SECRET_KEY = os.environ['AWS_SECRET_KEY']

SQLALCHEMY_MIGRATE_REPO = os.environ['SQLALCHEMY_MIGRATE_REPO']

SQLALCHEMY_USER = os.environ['SQLALCHEMY_USER']
SQLALCHEMY_PASSWORD = os.environ['SQLALCHEMY_PASSWORD']
SQLALCHEMY_HOST = os.environ['SQLALCHEMY_HOST']
SQLALCHEMY_PORT = os.environ['SQLALCHEMY_PORT']
SQLALCHEMY_DB = os.environ['SQLALCHEMY_DB']
postgresql_string = 'postgresql://{}:{}@{}:{}/{}'
SQLALCHEMY_DATABASE_URI = postgresql_string.format(
    SQLALCHEMY_USER, SQLALCHEMY_PASSWORD, SQLALCHEMY_HOST, SQLALCHEMY_PORT, SQLALCHEMY_DB)
LOCALSQS = os.environ['LOCALSQS']
SQS_QUEUE_NAME = os.environ['SQS_QUEUE_NAME']
EMAIL_SQS_QUEUE_NAME = os.environ['EMAIL_SQS_QUEUE_NAME']


FLASK_LOG_LEVEL = os.environ['FLASK_LOG_LEVEL']

LOGCONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            '()': 'text_message_api.extensions.JsonFormatter'
        },
        'audit': {
            '()': 'text_message_api.extensions.JsonAuditFormatter'
        }
    },
    'filters': {
        'contextual': {
            '()': 'text_message_api.extensions.ContextualFilter'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'filters': ['contextual'],
            'stream': 'ext://sys.stdout'
        },
        'audit_console': {
            'class': 'logging.StreamHandler',
            'formatter': 'audit',
            'filters': ['contextual'],
            'stream': 'ext://sys.stdout'
        }
    },
    'loggers': {
        'application': {
            'handlers': ['console'],
            'level': FLASK_LOG_LEVEL
        },
        'audit': {
            'handlers': ['audit_console'],
            'level': 'INFO'
        }
    }
}
