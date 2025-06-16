import json
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


@app.route('/exercices')
def hello_world():
    return render_template('exercices.html')

if __name__ == "__main__":
    app.run(debug=True)
