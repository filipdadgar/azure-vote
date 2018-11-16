from flask import Flask, request, render_template
from flaskext.mysql import MySQL
import os
import random
import socket
import sys

app = Flask(__name__)

# Load configurations
app.config.from_pyfile('config_file.cfg')
button1 =       app.config['VOTE1VALUE']  
button2 =       app.config['VOTE2VALUE']
button3 =       app.config['VOTE3VALUE']
button4 =       app.config['VOTE4VALUE']
button5 =       app.config['VOTE5VALUE']
title =         app.config['TITLE']

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = os.environ['MYSQL_USER'] 
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ['MYSQL_PASSWORD']
app.config['MYSQL_DATABASE_DB'] = os.environ['MYSQL_DATABASE']
app.config['MYSQL_DATABASE_HOST'] = os.environ['MYSQL_HOST']

# MySQL Object
mysql = MySQL()
mysql.init_app(app)

# Change title to host name to demo NLB
if app.config['SHOWHOST'] == "true":
    title = socket.gethostname()

@app.route('/', methods=['GET', 'POST'])
def index():

    # MySQL Connection
    connection = mysql.connect()
    cursor = connection.cursor()

    # Vote tracking
    vote1 = 0
    vote2 = 0
    vote3 = 0
    vote4 = 0
    vote5 = 0

    if request.method == 'GET':

        # Get current values
        cursor.execute('''Select votevalue, count(votevalue) as count From azurevote.azurevote
        group by votevalue''')
        results = cursor.fetchall()

        # Parse results
        for i in results:
            if i[0] == app.config['VOTE1VALUE']:
                vote1 = i[1]
            elif i[0] == app.config['VOTE2VALUE']:
                vote2 = i[1]
            elif i[0] == app.config['VOTE3VALUE']:
                vote3 = i[1]              
            elif i[0] == app.config['VOTE4VALUE']:
                vote4 = i[1]          
            elif i[0] == app.config['VOTE5VALUE']:
                vote5 = i[1]    

        # Return index with values
        return render_template("index.html", value1=vote1, value2=vote2, value3=vote3, value4=vote4, value5=vote5, button1=button1, button2=button2, button3=button3, button4=button4, button5=button5, title=title)
    elif request.method == 'POST':

        if request.form['vote'] == 'reset':
            
            # Empty table and return results
            #cursor.execute('''Delete FROM azurevote''')
            #connection.commit()
            return render_template("index.html", value1=vote1, value2=vote2, value3=vote3, value4=vote4, value5=vote5, button1=button1, button2=button2, button3=button3, button4=button4, button5=button5, title=title)
        else:

            # Insert vote result into DB
            vote = request.form['vote']
            cursor.execute('''INSERT INTO azurevote (votevalue) VALUES (%s)''', (vote))
            connection.commit()
            
            # Get current values
            cursor.execute('''Select votevalue, count(votevalue) as count From azurevote.azurevote
            group by votevalue''')
            results = cursor.fetchall()

            # Parse results
            for i in results:
                if i[0] == app.config['VOTE1VALUE']:
                    vote1 = i[1]
                elif i[0] == app.config['VOTE2VALUE']:
                    vote2 = i[1] 
                elif i[0] == app.config['VOTE3VALUE']:
                    vote3 = i[1]  
                elif i[0] == app.config['VOTE4VALUE']:
                    vote4 = i[1]
                elif i[0] == app.config['VOTE5VALUE']:
                    vote5 = i[1]             
                
            # Return results
            return render_template("index.html", value1=vote1, value2=vote2, value3=vote3, value4=vote4, value5=vote5, button1=button1, button2=button2, button3=button3, button4=button4, button5=button5, title=title)
            
@app.route('/results')
def results():

    # MySQL Connection
    connection = mysql.connect()
    cursor = connection.cursor()

    # Get current values
    cursor.execute('''Select * FROM azurevote''')
    rv = cursor.fetchall()
    return str(rv)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)