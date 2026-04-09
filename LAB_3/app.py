from flask import Flask, jsonify
import redis
import os

app = Flask(__name__)

redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'redis-service'),
    port=6379,
    decode_responses=True
)

@app.route('/')
def home():
    return jsonify({"message": "Python ML API is running!"})

@app.route('/counter')
def counter():
    count = redis_client.incr('request_counter')
    return jsonify({"counter": count, "service": "redis"})

@app.route('/health')
def health():
    try:
        redis_client.ping()
        return jsonify({"status": "healthy", "redis": "connected"})
    except:
        return jsonify({"status": "unhealthy", "redis": "disconnected"}), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)