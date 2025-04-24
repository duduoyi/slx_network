from datetime import timedelta

from flask import Flask, session, g

# local imports
from dash_flask_keycloak import FlaskKeycloak

# Setup server.
server = Flask(__name__)

KEYCLOAK_HOST = 'https://keycloak.qiuchengtong.cn:8445'
CLIENT_ID = 'dash-cilent'
REALM_NAME = 'test'
CLIENT_SECRET_KEY = 'tg8HCo2mxWtBWR4Er0fxBHNjbbsOiCGl'
KEYCLOAK_PYTHON_CERT = False
APP_PORT = 8050

conf = dict(server_url=KEYCLOAK_HOST,
            client_id=CLIENT_ID,
            realm_name=REALM_NAME,
            client_secret_key=CLIENT_SECRET_KEY,
            verify=KEYCLOAK_PYTHON_CERT)

FlaskKeycloak.build(
    server,
    config_data=conf,
    redirect_uri=f"http://127.0.0.1:{APP_PORT}",
    session_lifetime=timedelta(hours=12)
)


@server.route("/keycloak/callback")
def root_route():
    user = session["user"]
    data = session["data"]
    return (f"<div>Hello {user} - calling from {g.external_url}</div>"
            f"<div>{data}</div>"
            f"<a href='/logout'><button>Logout</button></a>")


if __name__ == '__main__':
    server.run(port=APP_PORT)