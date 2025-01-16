from flask import Blueprint, jsonify, request
from models.route import Route
from models.location import Location
from models.connection import Connection

in_route_bp = Blueprint('in_route', __name__, url_prefix='/internal')

@in_route_bp.route('/', methods=['GET'])
def index():
    start_location_id = request.args.get('from')
    end_location_id = request.args.get('to')
    
    if not start_location_id or not end_location_id:
        return jsonify({"error": "出発地点と目的地を指定してください"}), 400
    
    try:
        route = Route.get_or_none(
            Route.start_location == start_location_id,
            Route.end_location == end_location_id
        )
        
        if route:
            # 経路の詳細情報を取得
            connection_ids = route.connection_ids.split(':')
            route_details = []
            
            for conn_id in connection_ids:
                connection = Connection.get_by_id(int(conn_id))
                route_details.append({
                    'from': connection.from_location.location_name,
                    'to': connection.to_location.location_name,
                    'time': connection.travel_time
                })
            
            return jsonify({
                'route_name': route.route_name,
                'total_time': route.total_time,
                'details': route_details
            })
        else:
            return jsonify({"error": "指定された経路が見つかりません"}), 404
            
    except ValueError:
        return jsonify({"error": "不正なパラメータです"}), 400