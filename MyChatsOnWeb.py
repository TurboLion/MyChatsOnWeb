#!C:/Python27/python.exe

###############################################################################
'''
Copyright (c) 2014, Leonid Burceacov
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
	* Redistributions of source code must retain the above copyright
	  notice, this list of conditions and the following disclaimer.
	* Redistributions in binary form must reproduce the above copyright
	  notice, this list of conditions and the following disclaimer in the
	  documentation and/or other materials provided with the distribution.
	* Neither the name of the project's copyright holder nor the
	  names of its contributors may be used to endorse or promote products
	  derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''
###############################################################################
'''
In this project I've used the following:
- Bootstrap - http://getbootstrap.com/
- CherryPy  - http://www.cherrypy.org/
- jQuery    - http://jquery.com/
- Skype4Py  - https://github.com/awahlig/skype4py
'''
###############################################################################

import cgi
import cherrypy
import Skype4Py

###############################################################################

# Append to the HTML Body.
def printB(text):
	global body
	body += str(text) + '\n'

###############################################################################

class MyChatsOnWeb(object):

	def index(self):

		# Clear the HTML Body.
		global body
		body = ''

		# Let's start displaying the page.
		printB ("""
<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<title>MyLittleChat</title>
		<link href="//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css" rel="stylesheet">
		<script src="//code.jquery.com/jquery-1.11.0.min.js"></script>
		<script src="//netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js"></script>
		<style type="text/css">
			.the-table {
				table-layout: fixed;
				word-wrap: break-word;
			}

			/* Some text is just too small on my mobile in portrait mode... */
			@media (min-width: 768px) and (orientation: portrait) {
				.badge, .bigger-on-mobile {
					font-size: 24px !important;
				}
			}
		</style>
	</head>
	<body>
		<div class="container">
		<h1>Welcome!</h1>
		""")

		# If we got new messages, then display them.
		if len(skype.MissedMessages) > 0:

			# Display a panel with information about the missed chat messages.
			printB('<div class="panel panel-danger"><div class="panel-heading"><h4>Found <strong>%s</strong> missed messages, here\'s the latest:</h4></div></div>' 
				% str(len(skype.MissedMessages)))

			# Start a table.
			printB('<table class="table table-condensed the-table bigger-on-mobile">')

			# Iterate through all missed messages.
			for mssg in skype.MissedMessages:

				# Display each message in a table row.
				printB ('<tr><td><strong>%s</strong>: <span class="badge pull-right">%s</span><p>%s</td></tr>' 
					% (mssg.FromDisplayName.encode('utf-8'), mssg.Datetime, cgi.escape(mssg.Body.encode('utf-8')) ) )

				# Uncomment this if you want all of your missed messages to be marked as 'Seen'.
				# This is useful if you run this script for the first time and see, like, 
				# 500+ unread messages from ages ago.
				# mssg.MarkAsSeen()

			# Close the table.
			printB('</table>')

		# Display a panel with information regarding our latest chats.
		printB('<div class="panel panel-info"><div class="panel-heading"><h4>Recent chats: <strong>%s</strong></h4></div></div>' 
			% str(len(skype.RecentChats)))

		# Start the accordion.
		printB('<div class="panel-group" id="accordion">')

		# A iterator for each of accordion's elements.
		i = 0

		# Iterate through all recent chats.
		for chat in skype.RecentChats:

			# It's kinda sad that Python doesn't have ++
			i += 1

			# This is the accordion's element's title and start of body.
			printB("""
				<div class="panel panel-default">
					<div class="panel-heading">
						<h4 class="panel-title">
							<a data-toggle="collapse" data-parent="#accordion" href="#collapse%s">
								Chat with: %s <span class="badge pull-right">%s</span>
							</a>
						</h4>
					</div>
				</div>
				<div id="collapse%s" class="panel-collapse collapse">
					<div class="panel-body">
						<table class="table table-condensed the-table">
			""" % ( str(i), chat.FriendlyName.encode('utf-8'), str(len(chat.RecentMessages[-10:])), str(i) ) )

			# Iterate through 10 most recent messages.
			for mssg in chat.RecentMessages[-10:]:

				# This variable is used to 'color' the apropriate table row.
				addclass = ' class="active"'

				# In case you are the message sender.
				if mssg.FromDisplayName != name:
					addclass = ''

				# If the message is not yet read.
				if mssg.Status == 'RECEIVED':
					addclass = ' class="danger"'

				# Print each message in a separate table row.
				printB ( '<tr%s><td><strong>%s</strong>: <span class="badge pull-right">%s</span><p>%s</td></tr>' 
					% (addclass, mssg.FromDisplayName.encode('utf-8'), mssg.Datetime, cgi.escape(mssg.Body.encode('utf-8')) ) )

			# Close the table and the accordion's element's body.
			printB('</table></div></div>')

		# Close everything.
		printB ("</div></div></body></html>")

		# Return the contents of the Web page.
		return body

	# Only exposed methods can be called to answer a request.
	index.exposed = True

###############################################################################

#Change these variables according to your system settings.
ip = '192.168.0.29'			# IP adress
port = 8080					# Port
name = 'Leonid Burceacov'	# Your Skype name

# Instatinate a Skype object.
skype = Skype4Py.Skype()

# Set our application name.
skype.FriendlyName = 'MyChatsOnWeb'

# Attach to Skype. This may cause Skype to open a confirmation dialog.
skype.Attach()

# This global variable will contain the HTML Body.
body = ''

# Start the server.
cherrypy.config.update( {'server.socket_host': ip, 'server.socket_port': port } )
cherrypy.quickstart(MyChatsOnWeb())