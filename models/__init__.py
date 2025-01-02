from peewee import SqliteDatabase
from .db import db
from .location import Location
from .connection import Connection
from .route import Route
from collections import defaultdict
import heapq

# モデルのリストを定義
MODELS = [Location, Connection, Route]

def initialize_locations():
    # 既存のデータを削除
    Location.delete().execute()
    
    locations_data = [
        {'location_name': 'バス停'},#1
        {'location_name': '共通P'},#2
        {'location_name': '1号館'},#3
        {'location_name': '10号館'},#4
        {'location_name': '14号館'},#5
        {'location_name': '10号館大講義室棟'},#6
        {'location_name': '旧1号館'},#7
        {'location_name': '9号館'},#8
        {'location_name': '7号館'},#9
        {'location_name': '第1本部棟'},#10
        {'location_name': '第2本部棟'},#11
        {'location_name': '愛和会館'},#12
        {'location_name': '土木・建築実験棟'},#13
        {'location_name': '図書館'},#14
        {'location_name': '12号館'},#15
        {'location_name': '2号館'},#16
    ]
    for data in locations_data:
        Location.create(**data)

def initialize_connections():
    # 既存のデータを削除
    Connection.delete().execute()
    
    connections_data = [
        # 1号館、10号館、14号館あたり
        # 計測済み バス停からPまで
        {'from_location': 1, 'to_location': 2, 'travel_time': 130},

        # 1号館からPまでと1号館まで
        {'from_location': 2, 'to_location': 3, 'travel_time': 30},
        {'from_location': 3, 'to_location': 4, 'travel_time': 20},
        {'from_location': 4, 'to_location': 5, 'travel_time': 20},

        # ここから未計測
        {'from_location': 6, 'to_location': 4, 'travel_time': 20},

        # 1号館の北の方
        {'from_location': 7, 'to_location': 3, 'travel_time': 60},
        {'from_location': 8, 'to_location': 7, 'travel_time': 20},

        # 7号館（ルートわからんので適当）
        {'from_location': 9, 'to_location': 3, 'travel_time': 140},

        # 本部棟からPまで
        {'from_location': 10, 'to_location': 2, 'travel_time': 60},
        {'from_location': 11, 'to_location': 2, 'travel_time': 80},
        {'from_location': 14, 'to_location': 2, 'travel_time': 90},

        {'from_location': 12, 'to_location': 2, 'travel_time': 120},
        {'from_location': 13, 'to_location': 2, 'travel_time': 180},

        {'from_location': 15, 'to_location': 2, 'travel_time': 210},
        {'from_location': 16, 'to_location': 2, 'travel_time': 230},
    ]
    for data in connections_data:
        Connection.create(**data)
        # 逆方向の接続を作成
        Connection.create(
            from_location=data['to_location'],
            to_location=data['from_location'],
            travel_time=data['travel_time']
        )

def find_shortest_path(start_id, end_id):
    """ダイクストラ法で最短経路を見つける"""
    # 全ての接続を取得
    connections = Connection.select()
    
    # グラフの構築（接続IDも保持）
    graph = defaultdict(list)
    for conn in connections:
        graph[conn.from_location_id].append((conn.to_location_id, conn.travel_time, conn.connection_id))
    
    # 距離と経路の初期化
    distances = {loc.location_id: float('infinity') for loc in Location.select()}
    distances[start_id] = 0
    previous = {loc.location_id: None for loc in Location.select()}
    # 使用した接続を記録
    used_connections = {loc.location_id: None for loc in Location.select()}
    
    # プライオリティキューの初期化
    pq = [(0, start_id)]
    
    while pq:
        current_distance, current_vertex = heapq.heappop(pq)
        
        if current_distance > distances[current_vertex]:
            continue
            
        # 隣接ノードを探索
        for neighbor, weight, connection_id in graph[current_vertex]:
            distance = current_distance + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_vertex
                used_connections[neighbor] = connection_id
                heapq.heappush(pq, (distance, neighbor))
    
    if distances[end_id] == float('infinity'):
        return None, None
    
    # 接続IDの列を構築
    connection_path = []
    current = end_id
    while previous[current] is not None:
        connection_path.append(used_connections[current])
        current = previous[current]
    connection_path.reverse()
    
    return connection_path, distances[end_id]

def create_route(start_id, end_id, route_name=None):
    # 最短経路を計算してRouteテーブルに登録する
    connection_path, total_time = find_shortest_path(start_id, end_id)
    
    if connection_path is None:
        return None
        
    if route_name is None:
        start_location = Location.get_by_id(start_id)
        end_location = Location.get_by_id(end_id)
        route_name = f'{start_location.location_name}→{end_location.location_name}ルート'
    
    # 経路をコロン区切りの文字列に変換
    connection_ids = ':'.join(str(conn_id) for conn_id in connection_path)
    
    # ルートを作成して保存
    route = Route.create(
        route_name=route_name,
        start_location=start_id,
        end_location=end_id,
        connection_ids=connection_ids,
        total_time=total_time
    )
    
    return route

def initialize_routes():
    # 既存のデータを削除
    Route.delete().execute()
    
    # ルートを自動生成
    create_route(3, 1)
    create_route(4, 1)
    create_route(5, 1)
    create_route(6, 1)
    create_route(7, 1)
    create_route(8, 1)
    create_route(9, 1)
    create_route(10, 1)
    create_route(11, 1)
    create_route(12, 1)
    create_route(13, 1)
    create_route(14, 1)
    create_route(15, 1)
    create_route(16, 1)

# データベースの初期化関数
def initialize_database():
    db.connect()
    # テーブルが存在しない場合は作成
    db.create_tables(MODELS, safe=True)
    # 各テーブルのデータを初期化
    initialize_locations()
    initialize_connections()
    initialize_routes()
    db.close()
