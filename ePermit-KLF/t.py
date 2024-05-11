import requests
import json
from requests.auth import HTTPBasicAuth
from base64 import b64encode
from datetime import datetime


response = requests.request("POST", 'https://6401-102-166-94-145.ngrok-free.app/callback', callback_data = {
            "TransactionType": "CustomerPayBillOnline",
            "TransID": "123456789",
            "TransTime": "20240430215611",
            "TransAmount": "1",
            "BusinessShortCode": "174379",
            "BillRefNumber": "CompanyXLTD",
            "InvoiceNumber": "",
            "OrgAccountBalance": "",
            "ThirdPartyTransID": "",
            "MSISDN": "+254708051357",
            "FirstName": "John",
            "MiddleName": "Doe",
            "LastName": "Doe"
        })
print(response.text.encode('utf8'))
    


if __name__ == '__main__':
    pay()