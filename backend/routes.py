from flask import Blueprint, request, jsonify
from models import User, Alert
from extensions import db,socketio,cache,jwt
from utils import get_stock_price,send_stock_data
from yahoo_fin import stock_info
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import redis
from config import Config

stock_blueprint = Blueprint('stock', __name__)
auth_blueprint = Blueprint('auth', __name__)
scheduler = BackgroundScheduler()
scheduler.start()

jwt_redis_blocklist = redis.StrictRedis(
    host=Config.JWT_BLOCKLIST_SERVER, port=6379, db=2, decode_responses=True
)

ACCESS_EXPIRY = timedelta(days=1)


@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400
    
    new_user = User(email=email, password=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()
    user = User.query.filter_by(email=email).first()
    access_token = create_access_token(identity=user.id,expires_delta=ACCESS_EXPIRY)
    return jsonify(access_token=access_token), 200
    

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password,password):
        return jsonify({"msg": "Invalid username or password"}), 401

    access_token = create_access_token(identity=user.id,expires_delta=ACCESS_EXPIRY)
    return jsonify(access_token=access_token), 200

@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None



@auth_blueprint.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRY)
    return jsonify(msg="Access token revoked")

    


@stock_blueprint.route('/alerts', methods=['POST','GET'])
@jwt_required()
def alerts():
    if request.method == "POST":
        data = request.get_json()
        user_id = get_jwt_identity()
        stock_symbol = data.get('stock_symbol')
        price_threshold = data.get('price_threshold')
        alert_type = data.get('alert_type')
        
        
        alert = Alert(
            stock_symbol=stock_symbol,
            price_threshold=price_threshold,
            alert_type=alert_type,
            user_id=user_id
        )
        
        db.session.add(alert)
        db.session.commit()
        
        return jsonify({"message": "Alert created successfully"}), 201
    else:
        user_id = get_jwt_identity()
        data = Alert.query.filter_by(user_id=user_id)
        res = []
        for alert in data:
            res.append({
                "price": alert.price_threshold,
                "type" : alert.alert_type,
                "id":alert.id,
                "stock_symbol":alert.stock_symbol,
                "enabled":alert.enabled
            })
        return jsonify(res), 200



@stock_blueprint.route('/alerts/<int:alert_id>', methods=['PUT'])
@jwt_required()
def enable_disable(alert_id):
    data = request.get_json()
    enabled = data.get("enabled")
    alert = Alert.query.get(alert_id)
    if not alert:
        return jsonify({"error": "Alert not found"}), 404
    alert.enabled = enabled
    db.session.commit()
    
    return jsonify({"message": "Alert updated successfully"}), 200



@stock_blueprint.route('/stock/<symbol>', methods=['GET'])
@jwt_required()
def get_stock_details(symbol):
    """
    Fetches the real-time stock price for the given symbol.
    :param symbol: Stock symbol
    :return: JSON with stock price or error message
    """
    price, market_open = get_stock_price(symbol)
    if price is not None:
        return jsonify(price_history=price,market_open=market_open), 200
    else:
        return jsonify({"error": "Unable to fetch stock data"}), 404

@stock_blueprint.route('/', methods=['GET'])
@jwt_required()
def homepage():
    """
    Fetches the stock symbols to be displayed on the homepage. Currerntly using
    two indices but we can add as many as available on a requirement basis
    """
    cached_data = cache.get("stocks_list")
    if cached_data:
        nifty50_tickers =  cached_data
    else:
        nifty50_tickers = stock_info.tickers_nifty50()
        cache.set("stocks_list",nifty50_tickers)
    return jsonify({"nifty50_tickers": nifty50_tickers}), 200


# Stock data fetching and broadcasting
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('subscribe_to_stock')
def handle_stock_subscription(data):
    stock_symbol = data['stock_symbol']
    job = scheduler.add_job(send_stock_data, 'interval', seconds=60, args=[stock_symbol])
    scheduler.resume()
    socketio.emit("successful_subscription",{"jobId":job.id})

@socketio.on('unsubscribe')
def handle_unsubscription(data):
    job_id = data['jobId']
    scheduler.remove_job(job_id)
    scheduler.pause()
