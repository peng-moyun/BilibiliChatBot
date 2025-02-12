import time
import os, sys

import requests
import json

from bs4 import BeautifulSoup

import ChatEngineFunctions.SessionGet as SessionGet
import ChatEngineFunctions.ChatSession as ChatSession
import ChatEngineFunctions.HeaderTransfer as HeaderTransfer
import ChatEngineFunctions.ChatEngine as ChatEngine

'''
=====MAIN FUNCTION OF BILIBILI CHAT BOT=====



'''

# ==================== VARIABLES ====================

# the total time from the start of the main loop
totalTime = 0
# delta time betweem two main loop
deltaTime = 1
# time interval between two session checks
sessionCheckTime = 5

# root folder path of all the headers
headersPathRoot = os.getcwd() + '\\Headers\\'
# headers to get sessions
requestHeaders = {}

# root folder path of all the modules
modulePathRoot = os.getcwd() + '\\Modules\\'
# all the modules(ChatBehaviour objects)
chatBehaviours = []

# root folder path of other program data
dataPathRoot = os.getcwd() + '\\Data\\'


# the latest session's time stamp recorded in the last updated
latestSessionTS = 0
# stores all the chat sessions in the list
allChatSessions = []

# the user's UID

selfUid = ''


# ==================== PROGRAM INITIALIZE ====================

# load all the headers in the Headers folder
# the headers file should be saved in the Header.txt
def LoadHeaders():
    global headersPathRoot
    global requestHeaders

    headersFileLits = os.listdir(headersPathRoot)

    # load header
    if 'Header.txt' in headersFileLits:
        with open(headersPathRoot + 'Header.txt', 'r') as sessionHeaderFile:
            requestHeaders = HeaderTransfer.TransferHeader(sessionHeaderFile.read())
            print(requestHeaders)

def LoadUID():
    global dataPathRoot
    global selfUid

    # get all the data file in the Data folder
    dataFileList = os.listdir(dataPathRoot)

    # load user's UID
    if 'SelfUID.txt' in dataFileList:
        with open(dataPathRoot + 'SelfUID.txt', 'r') as uidFile:
            selfUid = int(uidFile.read())

# load all the modules in the Modules folder
def LoadModules():
    global modulePathRoot
    global chatBehaviours

    # get all the module file in the Modules folder
    moduleList = os.listdir(modulePathRoot)

    # ergodic all the module file name and load the module
    for moduleFileName in moduleList:
        if moduleFileName[len(moduleFileName) - 3:] == '.py':
            # add the path to sys in order to import module dynamically
            sys.path.append(modulePathRoot)
            module = __import__(moduleFileName[:len(moduleFileName) - 3])
            
            if hasattr(module, 'chatBehaviour'):
                chatBehaviours.append(getattr(module, 'chatBehaviour'))

# load the lastes session's time stamp into 'latestSessionTS'
def LoadLatestSessionTS():
    global dataPathRoot
    global latestSessionTS

    # get all the data file in the Data folder
    dataFileList = os.listdir(dataPathRoot)

    # load latest chat session's time stamp
    if 'LatestSessionTS.txt' in dataFileList:
        with open(dataPathRoot + 'LatestSessionTS.txt', 'r') as sessionTSFile:
            latestSessionTS = int(sessionTSFile.read())

# save the latest session's time stamp into 'LatestSessionTS.txt'
def SaveLatestSessionTS():
    global latestSessionTS
    global dataPathRoot

    # get all the data file in the Data folder
    dataFileList = os.listdir(dataPathRoot)

    # load latest chat session's time stamp
    if 'LatestSessionTS.txt' in dataFileList:
        with open(dataPathRoot + 'LatestSessionTS.txt', 'w') as sessionTSFile:
            sessionTSFile.write(str(latestSessionTS))

# Initialize all the ChatBehaviour, including setup request headers, set data path
def ChatBehaviourInitialize():
    global requestHeaders
    global dataPathRoot

    # set headers for all the ChatBehaviour
    for chatBehaviour in chatBehaviours:
        chatBehaviour.headers = requestHeaders
    
    for chatBehaviour in chatBehaviours:
        chatBehaviour.dataPath = dataPathRoot
    
    for chatBehaviour in chatBehaviours:
        chatBehaviour.UID = selfUid



# ==================== LIFE CYCLE FUNCTIONS ====================


# check all the new sessions happens after time 'latestSessionTS'
# return a list of all the new sessions
# all the elements in the list are the same as that in SessionGet.GetSession(header)[0] returns

def CheckNewSessions():
    # 假设 selfUid 是你已定义的当前用户ID
    selfUid = 'your_user_id_here'

    # 示例数据结构，用实际获取的数据替换
    allChatSessions = [
        {
            "last_msg": {
                "timestamp": 1620202020,
                "sender_uid": 123456
            },
            "other_key": "other_value"
        },
        {
            "last_msg": {
                "timestamp": 1620303030,
                "sender_uid": 654321
            },
            "other_key": "other_value"
        }
    ]

    latestSessionTS = 0  # 你可以根据需要初始化这个变量

    newChatSessionsList = []
    for session in allChatSessions:
        try:
            print(f"Debug: session = {session}")  # 调试输出
            last_msg = session['last_msg']
            timestamp = last_msg['timestamp']
            sender_uid = last_msg['sender_uid']

            if timestamp > latestSessionTS and str(sender_uid) != str(selfUid):
                newChatSessionsList.append(session)

        except KeyError as e:
            print(f"KeyError: {e} in session {session}")
        except TypeError as e:
            print(f"TypeError: {e} in session {session}")

    return newChatSessionsList




# ==================== MAIN FUNCTION ====================

def Loop():
    global requestHeaders
    global allChatSessions
    global sessionCheckTime

    # 用三引号定义 cookies 字符串，避免引号问题
    cookies = '''i-wanna-go-back=-1; b_ut=7; header_theme_version=CLOSE; CURRENT_FNVAL=4048; PVID=1; buvid_fp_plain=undefined; buvid3=0F584BD5-3446-06DC-4E58-488185FA23D601373infoc; b_nut=1703577601; _uuid=6232C7D7-DCEB-C8C10-F4B4-23BBF263354A01695infoc; buvid4=304CD76F-0F21-4156-3FA3-43A0FD67373902292-023122608-5V%2BS1%2B6ZgMsXijxDBM5%2BBg%3D%3D; rpdid=|(uYmmkuuRml0J'u~|Jl~~Y|k; enable_web_push=DISABLE; LIVE_BUVID=AUTO9417091739995791; hit-dyn-v2=1; DedeUserID=525446160; DedeUserID__ckMd5=43b2f4e8e9abbcfd; FEED_LIVE_VERSION=V_WATCHLATER_PIP_WINDOW3; CURRENT_BLACKGAP=0; bp_video_offset_525446160=923859611551793160; SESSDATA=86cdce96%2C1731481810%2Cc9ce7%2A52CjDi53A-Dj_YJL1GoB6_ow6YlpoRT2EJsoHnB8lj7_ySTOfbb2al7iEzFFS3inysK3wSVnY1eTR0NVl4OEdNTXRGNGlaV3FHc20wSmNSLVVyck9UOFVtRnhRVXJqT2dZSUdtZElkVWxfYXYzeWVnSlh2SjRDaTRfcmlhUDNBVDRRY2w4RmJteXN3IIEC; bili_jct=32474b142f3d5022127ce88dbaedf23f; sid=5qkpwqm6; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTY0NTY3NDgsImlhdCI6MTcxNjE5NzQ4OCwicGx0IjotMX0.Lh0EHstLRhuiXzpvNCQtF9oK93ESQXDnCZHFwIeBNYk; bili_ticket_expires=1716456688; fingerprint=367bded1043e9edd3ed6128297e8a666; home_feed_column=4; b_lsid=BBB10151D_18FA01D474D; bsource=search_bing; buvid_fp=367bded1043e9edd3ed6128297e8a666; bmg_af_switch=1; bmg_src_def_domain=i0.hdslb.com; bp_t_offset_525446160=934325476226236439; browser_resolution=484-2672'''

    requestHeaders = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36 Edg/123.0.0.0',
        'Cookie': cookies
    }
    
    # run the Update() of each ChatBehaviour
    for chatBehaviour in chatBehaviours:
        chatBehaviour.Update()
    
    # get all the sessions every 10 second
    if (totalTime % sessionCheckTime == 0):
        allChatSessions = SessionGet.GetSession(requestHeaders)[0]
        print('Got new session')
        for chatBehaviour in chatBehaviours:
            chatBehaviour.chatSessions = allChatSessions
    
    # check if there's new session, if so call the OnMessageReceive()
    newChatSessionsList = CheckNewSessions()
    # pass all the new chat sessions to ChatBehaviour
    for chatBehaviour in chatBehaviours:
        chatBehaviour.newChatSessions = newChatSessionsList
    if len(newChatSessionsList) != 0:
        for chatBehaviour in chatBehaviours:
            chatBehaviour.OnMessageReceive()

    # run the LateUpdate() of each ChatBehaviour
    for chatBehaviour in chatBehaviours:
        chatBehaviour.LateUpdate()

# the main function of the behaviour
def Main():
    global deltaTime
    global totalTime
    global latestSessionTS
    global requestHeaders

    # load all the headers
    LoadHeaders()
    # load the lastest session's time stamp
    LoadLatestSessionTS()
    # load the user's UID
    LoadUID()

    # load all the modules using reflect
    LoadModules()

    # initialize all the ChatBehaviour class
    ChatBehaviourInitialize()

    # run Activate() for all ChatBehaviours
    for chatBehaviour in chatBehaviours:
        chatBehaviour.Activate()
    
    # main loop of the program
    while True:
        Loop()

        time.sleep(deltaTime)
        totalTime += deltaTime

if __name__ == "__main__":
    Main()