# from flask import Flask, session, render_template, redirect, request, send_from_directory
# from json import JSONEncoder, JSONDecoder, JSONDecodeError
# app = Flask(__name__)
# app.template_folder = 'temps'

# @app.route('/')
# def homepage():
    return render_template('HomePage.html')

# @app.route('/app')
# def apphome():
#     return redirect('app/eval')

# @app.route('/app/eval')
# def appeval():
    return render_template('eval.html')

# @app.route('/files/<path>')
# def downloadfile(path):
#     print(path)
#     return send_from_directory('files', path)

# if __name__ == '__main__':
#     app.run(debug=True)