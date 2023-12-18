from celery_conf import app
from time import sleep
from app import socketio
import requests


def send_socket_event_from_celery(event_name, data=None, room=None):
    app_host = "http://localhost:5000"
    broadcast_path = f'{app_host}/broadcast'

    json_data = {
        'event_name': event_name,
        'data': data,
        'room': room,
    }

    requests.post(broadcast_path, json=json_data)


@app.task()
def test():
    print('Hello ! ')


@app.task
def delay_task(seconds, sid):
    print(sid)
    print(f"Sleep for {seconds} start")
    sleep(int(seconds))
    print("Task is completed.")
    send_socket_event_from_celery("completed", f"Task is completed in {seconds} seconds", sid)
    return sid
    
    
    # Informez le client via WebSocket que la tâche est terminée
    # socketio.emit('task_status', {'status': 'completed'}, room=client_sid, namespace='/test')
