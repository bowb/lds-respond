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

inbox = ''
popServer = ''
popPort = ''
popSSL = False
popPassword = ''
verbose = False

poplib._MAXLINE = 2147483647 
words = ['missionary','endowment','prophet','temple','indexing','priesthood','covenant','blessing','brethren','stake','ward','elder','church','lord','sacrament','ministering','saints','jesus']

def main():
    global inbox, popServer, popPort, popSSL, popPassword,  verbose

    try:
        opts, args = getopt.getopt(sys.argv[1:],"vhi:o:p:s:",["inbox=","pop=","pop-password=", "pop-port=","popSSL"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-i","--inbox"):
            inbox = arg
        elif opt in ("-p","--pop"):
            popServer = arg
        elif opt == "--pop-password":
            popPassword = arg
        elif opt == "--pop-port":
            popPort = arg
        elif opt == "popSSL":
            popSSL = True
        elif opt == "-v":
            verbose = True
        else:
            assert False, "unhandled option"

    hasrequired = True
    if(inbox == ''):
        hasrequired = False
        print("inbox is required")
    if(popServer == ''):
        hasrequired = False
        print("popserver is required")
    if(popPort == ""):
        hasrequired = False
        print("pop-port is required")
    if(popPassword == ""):
        hasrequired = False
        print("pop-password is required")

    if(not hasrequired):
        usage()
        sys.exit(2)

    if(verbose):
        print("POP_USER:" + inbox)
        print("POP_PASSWORD:" + popPassword)
        print("POP_SERVER:" + popServer)
        print("POP_PORT:" + popPort);

    Mailbox = poplib.POP3_SSL(popServer, popPort)
    Mailbox.user(inbox) 
    Mailbox.pass_(popPassword) 
    numMessages = len(Mailbox.list()[1])

    for i in range(numMessages):
        resp, lines, octets = Mailbox.retr(i+1) 
        msg_content = b'\r\n'.join(lines).decode('utf-8')
        for w in words:
            if w in msg_content.lower():
                print(msg_content)
                msg = Parser().parsestr(msg_content)
                message = Get_info(msg)
                subject = msg.get('Subject')
                date = msg.get('Date')
                replyTo = msg.get('Reply-to')
                sender = msg.get('From')
                break

    Mailbox.quit()

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

def usage():
    print(sys.argv[0] + " -i <inbox> -p <pop3server> --pop-port=<port> --pop-password=<passwprd>")


if __name__ == "__main__":
    main()

