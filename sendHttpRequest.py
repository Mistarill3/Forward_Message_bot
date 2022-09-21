import json
import urllib.parse
import urllib.request
import urllib.error


def sendMessage(token, chatId, messageText):
    print("==startSendHttpRequest.SendMessage")

    messageText_quote = urllib.parse.quote(messageText)
    url = "https://api.telegram.org/bot"+token+"/sendMessage?chat_id="+str(chatId)+"&text="+messageText_quote
    try:
        with urllib.request.urlopen(url) as response:
            print("==sendMessage")
            
            resBody = response.read()
            resBody_json = json.loads(resBody)
            print("==resBody_json")
            print(json.dumps(resBody_json))
            
            print("==endSendHttpRequest.SendMessage")
            return resBody_json
        
    except urllib.error.HTTPError as e:
        print("==except")        
        print(e.code)
        if e.code == 400:
            print("==userNotFoundInChatroom")
            print("==returnData")
            return
        elif e.code == 404:
            print("==wrongChatIdOrToken?")
            print("==returnData")
            return
        else:
            raise e



def deleteMessage(token, chatId, messageId):
    print("==startSendHttpRequest.DeleteMessage")

    url = "https://api.telegram.org/bot"+token+"/deleteMessage?chat_id="+str(chatId)+"&message_id="+str(messageId)
    try:
        with urllib.request.urlopen(url) as response:
            print("==deleteMessage")
            resBody = response.read()
            print(resBody)
            
            print("==endSendHttpRequest.DeleteMessage")
            return
        
    except urllib.error.HTTPError as e:
        print("==except")        
        print(e.code)
        if e.code == 400:
            print("==userNotFoundInChatroom")
            print("==returnData")
            return
        elif e.code == 404:
            print("==wrongChatIdOrToken?")
            print("==returnData")
            return
        else:
            raise e



def forwardMessage(token, chatId, fromChatId, messageId):
    print("==startSendHttpRequest.ForwardMessage")

    url = "https://api.telegram.org/bot"+token+"/forwardMessage?chat_id="+str(chatId)+"&from_chat_id="+fromChatId+"&message_id="+str(messageId)+"&disable_notification=true"
    try:
        with urllib.request.urlopen(url) as response:
            print("==forwardMessage")
            
            resBody = response.read()
            resBody_json = json.loads(resBody)
            print("==resBody_json")
            print(json.dumps(resBody_json))
            
            print("==endSendHttpRequest.ForwardMessage")
            return resBody_json
        
    except urllib.error.HTTPError as e:
        print("==except")        
        print(e.code)
        if e.code == 400:
            print("==userNotFoundInChatroom")
            print("==returnData")
            return
        elif e.code == 404:
            print("==wrongChatIdOrToken?")
            print("==returnData")
            return
        else:
            raise e



def pinChatMessage(token, chatId, messageId):
    print("==startSendHttpRequest.PinChatMessage")

    url = "https://api.telegram.org/bot"+token+"/pinChatMessage?chat_id="+str(chatId)+"&message_id="+str(messageId)+"&disable_notification=true"
    try:
        with urllib.request.urlopen(url) as response:
            print("==pinChatMessage")
            resBody = response.read()
            print(resBody)
            
            print("==endSendHttpRequest.PinChatMessage")
            return
        
        
    except urllib.error.HTTPError as e:
        print("==except")        
        print(e.code)
        if e.code == 400:
            print("==userNotFoundInChatroom")
            print("==returnData")
            return
        elif e.code == 404:
            print("==wrongChatIdOrToken?")
            print("==returnData")
            return
        else:
            raise e



def unpinChatMessage(token, chatId, messageId):
    print("==startSendHttpRequest.UnpinChatMessage")

    url = "https://api.telegram.org/bot"+token+"/unpinChatMessage?chat_id="+str(chatId)+"&message_id="+str(messageId)+"&disable_notification=true"
    try:
        with urllib.request.urlopen(url) as response:
            print("==unpinChatMessage")
            resBody = response.read()
            print(resBody)
            
            print("==endSendHttpRequest.UnpinChatMessage")
            return
        
    except urllib.error.HTTPError as e:
        print("==except")        
        print(e.code)
        if e.code == 400:
            print("==userNotFoundInChatroom")
            print("==returnData")
            return
        elif e.code == 404:
            print("==wrongChatIdOrToken?")
            print("==returnData")
            return
        else:
            raise e



def getChat(token, chatId):
    print("==startSendHttpRequest.GetChat")

    url = "https://api.telegram.org/bot"+token+"/getChat?chat_id="+chatId
    try:
        with urllib.request.urlopen(url) as response:
            print("==getChat")
            
            resBody = response.read()
            resBody_json = json.loads(resBody)
            print("==resBody_json")
            print(json.dumps(resBody_json))
            
            print("==endSendHttpRequest.GetChat")            
            return resBody_json
        
    except urllib.error.HTTPError as e:
        print("==except")        
        print(e.code)
        if e.code == 400:
            print("==userNotFoundInChatroom")
            print("==returnData")
            return
        elif e.code == 404:
            print("==wrongChatIdOrToken?")
            print("==returnData")
            return
        else:
            raise e



def getChatMember(token, chatId, userId):
    print("==startSendHttpRequest.GetChatMember")

    url = "https://api.telegram.org/bot"+token+"/getChatMember?chat_id="+str(chatId)+"&user_id="+str(userId)
    try:
        with urllib.request.urlopen(url) as response:
            print("==getChatMember")
            
            resBody = response.read()
            resBody_json = json.loads(resBody)
            print("==resBody_json")
            print(json.dumps(resBody_json))
            
            print("==endSendHttpRequest.GetChatMember")            
            return resBody_json
        
    except urllib.error.HTTPError as e:
        print("==except")        
        print(e.code)
        if e.code == 400:
            resBody_json = {"ok":False,"error_code":400,"description":"Bad Request: user not found"}

            print("==userNotFoundInChatroom")
            print("==endSendHttpRequest.GetChatMember")
            return resBody_json
            
        elif e.code == 404:
            print("==wrongChatIdOrToken?")
            print("==returnData")
            return
        else:
            raise e
