from flask import Flask, render_template
from flask_cors import CORS
from models import initialize_database
from routes import blueprints

app = Flask(__name__)
CORS(app)

# データベースの初期化
initialize_database()

# 各Blueprintをアプリケーションに登録
for blueprint in blueprints:
    app.register_blueprint(blueprint)


# ホームページのルート
@app.route('/')
def index():
    return "this is index"


if __name__ == '__main__':
    app.run(port=9999)
