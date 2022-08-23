import json
import re
import urllib.request
import urllib.error
import boto3


def lambda_handler(event, context):

    print("==event")
    print(json.dumps(event))
    print("==body")
    print(json.dumps(json.loads(event["body"])))
    
    returnData =  {
        "statusCode": 200
    }

    token = "xxxxxxxxxx"
    
    try:
        main(event, context)

    except Exception as e:
        import traceback
        traceback.print_exc()

        #エラー通知を投げる
        sendChatId = "xxxxxx"
        errorMessage = "Forward_Message_Bot functionエラー"
        errorMessage_quote = urllib.parse.quote(errorMessage)
        
        try:
            with urllib.request.urlopen("https://api.telegram.org/bot"+token+"/sendMessage?chat_id="+sendChatId+"&text="+errorMessage_quote) as response:
                resBody = response.read()
                print(json.dumps(json.loads(resBody)))

        except urllib.error.HTTPError as e:
            print("==botNotJoinedChatroom")        
            print(e.code)
            if e.code == 400:
                pass
            else:
                raise e

    print("==returnData")
    return returnData


def main(event, context): 

    chatId = "xxxxxxxxxx"
    fromChatId = "xxxxxxxxxx"
    
    s3 = boto3.resource("s3")
    bucket = s3.Bucket("xxx")

    # JSON文字列をpythonのオブジェクトへ変換する
    body = json.loads(event["body"])
    if "channel_post" not in body:
        print("==channelPostNotInBody")
        print("==returnData")
        return
        
    print("==body.channel_post")
    print(body["channel_post"])
    
    channelPost = body["channel_post"]
    if "text" not in channelPost:
        print("==textNotInChannelPost")
        print("==returnData")
        return
    
    messageId = channelPost["message_id"]
    print("==messageId")
    print(messageId)
    
    postContents = channelPost["text"]
    print("==postContents")
    print(postContents)
    
    m1 = re.compile("(.*)(aaa|bbb|ccc|ddd|eee)", re.DOTALL).match(postContents)
    print("==m1")
    print(m1)

    if m1 == None:
        print("==noWordMatchedForForward")
        print("==returnData")
        return
        
    else:
        print("==matched")
        
        #メッセージをチャンネルからグループへ転送する
        with urllib.request.urlopen("https://api.telegram.org/bot"+token+"/forwardMessage?chat_id="+chatId+"&from_chat_id="+fromChatId+"&message_id="+str(messageId)+"&disable_notification=true") as response:
            resBody = response.read()
            print(resBody)
            
            # JSON文字列をpythonのオブジェクトへ変換する
            resBody = json.loads(resBody)
            if "ok" not in resBody:
                print("==forwardMessageError")
                print("==returnData")
                return
            
            print("==resBody.message")
            print(resBody["ok"])
            
            okBoolean = resBody["ok"]
            if okBoolean == False:
                print("==okBoolean")
                print(okBoolean)
                print("==returnData")
                return
            
            forwardedMessageId = resBody["result"]["message_id"]
            print("==forwardedMessageId")
            print(forwardedMessageId)
        
    m2 = re.compile("(.*)(aaa)", re.DOTALL).match(postContents)
    print("==m2")
    print(m2)

    if m2 == None:
        print("==noWordMatchedForPin")
        print("==returnData")
        return
        
    else:
        print("==matched")

        #転送してきたメッセージをピン止めする
        with urllib.request.urlopen("https://api.telegram.org/bot"+token+"/pinChatMessage?chat_id="+chatId+"&message_id="+str(forwardedMessageId)+"&disable_notification=true") as response:
            resBody = response.read()
            print(resBody)
            
            resBody = json.loads(resBody)
            if "ok" not in resBody:
                print("==pinMessageError")
                print("==returnData")
                return
            
            print("==resBody.message")
            print(resBody["ok"])
            
            resultBoolean = resBody["result"]
            if resultBoolean == False:
                print("==resultBoolean")
                print(resultBoolean)
                return
            
        #ピン止めしたよメッセージを削除する
        pinnedMessageId = forwardedMessageId
        toBeDeletedMessageId = pinnedMessageId +1
        
        try:
            with urllib.request.urlopen("https://api.telegram.org/bot"+token+"/deleteMessage?chat_id="+chatId+"&message_id="+str(toBeDeletedMessageId)) as response:
                resBody = response.read()
                print(resBody)
                print("==messageDeleted")
            
        except urllib.error.HTTPError as e:
            print("==except")        
            print(e.code)
            if e.code == 400:
                pass
            else:
                raise e
        
        
        #前にピン止めされていたメッセージのピンを外す
        with urllib.request.urlopen("https://api.telegram.org/bot"+token+"/getChat?chat_id="+chatId) as response:
            resBody = response.read()
            print("==resBody.message")
            print(resBody)
            
            # JSON文字列を、pythonのオブジェクトへ変換する
            resBody = json.loads(resBody)
            
            okBoolean = resBody["ok"]
            print("==resBody['ok']")
            print(resBody["ok"])
            
            if okBoolean == False:
                print("==okBoolean")
                print(okBoolean)
                return
            
            mostRecentPinnedMessage = resBody["result"]["pinned_message"]["message_id"]
            print("==mostRecentPinnedMessage")
            print(mostRecentPinnedMessage)
            
            pinnedBy = resBody["result"]["pinned_message"]["from"]["id"]
            print("==pinnedBy")
            print(pinnedBy)
            
            
        #保存されていたpinnedMessageIdを呼び出してtoBeUnpinnedMessageIdに入れる
        # read from s3
        bucket.download_file("xxx.txt", "/tmp/xxx-download.txt")
        
        with open("/tmp/xxx-download.txt", mode="r") as f:
            toBeUpinnedMessageId = f.read()
            print("==toBeUpinnedMessageId")
            print(toBeUpinnedMessageId)

        # 特定のuserのピン留めはunpinしない
        if pinndBy == xxx or pinndBy == yyy:
            pass
        else:
            try:
                with urllib.request.urlopen("https://api.telegram.org/bot"+token+"/unpinChatMessage?chat_id="+chatId+"&message_id="+str(toBeUpinnedMessageId)+"&disable_notification=true") as response:
                    resBody = response.read()
                    print(resBody)
                    print("==messageUnpinned")
                    
                    #forwardedMessegeIdを保存する
                    # write to s3
                    with open("/tmp/test.txt", mode="w") as f:
                        f.write(str(pinnedMessageId))
                    bucket.upload_file("/tmp/test.txt", "xxx_pinnedMessageId.txt")                    
                    return
                
            except urllib.error.HTTPError as e:
                print("==except")        
                print(e.code)
                #forwardedMessegeIdを保存する
                # write to s3
                with open("/tmp/test.txt", mode="w") as f:
                    f.write(str(pinnedMessageId))
                bucket.upload_file("/tmp/test.txt", "xxx_pinnedMessageId.txt")
                if e.code == 400:
                    return
                else:
                    raise e
