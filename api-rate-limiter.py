from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import redis
import logging
from time import time

REDIS_URL = "redis://localhost:6379/0"
RATE_LIMIT_WINDOW = 60
RATE_LIMIT_REQUESTS = 5

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret'

jwt = JWTManager(app)

redis_client = redis.StrictRedis.from_url(REDIS_URL)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def rate_limited(user_id):
    key = f"rate_limit:{user_id}"
    current_time = time()

    redis_client.zremrangebyscore(key, 0, current_time - RATE_LIMIT_WINDOW)

    request_count = redis_client.zcard(key)
    if request_count >= RATE_LIMIT_REQUESTS:
        return False

    redis_client.zadd(key, {current_time: current_time})
    redis_client.expire(key, RATE_LIMIT_WINDOW)
    return True

@app.route('/api/token', methods=['POST'])
def get_token():
    username = request.json.get('username')
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

@app.route('/api/resource', methods=['GET'])
@jwt_required()
def get_resource():
    user_id = request.jwt['sub']

    if not rate_limited(user_id):
        logging.warning(f'Rate limit exceeded for user: {user_id}')
        return jsonify({'error': 'Rate limit exceeded'}), 429

    logging.info(f'Resource accessed by user: {user_id}')
    return jsonify({'data': 'This is your resource!'})

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(Exception)
def handle_exception(e):
    logging.error(f'Unhandled Exception: {str(e)}')
    return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
