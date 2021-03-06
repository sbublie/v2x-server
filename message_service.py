import models as models
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
        # TODO: Improve the performance of this implementation

        # Get all received SPAT and MAP messages
        spat_messages = self.udp_service.spat_responses
        map_messages = self.udp_service.map_responses
        messages = []

        # Go through all received MAP messages and add the respective Message models to the local list
        # or modify the existing entry
        if map_messages:
            for map in map_messages:
                intersection_id = map['map']['intersections'][0]['id']['id']
                if messages:
                    for message in messages:
                        if int(message.intersection_id) == int(intersection_id):
                            message.map_available = True
                        else:
                            messages.append(models.Message(
                                intersection_id, True, False))
                else:
                    messages.append(models.Message(
                        intersection_id, True, False))

        # Go through all received SPAT messages and add the respective Message models to the local list
        # or modify the existing entry
        if spat_messages:
            for spat in spat_messages:
                intersection_id = spat['spat']['intersections'][0]['id']['id']
                if messages:
                    for message in messages:
                        if int(message.intersection_id) == int(intersection_id):
                            message.spat_available = True
                        else:
                            messages.append(models.Message(
                                intersection_id, False, True))
                else:
                    messages.append(models.Message(
                        intersection_id, False, True))

        return messages

    # Called from the GraphQL client if the IntersectionResult is requested
    def get_intersection(self, intersection_id: int) -> (models.Intersection | None):

        map = self._get_single_map(intersection_id)

        if map:
            if "speedLimits" in map['map']['intersections'][0]:
                speed_limits = [models.SpeedLimit(
                    speed=map['map']['intersections'][0]['speedLimits'][0]['speed'],
                    type=map['map']['intersections'][0]['speedLimits'][0]['type'])
                ]
            else:
                speed_limits = None

            if 'refPoint' in map['map']['intersections'][0]:
                ref_position = models.Position(
                    map['map']['intersections'][0]['refPoint']['lat'], map['map']['intersections'][0]['refPoint']['long'])
            else:
                ref_position = models.Position(49, 9)

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
                speed_limits=speed_limits,
                ref_position=ref_position,
                lanes=self._get_lanes(intersection_id),
                signal_groups=self._get_signal_groups(intersection_id)
            )
        else:
            return None

    def _get_lanes(self, intersection_id: int) -> list[models.Lane]:

        single_map = self._get_single_map(intersection_id)
        lanes = []

        for lane in single_map['map']['intersections'][0]['laneSet']:

            nodes = []

            for node in lane['nodeList'][1]:
                nodes.append(models.Node(models.Offset(
                    node['delta'][1]['x'], node['delta'][1]['y'])))

            ingress_approach_id, egress_approach_id, approach_type, shared_with_id, maneuver_id = None, None, 0, None, None

            # TODO: Implement missing parameter
            if 'ingressApproach' in lane:
                ingress_approach_id = lane['ingressApproach']
            if 'egressApproach' in lane:
                egress_approach_id = lane['egressApproach']
            if 'directionalUse' in lane['laneAttributes']:
                if lane['laneAttributes']['directionalUse'][0] == b'\x80':
                    approach_type = 1
            # if 'sharedWith' in lane['laneAttributes']:
                #shared_with_id = lane['laneAttributes']['sharedWith']
            # if 'maneuvers' in lane['laneAttributes']:
                #maneuver_id = lane['laneAttributes']['maneuvers']

            connects_to = None
            if 'connectsTo' in lane and 'signalGroup' in lane['connectsTo'][0]:
                connects_to = models.ConnectsTo(
                    signal_group_id=lane['connectsTo'][0]['signalGroup'])

            lane_type = None
            if 'vehicle' in lane['laneAttributes']['laneType']:
                lane_type = "VEHICLELANE"
            if 'bikeLane' in lane['laneAttributes']['laneType']:
                lane_type = "BIKELANE"
            if 'crosswalk' in lane['laneAttributes']['laneType']:
                lane_type = "CROSSWALK"

            lanes.append(models.Lane(
                id=lane['laneID'],
                type=lane_type,
                nodes=nodes,
                connects_to=connects_to,
                ingress_approach_id=ingress_approach_id,
                egress_approach_id=egress_approach_id,
                approach_type=approach_type,
                shared_with_id=shared_with_id,
                maneuver_id=maneuver_id
            ))
        return lanes

    def _get_signal_groups(self, intersection_id):
        spat = self._get_single_spat(intersection_id)
        signal_groups = []

        if spat:
            for signal_group in spat['spat']['intersections'][0]['states']:

                min_end_time, max_end_time, likely_time, confidence = None, None, None, None

                if 'minEndTime' in signal_group['state-time-speed'][0]['timing']:
                    min_end_time = signal_group['state-time-speed'][0]['timing']['minEndTime']

                if 'maxEndTime' in signal_group['state-time-speed'][0]['timing']:
                    max_end_time = signal_group['state-time-speed'][0]['timing']['maxEndTime']

                if 'likelyTime' in signal_group['state-time-speed'][0]['timing']:
                    likely_time = signal_group['state-time-speed'][0]['timing']['likelyTime']

                if 'confidence' in signal_group['state-time-speed'][0]['timing']:
                    confidence = signal_group['state-time-speed'][0]['timing']['confidence']

                state = 'UNDEFINED'
                if 'eventState' in signal_group['state-time-speed'][0]:
                    match signal_group['state-time-speed'][0]['eventState']:
                        case 'permissive-Movement-Allowed':
                            state = "GREEN"
                        case 'pre-Movement':
                            state = "GREEN"
                        case 'protected-Movement-Allowed':
                            state = "GREEN"
                        case 'permissive-clearance':
                            state = 'YELLOW'
                        case 'protected-clearance':
                            state = 'YELLOW'
                        case 'caution-Conflicting-Traffic':
                            state = 'YELLOW'
                        case 'stop-And-Remain':
                            state = 'RED'
                        case 'stop-Then-Proceed':
                            state = 'RED'
                        case 'dark':
                            state = 'DARK'
                        case 'unavailable':
                            state = 'DARK'

                signal_groups.append(models.SignalGroup(
                    id=signal_group['signalGroup'],
                    state=state,
                    min_end_time=min_end_time,
                    max_end_time=max_end_time,
                    likely_time=likely_time,
                    confidence=confidence
                ))

        return signal_groups

    def _get_single_spat(self, intersection_id):
        spat_messages = self.udp_service.spat_responses
        for spat in spat_messages:
            if int(intersection_id) == int(spat['spat']['intersections'][0]['id']['id']):
                return spat

    def _get_single_map(self, intersection_id):
        map_messages = self.udp_service.map_responses
        for map in map_messages:
            if int(intersection_id) == int(map['map']['intersections'][0]['id']['id']):
                return map
