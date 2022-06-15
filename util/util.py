import socket
import util.const as const


def print_welcome_message():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print("")
    print("-------------------")
    print("V2X-Server Version " + const.APP_VERSION + " running on " + hostname)
    print("Endpoint for API requests and GraphQL playground: " + "http://" +
          ip_address + ":" + str(const.APP_PORT) + "/graphql")
    print("-------------------")
    print("")
