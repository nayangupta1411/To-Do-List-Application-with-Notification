import bson
from database.database import db
import pandas as pd
from datetime import datetime


class Task:

    def __init__(self):
        return
    
    def common_context(**kwargs):
        notifications=Task.notificationTask()
        notification_count=len(notifications)
        base_context={
            'notifications':notifications,
            'notification_count':notification_count
        }
        base_context.update(kwargs)
        return base_context

    def createTask(new_task_dict):
        print("new_task_dict",new_task_dict)
        new_one=db.task.insert_one({
            'inputTaskName':new_task_dict['inputTaskName'],
            'inputTaskDescription': new_task_dict['inputTaskDescription'],
            'inputDate': new_task_dict['inputDate'],
            'inputTime': new_task_dict['inputTime'],
            'inputCategory': new_task_dict['inputCategory']
        })
        print(new_one)
        return new_one
    
    def allTask():
        show_tasks=db.task.find()
        task_arr=[{**task, "_id":str(task["_id"])} for task in show_tasks]
        return task_arr[::-1]
    
    def activeTable(active_table):
        task_arr=[]
        if active_table=='all_task':
            task_arr=Task.allTask()
        elif active_table=='default_task':
            task_arr=Task.defaultTask()
        elif active_table=='personal_task':
            task_arr=Task.personalTask()
        elif active_table=='shopping_task':
            task_arr=Task.shoppingTask()
        elif active_table=='wishlist_task':
            task_arr=Task.wishlistTask()
        elif active_table=='work_task':
            task_arr=Task.workTask()
        return task_arr
        

    def delete_Task(id,active_table):
        del_task=db.task.delete_one({"_id":bson.ObjectId(id)})
        task_arr=Task.activeTable(active_table)
        return task_arr
    
    def fetch_data(id,active_table):
        update_task=db.task.find({"_id":bson.ObjectId(id)})
        fetch_data=[{**task, "_id":str(task["_id"])} for task in update_task]
        return {'fetch_data':fetch_data,'active_table':active_table}

    
    def defaultTask():
        default_tasks=db.task.find({'inputCategory':'Default'})
        default_task_arr=[{**task, "_id":str(task["_id"])} for task in default_tasks]
        print("default_task_arr-->",default_task_arr)
        return default_task_arr
    
    def personalTask():
        personal_tasks=db.task.find({'inputCategory':'Personal'})
        personal_task_arr=[{**task, "_id":str(task["_id"])} for task in personal_tasks]
        print("personal_task_arr-->",personal_task_arr)
        return personal_task_arr
    
    def shoppingTask():
        shopping_tasks=db.task.find({'inputCategory':'Shopping'})
        shopping_task_arr=[{**task, "_id":str(task["_id"])} for task in shopping_tasks]
        print("shopping_task_arr-->",shopping_task_arr)
        return shopping_task_arr
    
    def wishlistTask():
        wishlist_tasks=db.task.find({'inputCategory':'Wishlist'})
        wishlist_task_arr=[{**task, "_id":str(task["_id"])} for task in wishlist_tasks]
        print("shopping_task_arr-->",wishlist_task_arr)
        return wishlist_task_arr
    
    def workTask():
        work_tasks=db.task.find({'inputCategory':'Work'})
        work_task_arr=[{**task, "_id":str(task["_id"])} for task in work_tasks]
        print("shopping_task_arr-->",work_task_arr)
        return work_task_arr
    
    def notificationTask():
        current_time=datetime.now()
        tasks=Task.allTask()
        notifications=[]
        notifications_upcoming=[]
        notification_overdue=[]
        for task in tasks:
            task_deadline=datetime.strptime(f"{task['inputDate']} {task['inputTime']}", "%Y-%m-%d %H:%M")
            if 0<(task_deadline-current_time).total_seconds()<=3600:
                task['deadline']="upcoming"
                notifications_upcoming.append(task)
            elif (task_deadline-current_time).total_seconds()<0:
                task['deadline']="overdue"
                notification_overdue.append(task)
        notifications=notifications_upcoming+notification_overdue
        # print('notifications-->',notifications)
        return notifications
    
    def delete_Notification(id):
        del_notification=db.task.delete_one({"_id":bson.ObjectId(id)})
        task_arr=Task.allTask()
        return task_arr