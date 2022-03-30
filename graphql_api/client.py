from flask import Flask, request, jsonify
from flask_cors import CORS

from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, snake_case_fallback_resolvers, ObjectType, convert_kwargs_to_snake_case
from ariadne.constants import PLAYGROUND_HTML
    
def initialize(app, message_service):

    def _resolve_messages(obj, info):
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
    def _resolve_intersection(obj, info, intersection_id):

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
    
    query = ObjectType("Query")
    query.set_field("messages", _resolve_messages)
    query.set_field("intersection", _resolve_intersection)

    type_defs = load_schema_from_path("graphql_api/schema.graphql")
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
        
    

        