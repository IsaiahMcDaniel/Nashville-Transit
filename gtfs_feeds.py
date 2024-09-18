# import gtfs packages to access gtfs stream
# code and guide can be accessed at: https://gtfs.org/documentation/overview/

from google.transit import gtfs_realtime_pb2
from protobuf_to_dict import protobuf_to_dict
from pathlib import Path
import requests
import pandas as pd

def fetch(url, file_name):
    # to hold the current working directory to save the csv file.
    cwd = Path.cwd()

    # connects to the realtime feed and parses information
    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get(url, timeout=100)
    feed.ParseFromString(response.content)

    # uses the protobuf package to compile the feed into a dictionary
    transit_dict = protobuf_to_dict(feed)

    # normalizes the returned json and then adds it to a csv file
    try:
        file = pd.json_normalize(transit_dict['entity'])

        # creates the csv file if a name for the file is given.
        if file_name: 
            file.to_csv(path_or_buf = f"{cwd}\{file_name}.csv")
        return file
    
    except Exception as error:
        print(error)
        pass
