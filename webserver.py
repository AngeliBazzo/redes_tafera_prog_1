from threading import Thread
import socket
import os.path


class HTTPrequest(Thread):
    
    def __init__(self,  client):
        Thread.__init__(self)
        self.client = client

    def run(self):
        while True:
            try:
                self.processRequest()
            except Exception as e:
                print(e)

    
    def processRequest(self):

        data = self.client[0].recv(1024)

        if data:
            lines = data.splitlines()
                
            
            #print (name)
            # name = name[0].split()
            # filename = name[1].decode("utf-8")
            # print (filename)
            #print(type(filename))

            # for i in lines:
            #    print(i.decode("utf-8"))

            name = lines[0].split()
            filename = name[1].decode("utf-8")

            print(filename)

                #SEND FILE
            if os.path.isfile(filename[1:]):
                print("Hello World")
                with open(filename[1:],'rb') as f:
                    while(True):
                        bytes_read = f.read(4000000) #1024
                        if not bytes_read:
                            break
                        self.client[0].sendall(bytes_read)
                    
                self.client[0].close()


                


                
            
            #Se não existe retorna 404 not found
            else:
                print("Hello")
                html = '\n<!doctype html>\n'
                html += '<html>\n'
                html += '<head>\n'
                html += '<meta charset="utf-8">\n'
                html += '<title>404 File Not Found</title>\n'
                html += '</head>\n'
                html += '<body><p> 404 File Not Found </p></body>\n'
                html += '</html>\n'

                print(html)

                self.client[0].send(html.encode())
                self.client[0].close()




        



#Realiza conexão com o cliente
class webServer:


    def __init__(self):


        #Porta 
        PORT = 8000

        HOST = "localhost"
        #HOST = '0.0.0.0'

        #estabelece socket de escuta do servidor
        ServerSoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        ServerSoc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ServerSoc.bind((HOST, PORT))
        ServerSoc.listen(1)
        #socket do client

        socketCli = socket

        threads = []

        while(True):
            print("Servidor Ativo /n")

            #ServerSoc.listen(1)

            #escutar requisição de conexao TCP
            
            socketCli = ServerSoc.accept()
            #constroi objeto pra processar msg requisição http

            #req = HTTPrequest(socketCli) 


            #cria nova thread p orocessar novas reqs
            #newthread = ThreadingMixIn.Thread(req)

            newthread = HTTPrequest(socketCli)
            newthread.start()
            
            threads.append(newthread)
        #ServerSoc.close()


httpwebserver = webServer()




    



