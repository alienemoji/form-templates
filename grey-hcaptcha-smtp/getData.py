#!/usr/bin/env python3
import cgi, cgitb
import smtplib
import requests
import json
# Create instance of FieldStorage
form = cgi.FieldStorage()
# Get data from fields
customer_name = str(form.getvalue('customer_name'))
customer_email = str(form.getvalue('customer_email'))
customer_message = str(form.getvalue('message'))
# variables for mail
sender = 'noreply@yourdomain.com'
receivers = ['you@example.com']
# variables for hcaptcha
hcaptcha_token = form.getvalue('h-captcha-response')
hcaptcha_secret = '123456789'

def sendMessage():
    message = (
        f'From: Contact form <{sender}>\n'
        f'To: You <you@example.com>\n'
        f'Subject: Contact form submission\n'
        f'\n\n'
        f'Name: {customer_name}\n'
        f'Email: {customer_email}\n'
        f'------Message contents:------\n'
        f'{customer_message}\n'
        )
    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sender, receivers, message)
    except:
        print('Content-type:text/html\n\n')
        print('Error sending message')
        quit()

# post to endpoint with captcha token
api_endpoint = 'https://hcaptcha.com/siteverify'
hc_data = {'response':hcaptcha_token,'secret':hcaptcha_secret}
r = requests.post(url = api_endpoint, data = hc_data)
# now parse the response from /siteverify and check for success
answer = r.text
result = json.loads(r.text)
if result['success'] == bool(1):
    sendMessage()
else:
    print('Content-type:text/html\n\n')
    print('Please complete the captcha challenge.')
    quit()

print('Content-type:text/html')
print('')
print('')
print('<html>')
print('<head>')
print('</head>')
print('<body>')
print('<center><p>Your message has been sent. <br />You will be redirected to the home page in 5 seconds. </p></center>')
print('<script>setTimeout(function(){window.location.href = "https://example.com";}, 5000);</script>')
print('</body>')
print('</html>')
