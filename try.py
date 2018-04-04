import MySQLdb
from multiping import MultiPing
from multiping import multi_ping

if __name__ == "__main__":
    connection=MySQLdb.connect(host="localhost", user="cloudlet1", passwd="bekvs", db="cloudlet_info")  
    cur=connection.cursor()
	
    cur.execute("select IPaddress from neighbour_cloudlets")
    rows=cur.fetchall()

    addrs = [row[0] for row in rows]   
    mp = MultiPing(addrs)
    mp.send()
    responses, no_responses = mp.receive(0.01)

    for addr, rtt in responses.items():
        #print "%s responded in %f seconds" % (addr, rtt)
        cur.execute("Update neighbour_cloudlets set rtt='%f' where IPaddress='%s'" % (rtt,addr)) 

    #cur.execute("select * from neighbour_cloudlets")
    #mrows=cur.fetchall()
    #print mrows
    cur.close()                                      
    connection.close()
       
    
