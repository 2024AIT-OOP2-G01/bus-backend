<div id="top"></div>

## 使用技術一覧

<!-- シールド一覧 -->
<!-- 該当するプロジェクトの中から任意のものを選ぶ-->
<p style="display: inline">
  <!-- フロントエンドのフレームワーク一覧 -->
  <img src="https://img.shields.io/badge/-Node.js-000000.svg?logo=node.js&style=for-the-badge">
  <img src="https://img.shields.io/badge/-React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB">
  <!-- バックエンドの言語一覧 -->
  <img src="https://img.shields.io/badge/-Python-F2C63C.svg?logo=python&style=for-the-badge">
  <!-- バックエンドのフレームワーク一覧 -->
  <img src="https://img.shields.io/badge/-Flask-092E20.svg?logo=Flask&style=for-the-badge">
  <!-- ミドルウェア一覧 -->
  <img src="https://img.shields.io/badge/-SQlite-269539.svg?logo=SQlite&style=for-the-badge">
</p>

## 目次

1. [プロジェクトについて](#プロジェクトについて)
2. [環境](#環境)
3. [開発環境構築](#開発環境構築)

<br />
<div align="right">
    <a href="https://github.com/2024AIT-OOP2-G01/bus-frontend"><strong>フロントエンドのリポジトリ »</strong></a>
</div>
<br />
<div align="right">
    <a href="https://github.com/2024AIT-OOP2-G01/bus-backend"><strong>バックエンドのリポジトリ »</strong></a>
</div>
<br />
<div align="right">
    <a href="https://github.com/2024AIT-OOP2-G01/bus-timecalc/tree/main"><strong>計算関係のリポジトリ »</strong></a>
</div>
<br />

## プロジェクト名

[ギリ間に合うナビ](https://girimaniau.vercel.app/)

[プレゼンシート](https://www.canva.com/design/DAGcVM__sY0/gIzU1mzX6mKDp46_EtdA0A/view?utm_content=DAGcVM__sY0&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=ha8a2e16a01)

<!-- プロジェクトについて -->

## プロジェクトについて

**愛知工業大学と愛知環状鉄道をつなぐWebアプリケーション**

このアプリケーションは、愛知工業大学の学生が効率的に帰宅できるようサポートすることを目的としています。

**主な機能**

- ギリ表示機能：現在地であと何分間滞在できるかを表示します。

- 出発時間表示機能：直近の愛環列車およびシャトルバスの出発時間を表示します。

- 時刻表表示機能：愛環（高蔵寺行き・岡崎行き）の時刻表を確認できます。

**要件定義**

- 対象者: 愛知工業大学に通うすべての学生
- 利用シーン: 帰宅時間が不定期になった場合
- 使用環境: 主にスマートフォンでの利用を想定
- 設計の背景: 大学生は予定をギリギリまで調整する傾向があるため、それをサポートする直感的な設計を目指しました。

**計算方法**

ギリ表示機能における現在地であと何分間滞在できるかの計算方法は以下の通りです。

1. ユーザの現在地からバス停までにかかる時間を計算(Haversine公式を使用)
2. シャトルバスが出る時間までに間に合うか計算
3. 高蔵寺行きとか岡崎行きの電車に乗れるか計算

[詳細はこちらから »](https://github.com/2024AIT-OOP2-G01/bus-timecalc)

## 環境

| 言語・フレームワーク  | バージョン |
| --------------------- | ---------- |
| Python                | 3.10.12     |
| Flask                | 3.1.0      |
| Node.js               | 23.3.0    |
| React                 | 18.3.1     |

その他のパッケージのバージョンは [requirements.txt](https://github.com/2024AIT-OOP2-G01/bus-backend/blob/main/requirements.txt) と [package.json](https://github.com/2024AIT-OOP2-G01/bus-frontend/blob/main/package.json) を参照してください。

<p align="right">(<a href="#top">トップへ</a>)</p>

## 開発環境構築

<!-- コンテナの作成方法、パッケージのインストール方法など、開発環境構築に必要な情報を記載 -->

### リポジトリのダンロード

[フロントエンド »](https://github.com/2024AIT-OOP2-G01/bus-frontend)

[バックエンド »](https://github.com/2024AIT-OOP2-G01/bus-backend)

### フロントエンドのスタート

```cmd
npm i
npm run dev
```

### バックエンドのスタート

```cmd
pip install Flask==3.1.0 Flask-Cors==5.0.0 peewee==3.17.8 waitress==3.0.2
python app.py
```

必要に応じて仮想環境を使用してください。
