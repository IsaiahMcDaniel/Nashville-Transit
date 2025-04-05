from google.transit import gtfs_realtime_pb2
from typing import List

# Import your GTFS dataclasses
from gtfs_trip_updates import TripUpdate, TripDescriptor, StopTimeUpdate, StopTimeEvent, VehicleDescriptor
from gtfs_vehicle_positions import VehiclePosition, Position
from gtfs_service_alerts import ServiceAlert

# Import mappings from integer enum values to strings
from enums import (
    SCHEDULE_RELATIONSHIP,
    STOP_TIME_SCHEDULE_RELATIONSHIP,
    OCCUPANCY_STATUS,
    CONGESTION_LEVEL,
    VEHICLE_STOP_STATUS,
    ALERT_EFFECT,
    ALERT_CAUSE,
)

class GTFSRealtimeFeed:
    """
    Parses a GTFS-realtime FeedMessage and converts it into structured Python dataclasses.
    
    Handles:
    - TripUpdates (schedules, vehicles, stop events)
    - VehiclePositions (real-time GPS data)
    - ServiceAlerts (disruptions, detours, etc.)
    """

    def __init__(self, feed: gtfs_realtime_pb2.FeedMessage):
        # Lists to hold the parsed dataclass results
        self.trip_updates: List[TripUpdate] = []
        self.vehicle_positions: List[VehiclePosition] = []
        self.service_alerts: List[ServiceAlert] = []

        # Kick off the parsing of all entities
        self._parse_feed(feed)

    def _parse_feed(self, feed: gtfs_realtime_pb2.FeedMessage):
        """
        Iterates over each entity in the feed and dispatches it to the correct parser
        based on whether it contains a trip update, vehicle position, or service alert.
        """
        for entity in feed.entity:
            if entity.HasField("trip_update"):
                self.trip_updates.append(self._parse_trip_update(entity.trip_update))
            elif entity.HasField("vehicle"):
                self.vehicle_positions.append(self._parse_vehicle_position(entity.vehicle))
            elif entity.HasField("alert"):
                self.service_alerts.append(self._parse_service_alert(entity))

    def _parse_trip_update(self, tu_msg: gtfs_realtime_pb2.TripUpdate) -> TripUpdate:
        """
        Parses a GTFS TripUpdate message into a TripUpdate dataclass.
        """
        trip = tu_msg.trip
        vehicle = tu_msg.vehicle

        # Build TripDescriptor from GTFS protobuf, mapping enums to strings
        trip_desc = TripDescriptor(
            trip_id=trip.trip_id if trip.HasField("trip_id") else None,
            route_id=trip.route_id if trip.HasField("route_id") else None,
            direction_id=trip.direction_id if trip.HasField("direction_id") else None,
            start_time=trip.start_time if trip.HasField("start_time") else None,
            start_date=trip.start_date if trip.HasField("start_date") else None,
            schedule_relationship=SCHEDULE_RELATIONSHIP.get(trip.schedule_relationship, "UNKNOWN")
            if trip.HasField("schedule_relationship") else None,
        )

        # Build optional VehicleDescriptor if available
        vehicle_desc = VehicleDescriptor(
            id=vehicle.id if vehicle.HasField("id") else None,
            label=vehicle.label if vehicle.HasField("label") else None,
            license_plate=vehicle.license_plate if vehicle.HasField("license_plate") else None,
        ) if tu_msg.HasField("vehicle") else None

        # Build list of StopTimeUpdate entries (arrival/departure changes)
        stop_time_updates = []
        for stu in tu_msg.stop_time_update:
            arrival = StopTimeEvent(
                delay=stu.arrival.delay if stu.HasField("arrival") and stu.arrival.HasField("delay") else None,
                time=stu.arrival.time if stu.HasField("arrival") and stu.arrival.HasField("time") else None,
                uncertainty=stu.arrival.uncertainty if stu.HasField("arrival") and stu.arrival.HasField("uncertainty") else None,
            ) if stu.HasField("arrival") else None

            departure = StopTimeEvent(
                delay=stu.departure.delay if stu.HasField("departure") and stu.departure.HasField("delay") else None,
                time=stu.departure.time if stu.HasField("departure") and stu.departure.HasField("time") else None,
                uncertainty=stu.departure.uncertainty if stu.HasField("departure") and stu.departure.HasField("uncertainty") else None,
            ) if stu.HasField("departure") else None

            stop_time_updates.append(StopTimeUpdate(
                stop_sequence=stu.stop_sequence if stu.HasField("stop_sequence") else None,
                stop_id=stu.stop_id if stu.HasField("stop_id") else None,
                arrival=arrival,
                departure=departure,
                schedule_relationship=STOP_TIME_SCHEDULE_RELATIONSHIP.get(stu.schedule_relationship, "UNKNOWN")
                if stu.HasField("schedule_relationship") else None,
            ))

        # Final TripUpdate dataclass
        return TripUpdate(
            trip=trip_desc,
            vehicle=vehicle_desc,
            stop_time_update=stop_time_updates,
            timestamp=tu_msg.timestamp if tu_msg.HasField("timestamp") else None,
            delay=tu_msg.delay if tu_msg.HasField("delay") else None,
        )

    def _parse_vehicle_position(self, vp_msg: gtfs_realtime_pb2.VehiclePosition) -> VehiclePosition:
        """
        Parses a GTFS VehiclePosition message into a VehiclePosition dataclass.
        """
        pos = vp_msg.position
        trip = vp_msg.trip
        vehicle = vp_msg.vehicle

        # Build Position (lat/lon/speed/etc.)
        position = Position(
            latitude=pos.latitude if pos.HasField("latitude") else None,
            longitude=pos.longitude if pos.HasField("longitude") else None,
            bearing=pos.bearing if pos.HasField("bearing") else None,
            odometer=pos.odometer if pos.HasField("odometer") else None,
            speed=pos.speed if pos.HasField("speed") else None,
        ) if vp_msg.HasField("position") else None

        # Build optional TripDescriptor if attached
        trip_desc = TripDescriptor(
            trip_id=trip.trip_id if trip.HasField("trip_id") else None,
            route_id=trip.route_id if trip.HasField("route_id") else None,
            direction_id=trip.direction_id if trip.HasField("direction_id") else None,
            start_time=trip.start_time if trip.HasField("start_time") else None,
            start_date=trip.start_date if trip.HasField("start_date") else None,
            schedule_relationship=SCHEDULE_RELATIONSHIP.get(trip.schedule_relationship, "UNKNOWN")
            if trip.HasField("schedule_relationship") else None,
        ) if vp_msg.HasField("trip") else None

        # Build optional VehicleDescriptor if attached
        vehicle_desc = VehicleDescriptor(
            id=vehicle.id if vehicle.HasField("id") else None,
            label=vehicle.label if vehicle.HasField("label") else None,
            license_plate=vehicle.license_plate if vehicle.HasField("license_plate") else None,
        ) if vp_msg.HasField("vehicle") else None

        # Final VehiclePosition dataclass
        return VehiclePosition(
            vehicle=vehicle_desc,
            trip=trip_desc,
            position=position,
            current_stop_sequence=vp_msg.current_stop_sequence if vp_msg.HasField("current_stop_sequence") else None,
            stop_id=vp_msg.stop_id if vp_msg.HasField("stop_id") else None,
            current_status=VEHICLE_STOP_STATUS.get(vp_msg.current_status, "UNKNOWN") if vp_msg.HasField("current_status") else None,
            timestamp=vp_msg.timestamp if vp_msg.HasField("timestamp") else None,
            congestion_level=CONGESTION_LEVEL.get(vp_msg.congestion_level, "UNKNOWN") if vp_msg.HasField("congestion_level") else None,
            occupancy_status=OCCUPANCY_STATUS.get(vp_msg.occupancy_status, "UNKNOWN") if vp_msg.HasField("occupancy_status") else None,
        )

    def _parse_service_alert(self, entity: gtfs_realtime_pb2.FeedEntity) -> ServiceAlert:
        """
        Parses a GTFS ServiceAlert message into a ServiceAlert dataclass.
        """
        alert = entity.alert

        # Pull translated text (only first translation for now)
        header = alert.header_text.translation[0].text if alert.header_text.translation else None
        description = alert.description_text.translation[0].text if alert.description_text.translation else None

        # Final ServiceAlert dataclass
        return ServiceAlert(
            id=entity.id if entity.HasField("id") else None,
            header_text=header,
            description_text=description,
            cause=ALERT_CAUSE.get(alert.cause, "UNKNOWN") if alert.HasField("cause") else None,
            effect=ALERT_EFFECT.get(alert.effect, "UNKNOWN") if alert.HasField("effect") else None,
        )