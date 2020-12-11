import requests
import json
from urllib.request import urlopen, Request
import ssl
from multiprocessing import Lock
from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText
import sys
import sched, time
from datetime import datetime


smtpConfig = {
    "server":"smtp.sendgrid.net",
    "ports":465,
    "username":"apikey",
    "password":"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",
    "sender":"rohit@rthakur.com"
}

numOfEmailsSent = 0
s = sched.scheduler(time.time, time.sleep)



def sendEmail():
    global numOfEmailsSent
    # typical values for text_subtype are plain, html, xml
    text_subtype = 'plain'


    content="""\
    Bestbuy has 3080s in stock right now!!
    """

    subject="3080s are in stock!"
    try: 
        msg = MIMEText(content, text_subtype)
        msg['Subject']=       subject
        msg['From']   = smtpConfig["sender"] # some SMTP servers will do this automatically, not all


        conn = SMTP(smtpConfig["server"])
        conn.login(smtpConfig["username"], smtpConfig["password"])
        try:
            conn.sendmail(smtpConfig["sender"], "rohitt@gmail.com", msg.as_string())
            numOfEmailsSent+=1
        finally:
            conn.quit()
    except:
        sys.exit( "mail failed; %s" % "CUSTOM_ERROR" ) # give an error message



def pullPage(sc):
    
    found = False
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
    r = requests.get("https://www.bestbuy.ca/ecomm-api/availability/products?accept=application%2Fvnd.bestbuy.simpleproduct.v1%2Bjson&accept-language=en-CA&locations=937%7C943%7C956%7C223%7C237%7C965%7C925%7C985%7C931%7C62%7C200%7C927%7C932%7C977%7C949%7C203%7C617%7C57%7C959%7C613%7C938%7C795%7C916%7C544%7C910%7C954%7C207%7C202%7C926&postalCode=L3P&skus=14953248%7C15084753%7C14954116%7C14961449%7C14950588%7C14953249%7C15000077",headers = headers)
    r.encoding='utf-8-sig'
    bbyList = json.loads(r.text)

    now = datetime.now()
    for x in bbyList["availabilities"]:
        if (not x["shipping"]["purchasable"]):
            print(now.strftime("%d/%m/%Y %H:%M:%S")+": "+"Found following sku in stock:" + x["sku"])
            sendEmail()
            found=True
            break

    if (not found):
        
        print(now.strftime("%d/%m/%Y %H:%M:%S")+": "+"Nothing in stock.")

    if (numOfEmailsSent < 10):
        s.enter(60, 1, pullPage,(sc,))





if __name__ == "__main__":
    s.enter(1, 1, pullPage, (s,))
    s.run()
        


    