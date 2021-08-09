#!/usr/bin/env python3
# Import modules for CGI handling
import cgi, cgitb
import smtplib
# modules for making request to hcaptcha endpoint
import requests
import json
# Create instance of FieldStorage
form = cgi.FieldStorage()
# Get data from fields
customer_name = form.getvalue('customer_name')
customer_email = form.getvalue('customer_email')
customer_message = form.getvalue('message')
#variables for mail
sender = 'sender@example.com'
receivers = ['receiver@example.com']
#variables for hcaptcha
hcaptcha_token = form.getvalue('h-captcha-response')
hcaptcha_secret = '01234567890'

message = f"""From: Contact form <noreply@example.com>
To: You <you@example.com>
Subject: Contact form submission

Message from: {customer_name}
Email: {customer_email}
Message contents:

{customer_message}

"""

try:
    smtpObj = smtplib.SMTP('localhost')
    smtpObj.sendmail(sender, receivers, message)
except:
    print('Content-type:text/html\n\n')
    print('Error sending message')
    pass

# post to endpoint with captcha token
api_endpoint = 'https://hcaptcha.com/siteverify'
hc_data = {'response':hcaptcha_token,'secret':hcaptcha_secret}
r = requests.post(url = api_endpoint, data = hc_data)
#now parse the response from api endpoint and check for success
answer = r.text
result = json.loads(r.text)
if result['success'] == bool(1):
    pass
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
