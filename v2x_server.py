import threading
from flask import Flask
from flask_cors import CORS

from message_service import MessageService
from udp_service import UdpService
from graphql_api import client


def main():

    app = Flask(__name__)
    # initiate CORS handling to avoid any preflight or cross reference errors
    CORS(app)

    client.initialize(app, message_service)

    app.run(host="0.0.0.0", port=5000)


if __name__ == '__main__':

    # The UdpService decodes the messages which can then be accessed by the MessageService
    udp_service = UdpService()
    message_service = MessageService(udp_service)

    # The idea here is to run the message resolving and the web server on differnt threads
    # TODO: Optimize multithreding
    udp_thread = threading.Thread(target=udp_service.resolve_udp_packets, daemon=False)
    udp_thread.start()
    main()
