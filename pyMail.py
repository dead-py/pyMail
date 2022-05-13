# -*- coding: iso-8859-1 -*-

import smtplib, subprocess
from datetime import datetime
from email.mime.text import MIMEText
from time import sleep
from Secret import secret

class Mail:


    def __init__(self): # Variaveis de conexao da classe Mail

        self.port = 'Porta do servidor de email' # Porta para conexao SMTP
        self.smtp_server = "Servidor para envio do email" # Servidor para conexao SMTP
        self.sender_mail = "Conta que enviará o email" # Remetente
        self.password = secret # Senha do email de envio (deve ser trocada a variavel secret no arquivo Secret)


    def send(self, emails, content):

        with smtplib.SMTP(self.smtp_server, self.port) as server:
            server.ehlo() # Envio do 'hello' ao servidor de email, sem isso sera retornado um erro que solicita o 'hello'.
            server.starttls() # Inicia configuracao de TLS para o envio do email
            server.ehlo()

            print(f"Servidor SMTP - {self.smtp_server}")
            print(f"Porta - {self.port}")

            server.login(self.sender_mail, self.password) # Login usando credenciais do remetente
            print(f"Login efetuado - {self.sender_mail}")

            for email in emails: # leitura e envio para os emails na lista de destinatarios dentro de "__main__"
                print(f"Enviando email para {email}")
                result = server.sendmail(self.sender_mail, email, str(content))
                print(f"Email enviado com sucesso. Lendo proximo destinatario...")
            server.quit()


    def df(self, disk="/"): # Executa o comando de verificacao do disco informado em "disk"
        command = subprocess.Popen(f"df -H {disk} --output=source,size,used,pcent",
                shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]

        command = str(command.decode("utf-8")).replace("\\n", "") # Trata o excesso de informacoes no retorno do comando 'df'
        command = command.replace("Filesystem", "Disk\t\t\t   ") # "enfeita" a saida do comando df para o envio do email

        print(command)

        return str(f'{command}\n\nCriado por: Jayme Klein')
        # Retorno do comando df com customizacao de string


    def machine_Hostname(self): # Executa o comando que retorna o hostname do servidor
        command = subprocess.Popen(f"hostname", shell=True, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE).communicate()[0]

        return command.decode("utf-8") # Trata o excesso de informacoes no retorno do comando 'hostname'


    def pcent(self): # Retorna a porcentagem de disco em valor inteiro (0-100).
        df_output = str(mail.df()).split()
        print(df_output)
        df_output = int(str(df_output[-5:])[2:4])
        return df_output


    def check_Pcent(self, mails, content, wait, pcent): # Funcao para verificar o espaco em disco a cada x minutos
        while True:
            sleep(wait) # tempo em segundos entre cada verificacao de disco
            df_output = str(mail.df()).split()
            df_output = int(str(df_output[-5:])[2:4])


            if (df_output >= pcent):
                try:
                    mail.send(mails, content)
                    

                except Exception as E:
                    subject = f'exception {E}'
                    mail.logger(E) # cria arquivo de log com o erro apresentado
                    mail.send(mails, subject)


    def logger(self, error): # metodo para logar erros nao tratados

        log_time = datetime.now()
        dt_string = log_time.strftime("%d/%m/%Y %H:%M:%S") # Formatacao de data e hora para organizar os logs

        log = open("log.txt", "a+")
        log.write(f'{dt_string} [' + str(error) + ']\n')
        print("Log de erro registrado.")
        log.close()



if __name__ == '__main__': # execucao principal do script

    mail = Mail() # Instanciacao da classe Mail
    
    # Parametros utilizados pelo Mimetext, para deixar o email num formato aceito pelo servidor de email
    msg = MIMEText(mail.df())
    msg['Subject'] = f'Alerta de espaço em disco! Servidor {mail.machine_Hostname()} esta em {mail.pcent()}%'
    msg['From'] = mail.sender_mail
    #msg['To'] = 'jaymerebula04'
    
    mails = ['Destinatário1@google.com', 'Destinatário2@google.com'] 

    # Descricao dos parametros:
    # mails = lista de emails dos destinatarios
    # content = string customizada do assunto do email
    # wait = tempo em segundos entre cada verificacao de disco e envio de email
    # pcent = porcentagem em que o alerta sera gerado [0-100%]
    mail.check_Pcent(mails=mails, content=msg, wait=10, pcent=20)
