import sqlite3

header = """
<!-- header -->
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN"
"http://www.w3.org/TR/html4/strict.dtd">
<html>
	<head>
		<link href="style.css" media="all" rel="stylesheet" type="text/css" />
		<title>Rhymeless - Darwin's Origin of Species</title>
	</head>
<body>
<div id="content">

<h1>Random Walk 'Poetry'</h1>
<h2>trained on Darwin's <em>On the Origin of Species</em></h2>
<div id="description">Updates every minute. | Source code forthcoming.</div>
<hr>
<br><br>

"""

footer = """

</div>

<div id="footer">
	Made by Hamilton Ulmer, one morning in early 2009.
</div>

"""

###########################################
# Open the config file to get paths, etc. #
###########################################

import ConfigParser
config = ConfigParser.ConfigParser()

try:
	config.read('config.cnf')
except:
	raise IOError, "you have not properly defined a config.cnf file.  See the accompanying README file for more details."

##############################################################################

db_dir = config.get("sqlite", "db_dir")

conn = sqlite3.connect('%s/%s' % (db_dir, "sqlite.db"))
c = conn.cursor()

c.execute("""SELECT ROWID, used, content from entries 
	WHERE entries.used == 0 ORDER BY ROWID;""")
new_id, new_used, new_content = c.fetchone()

c.execute("""UPDATE entries SET used = 1 WHERE ROWID = ?;""", [new_id])

#################### get latest 10 poems. #####################################

c.execute("""SELECT ROWID, used, content from entries 
	WHERE entries.used == 1 ORDER BY ROWID desc LIMIT 0,10;""")
data = c.fetchall()
content = "\n\n".join([content for row_id, used, content in data])

page = """
%s
%s
%s""" % (header, content, footer)

index_html = config.get("site", "site_dir")
index_html = "%s/%s" % (index_html, "darwin.html")
index_html = open(index_html, 'w')
index_html.write(page)
index_html.close()

conn.commit()