from pythonjsonlogger import jsonlogger

from beauty_be.conf.settings import Env
from beauty_be.conf.settings import settings


class BaseJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(BaseJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record['level'] = record.levelname
        log_record['logger'] = record.name


class GunicornUvicornJsonFormatter(BaseJsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(GunicornUvicornJsonFormatter, self).add_fields(log_record, record, message_dict)

        if 'scope' in log_record:
            log_record['user_id'] = log_record['scope'].get('state', {}).get('user_id')
            log_record['event_id'] = log_record['scope'].get('state', {}).get('event_id')
            del log_record['scope']


log_level = settings.LOG_LEVEL.value

LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            '()': BaseJsonFormatter,
        },
        'uvicorn_json': {
            '()': GunicornUvicornJsonFormatter,
        },
        'local': {
            '()': 'logging.Formatter',
        },
    },
    'handlers': {
        'default': {
            'formatter': 'local' if settings.ENV == Env.LOCAL else 'json',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'gunicorn_uvicorn': {
            'formatter': 'local' if settings.ENV == Env.LOCAL else 'uvicorn_json',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        'beauty_be': {'handlers': ['default'], 'level': log_level},
        'uvicorn': {'handlers': ['gunicorn_uvicorn'], 'level': log_level},
        'gunicorn': {'handlers': ['gunicorn_uvicorn'], 'level': log_level},
        'gunicorn.access': {'handlers': ['gunicorn_uvicorn'], 'level': log_level},
        'gunicorn.error': {'handlers': ['gunicorn_uvicorn'], 'level': log_level},
    },
    'root': {'handlers': [], 'level': log_level},
}
