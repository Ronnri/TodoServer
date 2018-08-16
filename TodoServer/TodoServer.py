import pymysql
import time, datetime
from flask import Flask, request, render_template, jsonify
import json

app = Flask(__name__)

db = pymysql.connect("localhost", "root", "xxllyy123", "wechatTodo", charset='utf8')  # 打开数据库连接
cursor = db.cursor()  # 使用cursor()方法获取操作游标

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/signin', methods=['GET'])
def signin_form():
    return render_template('form.html')


@app.route('/addInfor', methods=['POST'])
def addInfor():#此接口僅供add
    recData = json.loads(request.data)
    try:
        if recData['usr'] and recData['title'] and recData['event_time'] is not None:  # 不爲空
            SQLCMD =(recData['usr'],recData['title'],recData['event_time']) #執行檢索，是否已有該記錄
            print(SQLCMD)
            cursor.execute("SELECT * FROM usrinfor where usr = %s AND title = %s AND event_time = %s",SQLCMD)
            db.commit()# 提交到数据库执行
            data = cursor.fetchall()
            if len(data) != 0:
                return "設置失敗！此紀錄已存在！\n"
            create_time = update_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
            SQLCMD=(recData['usr'],recData['title'],recData['content'],recData['backimg'],recData['repeat_type'],create_time,update_time,recData['event_time'])
            print(SQLCMD)
            cursor.execute("INSERT INTO usrinfor VALUES (%s,%s,%s,%s,%s,%s,%s,%s)" ,SQLCMD)
            db.commit()
            print(cursor.fetchall())
        else:
            return "usr title event_time字段不允許爲空\n"
    except (IOError, ZeroDivisionError) as e:
        print(e)
        db.rollback()# 发生错误时回滚
    else:
        return "written\n"



@app.route('/getInfor', methods=['GET'])
def getInforget():#此接口僅供query
    jsonData = {
        'param1': 1,
        'param2': 2,
        'param3': 3,
        'param4': "i have got your get"
    }
    return jsonify(jsonData)

@app.route('/getInfor', methods=['POST'])
def getInfor():#此接口僅供query
    recData = json.loads(request.data)
    try:
        if recData['usr']  is not None:  # 不爲空
            SQLCMD = (recData['usr'])  # 執行檢索，是否有該用戶的記錄
            print(SQLCMD)
            cursor.execute("SELECT * FROM usrinfor where usr = %s", SQLCMD)
            db.commit()# 提交到数据库执行
            data = cursor.fetchall()
            if len(data) == 0:
                return "查詢失敗！該用戶暫無數據！\n"
            print(data)
        else:
            return "usr title event_time字段不允許爲空\n"
    except (IOError, ZeroDivisionError) as e:
        print(e)
        # 发生错误时回滚
        db.rollback()
    else:
        return jsonify(data)



@app.route('/signin', methods=['POST'])
def signin():
    username = request.form['username']
    password = request.form['password']
    if username == 'admin' and password == '1234':
        return render_template('signin-ok.html', username=username)
    return render_template('form.html', message='Bad username or password', username=username)


if __name__ == '__main__':
    app.run("127.0.0.1", port=8080)
