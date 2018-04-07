import MySQLdb
from multiping import MultiPing
from multiping import multi_ping
import config

username = 'cloudlet3'
password = 'bekvs2018' 
db_name = 'cloudlet_info'

connection=MySQLdb.connect(host="localhost", user=username, passwd=password, db=db_name)
cur=connection.cursor()