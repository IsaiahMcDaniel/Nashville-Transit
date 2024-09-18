# import gtfs packages to access gtfs stream
from google.transit import gtfs_realtime_pb2
from protobuf_to_dict import protobuf_to_dict
from pathlib import Path
import geopandas as gp
import requests
import pandas as pd

def fetch(url, file_name):
    cwd = Path.cwd()

    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get(url, timeout=100)
    feed.ParseFromString(response.content)
    kat_dict = protobuf_to_dict(feed)
    try:
        print(kat_dict)
        file = pd.json_normalize(kat_dict['entity'])
        file.to_csv(fr"{cwd}\{file_name}.csv")
    except Exception as error:
        print(error)
        pass
