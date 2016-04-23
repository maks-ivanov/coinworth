import datetime, requests, sqlite3, schedule,time
# Shedule
from apscheduler.schedulers.background import BackgroundScheduler
import simplejson as json
# Flask imports
from flask import Flask, request, session, g, redirect, url_for, abort, \
	 render_template, flash
from flask.ext.mail import Mail # mail module
# DB tools
from contextlib import closing
# Utils
from abstractions import *
from graph_and_data import *
import os
##########################################################################

# Initialize the Flask application
app = Flask(__name__)

# Configuring Flask Mail with gmail
app.config['MAIL_SERVER']= 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'coinworthupdate@gmail.com'
app.config['MAIL_PASSWORD'] = 'fakepass'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEBUG'] = True

mailbox = Mail(app) # Initialize mail

# Defining a route for the default URL, which loads the form
@app.route('/')
def form():
	return render_template('layout.html')

 
# accepting: POST requests 
@app.route('/confirmation/', methods=['POST'])
def entry(ID=1):
	# assigning form input to variables
	name = request.form['Name']
	email = request.form['Email']
	btc = request.form['BTC']
	operator = None

	curr = Market().last
	# if user specified a btc rate above or equal to current 
	# 	select at_least
	# else, 
	# 	select at_most
	if float(btc) >= curr:
		operator = 0
	else:
		operator = 1
	# entering the information into the database 
	update_users(ID, name, email, btc, operator)
	return render_template('confirmation.html', name = name)


#######BACKGROUND PROCESS#######
@app.before_first_request
def initialize():
	"""Setting a schedule for the background process"""
	with app.app_context():
		print("Scheduling...")
		apsched = BackgroundScheduler()
		apsched.add_job(run_check, 'interval', seconds=60)
		apsched.start()


def run_check():
	"""Main"""
	with app.app_context():
		print("Sending a Bitstamp request")
		market = Market() # Bitstamp response dict
		row = create_row_template(market) # Row factory
		update_prices(row, connection='test_table.sqlite') # Insert row
		perform_check(market) 
		graph()




################################
# Run the app :)
if __name__ == '__main__':
  app.run(  debug=True,
			host="0.0.0.0",
			port=int("80")
  )
