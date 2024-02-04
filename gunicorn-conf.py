import json
import multiprocessing

from beauty_be.conf import settings
from beauty_be.conf.logging import LOG_CONFIG

workers_per_core = 2
cores = multiprocessing.cpu_count()
default_web_concurrency = workers_per_core * cores
web_concurrency = max(int(default_web_concurrency), 2)


# Gunicorn config variables
bind = f'0.0.0.0:{settings.PORT}'
workers = 2
graceful_timeout = 30  # default
timeout = 30  # default
keepalive = 2  # default
logconfig_dict = LOG_CONFIG

# For debugging and testing
log_data = {
    'message': 'GUNICORN CONFIG LOADED',
    'workers_per_core': workers_per_core,
    'cores': cores,
    'workers': workers,
    'bind': bind,
    'graceful_timeout': graceful_timeout,
    'timeout': timeout,
    'keepalive': keepalive,
}
