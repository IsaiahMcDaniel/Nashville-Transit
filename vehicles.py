# fetches the vehicle position information from the gtfs_feeds.py file

import geopandas
from gtfs_feeds import fetch
from pprint import pprint
import sql_connection

class VehicleData:
    def __init__(self, file= "vehicle_positions") -> None:
        self.vhpos_path = "http://transitdata.nashvillemta.org/TMGTFSRealTimeWebService/vehicle/vehiclepositions.pb"
        self.file = file
        self.gdf = None

    def update_vhpos(self):

        df = fetch(self.vhpos_path, self.file)
        self.gdf = geopandas.GeoDataFrame(df,geometry=geopandas.points_from_xy(df["vehicle.position.latitude"], df["vehicle.position.longitude"]), crs="EPSG:4326")

    # prints the gdf if non empty
    def print_gdf(self):
        if self.gdf is not None:
            pprint(self.gdf)
        else:
            print("GeoDataFrame is empty")


vh = VehicleData()
vh.update_vhpos()
vh.print_gdf()