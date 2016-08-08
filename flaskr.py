# coding: utf-8

import sqlite3
from flask import Flask, render_template, redirect, request, session, url_for, abort, flash
from contextlib import closing

# 配置文件
DATABASE = './flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql') as f:
			db.cursor().executescript(f.read())

@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	g.db.close()

@app.route('/')
def show_entries():
	cur = g.db.execute('select title, text from entries or der by id desc')
	entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
	return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(401)
	g.db.execute('insert into entries (title, text) values (?, ?)',[request.form['title'], request.form['text']])
	g.db.commit()
	flash('Newe entry was successfully posted')
	return redirect(url_for('show_entries'))

@app.route('login', methods=['GET','POST'])
def login():
	error = None
	if request.method == 'POST':
		if 

if __name__ == '__main__':
	app.run()