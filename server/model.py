# stdlib imports
import datetime

# vendor imports
import mongoengine as mongo

# local imports
from . import config


class ShortURL(mongo.Document):
    meta = {"collection": config.mongoDbCollection}

    token = mongo.StringField(primary_key=True, required=True)
    resolution = mongo.StringField(required=True)
    resolutionHash = mongo.BinaryField(required=False, max_bytes=64)
    created = mongo.DateTimeField(default=datetime.datetime.utcnow)
    creator = mongo.StringField(default=None)
    count = mongo.IntField(default=0)
