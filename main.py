from flask import Flask, session, render_template, redirect, request, send_from_directory, session
from json import dumps, load
from urllib import request as req

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = 'nobigdeal'
app.template_folder = 'templates'

apikey = '926760824190e0c5b4297c9645d6b6d8'

@app.route('/')
def homepage():
    info = False
    get = None
    if session.get('cityName'):
        session['cityName'] = session['cityName']
        info = {}
        lat = None
        lon = None
        with req.urlopen(f'http://api.openweathermap.org/geo/1.0/direct?q={session['cityName'].replace(' ','+')}&limit=1&appid={apikey}') as response:
            get = load(response)[0]
            info['country'] = get['country']
            lat = get['lat']
            lon = get['lon']
        with req.urlopen(f'https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={apikey}&units=metric') as response:
            get = load(response)['list'][0]
            main = get['main']
            aqi = main['aqi']
            info['aqi'] = aqi
            if aqi == 5:
                info['aqi_status'] = 'Very Poor!!'
            elif aqi == 4:
                info['aqi_status'] = 'Poor!'
            elif aqi == 3:
                info['aqi_status'] = 'Moderate'
            elif aqi == 2:
                info['aqi_status'] = 'Mild'
            elif aqi == 1:
                info['aqi_status'] = 'Clean'

        with req.urlopen(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={apikey}&units=metric') as response:
            get = load(response)
            main = get['main']
            info['temp'] = main['temp']
            info['pressure'] = main['pressure']
            info['humidity'] = main['humidity']
            info['wind_speed'] = get['wind']['speed']
    if info:
        return render_template('Home.html',cityName=session['cityName'],country=info['country'],aqi=info['aqi'],aqi_status=info['aqi_status'],temp=info['temp'],pressure=info['pressure'],humidity=info['humidity'],wind_speed=info['wind_speed'])
    else:
        return render_template('Home.html')

@app.route('/<path>')
def downloadfile(path):
    print(path)
    return send_from_directory('files', path)

@app.route('/action/sendmessage')
def actionsendmessage():
    name = request.args.get('Name')
    email = request.args.get('Email')
    message = request.args.get('Message')
    return name+email+message

@app.route('/action/search')
def actionsearch():
    keyword = request.args.get('keyword')
    session['cityName'] = keyword
    return redirect('/#app')

if __name__ == '__main__':
    app.run(debug=True)