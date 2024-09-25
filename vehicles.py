# fetches the vehicle position information from the gtfs_feeds.py file
import geopandas
from gtfs_feeds import fetch
from pprint import pprint
from sqlalchemy import create_engine
from creds import USERNAME, PASSWORD

class VehicleData:
    def __init__(self, db_name = "NashvilleTransit", table_name = "vehicles", file=None) -> None:
        self.vhpos_path = "http://transitdata.nashvillemta.org/TMGTFSRealTimeWebService/vehicle/vehiclepositions.pb"
        self.file = file
        self.db_name = db_name
        self.table_name = table_name
        self.connection = f"postgresql://postgres:activate@localhost:5432/{self.db_name}"
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
        engine = create_engine(self.connection)
        # Enter creditenials to SQL database here if not in environmental variables.
        self.gdf.to_postgis(self.table_name, engine, if_exists = "replace")


vh = VehicleData()
vh.print_gdf()
vh.create_db()