import models
import time

class MessageService():

    def __init__(self, udp_service):
        self.udp_service = udp_service

    def get_messages(self):
        spat_messages = self.udp_service.spat_responses
        map_messages = self.udp_service.map_responses
        messages = []

        for map in map_messages:
            intersection_id = map['map']['intersections'][0]['id']['id']
            if messages:
                for message in messages:
                    if str(message.intersection_id) == str(intersection_id):
                        message.map_available = True
                    else:
                        messages.append(models.Message(intersection_id, True, False))
            else: 
                messages.append(models.Message(intersection_id, True, False))
        
        for spat in spat_messages:
            intersection_id = spat['spat']['intersections'][0]['id']['id']
            if messages:
                for message in messages:
                    if str(message.intersection_id) == str(intersection_id):
                        message.spat_available = True
                    else:
                        messages.append(models.Message(intersection_id, False, True))
            else:
                messages.append(models.Message(intersection_id, False, True))
        

        return messages

    def get_intersection(self, intersection_id):
        
        map = self.get_single_map(intersection_id)
        spat = self.get_single_spat(intersection_id)

        if "speedLimits" in map['map']['intersections'][0]:
            speed_limits=[models.SpeedLimit(
                speed = map['map']['intersections'][0]['speedLimits'][0]['speed'],
                type = map['map']['intersections'][0]['speedLimits'][0]['type'])
                ]
        else:
            speed_limits = None
        new_intersection = models.Intersection(
            id=map['map']['intersections'][0]['id']['id'], 
            station_id = map['header']['stationID'],
            name = map['map']['intersections'][0]['name'],
            region=map['map']['intersections'][0]['id']['region'], 
            revision=map['map']['intersections'][0]['revision'], 
            status = None, 
            moy = None,
            timestamp = None,
            lane_width = None,
            speed_limits = speed_limits,
            lanes = self.get_lanes(intersection_id),
            signal_groups = self.get_signal_groups(intersection_id)
        )

        return new_intersection
    
    def get_lanes(self, intersection_id):
        single_map = self.get_single_map(intersection_id)
        
        vehicle_lanes, bike_lanes, crosswalks = [], [], []

        for lane in single_map['map']['intersections'][0]['laneSet']:
    
            nodes = []
            # Why 1 here?
            for node in lane['nodeList'][1]:
                nodes.append(models.Node(models.Offset(node['delta'][1]['x'], node['delta'][1]['y'])))
            
            if 'bikeLane' in lane['laneAttributes']['laneType']:
                bike_lanes.append(models.Lane(id=lane['laneID'], nodes=nodes))
            if 'vehicle' in lane['laneAttributes']['laneType']:
                vehicle_lanes.append(models.Lane(id=lane['laneID'], nodes=nodes))
            if 'crosswalk' in lane['laneAttributes']['laneType']:
                crosswalks.append(models.Lane(id=lane['laneID'], nodes=nodes))

        return models.IntersectionLanes(
            position=models.Position(
                single_map['map']['intersections'][0]['refPoint']['lat'],
                single_map['map']['intersections'][0]['refPoint']['long']),
            bike_lanes = bike_lanes,
            vehicle_lanes = vehicle_lanes,
            crosswalks = crosswalks
        )


    def get_signal_groups(self, intersection_id):
        spat = self.get_single_spat(intersection_id)
        signal_groups = []
        
        if spat:
            for signal_group in spat['spat']['intersections'][0]['states']:
                
                min_end_time, max_end_time, likely_time, confidence = None, None, None, None

                if 'minEndTime' in signal_group['state-time-speed'][0]['timing']:
                    min_end_time = self.convertTime(signal_group['state-time-speed'][0]['timing']['minEndTime'])
                
                if 'maxEndTime' in signal_group['state-time-speed'][0]['timing']:
                    max_end_time = self.convertTime(signal_group['state-time-speed'][0]['timing']['maxEndTime'])
                
                if 'likelyTime' in signal_group['state-time-speed'][0]['timing']:
                    likely_time = self.convertTime(signal_group['state-time-speed'][0]['timing']['likelyTime'])
                
                if 'confidence' in signal_group['state-time-speed'][0]['timing']:
                    confidence = signal_group['state-time-speed'][0]['timing']['confidence']

                new_state = models.SignalGroup(
                    id = signal_group['signalGroup'],
                    state = signal_group['state-time-speed'][0]['eventState'],
                    min_end_time = min_end_time,            
                    max_end_time = max_end_time,
                    likely_time = likely_time,
                    confidence = confidence
                )
                signal_groups.append(new_state)
        
        return signal_groups

    def get_single_spat(self, intersection_id):
        spat_messages = self.udp_service.spat_responses
        for spat in spat_messages:
            if str(intersection_id) == str(spat['spat']['intersections'][0]['id']['id']):
                return spat
    
    def get_single_map(self, intersection_id):
        map_messages = self.udp_service.map_responses
        for map in map_messages:
            if str(intersection_id) == str(map['map']['intersections'][0]['id']['id']):
                return map

    def convertTime(self, given_seconds):

        result = time.localtime(time.time())
        t = (result.tm_year, result.tm_mon, result.tm_mday, result.tm_hour, 0, 0, 0, 0, 0)
        lt = time.mktime(t)
        return time.ctime(lt+(int(given_seconds)/10))