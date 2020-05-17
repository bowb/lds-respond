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

import getpass, poplib, sys, smtplib, ssl, getopt, os.path, os, random, glob
from os import path
from email.parser import Parser
from email.header import decode_header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

inbox = ''
outbox = ''
popServer = ''
popPort = ''
popSSL = False
smtpServer = ''
popPassword = ''
smtpPassword = ''
smtpSSL = False
smtpPort = ''
verbose = False
txtFile = './txt'
htmlFile = './html'
useRandomFile = False 
noSendFile = None 
workDir = '.'
poplib._MAXLINE = 2147483647 
words = ['bishop','mission','endowment','prophet','temple','indexing','priesthood','covenant','bless','brethren','stake','ward','elder','church','lord','sacrament','minister','saint','jesus','baptism','family history','relief society','president','counselor','young men','young women','trek']

def main():
    global inbox, outbox, popServer, popPort, popSSL, smtpServer, popPassword, smtpPassword, smtpSSL, smtpPort, verbose, txtFile, htmlFile, useRandomFile, noSendFile, workDir

    try:
        opts, args = getopt.getopt(sys.argv[1:],"rvhi:o:p:s:w:",["inbox=","outbox=","pop=","smtp=","pop-password=","smtp-password=", "pop-port=","smtp-port=","smtpSSL","popSSL","txt-file=","html-file=","random","no-send-file=","work-dir="])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(2)

    print(opts)

    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-i","--inbox"):
            inbox = arg
        elif opt in ("-o","--outbox"):
            outbox = arg
        elif opt in ("-p","--pop"):
            popServer = arg
        elif opt in ("-s","--smtp"):
            smtpServer = arg
        elif opt == "--pop-password":
            popPassword = arg
        elif opt == "--smtp-password":
            smtpPassword = arg
        elif opt == "--pop-port":
            popPort = arg
        elif opt == "--smtp-port":
            smtpPort = arg
        elif opt == "--smtpSSL":
            smtpSSL = True
        elif opt == "--popSSL":
            popSSL = True
        elif opt == "-v":
            verbose = True
        elif opt == "--txt-file":
            txtFile = arg
        elif opt == "--html-file":
            htlmFile = arg
        elif opt == "--no-send-file":
            noSendFile = arg
        elif opt in  ("-r","--random"):
            useRandomFile = True
        elif opt in ("-w","--work-dir"):
            workDir = arg
        else:
            assert False, "unhandled option"

    hasrequired = True
    if(inbox == ''):
        hasrequired = False
        print("inbox is required")
    if(outbox == ''):
        hasrequired = False
        print("outbox is required")
    if(popServer == ''):
        hasrequired = False
        print("popserver is required")
    if(popPort == ""):
        hasrequired = False
        print("pop-port is required")
    if(smtpServer == ""):
        hasrequired = False
        print ("smtp-server is required")
    if(popPassword == ""):
        hasrequired = False
        print("pop-password is required")
    if(smtpPassword == ""):
        hasrequired = False
        print("smtp-password is required")
    if(smtpPort == ""):
        hasrequired = False
        print("smtp-port is required")

    if(not hasrequired):
        usage()
        sys.exit(2)

    if(useRandomFile):
        rFile = getFile(workDir)
        if(verbose):
            print(rFile)
        if(rFile):
            txtFile = rFile
            htmlFile = os.path.splitext(txtFile)[0] + ".html"
    
    if(verbose):
        print("POP_USER:" + inbox)
        print("POP_PASSWORD:" + popPassword)
        print("POP_SERVER:" + popServer)
        print("POP_PORT:" + popPort);
        print("SMTP_USER:" + outbox)
        print("SMTP_PASSWORD:" + smtpPassword)
        print("SMTP_PORT:" + smtpPort)
        print("txtFile:" + txtFile)
        print("htmlFile:" + htmlFile)
        print("useRandomFile:" + str(useRandomFile))
        print("workdir:" + workDir)

    Mailbox = poplib.POP3_SSL(popServer, popPort)
    Mailbox.user(inbox) 
    Mailbox.pass_(popPassword) 
    numMessages = len(Mailbox.list()[1])

    for i in range(numMessages):
        resp, lines, octets = Mailbox.retr(i+1) 
        msg_content = b'\r\n'.join(lines).decode('utf-8')
        for w in words:
            if w in msg_content.lower():
                msg = Parser().parsestr(msg_content)
                message = ""
                try:
                    message = Get_info(msg)
                except:
                    continue
                subject = msg.get('Subject')
                date = msg.get('Date')
                replyTo = msg.get('Reply-to')
                sender = msg.get('From')
                noSend = check_no_send(sender, replyTo, noSendFile)
                if(not noSend):
                    if(replyTo):
                        if(verbose):
                            print("using replyTo:" + replyTo)
                        sendResponse(replyTo, subject, txtFile, htmlFile) 
                    elif(sender):
                        if(verbose):
                            print("using sender:" + sender)
                        sendResponse(sender, subject, txtFile, htmlFile)
                    break

    Mailbox.quit()

def check_no_send(sender, replyTo, noSendfile):
    global verbose

    if(not noSendFile):
        return False

    if(verbose):
        print("noSendfile:" + noSendfile)

    if(path.exists(noSendfile)):
        with  open(noSendFile,'r') as fp:
            for line in fp:
                testLine = line.strip().lower()
                if(verbose):
                    print("checking:" + testLine)
                if((sender and testLine in sender.lower()) or (replyTo and replyTo.lower())):
                    if(verbose):
                        print("not sending response")
                    return True
    return False

def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset


def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


def Get_info(msg):
    if (msg.is_multipart()):
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            return Get_info(part)
    if not msg.is_multipart():
        content_type = msg.get_content_type()
        if content_type == 'text/plain':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
            return content

def getFile(workDir):
    global verbose

    if(verbose):
        print("Get file from workDir:" + workDir + "/reply-files")
    if(not path.exists(workDir +  '/reply-files')):
        if(verbose):
            print("workdir does not exist!.")
        return None
    globs = glob.glob(workDir + '/reply-files/*.txt')
    rndFile = random.choice(globs)
    return rndFile

def sendResponse(to, subject, txtFile, htmlFile):
    global outbox, smtpServer, smtpPassword, smtpSSL, smtpPort, verbose
    try:
        sender = outbox 
        context = ssl.create_default_context()

        message = MIMEMultipart('alternative')
        message['Subject'] = subject
        message['From'] = sender
        message['To'] = to

        txt = ""

        if(path.exists(txtFile)):
            if(verbose):
                print("using txt file:" + txtFile)
            with  open(txtFile, "r") as f:
                txt = f.read()
        else:
            txt = """\
                    Have you seen this essay on churchofjesuschrist.org?

            https://www.churchofjesuschrist.org/topics/plural-marriage-in-kirtland-and-nauvoo?lang=eng

            The footnotes gave me a bit of a shock actually. It said that Joseph Smith married between 30-40 women, 12-14 were already married to other living men, that he was intimate with his wives (one as young as 14) and that he possibly had 2-3 children with them.

            That can't be right can it?
            """
        txtPart = MIMEText(txt,'plain')

        html =""
        if(path.exists(htmlFile)):
            if(verbose):
                print("using html file:" + htmlFile)
            with open(htmlFile,"r") as f:
                html = f.read()
        else:
            html = """\
                    Have you seen this essay on churchofjesuschrist.org?
            <br />
            <br />
            <a href='https://www.churchofjesuschrist.org/topics/plural-marriage-in-kirtland-and-nauvoo?lang=eng'>https://www.churchofjesuschrist.org/topics/plural-marriage-in-kirtland-and-nauvoo</a>
            <br/>
            <br/>
            The footnotes gave me a bit of a shock actually. It said that Joseph Smith married between 30-40 women, 12-14 were already married to other living men, that he was intimate with his wives (one as young as 14) and that he possibly had 2-3 children with them.
            <br />   
            <br />
            <b><i>That can't be right can it?</i></b>
            """

        htmlPart = MIMEText('<div dir="auto">' + html + '</div>','html')
        message.attach(txtPart)
        message.attach(htmlPart)
        with smtplib.SMTP_SSL(smtpServer,smtpPort,context=context) as server:
            server.login(sender,smtpPassword)
            server.sendmail(sender, to, message.as_string())
    except Exception as e:
        print(e)


def usage():
    print(sys.argv[0] + " -i <inbox> -o <outbox> -p <pop3server> -s <smtpserver> --pop-port=<port> --smtp-port=<port> --pop-password=<passwprd> --smtp-password=<password> --txt-file=<optional path to text email> --html-file=<optional path to html email> --random")


if __name__ == "__main__":
    main()

