from threading import Thread
import socket
import os.path
import sys


class HTTPrequest(Thread):
    
    def __init__(self,  client):
        Thread.__init__(self)
        self.client = client
        self.clrf = '\r\n'

    def run(self):
        while True:
            try:
                self.processRequest()
            except Exception as e:
                #print(e.strerror)
                break

    
    def processRequest(self):

        data = self.client[0].recv(2048)

        if data:
            lines = data.splitlines()


            name = lines[0].split()

            filename = name[1][1:].decode("utf-8")


            stringlist = [x.decode("utf-8") for x in lines]
            
            
            for i in stringlist:
                if(i == ''):
                    break
                else:
                    print(i)


            if os.path.isfile(filename):

                header = 'HTTP/1.0 200 OK\n\n'
                print(header)

                
                if(filename.endswith('.jpeg')):
                    mimetype = 'image/jpeg'
                else:
                    mimetype = 'text/html'

                #header += 'Content-Type: ' + str(mimetype)+ str(self.clrf)#'\r\n'#'<strong>\n\n</strong>'   #self.crlf
                
                if(mimetype =='text/html'):

                    self.client[0].send(header.encode())

                    file = open(filename,'rb')
                    response = file.read()
                    file.close()


                    final_response = response

                    self.client[0].send(final_response)

                    self.client[0].send(str.encode('\r\n'))
                    self.client[0].close()
                
                elif (mimetype =='image/jpeg'):
                    

                    self.client[0].send(header.encode())
                    f = open(filename,'rb')
                    outputdata = f.read()
                    f.close()


                    for i in range(0, len(outputdata)):
                        self.client[0].sendall(outputdata[i].encode())


                    self.client[0].sendall(str.encode('\r\n'))
                    self.client[0].close()


                
                else:
                    pass

            #Se não existe retorna 404 not found
            else:
                
                header = "HTTP/1.0 404 Not Found \n\n"
                print(header)


                response = '<html><body><center><h3>Error 404: File not found</h3><p>Python HTTP Server</p></center></body></html>'.encode('utf-8')

                final_response = header.encode('utf-8')
                final_response += response

                self.client[0].send(final_response)


                self.client[0].close()







#Realiza conexão com o cliente
class webServer:


    def __init__(self):


        #Porta 
        PORT = 8001

        HOST =  '192.168.15.89'
        #HOST = "localhost"

        #estabelece socket de escuta do servidor
        try:
            ServerSoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ServerSoc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            ServerSoc.bind((HOST, PORT))
            ServerSoc.listen(1)
        except socket.error as e:
            print("Failed to create socket: " + e.strerror)
            ServerSoc.close()
            sys.exit()
        
        print("[+] Listening for connections on port "+str(PORT))

        
        #socket do client

        socketCli = socket

        threads = []
        try:
            while(True):
                print("Servidor Ativo \n")


                socketCli = ServerSoc.accept()

                #constroi objeto pra processar msg requisição http
                #cria nova thread p processar novas reqs

                newthread = HTTPrequest(socketCli)
                newthread.start()
                
                threads.append(newthread)
                #ServerSoc.close()
        except KeyboardInterrupt:
            ServerSoc.close()
            print("Servidor fechado")
            pass

httpwebserver = webServer()




    



