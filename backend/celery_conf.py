from __future__ import absolute_import
from celery import Celery

app = Celery('worker',
             broker='amqp://uac-rabbit:uac-rabbit@localhost/rabbit_vhost',
             backend="rpc:///",
             str="python-worker",
             include=['tasks.tasks' ]
             )

