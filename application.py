from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import db_function
import os
import sys
# import requests


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)


@app.route("/", methods=["GET"])
def index():
    """ Route function call to load login page
                     :param: none
                     :return: render login page
                     """
    try:
        return render_template("LoginPage.html", msg='')
    except Exception:
        print("Error occurred while loading login page.", sys.exc_info()[0])


@app.route("/home", methods=["POST", "GET"])
def home():
    """ Route function call to load login page after logout
                        :param: none
                        :return: render login page
                        """
    try:
        if request.method == "POST":
            data = request.form.to_dict(flat=False)
            db_function.delete_login_user(data['userid'][0])
            db_function.update_logout_time(data['userid'][0])
            onlineUser = db_function.get_online_users('Y')
            socketio.emit("announce status", {"onlineUser": onlineUser}, broadcast=True)
            db_function.close_connection()
            return render_template("LoginPage.html", msg='')
    except Exception:
        print("Error occurred during logout.", sys.exc_info()[0])


@app.route("/create_account", methods=["GET"])
def create_account():
    """ Route function call to load create account page
                        :param: none
                        :return: render new account page
                        """
    try:
        return render_template("CreateNewAccount.html", msg='')
    except Exception:
        print("Error occurred while loading create account page.", sys.exc_info()[0])


@app.route("/chat_page", methods=["POST"])
def chat_page():
    """ Route function call to load chat page
                        :param: none
                        :return: render main chat page
                        """
    try:
        if request.method == "POST":
            data = request.form.to_dict(flat=False)
            # print(data)
            if db_function.create_connection() is not None:
                user_details = db_function.get_login_details(data['userId'][0])
                if user_details[0][0] == data['password'][0]:
                    db_function.insert_online_status(data['userId'][0], user_details[0][1])
                    channel_list = db_function.get_channel_details(data['userId'][0])
                    other_channel_list = db_function.get_other_channel_details(data['userId'][0])
                    connected_members = db_function.get_connected_members(data['userId'][0])

                    notifications = db_function.get_notification_details(data['userId'][0], user_details[0][1])
                    # print(notifications)
                    return render_template("ChatRoomPage.html", name=user_details[0][1], isOnline="online",
                                           userid=data['userId'][0], channelList=channel_list, len=len(channel_list),
                                           otherChannelList=other_channel_list, members=connected_members,
                                           notifications=notifications)
                else:
                    return render_template("LoginPage.html", msg='Incorrect user ID or password.')
            else:
                print("Error! cannot create the database connection.")
    except Exception:
        print("Error occurred while loading chat page.", sys.exc_info()[0])


@app.route("/save_account", methods=["POST"])
def save_account():
    """ Route function call to load login page
                        :param: none
                        :return: render new account page after creating new account
                        """
    try:
        if request.method == "POST":
            data = request.form.to_dict(flat=False)
            # print(data)
            if db_function.create_connection() is not None:
                db_function.save_login_details(data)
            else:
                print("Error! cannot create the database connection.")
                return render_template("CreateNewAccount.html", msg="Database connection error.")
            return render_template("CreateNewAccount.html", msg="Account created successfully.")
    except Exception:
        print("Error occurred while saving new account.", sys.exc_info()[0])


@socketio.on("send message")
def vote(data):
    """ Socket function call to save message and  broadcast message
                        :param: none
                        :return: none
                        """
    try:
        selection = data["selection"]
        notification = data["notification"]
        lst_msg = data["selection"].split("|*|")
        # print(lst_msg)
        db_function.insert_chatbox_msg(lst_msg)
        emit("announce message", {"selection": selection, "notification": notification}, broadcast=True)
    except Exception:
        print("Error occurred while broadcasting message.", sys.exc_info()[0])


@socketio.on("submit status")
def status(data):
    """ Socket function call to save online users and broadcast online users
                        :param: none
                        :return: none
                        """
    try:
        onlineUser = db_function.get_online_users('Y')
        # print(onlineUser)
        emit("announce status", {"onlineUser": onlineUser}, broadcast=True)
    except Exception:
        print("Error occurred while broadcasting online users.", sys.exc_info()[0])


@socketio.on("submit channel")
def channel(data):
    """ Socket function call to save new channel and broadcast channels details
                        :param: none
                        :return: none
                        """
    try:
        lst_channel = data['channel'].split(":")
        # print(lst_channel)
        db_function.insert_channel(lst_channel)
        channel_list = db_function.get_channel_details(lst_channel[2])
        other_channel_list = db_function.get_other_channel_details(lst_channel[2])
        emit("announce channel",
             {"success": "Channel Added successfully", "channelList": channel_list,
              "otherChannelList": other_channel_list},
             broadcast=True)
    except Exception:
        print("Error occurred while broadcasting channel updates.", sys.exc_info()[0])


@socketio.on("submit channelName")
def channelName(data):
    """ Socket function call to get messages of specific channel and  broadcast messages
                        :param: none
                        :return: none
                        """
    try:
        channelUser = []
        channelMsg = []
        channelMsgUser = []
        date1 = []
        time1 = []

        channel_User = db_function.get_channel_users(data['channelName'])
        channel_msg = db_function.get_channel_msg(data['channelName'], data['chatMode'])

        if len(channel_msg) == 0:
            channel_name = data['channelName']
        else:
            channel_name = channel_msg[0][4]

        for x in channel_User:
            channelUser.append(x[0])

        for x in channel_msg:
            channelMsgUser.append(x[0])
            channelMsg.append(x[1])
            date1.append(x[2])
            time1.append(x[3])

        emit("announce channelUsers",
             {"channelUser": channelUser, "channelMsg": channelMsg, "channelMsgUser": channelMsgUser,
              "ChannelName": channel_name, "date": date1, "time": time1}, broadcast=True)
    except Exception:
        print("Error occurred while broadcasting channel specific message details.", sys.exc_info()[0])


@app.route("/chat_back", methods=["POST"])
def chat_back():
    """ Route function call to chat page after updating channels data
                        :param: none
                        :return: none
                        """
    try:
        if request.method == "POST":
            data = request.form.to_dict(flat=False)
            # print(data)
            db_function.insert_channel(data)
            channel_list = db_function.get_channel_details(data['userid'][0])
            other_channel_list = db_function.get_other_channel_details(data['userid'][0])
            connected_members = db_function.get_connected_members(data['userid'][0])
            return render_template("ChatRoomPage.html", name=data['name'][0], isOnline="online",
                                   userid=data['userid'][0], channelList=channel_list, len=len(channel_list),
                                   otherChannelList=other_channel_list, member=connected_members)
    except Exception:
        print("Error occurred while loading chat page again.", sys.exc_info()[0])


if __name__ == '__main__':
    try:
        app.run()
    except Exception:
        print("Error occurred while executing main.", sys.exc_info()[0])

