from collections import defaultdict

import models
import const
from udp_service import UdpService


class MessageService():
    ''' 
    Class for constructing data models from decoded SPATEM/MAPEM messages.

    The methods are called by the GraphQL client after a request is received.
    '''

    # Called in main at startup
    def __init__(self, udp_service: UdpService):
        self.udp_service = udp_service

    # Called from the GraphQL client if the MessageResult is requested
    def get_messages(self) -> list[models.Message]:
        '''
        Returns a list of Message to represent the received MAPEM/SPATEM messages. 
        '''
        map_intersection_ids = self.udp_service.map_messages.keys()
        spat_intersection_ids = self.udp_service.spat_messages.keys()
        # Create a set with all intersection ids to avoid the use two for-loops
        intersection_ids = set(map_intersection_ids).union(set(spat_intersection_ids))
        # Create a dict that uses a Message object as a default value for a nonexistent key
        messages = defaultdict(lambda: models.Message(intersection_id, False, False))
        for intersection_id in intersection_ids:
            messages[intersection_id].map_available = intersection_id in map_intersection_ids
            messages[intersection_id].spat_available = intersection_id in spat_intersection_ids

        # Return a list containing only the Message objects
        return list(messages.values())

    # Called from the GraphQL client if the IntersectionResult is requested
    def get_intersection(self, intersection_id: int) -> (models.Intersection | None):

        map = self.udp_service.map_messages[intersection_id]
        if map:
            # TODO: Implement missing parameter
            return models.Intersection(
                id=map['map']['intersections'][0]['id']['id'],
                station_id=map['header']['stationID'],
                name=map['map']['intersections'][0]['name'],
                region=map['map']['intersections'][0]['id']['region'],
                revision=map['map']['intersections'][0]['revision'],
                status=None,
                moy=None,
                timestamp=None,
                lane_width=None,
                speed_limits=None,
                ref_position=models.Position(
                    map.get('map').get('intersections', [{}])[0].get('refPoint').get('lat'),
                    map.get('map').get('intersections', [{}])[0].get('refPoint').get('long')),
                lanes=self._get_lanes(intersection_id),
                signal_groups=self._get_signal_groups(intersection_id)
            )
        else:
            return None

    def _get_lanes(self, intersection_id: int) -> list[models.Lane]:

        single_map = self.udp_service.map_messages[intersection_id]
        lanes = []
        for lane in single_map['map']['intersections'][0]['laneSet']:
            nodes = []
            for node in lane['nodeList'][1]:
                nodes.append(models.Node(models.Offset(
                    node['delta'][1]['x'], node['delta'][1]['y'])))

            # TODO: Investigate different approach types
            # If b'\x80' is set on the directionalUse property the approach type is 1
            approach_type = 1 if lane.get('laneAttributes').get(
                'directionalUse')[0] == b'\x80' else 0
            # TODO: Implement missing parameter
            lanes.append(models.Lane(
                id=lane.get('laneID'),
                type=const.LANE_TYPES_MAP[lane.get(
                    'laneAttributes').get('laneType')[0]],
                nodes=nodes,
                connects_to=models.ConnectsTo(signal_group_id=lane.get(
                    'connectsTo', [{}])[0].get('signalGroup')),
                ingress_approach_id=lane.get('ingressApproach'),
                egress_approach_id=lane.get('egressApproach'),
                approach_type=approach_type,
                shared_with_id=None,
                maneuver_id=None
            ))
        return lanes

    def _get_signal_groups(self, intersection_id):

        signal_groups = []
        spat = self.udp_service.spat_messages[intersection_id]
        if spat:
            for signal_group in spat['spat']['intersections'][0]['states']:
                signal_groups.append(models.SignalGroup(
                    id=signal_group.get('signalGroup'),
                    state=const.SIGNAL_GROUP_STATE_MAP[signal_group.get(
                        'state-time-speed', [{}])[0].get('eventState', "UNDEFINED")],
                    min_end_time=signal_group.get(
                        'state-time-speed', [{}])[0].get('timing').get('minEndTime'),
                    max_end_time=signal_group.get(
                        'state-time-speed', [{}])[0].get('timing').get('maxEndTime'),
                    likely_time=signal_group.get(
                        'state-time-speed', [{}])[0].get('timing').get('likelyTime'),
                    confidence=signal_group.get(
                        'state-time-speed', [{}])[0].get('timing').get('confidence')
                ))
        return signal_groups

