import os
import threading
import psutil
from flask import Flask, jsonify, render_template, request, send_from_directory, abort
from flask_restful import Api, Resource
from werkzeug.middleware.proxy_fix import ProxyFix
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


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

# Serve all files from the templates directory
@app.route('/<path:filename>', methods=['GET'])
def serve_file(filename):
    # Ensure the requested file is within the templates directory
    templates_dir = os.path.join(app.root_path, 'templates')
    return send_from_directory(templates_dir, filename)

# Home Route
@app.route('/')
def home():
    return render_template('index.html')  # Flask will look for index.html in the templates directory

# Script Runner Class


# Main Execution
if __name__ == '__main__':
    host = '0.0.0.0'
    port = 8000
    app.run(host=host, port=port, debug=True)