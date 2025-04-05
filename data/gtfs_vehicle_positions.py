# gtfs_vehicle_positions.py
#
# This module defines dataclasses for GTFS-realtime VehiclePosition messages.
# It includes GPS location, trip and vehicle descriptors, and status information.

from dataclasses import dataclass
from typing import Optional
from gtfs_trip_updates import dataclass_to_dict, TripDescriptor, VehicleDescriptor

@dataclass
class Position:
    """
    Real-time geographic and movement data for a vehicle.
    """
    latitude: Optional[float] = None      # Latitude in degrees (WGS-84)
    longitude: Optional[float] = None     # Longitude in degrees (WGS-84)
    bearing: Optional[float] = None       # Direction of travel, in degrees (0 = North)
    odometer: Optional[float] = None      # Distance traveled by the vehicle (in meters, if available)
    speed: Optional[float] = None         # Current speed of the vehicle (in meters/second)

    def to_dict(self):
        return dataclass_to_dict(self)

@dataclass
class VehiclePosition:
    """
    Represents the current position and status of a transit vehicle.
    """
    vehicle: Optional[VehicleDescriptor] = None       # Identifies the vehicle (fleet number, ID, etc.)
    trip: Optional[TripDescriptor] = None             # Identifies the trip the vehicle is serving
    position: Optional[Position] = None               # Current GPS position and movement data
    current_stop_sequence: Optional[int] = None       # Index of the next stop in the trip's stop sequence
    stop_id: Optional[str] = None                     # ID of the current or next stop
    current_status: Optional[str] = None              # Vehicle's stop status (e.g., IN_TRANSIT_TO, STOPPED_AT)
    timestamp: Optional[int] = None                   # Time the position was recorded (UNIX timestamp)
    congestion_level: Optional[str] = None            # Level of congestion (e.g., RUNNING_SMOOTHLY, STOP_AND_GO)
    occupancy_status: Optional[str] = None            # Crowd level (e.g., EMPTY, MANY_SEATS_AVAILABLE, FULL)

    def to_dict(self):
        return dataclass_to_dict(self)