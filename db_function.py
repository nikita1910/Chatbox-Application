import sqlite3
from sqlite3 import Error
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
database = os.path.join(THIS_FOLDER, 'chatBoxInfo.db')


def create_connection():
    """ create a database connection to the SQLite database
           specified by db_file
       :param db_file: database
       :return: Connection object or None
       """
    conn = None
    try:
        conn = sqlite3.connect(database)
    except Error as e:
        print(f"Database connection error:\t{e}")
    return conn


def close_connection():
    """ close a database connection to the SQLite database
             :param conn:
             """
    try:
        conn = create_connection()
        conn.close()
    except Error as e:
        print(f"Database close connection error:\t{e}")


def get_login_details(param):
    """ DB function call to get login details from database
                  :param: userid
                  :return: password and name
                  """
    try:
        conn = create_connection()
        c = conn.cursor()
        data = c.execute("SELECT login.password,login.name FROM login where login.userid = ?", (param,))
        conn.commit()
        return data.fetchall()
    except Error as e:
        print(f"Error occurred while executing get_login_details():\t{e}")


def save_login_details(user_data):
    """ DB function call to save user details in database
              :param: uername, password and name
              :return: none
              """
    try:
        conn = create_connection()
        c = conn.cursor()
        c.execute("INSERT INTO login(userid,password,name) VALUES(?,?,?)",
                  (user_data['userId'][0], user_data['password'][0], user_data['name'][0]))
        conn.commit()
    except Error as e:
        print(f"Insert SQL execution error save_login_details():\t{e}")


def delete_login_user(param):
    """ DB function call to delete online user entry from database
                      :param: userid
                      :return: none
                      """
    try:
        conn = create_connection()
        c = conn.cursor()
        c.execute("delete from status where userid =?",
                  (param,))
        conn.commit()
    except Error as e:
        print(f"delete SQL execution error:\t{e}")


def update_logout_time(param):
    """ DB function call to update logout details in database
                      :param: userid
                      :return: none
                      """
    try:
        conn = create_connection()
        c = conn.cursor()
        c.execute("update login set logoutTime = datetime('now', 'localtime') where userid =?",
                  (param,))
        conn.commit()
    except Error as e:
        print(f"Update SQL execution error update_logout_time():\t{e}")


def insert_online_status(param1, param2):
    """ DB function call to insert online user status details into database
                      :param: userid and name
                      :return: password and name
                      """
    try:
        conn = create_connection()
        c = conn.cursor()
        c.execute("INSERT INTO status(online,name,userid) VALUES(?,?,?)",
                  ('Y', param2, param1))
        conn.commit()
    except Error as e:
        print(f"Insert SQL execution error in insert_online_status() :\t{e}")


def get_channel_details(param):
    """ DB function call to get channel details from database
                      :param: userid
                      :return: channelname
                      """
    try:
        channel_list = []
        conn = create_connection()
        c = conn.cursor()
        data = c.execute("SELECT DISTINCT channelname FROM channel where userid = ?", (param,))

        for x in data.fetchall():
            channel_list.append(x[0])
        conn.commit()
        return channel_list
    except Error as e:
        print(f"Error occurred while executing get_channel_details():\t{e}")


def get_other_channel_details(param):
    """ DB function call to other get channel details from database
                      :param: userid
                      :return: channelname
                      """
    try:
        other_channel_list = []
        conn = create_connection()
        c = conn.cursor()
        data = c.execute("select DISTINCT channelname from channel where channelname NOT in (select channelname from "
                         "channel where userid = ?)", (param,))

        for x in data.fetchall():
            other_channel_list.append(x[0])
        conn.commit()
        return other_channel_list
    except Error as e:
        print(f"Error occurred while executing get_other_channel_details():\t{e}")


def get_connected_members(param):
    """ DB function call to get connected member details from database
                      :param: userid
                      :return: user
                      """
    try:
        connected_mem = []
        conn = create_connection()
        c = conn.cursor()
        data = c.execute("select DISTINCT user from channel where channelname in (select channelname from "
                         "channel where userid = ?)", (param,))

        for x in data.fetchall():
            connected_mem.append(x[0])
        conn.commit()
        return connected_mem
    except Error as e:
        print(f"Error occurred while executing get_other_channel_details():\t{e}")


def get_notification_details(param, param1):
    """ DB function call to get notification details from database
                      :param: userid
                      :return: message, name, channelname and chatmode
                      """
    try:
        notifications = []
        name_lst = param1.split(" ")
        conn = create_connection()
        c = conn.cursor()
        data = c.execute(
            "select msg,name,channelname,chatmode from chatboxmsg where (channelname in  (select channelname from "
            "channel "
            "where userid = ? ) "
            "or  channelname like ?)"
            "and datetime > (select logoutTime from login where userid = ?)", (param, '%' + name_lst[0] + '%', param))

        for x in data.fetchall():
            notifications.append(x)
        # print(notifications)
        conn.commit()
        return notifications
    except Error as e:
        print(f"Error occurred while executing get_notification_details():\t{e}")


def insert_chatbox_msg(lst_msg):
    """ DB function call to insert user message details into database
                      :param: name, message, channelname, date, time, chatmode and datetime
                      :return: none
                      """
    try:
        conn = create_connection()
        c = conn.cursor()
        c.execute("INSERT INTO chatboxmsg(name,msg,channelname,date,time,chatmode,datetime) VALUES(?,?,?,?,?,?,"
                  "datetime('now', "
                  "'localtime'))",
                  (lst_msg[0], lst_msg[1], lst_msg[2], lst_msg[3], lst_msg[4], lst_msg[5]))
        conn.commit()
    except Error as e:
        print(f"Insert SQL execution error insert_chatbox_msg():\t{e}")


def get_online_users(param):
    """ DB function call to get online users details from database
                      :param: online status
                      :return: user name
                      """
    try:
        onlineUser = []
        conn = create_connection()
        c = conn.cursor()
        data = c.execute("SELECT name FROM status where online = ?", (param,))
        for x in data:
            onlineUser.append(x[0])
        conn.commit()
        return onlineUser
    except Error as e:
        print(f"Error occurred while executing get_online_users():\t{e}")


def insert_channel(data):
    """ DB function call to insert channel details into database
                      :param: channelname, username and userid
                      :return: none
                      """
    try:
        conn = create_connection()
        c = conn.cursor()
        c.execute("INSERT INTO channel(channelname,user,userid) VALUES(?,?,?)",
                  (data['newChannel'][0], data['name'][0], data['userid'][0]))
        conn.commit()
    except Error as e:
        print(f"Error while inserting data insert_channel() :\t{e}")


def get_channel_users(param):
    """ DB function call to get channel users details from database
                      :param: channelname
                      :return: users
                      """
    try:
        conn = create_connection()
        c = conn.cursor()
        data = c.execute("SELECT user FROM channel where channelname = ?", (param,))
        conn.commit()
        return data.fetchall()
    except Error as e:
        print(f"Error occurred while executing get_channel_users():\t{e}")


def get_channel_msg(param, param1):
    """ DB function call to get channel message details from database
                      :param: channelname and chatmode
                      :return: name, message, date, time and channelname
                      """
    try:
        conn = create_connection()
        c = conn.cursor()
        if param1 == "G":
            data = c.execute("SELECT name,msg,date,time,channelname FROM chatboxmsg where channelname = ?",
                             (param,))
        else:
            param_list = param.split("-")

            data = c.execute("SELECT name,msg,date,time,channelname FROM chatboxmsg where channelname = ? or "
                             "channelname = ? ",
                             (param_list[0] + '-' + param_list[1], param_list[1] + '-' + param_list[0]))
        conn.commit()
        return data.fetchall()
    except Error as e:
        print(f"Error occurred while executing get_channel_msg():\t{e}")
