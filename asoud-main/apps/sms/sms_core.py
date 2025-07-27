import os
import json
import requests


class SMSCoreHandler:
    @staticmethod
    def send_bulk(payload):
        headers = {
            'X-API-KEY': os.environ.get('SMS_API'),
            'Content-Type': 'application/json'
        }

        URL = "https://api.sms.ir/v1/send/" + "bulk"
        res = requests.post(URL, json=payload, headers=headers)

        return res.json()

    @staticmethod
    def send_pattern(payload):
        headers = {        
            'Content-Type': 'application/json',
            'Accept': 'text/plain',
            'x-api-key': os.environ.get('SMS_API')
        }

        URL = "https://api.sms.ir/v1/send/" + "verify"
        res = requests.post(URL, json=payload, headers=headers)
        
        return res.json()

    @staticmethod
    def send_verification_code(mobile: str, code: str):
        payload  = {
            "mobile": mobile,
            "templateId": "260323",
            "parameters": [
                {
                    "name": "code",
                    "value": code
                }
            ]
        }

        headers = {        
            'Content-Type': 'application/json',
            'Accept': 'text/plain',
            'x-api-key': os.environ.get('SMS_API')
        }
        
        URL = "https://api.sms.ir/v1/send/" + "verify"
        res = requests.post(URL, json=payload, headers=headers)
        return res.json()
        


# example bulk payload:
# payload = {
#     "lineNumber": 300000000000,
#     "messageText": "Your Text",
#     "mobiles": [
#         "Your Mobile 1",
#         "Your Mobile 2"
#     ],
#     "sendDateTime": None
# }


# example pattern payload: 
# payload = {
#     "mobile": "Mobile",
#     "templateId": "templateID",
#     "parameters": [
#         {
#             "name": "PARAMETER1",
#             "value": "000000"
#         },
#         {
#             "name": "PARAMETER2",
#             "value": "000000"    
#         }
#     ]
# }


