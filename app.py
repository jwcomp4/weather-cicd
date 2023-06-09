import dash
from flask_caching import Cache
import os

app = dash.Dash(__name__)

cache = Cache(app.server, config={
    # try 'filesystem' if you don't want to setup redis
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379')
})


