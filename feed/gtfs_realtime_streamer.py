import requests
from google.transit import gtfs_realtime_pb2
from typing import List

from data import TripUpdate, VehiclePosition, ServiceAlert
from feed import GTFSRealtimeFeed

class GTFSRealtimeStreamer:
    """
    Fetches and parses GTFS-realtime data from public URLs into structured TripUpdates,
    VehiclePositions, and ServiceAlerts using GTFSRealtimeFeed.
    """

    def __init__(self):
        self.trip_updates: List[TripUpdate] = []
        self.vehicle_positions: List[VehiclePosition] = []
        self.service_alerts: List[ServiceAlert] = []

    def fetch_and_parse(self):
        """
        Pulls GTFS-realtime feeds from URLs and parses them using GTFSRealtimeFeed.
        """
        self.trip_updates = self._fetch_trip_updates(
            "http://transitdata.nashvillemta.org/TMGTFSRealTimeWebService/tripupdate/tripupdates.pb"
        )
        self.vehicle_positions = self._fetch_vehicle_positions(
            "http://transitdata.nashvillemta.org/TMGTFSRealTimeWebService/vehicle/vehiclepositions.pb"
        )
        self.service_alerts = self._fetch_service_alerts(
            "http://transitdata.nashvillemta.org/TMGTFSRealTimeWebService/alert/alerts.pb"
        )

    def _download_feed(self, url: str) -> gtfs_realtime_pb2.FeedMessage:
        """
        Downloads a GTFS-realtime protobuf feed and returns a parsed FeedMessage.
        """
        response = requests.get(url)
        response.raise_for_status()
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(response.content)
        return feed

    def _fetch_trip_updates(self, url: str) -> List[TripUpdate]:
        """
        Fetches and parses TripUpdate data from the GTFS feed.
        """
        feed = self._download_feed(url)
        return GTFSRealtimeFeed(feed).trip_updates

    def _fetch_vehicle_positions(self, url: str) -> List[VehiclePosition]:
        """
        Fetches and parses VehiclePosition data from the GTFS feed.
        """
        feed = self._download_feed(url)
        return GTFSRealtimeFeed(feed).vehicle_positions

    def _fetch_service_alerts(self, url: str) -> List[ServiceAlert]:
        """
        Fetches and parses ServiceAlert data from the GTFS feed.
        """
        feed = self._download_feed(url)
        return GTFSRealtimeFeed(feed).service_alerts

    def get_all_data_as_dicts(self):
        """
        Converts all GTFS data objects to dictionaries for easy export (e.g. JSON).
        """
        return {
            "trip_updates": [t.to_dict() for t in self.trip_updates],
            "vehicle_positions": [v.to_dict() for v in self.vehicle_positions],
            "service_alerts": [a.to_dict() for a in self.service_alerts],
        }