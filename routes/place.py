from flask import Blueprint, jsonify, request
from models.route import Route
from models.location import Location
from models.connection import Connection
import math

place_bp = Blueprint('place', __name__, url_prefix='/place')

def calculate_distance(lat1, lon1, lat2, lon2):
    # 2点間の距離をヘベルサイン公式で計算（メートル単位）
    R = 6371000  # 地球の半径（メートル）
    
    # 緯度経度をラジアンに変換
    lat1_rad = math.radians(float(lat1))
    lon1_rad = math.radians(float(lon1))
    lat2_rad = math.radians(float(lat2))
    lon2_rad = math.radians(float(lon2))
    
    # 緯度経度の差分
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c

@place_bp.route('/', methods=['GET'])
def index():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    
    if not lat or not lon:
        return jsonify({"error": "緯度と経度を指定してください"}), 400
    
    try:
        # 全ての場所を取得
        locations = Location.select()
        
        # 最も近い場所を探す
        nearest_location = None
        min_distance = float('inf')
        
        for location in locations:
            distance = calculate_distance(
                lat, lon,
                location.latitude, location.longitude
            )
            
            if distance < min_distance:
                min_distance = distance
                nearest_location = location
        
        if nearest_location:
            return jsonify({
                "location_id": nearest_location.location_id,
                "location_name": nearest_location.location_name,
                "distance": round(min_distance, 2),  # メートル単位で小数点2桁まで
                "latitude": nearest_location.latitude,
                "longitude": nearest_location.longitude
            })
        else:
            return jsonify({"error": "場所が見つかりません"}), 404
            
    except ValueError:
        return jsonify({"error": "不正な緯度経度の値です"}), 400
    
    