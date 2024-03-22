from socket import *
import os
import datetime


class PTATServer():
    host = '127.0.0.1'
    serverPort = 12000

    def __init__(self):
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.serverSocket.bind((self.host, self.serverPort))
        self.serverSocket.listen(1)


    def realiza_requisicao(self):
        match(self.op):
            case '0':
                # read
                caminho_arq = str(self.path + "\\" + self.filename)

                if(os.path.exists(caminho_arq)):
                    with open(caminho_arq, 'r') as file:
                        
                        self.length = os.path.getsize(caminho_arq)
                        self.body = file.read()
                        
                        self.code = 0
                        self.message = "Arquivo lido com sucesso"
                
                else:
                    self.length = 1  
                    self.code = 2      
                    self.message = "Nome de arquivo não existente no servidor"
                    self.body = ""


            case '1':
                # write
                caminho_arq = self.path + "\\" + self.filename

                print(caminho_arq)

                if(os.path.exists(self.path)):
                    self.body = self.body[1:-1]
                    with open(caminho_arq, 'w') as file:
                        file.write(self.body)
                    
                    self.length = 1
                    self.body = ""
                    self.code = 0
                    self.message = "Arquivo escrito com sucesso"

                else:
                    self.length = 1
                    self.code = 1
                    self.message = "Caminho não existente no servidor"
                    self.body = ""

            case '2':
                # delete
                caminho_arq = str(self.path + "\\" + self.filename)
                
                if(os.path.exists(caminho_arq)):
                    os.remove(caminho_arq)

                    self.length = 1
                    self.body = ""
                    self.code = 0
                    self.message = "Arquivo deletado com sucesso"

                else:
                    self.length = 1
                    self.code = 2
                    self.message = "Nome de arquivo não existente no servidor"
                    self.body = ""

            case '3':
                # list
                diretorio = self.path
                if(os.path.exists(diretorio)):
                    arquivos_diretorio = os.listdir(diretorio)
                    
                    body = ""
                    for arquivo in arquivos_diretorio:
                        body = body + arquivo + "\n"
                                        
                    self.length = 1
                    self.body = body
                    self.code = 0
                    self.message = "Arquivos listados com sucesso"

                else:
                    self.length = 1
                    self.code = 1
                    self.message = "Caminho não existente no servidor"
                    self.body = ""
                    
            case _:
                self.length = 1
                self.code = 4
                self.message = "Operação inválida"
                self.body = ""

        horario = datetime.datetime.now().strftime("%H:%M:%S")

        return f"HORA:{horario}, OP:{self.op}, PATH:{self.path}, CODE:{self.code}"

    def enviar_resposta(self):
        string_resposta = f"{self.op},{self.length},{self.filename},{self.path},{self.code},{self.message},{self.body}"
        
        self.connectionSocket.send(string_resposta.encode())

    def aguarda_requisicao(self):
        while True:
            self.connectionSocket, self.addr = self.serverSocket.accept()

            self.recebe_requisicao()
            log = self.realiza_requisicao()
            self.enviar_resposta()

            yield log

            self.connectionSocket.close()

    def recebe_requisicao(self):   
        string_recebida = self.connectionSocket.recv(1000000000).decode()

        self.op, self.length, self.filename, self.path, self.body = string_recebida.split(",")
               


def main():
    server = PTATServer()

    print("Server aberto")

    for log in server.aguarda_requisicao():
        print(log)

        

main()
        
