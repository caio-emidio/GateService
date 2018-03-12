from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from sqlalchemy.orm import sessionmaker
from tabledef import *
engine = create_engine('sqlite:///tutorial.db', echo=True)
 
app = Flask(__name__)

#Inicio MQTT
import paho.mqtt.client as paho

def on_publish(client, userdata, mid):
    print("mid: "+str(mid))
 
client = paho.Client()
client.on_publish = on_publish
client.username_pw_set("comunidade", "comunidade")
client.connect("m12.cloudmqtt.com", 16903, 60)
client.loop_start()
#Fim MQTT

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
 
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html', comment = "Seja Bem Vindo :D")
    else:
        bottons = [['/botao1','Alarme','glyphicon glyphicon-volume-up'],['/botao2','Portão 1', 'glyphicon glyphicon-inbox'],['/botao3','Portão 2', 'glyphicon glyphicon-inbox'],['/botao4','Portão 3', 'glyphicon glyphicon-inbox']]
        return render_template('template.html', bottons=bottons)
        
        
@app.route('/login', methods=['POST'])
def do_admin_login():
 
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
 
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()
    print(result)
    if result:
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()

@app.route('/botao1')
def botao():
    if not session.get('logged_in'):
        return render_template('login.html', comment = "Sessão Expirada")
    else:
        msg = '{"sender":"1735900359776976","msg":"Alarme Pressionado"}'
        (rc, mid) = client.publish("comunidade/teste", msg, qos=1)
        session['alert'] = "Alarme"
    return redirect('/')


@app.route('/botao2')
def botao2():
    if not session.get('logged_in'):
        return render_template('login.html', comment = "Sessão Expirada")
    else:
        msg = '{"sender":"[ID - Facebook]","msg":"Portao 1 Pressionado"}'
        (rc, mid) = client.publish("comunidade/teste", msg, qos=1)
        session['alert'] = "Portão 1"
    return redirect('/')


@app.route('/botao3')
def botao3():
    if not session.get('logged_in'):
        return render_template('login.html', comment = "Sessão Expirada")
    else:
        msg = '{"sender":"1735900359776976","msg":"Portao 2 Pressionado"}'
        (rc, mid) = client.publish("comunidade/teste", msg, qos=1)
        session['alert'] = "Portão 2"
    return redirect('/')


@app.route('/botao4')
def botao4():
    if not session.get('logged_in'):
        return render_template('login.html', comment = "Sessão Expirada")
    else:
        msg = '{"sender":"1735900359776976","msg":"Portao 3 Pressionado"}'
        (rc, mid) = client.publish("comunidade/teste", msg, qos=1)
        session['alert'] = "Portão 3"
    return redirect('/')

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect('/')


@app.route("/settings")
def settings():
    if not session.get('logged_in'):
        return render_template('login.html', comment = "Sessão Expirada")
    else:
        nome = "admin"
        return render_template('settings.html', nome = nome)

@app.route("/settings/changepassword")
def changepassword():
    if not session.get('logged_in'):
        return render_template('login.html', comment = "Sessão Expirada")
    else:
        nome = "admin"
        return render_template('changepassword.html', nome = nome)



if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0', port=8080, debug=True)
