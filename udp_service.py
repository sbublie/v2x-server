import threading
import socket
import time
import asn1tools
import sys
import logging

import const


class UdpService():
    def __init__(self):
        # Create socket for IPv6 UDP connection
        self.s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        # Bind any address to port 37008
        self.s.bind(("::", 37008))

        # Use asn specification to decode uper strings
        self.foo = asn1tools.compile_files("rsc/etsi_mapem_spatem.asn", 'uper')

        self.map_messages = {}
        self.spat_messages = {}

    def _handle_mapem(self, data):
        logging.debug('decode map')
        decoded = False
        try:
            # Use asn sequence 'MAPEM' with asn1tools to decode the bytestring after the MAPEM identifier
            decoded = self.foo.decode(
                'MAPEM', data[data.index(const.MAPEM_IDENTIFIER):])
        except Exception as error:
            # TODO: Error handling
            pass

        if decoded:
            intersection_id = decoded['map']['intersections'][0]['id']['id']
            self.map_messages[intersection_id] = decoded
            logging.debug('new map added')


    def _handle_spatem(self, data):
        logging.debug('decode spat')
        decoded = False
        try:
            # Use asn sequence 'SPATEM' with asn1tools to decode the bytestring after the SPATEM identifier
            decoded = self.foo.decode(
                'SPATEM', data[data.index(const.SPATEM_IDENTIFIER):])
        except Exception as error:
            pass

        if decoded:
            # TODO: implement generic decoding for all intersections
            intersection_id = decoded['spat']['intersections'][0]['id']['id']
            self.spat_messages[intersection_id] = decoded

    def resolve_udp_packets(self):
        try:
            mode = sys.argv[1]
        except IndexError:
            mode = "live"

        if mode == 'debug':

            for data in const.EXAMPLE_MAPEM_SPATEM_DATA:
                if const.MAPEM_IDENTIFIER in data:
                    with threading.Lock():
                        self._handle_mapem(data)
                if const.SPATEM_IDENTIFIER in data:
                    with threading.Lock():
                        self._handle_spatem(data)

        if mode == 'live':
            while True:
                time.sleep(.01)
                data, addr = self.s.recvfrom(4096)
                if const.MAPEM_IDENTIFIER in data:
                    with threading.Lock():
                        self._handle_mapem(data)
                if const.SPATEM_IDENTIFIER in data:
                    with threading.Lock():
                        self._handle_spatem(data)
