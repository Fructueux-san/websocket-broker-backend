from celery_conf import app
from time import sleep
from app import socketio


@app.task()
def test():
    print('Hello ! ')


@app.task
def delay_task(seconds, sid):
    print(sid)
    print(f"Sleep for {seconds} start")
    sleep(int(seconds))
    print("Task is completed.")
    socketio.emit('completed', "task is complete", room=sid, to=sid)
    
    
    # Informez le client via WebSocket que la tâche est terminée
    # socketio.emit('task_status', {'status': 'completed'}, room=client_sid, namespace='/test')
