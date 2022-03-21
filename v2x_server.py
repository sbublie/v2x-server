import threading
from flask import Flask, request, jsonify
from flask_cors import CORS

from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, snake_case_fallback_resolvers, ObjectType, convert_kwargs_to_snake_case
from ariadne.constants import PLAYGROUND_HTML

from message_service import MessageService
from udp_service import UdpService


def main():

    app = Flask(__name__)
    CORS(app)

    query = ObjectType("Query")
    query.set_field("messages", resolve_messages)
    query.set_field("intersection", resolve_intersection)

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


def resolve_messages(obj, info):
    messages = message_service.get_messages()

    if not messages:
        messages = 'None'

    try:
        payload = {
            "success": True,
            "messages": messages
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }

    return payload


@convert_kwargs_to_snake_case
def resolve_intersection(obj, info, intersection_id):

    intersection = message_service.get_intersection(intersection_id)

    if not intersection:
        intersection = 'None'

    try:
        payload = {
            "success": True,
            "item": intersection
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
