# Web app made with old way
#Author:Ankit Raj Ojha



import cgi

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database_setup import Base, Restaurant


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class WebserverHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        result = session.query(Restaurant).all()
        try:
            if self.path.endswith("/restaurant"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output= ""
                for result in result:
                    output+="<html><body>"+result.name+\
                            "<br></br>" \
                            "<a href='/restaurant/%s/edit'>Edit</a>" % result.id
                    output+="<br></br>" \
                            "<a href = '/restaurant/%s/delete'>Delete</a>" % result.id
                output+="<br></br><h2><a href='/restaurant/new'> Add a new restaurant</a></h2>" \
                        "</body></html>"
                self.wfile.write(output)
                print output
                return
            if self.path.endswith("/restaurant/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output= ""
                output += "<html><body>" \
                          "<h2>Enter the name of the restaurant</h2>" \
                          "<form method = 'POST' enctype='multipart/form-data'" \
                          "action = '/restaurant/new'><h2>Enter the name</h2>" \
                          "<input name ='message' type ='text'>" \
                          "<input type = 'submit' value = 'Submit'></form>"
                output += "</body></html>"

                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/edit"):
                restaurantIDpath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDpath).one()
                if myRestaurantQuery!=[]:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output= ""
                    output += "<html><body>" \
                              "<h2>Enter the new name of the"+myRestaurantQuery.name+"</h2>" \
                              "<form method = 'POST' enctype='multipart/form-data'" \
                              "action = '/restaurant/%s/edit'>" % restaurantIDpath
                    output += "<h2>Enter the new name</h2>" \
                              "<input name ='message' type ='text'>" \
                              "<input type = 'submit' value = 'Submit'></form>"
                    output += "</body></html>"

                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/delete"):
                restaurantIDpath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDpath).one()
                if myRestaurantQuery!=[]:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output= ""
                    output += "<html><body>" \
                              "<h2>Do you want to delete the"+myRestaurantQuery.name+"</h2>" \
                              "<form method = 'POST' enctype='multipart/form-data'" \
                              "action = '/restaurant/%s/delete'>" % restaurantIDpath
                    output += "<input type = 'submit' value = 'Delete'></form>"
                    output += "</body></html>"

                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, "File Not Found %s" %self.path)

    def do_POST(self):
        try:
            if self.path.endswith('/restaurant/new'):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurant')
                self.end_headers()

                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')
                newRestaurant = Restaurant(name=messagecontent[0])
                session.add(newRestaurant)
                session.commit()
                return

            if self.path.endswith('/edit'):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')
                restaurantIDpath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDpath).one()
                if myRestaurantQuery!=[]:
                    myRestaurantQuery.name = messagecontent[0]
                    session.add(myRestaurantQuery )
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurant')
                    self.end_headers()
                return

            if self.path.endswith('/delete'):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))


                restaurantIDpath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDpath).one()
                if myRestaurantQuery!=[]:
                    session.delete(myRestaurantQuery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurant')
                    self.end_headers()
                return

        except:
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('',port), WebserverHandler)
        print "Web server running on port %s" % port
        server.serve_forever()

    except KeyboardInterrupt:
        print "^C entered, stopping web server..."
        server.socket.close()

if __name__=='__main__':
    main()


#Source: Udacity