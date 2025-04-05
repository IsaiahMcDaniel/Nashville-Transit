# gtfs_trip_updates.py
#
# This module defines dataclasses for parsing GTFS-realtime TripUpdate messages,
# including trip descriptors, stop time updates, and vehicle descriptors.

from dataclasses import dataclass
from typing import Optional, List

def dataclass_to_dict(obj):
    """
    Recursively converts dataclass objects (and lists of them) into dictionaries.
    Useful for JSON serialization and general use.
    """
    if isinstance(obj, list):
        return [dataclass_to_dict(i) for i in obj]
    elif hasattr(obj, "__dataclass_fields__"):
        return {
            k: dataclass_to_dict(v)
            for k, v in obj.__dict__.items()
        }
    else:
        return obj

@dataclass
class StopTimeEvent:
    """
    Represents a change in arrival and/or departure times at a stop.
    """
    delay: Optional[int] = None        # Delay in seconds (positive = late, negative = early)
    time: Optional[int] = None         # Updated absolute time as a UNIX timestamp
    uncertainty: Optional[int] = None  # Uncertainty in seconds about arrival/departure time

    def to_dict(self):
        return dataclass_to_dict(self)

@dataclass
class StopTimeUpdate:
    """
    Updates for arrival and/or departure events at a specific stop.
    """
    stop_sequence: Optional[int] = None             # The order of the stop in the trip's stop sequence
    stop_id: Optional[str] = None                   # Unique identifier for the stop
    arrival: Optional[StopTimeEvent] = None         # Updated arrival time information
    departure: Optional[StopTimeEvent] = None       # Updated departure time information
    schedule_relationship: Optional[str] = None     # Relationship to schedule: e.g. 'SCHEDULED', 'SKIPPED'

    def to_dict(self):
        return dataclass_to_dict(self)

@dataclass
class TripDescriptor:
    """
    Identifies a specific scheduled or real-time trip.
    """
    trip_id: Optional[str] = None                   # Unique identifier for the trip
    route_id: Optional[str] = None                  # Identifier for the route the trip belongs to
    direction_id: Optional[int] = None              # Direction of travel (0 = outbound, 1 = inbound)
    start_time: Optional[str] = None                # Scheduled start time of the trip (HH:MM:SS)
    start_date: Optional[str] = None                # Scheduled start date of the trip (YYYYMMDD)
    schedule_relationship: Optional[str] = None     # e.g., 'SCHEDULED', 'CANCELED'

    def to_dict(self):
        return dataclass_to_dict(self)

@dataclass
class VehicleDescriptor:
    """
    Describes the vehicle performing the trip.
    """
    id: Optional[str] = None                        # Unique ID for the vehicle
    label: Optional[str] = None                     # Public-facing label (e.g., fleet number)
    license_plate: Optional[str] = None             # Vehicle's license plate (if available)

    def to_dict(self):
        return dataclass_to_dict(self)

@dataclass
class TripUpdate:
    """
    Realtime updates for a specific trip, including stop time adjustments and vehicle info.
    """
    trip: TripDescriptor                            # Information identifying the trip
    vehicle: Optional[VehicleDescriptor] = None     # Information about the vehicle
    stop_time_update: List[StopTimeUpdate] = None   # List of updated stop times along the route
    timestamp: Optional[int] = None                 # Time the update was recorded (UNIX timestamp)
    delay: Optional[int] = None                     # Overall delay for the trip in seconds

    def to_dict(self):
        return dataclass_to_dict(self)