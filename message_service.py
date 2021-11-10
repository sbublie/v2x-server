import models
import time


class MessageService():

    def __init__(self, udp_service):
        self.udp_service = udp_service

    def get_intersections(self):
    
        intersections = []
        maps = self.udp_service.map_responses
        for intersection in maps:
            
            if "speedLimits" in intersection['map']['intersections'][0]:
                speed_limits=[models.SpeedLimit(
                    speed = intersection['map']['intersections'][0]['speedLimits'][0]['speed'],
                    type = intersection['map']['intersections'][0]['speedLimits'][0]['type'])
                    ]
            else:
                speed_limits = None
            new_intersection = models.IntersectionMeta(
                id=intersection['map']['intersections'][0]['id']['id'], 
                region=intersection['map']['intersections'][0]['id']['region'], 
                revision=intersection['map']['intersections'][0]['revision'], 
                status=None, 
                moy=None, 
                timestamp=None,
                
            )
            intersections.append(new_intersection)
        
        return intersections
    
    def get_map(self, intersection_id):
        single_map = self.get_single_map(intersection_id)
        
        vehicle_lanes, bike_lanes, crosswalks = [], [], []

        for lane in single_map['map']['intersections'][0]['laneSet']:
            if 'bikeLane' in lane['laneAttributes']['laneType']:
                bike_lanes.append(models.Lane(id=lane['laneID']))
            if 'vehicle' in lane['laneAttributes']['laneType']:
                vehicle_lanes.append(models.Lane(id=lane['laneID']))
            if 'crosswalk' in lane['laneAttributes']['laneType']:
                crosswalks.append(models.Lane(id=lane['laneID']))

        return models.Map(
            position=models.Position(
                single_map['map']['intersections'][0]['refPoint']['lat'],
                single_map['map']['intersections'][0]['refPoint']['long']),
            bike_lanes = bike_lanes,
            vehicle_lanes = vehicle_lanes,
            crosswalks = crosswalks
        )


    def get_states(self, intersection_id):
        single_spat = self.get_single_spat(intersection_id)
        states = []
        
        if single_spat:
            for state in single_spat['spat']['intersections'][0]['states']:
                
                min_end_time, max_end_time, likely_time, confidence = None, None, None, None

                if 'minEndTime' in state['state-time-speed'][0]['timing']:
                    min_end_time = self.convertTime(state['state-time-speed'][0]['timing']['minEndTime'])
                
                if 'maxEndTime' in state['state-time-speed'][0]['timing']:
                    max_end_time = self.convertTime(state['state-time-speed'][0]['timing']['maxEndTime'])
                
                if 'likelyTime' in state['state-time-speed'][0]['timing']:
                    likely_time = self.convertTime(state['state-time-speed'][0]['timing']['likelyTime'])
                
                if 'confidence' in state['state-time-speed'][0]['timing']:
                    confidence = state['state-time-speed'][0]['timing']['confidence']

                new_state = models.IntersectionState(
                    signal_group = state['signalGroup'],
                    event_state = state['state-time-speed'][0]['eventState'],
                    min_end_time = min_end_time,            
                    max_end_time = max_end_time,
                    likely_time = likely_time,
                    confidence = confidence
                )
                states.append(new_state)
        
        return states

    def get_single_spat(self, intersection_id):
        all_spat = self.udp_service.spat_responses
        for spat in all_spat:
            if intersection_id == str(spat['spat']['intersections'][0]['id']['id']):
                return spat
    
    def get_single_map(self, intersection_id):
        all_map = self.udp_service.map_responses
        for map in all_map:
            if intersection_id == str(map['map']['intersections'][0]['id']['id']):
                return map


    def get_lanes(self):
        message = self.udp_service.map_responses[0]
        if message:
            return message['map']['intersections'][0]['laneSet']
        return 'Error'

    def get_signal_groups(self):
        message = self.udp_service.spat_responses[0]
        if message:
            return message['spat']['intersections'][0]['states']
        return 'Error'

    def convertTime(given_seconds):

        result = time.localtime(time.time())
        t = (result.tm_year, result.tm_mon, result.tm_mday, result.tm_hour, 0, 0, 0, 0, 0)
        lt = time.mktime(t)
        return time.ctime(lt+(int(given_seconds)/10))