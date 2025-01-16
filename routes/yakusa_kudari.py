from flask import Blueprint, jsonify, request
from datetime import datetime

# Blueprint の初期化
yakusa_to_kouzouzi_bp = Blueprint('yakusa_to_kouzouzi_', __name__)
# 八草の時刻データ
yakusa_to_kouzouzi_timetable = [
    "5:55", "6:23", "6:40", "6:56", "7:12", "7:28", "7:45",
    "8:01", "8:17", "8:33", "8:49", "9:05", "9:21", "9:37",
    "9:53", "10:09", "10:26", "10:48", "10:57", "11:20", "11:37",
    "11:53", "12:09", "12:25", "12:41", "12:57", "13:13", "13:29",
    "13:45", "14:01", "14:17", "14:33", "14:49", "15:05", "15:21",
    "15:37", "15:53", "16:09", "16:25", "16:41", "16:57", "17:13",
    "17:29", "17:45", "18:01", "18:17", "18:33", "18:49", "19:05",
    "19:21", "19:37", "19:53", "20:09", "20:25", "20:41", "20:57",
    "21:13", "21:29", "21:45", "22:01", "22:23", "22:39", "22:56",
    "23:21", "23:40",
]
# エンドポイント定義
@yakusa_to_kouzouzi_bp.route('/api/aikann/yakusa_to_kouzouzi', methods=['GET'])
def get_yakusa_to_kouzouzi_timetable():
    """
    APIエンドポイント: 八草の時刻表を取得
    """
    return jsonify(yakusa_to_kouzouzi_timetable)

@yakusa_to_kouzouzi_bp.route('/api/aikann/yakusa_to_kouzouzi/next', methods=['GET'])
def get_next_time():
    """
    APIエンドポイント: 現在時刻より後の八草の最も近い時刻を取得
    """
    time = request.args.get("time")
    train_time = datetime.strptime(time, "%H:%M")  # timeに現在時刻にバスの時間を足した値をいれたらギリギリ乗れる電車がわかるはず
    today = train_time.date()  # 今日の日付

    # 時刻表を datetime オブジェクトに変換
    timetable_datetime = [
        datetime.combine(today, datetime.strptime(time, "%H:%M").time())
        for time in yakusa_to_kouzouzi_timetable
    ]

    # 現在時刻より後の時刻をフィルタリング
    future_times = [t for t in timetable_datetime if t > train_time]

    # 未来の時刻がない場合はメッセージを返す
    if not future_times:
        return jsonify({"message": "No future times available today."})

    # 最も近い時刻を取得
    next_time = min(future_times, key=lambda t: t - train_time)
        
    # future_timesから次の時刻を削除
    future_times.remove(next_time)

    next_times = []

    # 次の3つの時刻を取得
    for i in range(3):
        if future_times:
            a = min(future_times, key=lambda t: t - train_time)
            next_times.append(a.strftime("%H:%M"))
            future_times.remove(a)

    # 結果をフォーマットして返す
    return jsonify({"next_time": next_time.strftime("%H:%M"), "next_times": next_times})