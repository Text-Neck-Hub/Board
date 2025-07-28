import os


REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.pubsub.RedisPubSubChannelLayer",  #
        "CONFIG": {

            "hosts": [(REDIS_HOST, 6379)],

            "channel_layer_db": 2,
        },
    },
}
