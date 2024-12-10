from flask import Flask, render_template,request
from flask_cors import CORS
import bson
from database.database import db
from models import Task


app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    active_section='view_task'
    show_task=Task.allTask()
    active_table = 'all_task'
    return render_template("index.html",active_section=active_section,show_task=show_task,active_table=active_table,**Task.common_context(),popup_notifications=True)


@app.route('/add_task')
def add_task():
    active_section='add_task' 
    return render_template("index.html",active_section=active_section,**Task.common_context())


@app.route('/view_task')
def view_task():
    active_section='view_task'
    show_task=Task.allTask()
    active_table = 'all_task'
    return render_template("index.html",active_section=active_section,show_task=show_task,active_table=active_table,**Task.common_context(),popup_notifications=True)


@app.route('/addTask',methods=['POST','GET'])
def addTask():
    if request.method == 'POST':
        result = request.form.to_dict()
        print("result-->",result)
        new_task=Task.createTask(result)
        show_task=Task.allTask()
        active_section='view_task'
        active_table = 'all_task' 
        return render_template("index.html",active_section=active_section,show_task=show_task,active_table=active_table,**Task.common_context())


@app.route('/all_task',methods=['POST','GET'])
def all_task():
    show_task=Task.allTask()
    print("all show_task-->",show_task)
    active_section='view_task'
    active_table = 'all_task'
    return render_template("index.html",active_section=active_section,show_task=show_task,active_table=active_table,**Task.common_context())


@app.route('/default_task',methods=['POST','GET'])
def default_task():
    show_task=Task.defaultTask()
    print("show_task",show_task)
    active_section='view_task'
    active_table = 'default_task' 
    return render_template("index.html",active_section=active_section,show_task=show_task,active_table=active_table,**Task.common_context())

@app.route('/personal_task',methods=['POST','GET'])
def personal_task():
    show_task=Task.personalTask()
    print("show_task",show_task)
    active_section='view_task'
    active_table = 'personal_task'
    return render_template("index.html",active_section=active_section,show_task=show_task,active_table=active_table,**Task.common_context())

@app.route('/shopping_task',methods=['POST','GET'])
def shopping_task():
    show_task=Task.shoppingTask()
    print("show_task",show_task)
    active_section='view_task'
    active_table = 'shopping_task'
    return render_template("index.html",active_section=active_section,show_task=show_task,active_table=active_table,**Task.common_context())

@app.route('/wishlist_task',methods=['POST','GET'])
def wishlist_task():
    show_task=Task.wishlistTask()
    print("show_task",show_task)
    active_section='view_task'
    active_table = 'wishlist_task'
    return render_template("index.html",active_section=active_section,show_task=show_task,active_table=active_table,**Task.common_context())

@app.route('/work_task',methods=['POST','GET'])
def work_task():
    show_task=Task.workTask()
    print("show_task",show_task)
    active_section='view_task'
    active_table = 'work_task' 
    return render_template("index.html",active_section=active_section,show_task=show_task,active_table=active_table,**Task.common_context())

@app.route('/deleteTask/<user_id>/<active_table>',methods=['POST','GET'])
def deleteTask(user_id,active_table):
    show_task=Task.delete_Task(user_id,active_table)
    active_section='view_task'
    return render_template("index.html",active_section=active_section,show_task=show_task,active_table=active_table,**Task.common_context())

@app.route('/updateTask/<user_id>/<active_table>',methods=['POST','GET'])
def updateTask(user_id,active_table):
    data=Task.fetch_data(user_id,active_table)
    print("data-->",data)
    fetch_data=data['fetch_data'][0]
    print("fetch_data-->",fetch_data)
    active_table=data['active_table']
    return render_template("updateTask.html",fetch_data=fetch_data,active_table=active_table)

@app.route('/new_Update_Task/<user_id>/<active_table>',methods=['POST','GET'])
def new_Update_Task(user_id,active_table):
    print("user_id-->",user_id)
    print("active_table-->",active_table)
    if request.method == 'POST':
        result = request.form.to_dict()
        update_item=db.task.update_one({"_id":  bson.ObjectId(user_id)}, { "$set" :
            {
                'inputTaskName': result.get("inputTaskName"),
                'inputTaskDescription': result.get("inputTaskDescription"),
                'inputDate': result.get("inputDate"),
                'inputTime': result.get("inputTime"),
                'inputCategory':result.get("inputCategory").split()[0]

            }
            }
        )
        default_tasks=db.task.find({'inputCategory':'Default'})
        default_task_arr=[{**task, "_id":str(task["_id"])} for task in default_tasks]
        print("main default_task_arr-->",default_task_arr)
        show_task=Task.activeTable(active_table)
        active_section='view_task'

    return render_template("index.html",active_section=active_section,show_task=show_task,active_table=active_table,**Task.common_context())


@app.route('/notification_task')
def notification_task():   
    active_section='notification_task'
    # print('notifications-->',notifications)
    return render_template("index.html",active_section=active_section,**Task.common_context())

@app.route('/deleteNotification/<user_id>',methods=['POST','GET'])
def deleteNotification(user_id):
    show_task=Task.delete_Notification(user_id)
    active_section='notification_task'
    
    return render_template("index.html",active_section=active_section,show_task=show_task,**Task.common_context())



if __name__ == '__main__':
    app.run(debug=True)