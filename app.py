from flask import Flask, render_template
from models import initialize_database
from routes import blueprints

app = Flask(__name__)

# 各Blueprintをアプリケーションに登録
for blueprint in blueprints:
    app.register_blueprint(blueprint)


# ホームページのルート
@app.route('/')
def index():
    return "this is index"


if __name__ == '__main__':
    initialize_database()
    app.run(port=9999, debug=True)
