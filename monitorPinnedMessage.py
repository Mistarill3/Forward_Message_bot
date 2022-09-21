import json
import os
import boto3
import botocore

import s3FileOperation


s3 = boto3.resource("s3")
bucket = s3.Bucket("for-octane-bot")


def monitorPinnedMessage(pinnedIn, pinnedBy_Id, pinnedBy_Username, pinnedMessageId):
    print("==startMonitorPinnedMessage")

    userId1 = os.environ["TELEGRAM_USER_ID_1"]
    userId2 = os.environ["TELEGRAM_USER_ID_2"]
    userId3 = os.environ["TELEGRAM_USER_ID_3"]

    if pinnedBy_Id == userId1 or pinnedBy_Id == userId2 or pinnedBy_Id == userId3:
        print("==pinndByExceptionUser")
        print("==returnData")
        return
        
    else:
        newPinnedMessage = {
            "chat_id":pinnedIn,
            "pinnedUser_UserId":pinnedBy_Id,
            "pinnedUser_UserName":pinnedBy_Username,
            "pinnedMessageId":pinnedMessageId
        }
        
        print("==newPinnedMessage")
        print(newPinnedMessage)


    fileName = "monitor-pinnedMessage-bot_pinnedMessageList.json"
    downloadedFileName = "monitor-pinnedMessage-bot_pinnedMessageList-download.txt"
    
    pinnedMessageList = s3FileOperation.downloadAndReadFile(fileName)
    print("==openPinnedMessageList")

    pinnedMessageList_dict = json.loads(pinnedMessageList)
    print("==convertToPinnedMessageList_dict")
    
    
    pinnedMessageList_dict.append(newPinnedMessage)
    print("==appendNewPinnedMessage")
    print(json.dumps(pinnedMessageList_dict))
    

    newFileContents = json.dumps(pinnedMessageList_dict, ensure_ascii=False, indent=4)
    print("==newFileContents")
    #print(newFileContents)
    s3FileOperation.writeAndUploadFile(newFileContents, fileName)

    print("==endMonitorPinnedMessage")
    return
