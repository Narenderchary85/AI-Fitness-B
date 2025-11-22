import os
from flask import Flask, jsonify
from dotenv import load_dotenv
from flask_cors import CORS 
from flask_jwt_extended import JWTManager
from auth import auths
from plans import plans
from ai import init_ai_clients

load_dotenv()
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)


app.register_blueprint(auths, url_prefix='/auth')
app.register_blueprint(plans, url_prefix='/plan')

init_ai_clients(os.getenv('PPLX_API_KEY'), os.getenv('ELEVENLABS_API_KEY'), os.getenv('REPLICATE_API_KEY'))

@app.route('/')
def index():
    return jsonify({"ok": True, "message": "Fitness AI backend running"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
