from flask import Flask, Blueprint, jsonify,render_template, request, redirect, url_for
import subprocess

views = Blueprint(__name__, "views")

#@app.route('/run-script')
#def run_script():
#    result = subprocess.run(['python', 'python_script.py'], capture_output=True, text=True)
#    return jsonify({'output': result.stdout})

@views.route('/')
def home():
    items = ['Option 1', 'Option 2', 'Option 3', 'Option 4']
    return render_template('home.html', items=items)

#http://127.0.0.1:8080/profile/chandni
@views.route('/profile/<username>')
def profile(username):
    return f"Hi {username}"


#http://127.0.0.1:8080/profile2?username=Chandni
@views.route('/profile2')
def profile2():
    args = request.args
    username = args.get("username")
    return f"Hi {username}"

@views.route('/json')
def get_json():
    return jsonify({'name':'chandni', 'age':'30'})

@views.route('/go-to-home')
def go_to_home():
    return redirect(url_for("views.home"))