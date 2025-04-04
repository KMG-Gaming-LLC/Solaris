import os
import threading
import psutil
from flask import Flask, jsonify, render_template, send_from_directory, request
from flask_restful import Api, Resource
from werkzeug.middleware.proxy_fix import ProxyFix
from dotenv import load_dotenv
from models import db, Review


# Review Resource Class
class ReviewResource(Resource):
    def get(self):
        reviews = Review.query.all()
        return [{'id': r.id, 'game_title': r.game_title, 'review_text': r.review_text, 'rating': r.rating} for r in reviews], 200

    def post(self):
        json_data = request.get_json(force=True)
        new_review = Review(game_title=json_data['game_title'], review_text=json_data['review_text'], rating=json_data['rating'])
        db.session.add(new_review)
        db.session.commit()
        return {'message': 'Review created', 'id': new_review.id}, 201

    def put(self, review_id):
        json_data = request.get_json(force=True)
        review = Review.query.get(review_id)
        if not review:
            return {'message': 'Review not found'}, 404
        review.game_title = json_data['game_title']
        review.review_text = json_data['review_text']
        review.rating = json_data['rating']
        db.session.commit()
        return {'message': 'Review updated'}, 200

    def delete(self, review_id):
        review = Review.query.get(review_id)
        if not review:
            return {'message': 'Review not found'}, 404
        db.session.delete(review)
        db.session.commit()
        return {'message': 'Review deleted'}, 204


# Flask Application Setup
app = Flask(__name__)
app.config.from_object('config')
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)
db.init_app(app)

# API Setup
api = Api(app)
api.add_resource(ReviewResource, '/reviews', '/reviews/<int:review_id>')


# Status Route
@app.route('/status', methods=['GET'])
def status():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent
    disk_info = psutil.disk_usage('/')
    disk_usage = disk_info.percent

    status_data = {
        'cpu_usage': cpu_usage,
        'memory_usage': memory_usage,
        'disk_usage': disk_usage,
        'total_memory': memory_info.total,
        'available_memory': memory_info.available,
        'total_disk': disk_info.total,
        'available_disk': disk_info.free
    }

    return jsonify(status_data)

# Home Route
@app.route('/')
def home():
    return render_template('index.html')


# Serve Static Files
BASE_DIR = os.path.join(os.getcwd(), 'src', 'frontend')
@app.route('/<path:filename>', methods=['GET'])
def serve_file(filename):
    return send_from_directory(BASE_DIR, filename)


# Script Runner Class
class ScriptRunner:
    def __init__(self, scripts):
        self.scripts = scripts
        self.threads = []

    def run_script(self, script):
        exec(open(script).read())

    def start_scripts(self):
        for script in self.scripts:
            thread = threading.Thread(target=self.run_script, args=(script,))
            thread.start()
            self.threads.append(thread)
        print("Scripts are running!")


# Main Execution
if __name__ == '__main__':
    scripts = ['config.py', 'server.py']
    runner = ScriptRunner(scripts)
    runner.start_scripts()

    host = '0.0.0.0'
    port = 8000
    app.run(host=host, port=port, debug=True)