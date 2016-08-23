#!/usr/bin/python
import socket
import sys
import re
from bs4 import BeautifulSoup
CRLF = "\r\n"
flag_count=0
flaglist=[]

##ARGUMENT CHECK##
if (len(sys.argv) !=3):
        print 'Enter valid arguments'
	sys.exit()

username=sys.argv[1]
password=sys.argv[2]

##checks for valid NUID##
if (len(username)==9)and(username.isdigit()==True)!=1:
        print 'Please enter a correct username'
        sys.exit()

###########SOCKET CONNECTION########
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = 'cs5700sp16.ccs.neu.edu'
port = 80
try:
	
	remote = socket.gethostbyname( host )
	s.connect((host, port))
        #print 'Connected'
	request=("GET /accounts/login/?next=/fakebook/ HTTP/1.1\r\n"
        	 "Host: cs5700sp16.ccs.neu.edu\r\n"
         	"Connection: keep-alive\r\n"
         	"\r\n"
         	)
	#print request
	s.sendall(request)
	d =s.recv(7222)
        if 'Content-Length: 0' not in d:
                while '</html>' not in d: 
                        d=d+ s.recv(4096)
                        s.close()
except socket.error:
	print 'SOCKET ERROR'
        sys.exit()

#print d
#d =response.decode()
csrf_token1=d[245:277]
#print csrf_token1
#print(type(csrf_token1))
#a=response.find('sessionid')
#print a
sessionid=d[366:398]
#print sessionid
#print(len('csrfmiddlewaretoken='+csrf_token1+'&username=001773693&password=WZMSZ1TU&?next=/fakebook/\r\n'))
request_post=(
           'POST /accounts/login/ HTTP/1.1 \r\n'
           'Host: cs5700sp16.ccs.neu.edu\r\n'
           'Connection: keep-alive\r\n'
           'Content-Length: 108\r\n'
           'Origin: http://cs5700sp16.ccs.neu.edu\r\n'
           'Content-Type: application/x-www-form-urlencoded\r\n'
           'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n'
           'Referer: http://cs5700sp16.ccs.neu.edu/accounts/login/?next=/fakebook/\r\n'
           'Accept-Encoding: gzip, deflate\r\n'
           'Cookie: csrftoken=' + csrf_token1 + '; sessionid=' +sessionid+'\r\n'
           '\r\n'
           'csrfmiddlewaretoken='+csrf_token1+'&username='+username+'&password='+password+'&?next=/fakebook/\r\n'
)
#print request_post
try:    
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.sendall(request_post)
        response_post=s.recv(4096)
        while '302 FOUND' not in response_post:
                s.sendall(request_post)
                response_post=s.recv(10000)
except socket.error:
        print 'SOCKET ERROR Request Post'
        sys.exit()
#a1=response_post.find('sessionid')
#print a1
sessionid1=response_post[248:280]
#print sessionid1
#d1=request_post.find('/fakebook/')
#print d1

request1=request_post[329:339]
#print request1

redirect_request=("GET " +request1+ " HTTP/1.1\r\n"
        "Host: cs5700sp16.ccs.neu.edu\r\n"
        "Connection: keep-alive\r\n"
        "Referer: http://cs5700sp16.ccs.neu.edu/accounts/login/?next=/fakebook/\r\n"
        "Cookie: csrftoken=" + csrf_token1 +"; sessionid=" + sessionid1 +"\r\n"
        "\r\n"

)
#print redirect_request
s.sendall(redirect_request)
redirect_response=s.recv(4096)
if 'Content-Length: 0' not in redirect_response:
 	while '</html>' not in redirect_response:
 		redirect_response=redirect_response+s.recv(4096)
#print redirect_response
l=[]
x=[]
s.close()
soup= BeautifulSoup(redirect_response, 'html.parser')
for link in soup.find_all('a'):
                              bu=link.get('href')
                              #print bu
                              l.append(str(bu))
                              x.append(str(bu))

del l[-3:]
del x[-3:]
global req1
def internal_server(resp1):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         	host = 'cs5700sp16.ccs.neu.edu'
       		port = 80
        	remote = socket.gethostbyname( host )
       		s.connect((host, port))
		req1=('GET ' +url+ ' HTTP/1.1\r\n'
              	'Host: cs5700sp16.ccs.neu.edu\r\n'
              	'Connection: keep-alive\r\n'
              	'Referer: http://cs5700sp16.ccs.neu.edu/accounts/login/?next=/fakebook/\r\n'
              	'Cookie: csrftoken=' + csrf_token1 + '; sessionid=' +sessionid1+'\r\n'
              	'\r\n'
             	 )
		s.sendall(req1)
                resp1=s.recv(1000000)
                if '200 OK' in resp1:
                     while '</html>' not in resp1:
                                resp1=resp1+s.recv(1000000)
		     s.close()	                   
		if "500 INTERNAL SERVER" in resp1:
		     s.close()
		     resp1=internal_server(resp1)
                return resp1						
	
def get_request(url):

        req1=('GET ' +url+ ' HTTP/1.1\r\n'
              'Host: cs5700sp16.ccs.neu.edu\r\n'
              'Connection: keep-alive\r\n'
              'Referer: http://cs5700sp16.ccs.neu.edu/accounts/login/?next=/fakebook/\r\n'
              'Cookie: csrftoken=' + csrf_token1 + '; sessionid=' +sessionid1+'\r\n'
              '\r\n'
              )
        #print req1
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	host = 'cs5700sp16.ccs.neu.edu'
	port = 80
	remote = socket.gethostbyname( host )
	s.connect((host, port))
        s.sendall(req1)
        resp1=s.recv(1000000)
       	########HANDLING codes##########
	if "500 INTERNAL SERVER ERROR" in resp1:
		s.close()
		resp1=internal_server(resp1)
        if '200 OK' in resp1:
                 while '</html>' not in resp1:
                      	       resp1=resp1+s.recv(10000)
		 s.close()
	######ERRROR#####
        elif "403 Forbidden" in resp1:
			#print '403 Forbidden'
			s.close()
	elif "404 Not Found" in resp1:	
			#print '404 not found'
			s.close()
	else:
        		#print resp1
        		s.close()
 
        global flag_count
        soup= BeautifulSoup(resp1, 'html.parser')
        for link in soup.find_all('a'):
                              bu=link.get('href')
                              #print bu
                              c=(str(bu))
                              if (c!='/fakebook/') and (c not in l) and (c!='http://www.ccs.neu.edu/home/choffnes/') and (c!='http://www.northeastern.edu') and (c!='mailto:choffnes@ccs.neu.edu') :
                                l.append(c)
                                x.append(c)
        p = str(soup.find('h2', attrs={'class': 'secret_flag'}))
        if(p != 'None'):
            flag=p[48:112]
            if flag not in flaglist:
                flaglist.append(flag)
                flag_count = flag_count+1
                print "Flag:", flag
                if(flag_count == 5):
                     sys.exit()

flag_count=0
secondlist=[]
##MAIN LOOP BFS IMPLEMENTED##
while True:
        secondlist=x[:]  #Assigning discovered list to secondlist which will be  traversed#
        #print 'SECOND LIST',secondlist
        x=[]
	for i in range(len(secondlist)):
           	url=secondlist[i]
           	#print url
           	get_request(url)
                print 'LENGTHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH',len(l),len(x)
