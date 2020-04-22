# Reply to lds tools. (no pun intended)
autoresponder to things churchy

MIT License

Copyright (c) 2020 TL

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

# Why?

Still have an email account that gets "churchy" things sent to it? This will send an email to the Reply-to email address if set, else to the from address with txt, html that can be customised.

# How to

Uses two different email accounts to auto reply to the Reply-to field sent in emails. Avoids email loops. Only works with gmail ssl for now, using two different gmail accounts. The accounts have to have Less Secure app permissions turned on and no two factor enabled. 
See https://support.google.com/accounts/answer/6010255?hl=en

Change the words in the autoresponder.py file to filter on specified words. TODO: loads words from file.

Use the --txt-file=<path> --html-file=<path> to set custom messages.

run in crontab every hour on linux

crontab -e

0 * * * * <path to python3> <path to autoresponder.py> -i <pop email account> -o <smtp email account> --pop-password=<pop password> --smtp-password=<smtp password> --pop-port=995 --smtp-port=465 -p pop.gmail.com -s smtp.gmail.com
