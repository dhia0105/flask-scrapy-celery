from flask import Flask, request, jsonify, render_template
from tasks import create_task
import json
from scrapy.crawler import CrawlerRunner


app = Flask(__name__)


@app.route('/start', methods=['GET'])
def render_start_page():
    if (request.method != "GET"):
        return "<p>Method is not allowed.</p>"
    return render_template('index.html')

@app.route('/movies', methods=['POST'])
def launch_task():
    #gets genre variable from the browser and creates a task for the celery worker with this variable
    if (request.method != "POST"):
        return "<p>Method is not allowed.</p>"
    data = request.data
    body =  json.loads(data.decode('utf-8'))
    genre = body["genre"]
    #creates a task to the celery worker 
    task = create_task.delay(genre)
    return jsonify({"success": True}), 202


if __name__ == "__main__" :
    app.run(debug=True, host='0.0.0.0', port=8000)
