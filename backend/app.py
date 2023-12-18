from flask import Flask, jsonify, make_response, request
from flask_socketio import SocketIO
from flask_cors import CORS
from celery import Celery
from time import sleep

app = Flask(__name__)
CORS(app, resources={r"/*": {"origin": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")

celery = Celery(
    app.name,
    broker='amqp://uac-rabbit:uac-rabbit@localhost:5672/rabbit_vhost',
    backend='rpc://'
)

# Dictionnaire pour stocker les identifiants de connexion associés aux tâches
task_clients = []


@app.route("/")
def index():
    return "welcome !"

@app.route("/launch_task/<seconds>/<sid>", methods=['POST'])
def launch_task(seconds, sid):
    # seconds = request.form.get('seconds')
    # client_sid = request.form.get('client_sid')
    print(seconds, sid)

    # Lancez la tâche asynchrone
    task = celery.send_task("tasks.tasks.delay_task", args=[seconds, sid])
    # Associez l'identifiant de connexion à la tâche dans le dictionnaire


    return make_response(jsonify({'msg': 'Task created', 'id': task.id}))


@socketio.on('connect')
def handle_connect():
    client_sid = request.sid
    print(f"Client connected with SID: {client_sid}")
        
    # Envoyez l'identifiant de session au client
    socketio.emit('client_sid', client_sid)
    task_clients.append(client_sid)


@app.route('/broadcast',methods = ['POST'])
def broadcast_to_client():
    json_data = request.get_json()
    event_name = json_data.get('event_name')
    room = json_data.get('room')
    data = json_data.get('data')

    status_code, emitted = 400,  False
    socketio.emit(event_name, data, room=room)
    status_code, emitted = 200, True

    return {'emitted': emitted}, status_code

if __name__ == '__main__':
    socketio.run(app, debug=True)
