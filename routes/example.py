from flask import Blueprint, jsonify, render_template
from models import Example
from datetime import datetime

# Blueprintの作成
example_bp = Blueprint('example', __name__, url_prefix='/example')


@example_bp.route('/')
def list():
    return jsonify({"message": "this is example"})


@example_bp.route('/hello', methods=['GET'])
def get():
    data = Example.select()

    return jsonify(data)
