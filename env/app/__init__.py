import os
import sqlite3
from . import dbc
from werkzeug.security import generate_password_hash, check_password_hash

from flask import Flask, render_template, request, flash, redirect
from sqlite3 import Error
def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = dbc.SEC,
        DATABASE = os.path.join(app.instance_path, 'app.sqlite'),
    )

    
    @app.route('/')
    @app.route('/inicio')
    def home():
        return render_template('index.html')

    @app.route('/register/', methods=['POST, GET'])
    def register_save():
        if request.method == 'POST':
            usuario =request.form['username']
            email =request.form['email']
            password =request.form['password']
            hashClave =generate_password_hash(password)
            try: 
                with sqlite3.connect('basedatos.db') as conex:
                    cur = conex.cursor() #manipula la conexion a la bd
                    cur.execute("INSERT INTO user (username, email, password) VALUES(?,?,?)",(usuario, email, password) )
                    conex.commit()
                    flash("Usuario registrado con éxito")
                    return render_template('login.html')
            except Error:
                print(Error)
                flash("Usuario no registrado")
                return render_template('register.html')

                    

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)
    
    from . import auth
    app.register_blueprint(auth.bp)
    
    from . import inbox
    app.register_blueprint(inbox.bp)
    app.add_url_rule('/show', endpoint='index.show')
    app.add_url_rule('/show.html', endpoint='index.show')

    
    return app

    