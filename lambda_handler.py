import os
import json
import urllib.parse

import ypsilon_function
import sendHttpRequest

token = os.environ["TELEGRAM_BOT_TOKEN"]



def lambda_handler(event, context):

    print("==startLambdaHandler")
    print("==event")
    print(json.dumps(event))
    print("==body")
    print(json.dumps(json.loads(event["body"])))
    
    returnData =  {
        "statusCode": 200
    }

    try:
        ypsilon_function.ypsilon_handler(event, context, token)
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        
        #エラー通知を投げる
        chatId = os.environ["TELEGRAM_CHAT_ID_FOR_ERRORMESSAGE"]
        messageText = "forward-message-functionがエラー吐いてまーす"
        messageText_quote = urllib.parse.quote(messageText)
        sendHttpRequest.sendMessage(token, chatId, messageText_quote)

    print("==endLamdaHandler")
    print(returnData)
    return returnData
