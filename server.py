import SocketServer, os.path
# coding: utf-8

# Copyright 2015 Abram Hindle, Eddie Antonio Santos, Chongyang Ye
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        #get the request
        requestList = self.data.split()
        
        requestType = requestList[0]
        requestUrl = requestList[1]
        if requestType == "GET":
            self.getRequest(requestUrl)
       

    
    def getRequest(self, requestUrl):
        
        if "/../" in requestUrl or "/.." in requestUrl:
            self.pageNotFound()
            return        
        
        dirc="/www"
        contentType = ""
        #set index.html as default
        if requestUrl[-1] =="/":
            requestUrl = requestUrl +"index.html"
            contentType = "text/html"
            if os.path.isfile(os.getcwd()+dirc+requestUrl):
                fp = open(os.getcwd()+dirc+requestUrl,"r").read()
                fp2 = open(os.getcwd()+dirc+"/base.css", "r").read()
                self.sendResponse(contentType, fp,fp2)
            else:
                fp = open(os.getcwd()+requestUrl,"r").read()
                fp2 = open(os.getcwd()+dirc+"/deep.css", "r").read()
                self.sendResponse(contentType, fp,fp2)
        #check the file is css or not 
        elif requestUrl[-3:].lower() == "css":
            contentType = "text/css"
            fp2=""
            if os.path.isfile(os.getcwd()+dirc+requestUrl):
                fp = open(os.getcwd()+dirc+requestUrl,"r").read()
                self.sendResponse(contentType, fp,fp2)
            else:
                fp = open(os.getcwd()+requestUrl,"r").read()
                self.sendResponse(contentType, fp,fp2)
        #check the file is html or not         
        elif requestUrl[-4:].lower() =="html":
            contentType = "text/html"
            if os.path.isfile(os.getcwd()+dirc+requestUrl):
                fp = open(os.getcwd()+dirc+requestUrl,"r").read()
                fp2 = open(os.getcwd()+dirc+"/base.css", "r").read()
                self.sendResponse(contentType, fp,fp2)
            else:
                fp = open(os.getcwd()+requestUrl,"r").read()
                fp2 = open(os.getcwd()+dirc+"/deep.css", "r").read()
                self.sendResponse(contentType, fp, fp2)
        #handle the case for /deep, there is no / behind        
        elif requestUrl[-4:].lower()== "deep":
            contentType = "text/html"
            requestUrl = requestUrl +"/index.html"
            fp = open(os.getcwd()+dirc+requestUrl,"r").read()
            fp2 = open(os.getcwd()+dirc+"/base.css", "r").read()
            self.sendResponse(contentType, fp,fp2)            
            
        #if file is not html or css, then it's not a correct file 
        else:
            self.pageNotFound()
        
            
        
    def sendResponse(self, contentType, fp,fp2):    
        self.request.sendall("HTTP/1.1 200 OK\r\n"+
                             "Content-Type: "+contentType +"\r\n"+
                             fp+"<style>"+fp2+"</style>")
            
        
    def pageNotFound(self):
        self.request.sendall("HTTP/1.1 404 Not Found\r\n" +
                             "Content-Type: text/html\n"+
                             "<html><body><h1>404 Page Not Found"+
                             "</h1></body></html>\n")

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
