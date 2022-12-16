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

        self.map_responses = []
        self.spat_responses = []

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

            if not self.map_responses:
                self.map_responses.append(decoded)
                logging.debug('first map added')
            else:
                for map in self.map_responses:
                    if decoded['header']['stationID'] == map['header']['stationID']:
                        logging.debug('map not added')
                        return
                self.map_responses.append(decoded)
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
            if str(decoded['spat']['intersections'][0]['id']['id']) == str(309):

                if self.spat_responses:
                    self.spat_responses[0] = decoded
                    logging.debug('309 spat replaced')
                else:
                    self.spat_responses.append(decoded)
                    logging.debug('309 spat added')

    def resolve_udp_packets(self):
        try:
            mode = sys.argv[1]
        except IndexError:
            mode = "live"

        if mode == 'debug':

            for data in const.EXAMPLE_MAPEM_SPATEM_DATA:
                # TODO: Use ItsPduHeader to identify message type
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

                # TODO: Use ItsPduHeader to identify message type
                if const.MAPEM_IDENTIFIER in data:
                    with threading.Lock():
                        self._handle_mapem(data)
                if const.SPATEM_IDENTIFIER in data:
                    with threading.Lock():
                        self._handle_spatem(data)
