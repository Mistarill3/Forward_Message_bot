import json
import os
import urllib.parse
import urllib.request
import urllib.error
import boto3
import botocore
import re

import monitorPinnedMessage
import sendHttpRequest
import s3FileOperation


def ypsilon_handler(event, context, token):  
    print("==startYpsilonHandler")
    
    #chatId = os.environ["TELEGRAM_CHAT_ID_FOR_TEST"]
    chatId = os.environ["TELEGRAM_CHAT_ID"]

    #fromChatId = os.environ["TELEGRAM_CHANNEL_ID_FOR_TEST"]
    fromChatId = os.environ["TELEGRAM_CHANNEL_ID"]

    body = json.loads(event["body"])
    if "channel_post" in body:
        channelPost = body["channel_post"]
        print("==channelPost")
        
        if "text" in channelPost:
            main(event, context, token, channelPost, chatId, fromChatId)
            print("==returnData")
            return
        else:
            print("==channelPostWithoutText")
            print("==returnData")
            return
        
    elif "edited_channel_post" in body:
        channelPost = body["edited_channel_post"]
        print("==editedChannelPost")
        
        if "text" in channelPost:
            main(event, context, token, channelPost, chatId, fromChatId)
            print("==returnData")
            return
        else:
            print("==channelPostWithoutText")
            print("==returnData")
            return
        
    elif "message" in body:
        if "pinned_message" in body["message"]:
            print("==pinnedMessage")
            
            pinnedIn = body["message"]["pinned_message"]["chat"]["id"]
            pinnedBy_Id = body["message"]["from"]["id"]
            pinnedBy_Username = body["message"]["from"]["username"]
            pinnedMessageId = body["message"]["pinned_message"]["message_id"]
            
            monitorPinnedMessage.monitorPinnedMessage(pinnedIn, pinnedBy_Id, pinnedBy_Username, pinnedMessageId)
            print("==returnData")
            return        
        
    else:
        print("==NeitherchannelPostNorPinnedMessage")
        print("==returnData")
        return
 
 
    print("==endYpsilonHandler")



def main(event, content, token, channelPost, chatId, fromChatId):
    print("==startMain")

    messageId = channelPost["message_id"]
    print("==messageIdInChannel")
    print(messageId)
    
    postContents = channelPost["text"]
    print("==postContents")

    #現時点で最新のピン留めのmessage_idを取得する
    #暫定運用
    resBody_json = sendHttpRequest.getChat(token, chatId)

    mostRecentPinnedMessage = resBody_json["result"]["pinned_message"]["message_id"]
    print("==mostRecentPinnedMessageInChat")
    print(mostRecentPinnedMessage)


    #特定の語句が含まれる投稿のみを転送する
    m1 = re.compile("(.*)(aaa|bbb|ccc|ddd|eee)", re.DOTALL).match(postContents)
    print("==m1")
    print(m1)

    if m1 == None:
        print("==noWordMatchedForForward")
        print("==returnData")
        return
        
    else:
        print("==m1Matched")
        
        resBody_json = sendHttpRequest.forwardMessage(token, chatId, fromChatId, messageId)
       
        pinnedMessageId = resBody_json["result"]["message_id"]
        print("==pinnedMessageId")
        print(pinnedMessageId)

  
    #特定の語句が含まれる投稿のみをピン留めする
    m2 = re.compile("(.*)(Fevgames Anmeldung)", re.DOTALL).match(postContents)
    print("==m2")
    print(m2)

    if m2 == None:
        print("==noWordMatchedForPin")
        print("==returnData")
        return
        
    else:
        print("==m2Matched")
        messageId = pinnedMessageId
        toBeDeletedMessageId = pinnedMessageId +1
        
        resBody_json = sendHttpRequest.pinChatMessage(token, chatId, messageId)


    #ピン留めしたよメッセージを削除する
    # monitorPinnedMessage.pyに移植予定
    #メッセージIDは記録しといて一括でunpinする
    userId4 = os.environ["TELEGRAM_USER_ID_4"]
    pinnedBy_Id = "1"
    
    if pinnedBy_Id != userId4:
        messageId = toBeDeletedMessageId
        sendHttpRequest.deleteMessage(token, chatId, messageId)


    #前にピン留めされていたメッセージのmessage_idを取得する
    #(新しいpinnedMessageIdを書き込む前に今の値を読み出して保存しておく)
    #将来的にはJSONファイルでの読み書きに移行
    fileName = "octane-forward-message-bot_pinnedMessageId.txt"
    toBeUnpinnedMessageId = s3FileOperation.downloadAndReadFile(fileName)
    print("==toBeUnpinnedMessageId")
    print(toBeUnpinnedMessageId)


    #前にピン留めされていたメッセージのピンを外す
    messageId = toBeUnpinnedMessageId
    sendHttpRequest.unpinChatMessage(token, chatId, messageId)


    #ピン留めしたメッセージのmessage_idを保存する2(as text)
    #暫定運用
    newFileContents = str(pinnedMessageId)
    print("==newFileContents")
    print(newFileContents)
    s3FileOperation.writeAndUploadFile(newFileContents, fileName)

    print("==endMain")
    return
