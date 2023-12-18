# WEBSOCKET BROKER

*This project aim to use websocket in flask based backend.*
* The react frontend will send http request to a specific endpoint to launch a task.
* The task (registered in Rabbitmq broker based on Celery python package) is sent
* The __HTTP__ request is immediatly sent to client, tell the task is started.
* in the task progress, websocket send message to client to tell him if it's finish or not.


The client is registered on websocket backend and can also send http request. 
---

### In order to send task request, client will specify his websocket connexion sid for instant response.

In the backent, we'll store connected user
