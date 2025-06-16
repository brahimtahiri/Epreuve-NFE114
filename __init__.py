import json
from collections import Counter
from datetime import datetime
from urllib.request import urlopen

from flask import Flask, render_template, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/tawarano')
def tawarano():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')

    raw_content = response.read()

    json_content = json.loads(raw_content.decode('utf-8'))

    results = []

    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15
        results.append({'Jour': dt_value, 'temp': temp_day_value})

    return jsonify(results=results)


@app.route('/rapport')
def rapport():
    return render_template('graphique.html')


@app.route('/histogramme')
def histogramme():
    return render_template('histogramme.html')

@app.route('/commits/')
def commits():
    return render_template("commits.html")

@app.route('/commits/data/')
def commits_data():
    response = urlopen('https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))

    minutes_list = []
    for commit in json_content:
        date_str = commit.get('commit', {}).get('author', {}).get('date')
        date_object = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
        minutes_list.append(date_object.minute)

    counter = Counter(minutes_list)
    results = [{'minute': minute, 'count': count} for minute, count in sorted(counter.items())]

    return jsonify(results=results)

if __name__ == "__main__":
    app.run(debug=True)
