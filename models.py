class IntersectionMeta():
    def __init__(self, id, region=None, revision=None, status=None, moy=None, timestamp=None, speed_limits=None):
        self.id = id
        self.region = region
        self.revision = revision
        self.status = status
        self.moy = moy
        self.timestamp = timestamp
        self.speed_limits = speed_limits

class IntersectionState():
    def __init__(self, signal_group, event_state=None, min_end_time=None, max_end_time=None, likely_time=None, confidence=None) -> None:
        self.signal_group = signal_group
        self.event_state = event_state
        self.min_end_time = min_end_time
        self.max_end_time = max_end_time
        self.likely_time = likely_time
        self.confidence = confidence

class Map():
    def __init__(self, position, vehicle_lanes, bike_lanes, crosswalks) -> None:
        self.position = position
        self.vehicle_lanes = vehicle_lanes
        self.bike_lanes = bike_lanes
        self.crosswalks = crosswalks

class Lane():
    def __init__(self, id, attributes=None, nodes=None, connects_to=None) -> None:
        self.id = id
        self.attributes = attributes
        self.nodes = nodes
        self.connects_to = connects_to

class LaneAttributes():
    def __init__(self, ingress_approach, egress_approach, directional_use, shared_with, maneuvers) -> None:
        self.ingress_approach = ingress_approach
        self.egress_approach = egress_approach
        self.directional_use = directional_use
        self.shared_with = shared_with
        self.maneuvers = maneuvers

class Node():
    def __init__(self, offset, d_width) -> None:
        self.offset = offset
        self.d_width = d_width

class Offset():
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

class ConnectsTo():
    def __init__(self, lane_id, maneuver, signal_group_id) -> None:
        self.lane = lane_id
        self.maneuver = maneuver
        self.signal_group = signal_group_id

class Position():
    def __init__(self, lat, long) -> None:
        self.lat = lat
        self.long = long

class SpeedLimit():
    def __init__(self, speed, type):
        self.speed = speed
        self.type = type
