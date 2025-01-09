# 今やっていること
- データベースの設計
	- ノードとコネクションとルートのテーブルを用意して、ノード(場所)、コネクション(ノード同士の接続)、ルート(バス停までのコネクションの集まり)で表現して、スタート地点からバス停までの時間を計算する形。基本ルートが1択なのでリアルタイムの最短経路探索はやらないことにした
	- とりあえず1号館周りから2号館あたりまでで登録済み
	- 拡張やルート探索の自動化はあとからやればできるように設計したつもり
    - データ登録の段階でダイクストラ法を使った
- データベースの設計に基づく実装
	- 現在地のID(dbのノード)をクエリで渡すとバス停までの時間をJSONで返すエンドポイントの実装。ルートのデータベースから通るコネクションを参照して時間を合計して返すだけ。