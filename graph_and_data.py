import abstractions as ab
from time import sleep
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.tools as tls
stream_1 = None
s = None
def initialize_graph():
	global stream_1
	global s

	tls.set_credentials_file(username='m0597', api_key='9pjer55x5e', stream_ids=['efzmil96bw'])
	stream_id = tls.get_credentials_file()['stream_ids'][0]

	stream_1 = go.Stream(
	    token=stream_id,  # link stream id to 'token' key
	    maxpoints=80      # keep a max of 80 pts on screen
	)

	# pick up where we left off 
	x_data = ab.get_column('time', 'prices', 'test_table.sqlite')
	y_data = ab.get_column('last', 'prices', 'test_table.sqlite')

	# some magic that makes the plot and uploads it to the plotly hosting site
	trace0 = go.Scatter(x=x_data, y=y_data, stream=stream_1)
	data = [trace0]
	layout = go.Layout(
    	xaxis=dict(
	        showticklabels=False
    	)
	)
	fig = go.Figure(data=data, layout=layout)
	unique_url = py.plot(fig, filename = 'basic-line', auto_open=False)
	# open stream connection
	s = py.Stream(stream_id)
	s.open()


def graph(m):
	print("Graphing...")
	"""Use a market object to write new data to the graph stream"""
	x = m.time
	y = m.last

	s.write(dict(x=x, y=y)) 


