import requests
import json
from requests.auth import HTTPBasicAuth
from base64 import b64encode
from datetime import datetime

    
def pay():
    """ registers a business """
    consumer_key = 'ogBEljyvnKUgUQYyyBDzD1QQqsiQUgxRFI2RrjGramfqv0Qs'
    consumer_secret = '5kZfOqrXAfWFMcBB2hZtNbu4hGwrEWrCrIyWhWWjJ9z85R4lCJtcMwNUAWsE8k0L'


    phone_number = +254743966928
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer bLEI4EktouoZDUecyaZ16PQTI1Y6'
    }

    time_stamp = datetime.now().strftime("%Y%m%d%H%M%S")
    password = "174379" + "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919" + time_stamp
    pwd = b64encode(password.encode("utf-8")).decode("utf-8")
    
    payload = {
    "BusinessShortCode": 174379,
    "Password": pwd,
    "Timestamp": time_stamp,
    "TransactionType": "CustomerPayBillOnline",
    "Amount": 1,
    "PartyA": phone_number,
    "PartyB": 174379,
    "PhoneNumber": phone_number,
    "CallBackURL": "https://mydomain.com/path",
    "AccountReference": "CompanyXLTD",
    "TransactionDesc": "Payment of X" 
    }
    payload_json = json.dumps(payload)
    response = requests.request("POST", 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', headers = headers, data = payload_json)
    print(response.text.encode('utf8'))
    


if __name__ == '__main__':
    pay()