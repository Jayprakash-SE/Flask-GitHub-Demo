from flask import Flask, redirect, request, session, url_for
import requests

# Create Flask App
app = Flask(__name__)
app.config["SECRET_KEY"] = 'AnyStrongKey'

"""
Get ID and Secret from https://github.com/settings/developers by create a OAuth App
Remember Authorization callback URL will be http://127.0.0.1:5000/login/callback
"""
CLIENT_ID = '58b18c8354179858acdb'
CLIENT_SECRET = '94e0514527650cd1c454341b55924ab47519c831'

# Fixed Variables. Don't need to change it
AUTHORIZE_URL = 'https://github.com/login/oauth/authorize?client_id=' + CLIENT_ID
ACCESS_TOKEN_URL = 'https://github.com/login/oauth/access_token'

@app.route('/')
def index():
    # Link for redirect app authorization
    return '<a href="'+ AUTHORIZE_URL +'">Login with GitHub</a>'

# It will handle callback from GitHub
@app.route('/login/callback')
def loginCallback():
    # Store code paramenter value from request arguments
    res_code = request.args["code"]

    if res_code == '' or res_code == None:
        return " Error :( "

    # Required parameter to make POST request for access token
    data_param = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": res_code,
    }

    # Header to take response in JSON Format
    header = {
        "Accept": "application/json"
    }

    # Making POST request for access token
    res = requests.post(
        url = ACCESS_TOKEN_URL, 
        data = data_param, 
        headers = header
    )

    # Store access token in Session
    session["access_token"] = res.json()["access_token"]

    # Redirect to http://127.0.0.1:5000/user
    return redirect( url_for('user') )

@app.route('/user')
def user():
    # Specifing header to include access token in request
    header = {
        "Authorization": "token " + session["access_token"]
    }

    # Request with token to get User Data
    res = requests.get("https://api.github.com/user", headers=header)
    user_data = res.json()

    # You can extract data from dict like user_data["email"]
    return user_data

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)