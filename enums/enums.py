# enums.py
#
# This file provides mappings from GTFS-realtime enum values to their string names
# for use in parsing and displaying GTFS data in a human-readable format.

# TripDescriptor.ScheduleRelationship
SCHEDULE_RELATIONSHIP = {
    0: "SCHEDULED",     # The trip is scheduled as part of the static GTFS dataset
    1: "ADDED",         # The trip was added in realtime and is not part of the static schedule
    2: "UNSCHEDULED",   # The trip is running but is not part of the schedule
    3: "CANCELED",      # The scheduled trip has been canceled
}

# StopTimeUpdate.ScheduleRelationship
STOP_TIME_SCHEDULE_RELATIONSHIP = {
    0: "SCHEDULED",     # Stop is part of the scheduled trip
    1: "SKIPPED",       # Stop will not be visited
    2: "NO_DATA",       # No data is given for this stop
}

# VehiclePosition.OccupancyStatus
OCCUPANCY_STATUS = {
    0: "EMPTY",                           # Vehicle has no passengers
    1: "MANY_SEATS_AVAILABLE",           # Vehicle has many available seats
    2: "FEW_SEATS_AVAILABLE",            # Vehicle has few available seats
    3: "STANDING_ROOM_ONLY",             # Vehicle is full seated; only standing room
    4: "CRUSHED_STANDING_ROOM_ONLY",     # Vehicle is crowded, standing passengers only
    5: "FULL",                           # Vehicle is full and cannot take more passengers
    6: "NOT_ACCEPTING_PASSENGERS",       # Vehicle is not accepting any passengers
}

# VehiclePosition.CongestionLevel
CONGESTION_LEVEL = {
    0: "UNKNOWN_CONGESTION_LEVEL",   # Congestion status unknown
    1: "RUNNING_SMOOTHLY",           # Traffic is moving without delay
    2: "STOP_AND_GO",                # Traffic is slow, with frequent stops
    3: "CONGESTION",                 # Delayed due to congestion
    4: "SEVERE_CONGESTION",          # Significant delay due to heavy traffic
}

# VehiclePosition.VehicleStopStatus
VEHICLE_STOP_STATUS = {
    0: "INCOMING_AT",    # Vehicle is approaching the stop
    1: "STOPPED_AT",     # Vehicle is currently stopped at the stop
    2: "IN_TRANSIT_TO",  # Vehicle has departed and is en route to the next stop
}

# Alert.Effect
ALERT_EFFECT = {
    0: "NO_SERVICE",                  # No service at all
    1: "REDUCED_SERVICE",            # Reduced service
    2: "SIGNIFICANT_DELAYS",         # Long delays
    3: "DETOUR",                     # Route has a detour
    4: "ADDITIONAL_SERVICE",         # Extra service added
    5: "MODIFIED_SERVICE",           # Route changed but still operating
    6: "OTHER_EFFECT",               # Other unspecified impact
    7: "UNKNOWN_EFFECT",             # Effect not known
    8: "STOP_MOVED",                 # Stop has been relocated
    9: "NO_EFFECT",                  # Used to clear a previous alert
    10: "ACCESSIBILITY_ISSUE",       # Vehicle or station inaccessible
}

# Alert.Cause
ALERT_CAUSE = {
    0: "UNKNOWN_CAUSE",              # Unknown cause
    1: "OTHER_CAUSE",                # Other cause
    2: "TECHNICAL_PROBLEM",          # Technical failure or malfunction
    3: "STRIKE",                     # Labor strike
    4: "DEMONSTRATION",              # Protest or demonstration
    5: "ACCIDENT",                   # Collision or similar event
    6: "HOLIDAY",                    # Holiday-related schedule change
    7: "WEATHER",                    # Weather impact (snow, flooding, etc.)
    8: "MAINTENANCE",                # Scheduled or emergency maintenance
    9: "CONSTRUCTION",               # Construction project impact
    10: "POLICE_ACTIVITY",           # Police or emergency presence
    11: "MEDICAL_EMERGENCY",         # Passenger illness or injury
}