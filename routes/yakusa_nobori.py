from flask import Blueprint, jsonify   
from datetime import datetime
# Blueprint の初期化
yakusa_to_okazaki_bp = Blueprint('yakusa_to_okazaki', __name__)
# 八草の時刻データ
yakusa_to_okazaki_timetable = [
    "6:16", "6:31", "6:48", "7:04", "7:21", "7:37", "7:53",
    "8:09", "8:25", "8:41", "8:57", "9:13", "9:29", "9:45",
    "10:01", "10:18", "10:34", "10:56", "11:13", "11:29", "11:45",
    "12:01", "12:17", "12:33", "12:49", "13:05", "13:21", "13:37",
    "13:53", "14:09", "14:25", "14:41", "14:57", "15:13", "15:29",
    "15:45", "16:01", "16:17", "16:33", "16:49", "17:05", "17:21",
    "17:37", "17:53", "18:09", "18:25", "18:41", "18:57", "19:13",
    "19:29", "19:45", "20:01", "20:17", "20:32", "20:49", "21:05",
    "21:21", "21:37", "21:53", "22:08", "22:30", "22:55", "23:12",
    "23:38", "23:55",
]
# エンドポイント定義
@yakusa_to_okazaki_bp.route('/api/aikann/yakusa_to_okazaki', methods=['GET'])
def get_yakusa_to_okazaki_timetable():
    """
    APIエンドポイント: 八草の時刻表を取得
    """
    return jsonify(yakusa_to_okazaki_timetable)
# 最も近いエンドポイント定義(現在時刻よりも未来)
@yakusa_to_okazaki_bp.route('/api/aikann/yakusa_to_okazaki/next', methods=['GET'])
def get_next_time():
    """
    APIエンドポイント:最も近い時刻を取得
    """
    train_time = datetime.strptime("time", "%H:%M") # timeに現在時刻にバスの時間を足した値をいれたらギリギリ乗れる電車がわかるはず
    today = train_time.date()  # 今日の日付

    # 時刻表を datetime オブジェクトに変換
    timetable_datetime = [
        datetime.combine(today, datetime.strptime(time, "%H:%M").time())
        for time in yakusa_to_okazaki_timetable
    ]

    # 現在時刻より後の時刻をフィルタリング
    future_times = [t for t in timetable_datetime if t > train_time]

    # 未来の時刻がない場合はメッセージを返す
    if not future_times:
        return jsonify({"message": "No future times available today."})

    # 最も近い時刻を取得
    next_time = min(future_times, key=lambda t: t - train_time)

    # 結果をフォーマットして返す
    return jsonify({"next_time": next_time.strftime("%H:%M")})