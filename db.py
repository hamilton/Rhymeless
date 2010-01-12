import MySQLdb
from datetime import datetime
import sqlite3
import os
#from contextless import 
from helpers import unescape, Search
from random import randint
from time import sleep

def reset():
	os.remove('data/test')

	con = sqlite3.connect('test')
	c = con.cursor()
	c.execute("""create table tweets(
		created_at ,
		username varchar(16),
		user_id int,
		tweet_id int UNIQUE PRIMARY KEY, 
		tweet text,
		to_user_id int,
		query varchar(30)
	)""")

search = Search()

QUERY = "awesome"

results = search.search(QUERY, results=1000)

print "results returned."

def insert_tweets(resultset, query):
	con = sqlite3.connect('test')
	c = con.cursor()
	for result in resultset:
		created_at = result['created_at']
		username = result['from_user']
		user_id = result['from_user_id']
		tweet_id = result['id']
		tweet = result['text']
		to_user_id = result['to_user_id']
		c.execute("""INSERT OR REPLACE INTO tweets values(?, ?, ?, ?, ?,?,?)""", (created_at,username,user_id,tweet_id,tweet,to_user_id, query))
	con.commit()
	c.close()

con = sqlite3.connect('test')
c = con.cursor()
import pprint
#p = pprint.PrettyPrinter(indent=4)
#p.pprint(results)
insert_tweets(results, QUERY)

#con.commit()

c.execute("""SELECT count(*) from tweets""")
total = c.fetchall()
print total, ": Total.  Good evening."

c.close()



#datetime.datetime.strptime(date[0:-6], "%a, %d %b %Y %H:%M:%S")