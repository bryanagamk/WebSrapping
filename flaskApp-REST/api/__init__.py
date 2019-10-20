from flask_restful import Api
from app import flaskAppInstance
from .TaskAPI import Task
from .TaskByIDAPI import TaskByID
from db_config import mysql


restServerInstance = Api(flaskAppInstance)

restServerInstance.add_resource(Task,"/api/task")
restServerInstance.add_resource(TaskByID,"/api/task/<string:taskId>")