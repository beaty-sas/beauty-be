import uvicorn

from beauty_be.app import create_app
from beauty_be.conf import settings
from beauty_be.conf.logging import LOG_CONFIG

app = create_app()

if __name__ == '__main__':
    uvicorn.run(
        app,
        host='0.0.0.0',
        port=settings.PORT,
        log_level=settings.LOG_LEVEL.value.lower(),
        log_config=LOG_CONFIG,
        loop='uvloop'
    )
