# https://discord.gg/AE38RbwkmT space4life discord dont join

import flask
import os
import threading
import psutil
import dotenv

from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask, jsonify, render_template, send_from_directory
from dotenv import load_dotenv
from flask_restful import Api
from models import db
from resources.review import ReviewResource


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
        print("Scripts 1-3 are running!")

app = Flask(__name__)


app.config.from_object('config')
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)
db.init_app(app)


BASE_DIR = os.path.join(os.getcwd(), 'src', 'frontend')


@app.route('/status', methods=['GET'])
def status():
    # Get CPU usage
    cpu_usage = psutil.cpu_percent(interval=1)
    
    # Get memory usage
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent
    
    # Get disk usage
    disk_info = psutil.disk_usage('/')
    disk_usage = disk_info.percent
    
    # Prepare the status data
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

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/<path:filename>', methods=['GET'])
def serve_file(filename):
    return send_from_directory(BASE_DIR, filename)

if __name__ == '__main__':
    scripts = ['config.py', 'server.py']
    runner = ScriptRunner(scripts)
    runner.start_scripts()

    host = '0.0.0.0'
    port = 8000
    app.run(host=host, port=port, debug=True)
