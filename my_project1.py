import sqlite3
from datetime import datetime, timedelta
from discordwebhook import Discordwebhook, Discord
from flask import request, Flask, jsonify, render_template,redirect

app = Flask(__name__)

def get_conn():
    conn = sqlite3.connect('project_db.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS messages_1 ( id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    print("the message saved !")
    conn.commit()
    return conn

def send_to_discord(text):
    discord = Discord(
        url="https://discordapp.com/api/webhooks/1339220882068869240/3oBkTRq2sN6VUDlpqrCLmSDgNEgWei0W9KfyiINd8eUCmXzvOkMFf9XuTMwlS5vzQfpp")
    discord.post(content=text)
    return

def save_to_database(text):
    conn = get_conn()
    cursor = conn.cursor()
    timestamp = datetime.now()
    cursor.execute('INSERT INTO messages_1 (content, timestamp) VALUES (?, ?)', (text, timestamp))
    conn.commit()
    print("Saved message:", text, "at", timestamp)


@app.route('/input_text', methods =['POST'])
def add_text():
        text = request.form.get('text')
        send_to_discord(text)

        save_to_database(text)
        return redirect('/')


@app.route('/get_messages', methods = ['GET'])
def get_messages():
    try:
        cutoff_time= datetime.now() - timedelta(minutes=30)
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute('SELECT content, timestamp FROM messages_1')
        messages = cursor.fetchall()
        conn.close()
        print("messages:", messages)
        formatted_messages = [{"content": msg[0], "timestamp": msg[1]} for msg in messages]

        return jsonify({"status": "success", "messages": formatted_messages})
    except:
        return jsonify({"status:error"})


@app.route('/')
def index():
    conn = get_conn()
    cursor = conn.cursor
    return render_template('templates.html')

if __name__=="__main__":
    get_conn()
    app.run(debug=True)






# def get_conn():
#     conn = sqlite3.connect('project_db.db')
#     cursor = conn.cursor()
#     cursor.execute('''CREATE TABLE IF NOT EXISTS messages_1 ( id INTEGER PRIMARY KEY AUTOINCREMENT,
#     content TEXT,
#     timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
#     )
#     ''')
#     print("the message saved !")
#     conn.commit()
#     return conn
# #     discord_webhook_url = Discord( url= "https://discordapp.com/api/webhooks/1339220882068869240/3oBkTRq2sN6VUDlpqrCLmSDgNEgWei0W9KfyiINd8eUCmXzvOkMFf9XuTMwlS5vzQfpp")
# #     discord_webhook_url.post(content = "hello, project !")
# # discord_webhook_url = "https://discordapp.com/api/webhooks/1339220882068869240/3oBkTRq2sN6VUDlpqrCLmSDgNEgWei0W9KfyiINd8eUCmXzvOkMFf9XuTMwlS5vzQfpp"
#
# def send_to_discord(text):
#     discord = Discord(
#         url="https://discordapp.com/api/webhooks/1339220882068869240/3oBkTRq2sN6VUDlpqrCLmSDgNEgWei0W9KfyiINd8eUCmXzvOkMFf9XuTMwlS5vzQfpp")
#     discord.post(content=text)
#     return
#
# def save_to_database(text):
#     conn = get_conn()
#     cursor = conn.cursor()
#     timestamp = datetime.now()
#     cursor.execute('INSERT INTO messages_1 (content, timestamp) VALUES (?, ?)', (text, timestamp))
#     conn.commit()
#     print("Saved message:", text, "at", timestamp)
#     # conn.close()
#
#
# @app.route('/input_text', methods =['POST'])
# def add_text():
#     # try:
#         data = request.get_json()
#         text = data['text']
#         # send_to_discord(text)
#         send_to_discord(text)
#         # if discord_response.status_code != 204:
#         #     return jsonify({"status": "error", "message": "Failed to send to Discord"})
#
#         save_to_database(text)
#         return "ok"
#         # return jsonify({"status":"success"})
#     # except Exception as e :
#     #     return jsonify({"status":"error", "massage": "400"})
# # app.run(debug= True)
#
#
# @app.route('/get_messages', methods = ['get'])
# def get_messages():
#     try:
#         cutoff_time= datetime.now() - timedelta(minutes=30)
#         conn = get_conn()
#         cursor = conn.cursor()
#         cursor.execute('SELECT content, timestamp FROM messages_1')
#         messages = cursor.fetchall()
#         conn.close()
#         print("messages:", messages)
#         return jsonify({"status": "success", "messages": [{"content": row['content'],
#         "timestamp": row['timestamp']} for row in messages]})
#     except:
#         return jsonify({"status:error"})
# @app.route('/')
# def index():
#     conn = get_conn()
#     cursor = conn.cursor
#     return render_template('templates.html')
# if __name__=="__main__":
#     get_conn()
#     app.run(debug=True)
