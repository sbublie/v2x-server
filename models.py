class Intersection():
    def __init__(self, id, station_id=None, name=None, region=None, revision=None, status=None, moy=None, timestamp=None, lane_width=None, speed_limits=None, ref_position=None, lanes=None, signal_groups=None):
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
        self.ref_position = ref_position
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

class Lane():
    def __init__(self, id, type, nodes=None, connects_to=None, ingress_approach_id=None, egress_approach_id=None, approach_type=None, shared_with_id=None, maneuver_id=None) -> None:
        self.id = id
        self.type = type
        self.nodes = nodes
        self.connects_to = connects_to
        self.ingress_approach_id = ingress_approach_id
        self.egress_approach_id = egress_approach_id
        self.approach_type = approach_type
        self.shared_with_id = shared_with_id
        self.maneuver_id = maneuver_id

class Node():
    def __init__(self, offset, d_width=None) -> None:
        self.offset = offset
        self.d_width = d_width

class Offset():
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

class ConnectsTo():
    def __init__(self, lane_id = None, maneuver = None, signal_group_id = None) -> None:
        self.lane = lane_id
        self.maneuver = maneuver
        self.signal_group_id = signal_group_id

class Position():
    def __init__(self, lat, long) -> None:
        self.lat = lat
        self.long = long

class SpeedLimit():
    def __init__(self, speed, type):
        self.speed = speed
        self.type = type
