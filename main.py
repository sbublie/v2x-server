import threading
from flask import Flask, request, jsonify

from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, snake_case_fallback_resolvers, ObjectType, convert_kwargs_to_snake_case
from ariadne.constants import PLAYGROUND_HTML

from message_service import MessageService
from udp_service import UdpService 

import models

def main():
    
    app = Flask(__name__)

    query = ObjectType("Query")
    query.set_field("intersections_meta", resolve_intersections)
    query.set_field("intersection_state", resolve_intersection_state)
    query.set_field("intersection_map", resolve_intersection_map)

    type_defs = load_schema_from_path("schema.graphql")
    schema = make_executable_schema(
        type_defs, query, snake_case_fallback_resolvers
    )

    @app.route("/graphql", methods=["GET"])
    def graphql_playground():
        return PLAYGROUND_HTML, 200

    @app.route("/graphql", methods=["POST"])
    def graphql_server():
        data = request.get_json()

        success, result = graphql_sync(
            schema,
            data,
            context_value=request,
            debug=app.debug
        )

        status_code = 200 if success else 400
        return jsonify(result), status_code

    app.run(host="0.0.0.0", port=5000)

def resolve_intersections(obj, info):
    intersections = message_service.get_intersections()
    
    try:
        payload = {
            "success": True,
            "intersections": intersections
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    
    return payload

@convert_kwargs_to_snake_case
def resolve_intersection_state(obj, info, intersection_id): 
    
    states = message_service.get_states(intersection_id)
    
    if not states:
        states = 'None'
    
    try:
        payload = {
            "success": True,
            "states": states
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload

@convert_kwargs_to_snake_case
def resolve_intersection_map(obj, info, intersection_id): 
    map = message_service.get_map(intersection_id)
    try:
        payload = {
            "success": True,
            "map": map
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload

if __name__ == '__main__':
    udp_service = UdpService()
    message_service = MessageService(udp_service)
    x = threading.Thread(target=udp_service.resolve_udp_packets, daemon=True)
    x.start()
    main()
    
