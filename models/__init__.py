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
        {'location_name': 'バス停', 'latitude': 35.18233580606756, 'longitude': 137.1099265887362},  #1
        {'location_name': '共通P', 'latitude': 35.18364017243178, 'longitude': 137.11090827724146},  #2
        {'location_name': '1号館', 'latitude': 35.18390542756324, 'longitude': 137.11124355336062},  #3
        {'location_name': '10号館', 'latitude': 35.184186027090554, 'longitude': 137.11097265025634},  #4
        {'location_name': '14号館', 'latitude': 35.18444755306055, 'longitude': 137.11130383998838},  #5
        {'location_name': '10号館大講義室棟', 'latitude': 35.18454395645997, 'longitude': 137.11164231490918},  #6
        {'location_name': '旧1号館', 'latitude': 35.18476191155015, 'longitude': 137.11151282260994},  #7
        {'location_name': '9号館', 'latitude': 35.18467577053099, 'longitude': 137.11248810598033},  #8
        {'location_name': '7号館', 'latitude': 35.18355242335979, 'longitude': 137.11183651330035},  #9
        {'location_name': '第1本部棟', 'latitude': 35.18358570794326, 'longitude': 137.11242192860885},  #10
        {'location_name': '第2本部棟', 'latitude': 35.18425971783185, 'longitude': 137.1123532059479},  #11
        {'location_name': 'AITプラザ', 'latitude': 35.184278440253266, 'longitude': 137.1118212416126},  #12
        {'location_name': '愛和会館', 'latitude': 35.18413282133835, 'longitude': 137.11294880241238},  #13
        {'location_name': '土木・建築実験棟', 'latitude': 35.18364811650855, 'longitude': 137.11285717219016},  #14
        {'location_name': '図書館', 'latitude': 35.183760451790825, 'longitude': 137.1134349516468},  #15
        {'location_name': '12号館', 'latitude': 35.18377085319801, 'longitude': 137.11344258749864},  #16
        {'location_name': '2号館', 'latitude': 35.18382702077372, 'longitude': 137.11411963302933},  #17
    ]
    
    # データベースを再作成
    db.drop_tables([Location])
    db.create_tables([Location])
    
    for data in locations_data:
        Location.create(**data)

def initialize_connections():
    # 既存のデータを削除
    Connection.delete().execute()
    
    connections_data = [
        # バス停 ←→ 共通P
        {'from_location': 1, 'to_location': 2, 'travel_time': 130},

        # 共通P ←→ 1号館
        {'from_location': 2, 'to_location': 3, 'travel_time': 30},
        
        # 1号館 ←→ 10号館
        {'from_location': 3, 'to_location': 4, 'travel_time': 20},
        
        # 10号館 ←→ 14号館
        {'from_location': 4, 'to_location': 5, 'travel_time': 20},

        # 10号館大講義室棟 ←→ 10号館
        {'from_location': 6, 'to_location': 4, 'travel_time': 20},

        # 旧1号館 ←→ 1号館
        {'from_location': 7, 'to_location': 3, 'travel_time': 60},
        
        # 9号館 ←→ 旧1号館
        {'from_location': 8, 'to_location': 7, 'travel_time': 20},

        # 7号館 ←→ 1号館
        {'from_location': 9, 'to_location': 3, 'travel_time': 140},

        # 第1本部棟 ←→ 共通P
        {'from_location': 10, 'to_location': 2, 'travel_time': 60},
        
        # 第2本部棟 ←→ 共通P
        {'from_location': 11, 'to_location': 2, 'travel_time': 80},
        
        # 土木・建築実験棟 ←→ 共通P
        {'from_location': 14, 'to_location': 2, 'travel_time': 140},

        # AITプラザ ←→ 共通P
        {'from_location': 12, 'to_location': 2, 'travel_time': 60},
        
        # 愛和会館 ←→ 共通P
        {'from_location': 13, 'to_location': 2, 'travel_time': 80},

        # 図書館 ←→ 共通P
        {'from_location': 15, 'to_location': 2, 'travel_time': 120},
        
        # 12号館 ←→ 共通P
        {'from_location': 16, 'to_location': 2, 'travel_time': 160},

        # 2号館 ←→ 共通P
        {'from_location': 17, 'to_location': 2, 'travel_time': 180},
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
    create_route(17, 1)

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
