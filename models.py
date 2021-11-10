class Intersection():
    def __init__(self, id, station_id=None, name=None, region=None, revision=None, status=None, moy=None, timestamp=None, lane_width=None, speed_limits=None, lanes=None, signal_groups=None):
        self.id = id
        self.station_id = station_id
        self.name = name
        self.region = region
        self.revision = revision
        self.status = status
        self.moy = moy
        self.timestamp = timestamp
        self.lane_width = lane_width
        self.speed_limits = speed_limits
        self.lanes = lanes
        self.signal_groups = signal_groups

class Message():
    def __init__(self, intersection_id, map_available, spat_available):
        self.intersection_id = intersection_id
        self.map_available = map_available
        self.spat_available =  spat_available

class SignalGroup():
    def __init__(self, id, state=None, min_end_time=None, max_end_time=None, likely_time=None, confidence=None) -> None:
        self.id = id
        self.state = state
        self.min_end_time = min_end_time
        self.max_end_time = max_end_time
        self.likely_time = likely_time
        self.confidence = confidence

class IntersectionLanes():
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
    def __init__(self, offset, d_width=None) -> None:
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
