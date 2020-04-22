#!/usr/bin/env python

# MIT License

# Copyright (c) 2020 TL

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import getpass, poplib, sys, smtplib, ssl, getopt, os.path
from os import path
from email.parser import Parser
from email.header import decode_header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

outbox = ''
smtpServer = ''
smtpPassword = ''
smtpSSL = False
smtpPort = ''
verbose = False
to = ''

def main():
    global outbox, smtpServer, smtpPassword, smtpSSL, smtpPort, verbose, to

    try:
        opts, args = getopt.getopt(sys.argv[1:],"vho::s:t:",["outbox=","smtp=","smtp-password=","smtp-port=","smtpSSL","to="])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-o","--outbox"):
            outbox = arg
        elif opt in ("-s","--smtp"):
            smtpServer = arg
        elif opt == "--smtp-password":
            smtpPassword = arg
        elif opt == "--smtp-port":
            smtpPort = arg
        elif opt == "smtpSSL":
            smtpSSL = True
        elif opt == "-v":
            verbose = True
        elif opt in ("-t", "--to"):
            to = arg
        else:
            assert False, "unhandled option"

    hasrequired = True
    if(outbox == ''):
        hasrequired = False
        print("outbox is required")
    if(smtpServer == ""):
        hasrequired = False
        print ("smtp-server is required")
    if(smtpPassword == ""):
        hasrequired = False
        print("smtp-password is required")
    if(smtpPort == ""):
        hasrequired = False
        print("smtp-port is required")
    if(to  == ""):
        hasrequired = False
        print("to is required")

    if(not hasrequired):
        usage()
        sys.exit(2)

    if(verbose):
        print("SMTP_USER:" + outbox)
        print("SMTP_PASSWORD:" + smtpPassword)
        print("SMTP_PORT:" + smtpPort)
        print("to:" + to)

    sendResponse(to, "Test")

def sendResponse(to, subject):
    global outbox, smtpServer, smtpPassword, smtpSSL, smtpPort, verbose
    try:
        sender = outbox 
        context = ssl.create_default_context()
        
        message = MIMEMultipart('alternative')
        message['Subject'] = subject
        message['From'] = sender
        message['To'] = to

        txt = "Test"
        txtPart = MIMEText(txt,'plain')
        
        html ="Test"
        htmlPart = MIMEText('<div dir="auto">' + html + '</div>','html')
        
        message.attach(txtPart)
        message.attach(htmlPart)
        with smtplib.SMTP_SSL(smtpServer,smtpPort,context=context) as server:
            server.login(sender,smtpPassword)
            server.sendmail(sender, to, message.as_string())
    except Exception as e:
        print(e)


def usage():
    print(sys.argv[0] + " -o <outbox> -s <smtpserver> --smtp-port=<port> --smtp-password=<password> -t <email address>")


if __name__ == "__main__":
    main()
