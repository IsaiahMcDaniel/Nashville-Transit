# fetches the vehicle position information from the gtfs_feeds.py file

import geopandas
from gtfs_feeds import fetch
from pprint import pprint
from sqlalchemy import create_engine

class VehicleData:
    def __init__(self, connection, table_name = "vehicles", file=None) -> None:
        self.vhpos_path = "http://transitdata.nashvillemta.org/TMGTFSRealTimeWebService/vehicle/vehiclepositions.pb"
        self.file = file
        self.connection = connection
        self.table_name = table_name
        self.gdf = None
        self.update_vhpos()

    def update_vhpos(self):
        # loads information to DataFrame
        df = fetch(self.vhpos_path, self.file)

        # converts pandas DataFrame to GeoDataFrame
        self.gdf = geopandas.GeoDataFrame(df,geometry=geopandas.points_from_xy(df["vehicle.position.latitude"], df["vehicle.position.longitude"]), crs="EPSG:4326")

    # prints the gdf if non empty
    def print_gdf(self):
        if self.gdf is not None:
            pprint(self.gdf)
        else:
            print("GeoDataFrame is empty")
    
    # adds the GeoDatabase to Postgresql as a PostGIS database
    def create_db(self):
        engine = create_engine(self.table_name, self.connection, if_exists = "replace")
        self.gdf.to_postgis()


vh = VehicleData()
vh.print_gdf()