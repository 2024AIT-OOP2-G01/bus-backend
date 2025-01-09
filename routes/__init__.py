from .yakusa_kudari import yakusa_to_kouzouzi_bp
from .yakusa_nobori import yakusa_to_okazaki_bp
from .internal_route import in_route_bp
from .place import place_bp

# Blueprintをリストとしてまとめる
blueprints = [
    yakusa_to_kouzouzi_bp, yakusa_to_okazaki_bp, in_route_bp, place_bp
]
