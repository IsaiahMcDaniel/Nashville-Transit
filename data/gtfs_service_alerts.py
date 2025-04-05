# gtfs_service_alerts.py
#
# This module defines the ServiceAlert dataclass for GTFS-realtime alerts.
# These alerts notify riders about issues like delays, detours, or service changes.

from dataclasses import dataclass
from typing import Optional
from gtfs_trip_updates import dataclass_to_dict

@dataclass
class ServiceAlert:
    """
    Represents an active service alert from the GTFS-realtime feed.
    These are typically used to inform riders of service disruptions.
    """
    id: Optional[str] = None                    # Unique identifier for the alert (from FeedEntity.id)
    header_text: Optional[str] = None           # Short headline or summary of the alert (e.g., "Detour on Route 5")
    description_text: Optional[str] = None      # Detailed description of the issue affecting service
    cause: Optional[str] = None                 # Cause of the alert (e.g., CONSTRUCTION, ACCIDENT, WEATHER)
    effect: Optional[str] = None                # Effect on service (e.g., DETOUR, DELAY, CANCELLED)

    def to_dict(self):
        return dataclass_to_dict(self)