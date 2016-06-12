# -*- coding: utf-8 -*-
#from temp import *
from http.client import HTTPConnection
from http.server import BaseHTTPRequestHandler, HTTPServer
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import urllib

conn = None
server = "openAPI.seoul.go.kr:8088"
Key = '507546756775376939356151527963'

host = "smtp.gmail.com"
port = "587"



def connectOpenAPIServer():
    global conn, server
    conn = HTTPConnection(server)
    


#호선별 역검색

def userURIBuilder(server,**user):
    global Key
    print("1~9: 1~9호선, I: 인천1호선, K: 경의중앙선, B: 분당선, A: 공항철도, G: 경춘선, S:신분당선, SU:수인선")
    n = input("알고싶은 지하철 호선을 선택해주세요:")
    str = "http://" + server + "/"+Key+"/xml/SearchSTNBySubwayLineService/1/100/"+n+"/"
    return str
    
    
def UndergroundAllsearch():
    global server, regKey, conn
    if conn == None :
        connectOpenAPIServer()
    uri = userURIBuilder(server)
    conn.request("GET", uri)
    req = conn.getresponse()
    if int(req.status) == 200 :
        print("지하철 데이터를 가져왔습니다")
        return extractUndergroundData(req.read())
    else:
        print ("실패했습니다. 다시 시도해보세요")
        return None
        
def extractUndergroundData(strXml):
    from xml.etree import ElementTree
    tree = ElementTree.fromstring(strXml)
    itemElements = tree.getiterator("row")
    for item in itemElements:
        CD = item.find("STATION_CD")
        NM = item.find("STATION_NM")
        if len(NM.text) > 0 :
           print("역코드 :",CD.text,"역이름:",NM.text)
           print("-------------------------------------")
           
           
# 메일보내기           
           
def SendMail():
    global host, port
    title = str(input ('메일 제목 :'))
    senderAddr = str(input ('보내는 메일 :'))
    passwd = str(input ('비밀번호 입력 :'))
    recipientAddr = str(input ('받는 메일 :'))
    msgtext = str(input ('메일 내용 :'))
    
    msg = MIMEMultipart('alternative') 
    msg['Subject'] = title
    msg['From'] = senderAddr
    msg['To'] = recipientAddr
    msgPart = MIMEText(msgtext, 'plain')
    msg.attach(msgPart)
    
    print ("connect smtp server ... ")
    s = smtplib.SMTP(host,port)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(senderAddr, passwd)    
    s.sendmail(senderAddr , [recipientAddr], msg.as_string())
    s.close()
    
    print ("메일이 보내졌습니다!!")
    



#지하철 시간표
    
def timeURIBuilder(server,**user):
    global Key
    #http://openAPI.seoul.go.kr:8088/(인증키)/xml/SearchSTNTimeTableByIDService/1/5/0151/1/1/
    n = input("알고싶은 역의 역코드를 입력해주세요 : ")
    m = input("요일을 선택해주세요(1:평일 2:토요일 3:일요일,빨간날) : ")
    o = input("상/하행선을 입력해주세요(1:상행선 2:하행선) : ")
    str = "http://" + server + "/"+Key+"/xml/SearchSTNTimeTableByIDService/1/100/"+n+"/"+m+"/"+o+"/"
    return str
    
    
    
    
def TimeList():
    global server, Key, conn
    if conn == None :
        connectOpenAPIServer()
    uri = timeURIBuilder(server)
    conn.request("GET", uri)
    
    req = conn.getresponse()
    
    if int(req.status) == 200 :
        print("지하철 데이터를 가져왔습니다")
        return extractTimeListdData(req.read())
    else:
        print ("실패했습니다. 다시 시도해보세요")
        return None
        
def extractTimeListdData(strXml):
    from xml.etree import ElementTree
    tree = ElementTree.fromstring(strXml)
    itemElements = tree.getiterator("row")
    for item in itemElements:
        CD = item.find("STATION_CD")
        NM = item.find("STATION_NM")
        AT = item.find("ARRIVETIME")
        LT = item.find("LEFTTIME")
        SS = item.find("SUBWAYSNAME")
        SE = item.find("SUBWAYENAME")

        if len(NM.text) > 0 :
           print("역코드 :",CD.text,"역이름:",NM.text)
           print("도착시간:",AT.text,"출발시간",LT.text,"시발역",SS.text,"종착역",SE.text)
           print("---------------------------------------------------------------------")
           
           
           
# 개별적인 지하철 검색           
           
def OneURIBuilder(server,**user):
    global Key
    n = input("알고싶은 지하철 이름(역을 제외하고 입력해주세요 예:신도림 ):")
    f = urllib.parse.quote(n)
    str = "http://" + server + "/"+Key+"/xml/SearchInfoBySubwayNameService/1/5/"+f+"/"
    return str           
           
def UndergroundOnesearch():
    global server, Key, conn
    if conn == None :
        connectOpenAPIServer()
    uri = OneURIBuilder(server)
    conn.request("GET", uri)
    req = conn.getresponse()
    if int(req.status) == 200 :
        print("지하철 데이터를 가져왔습니다!")
        return extractOneData(req.read())
    else:
        print ("실패했습니다. 다시 시도해보세요")
        return None
        
def extractOneData(strXml):
    from xml.etree import ElementTree
    tree = ElementTree.fromstring(strXml)
    itemElements = tree.getiterator("row")
    for item in itemElements:
        CD = item.find("STATION_CD")
        NM = item.find("STATION_NM")
        LN = item.find("LINE_NUM")
        print("--------------------------------------------------------")
        print(NM.text,"는",LN.text,"의 역이면 역코드는 ",CD.text,"입니다.")
        print("--------------------------------------------------------")

       

#지하철 위처검색


def MapURIBuilder(server,**user):
    global Key
    #http://openAPI.seoul.go.kr:8088/(인증키)/xml/SearchLocationOfSTNByIDService/1/5/0335/
    n = input("알고싶은 지하철 역코드:")
    str = "http://" + server + "/"+Key+"/xml/SearchLocationOfSTNByIDService/1/5/"+n+"/"
    return str 


           
def undergroundMap():
    global server, Key, conn
    if conn == None :
        connectOpenAPIServer()
    uri = MapURIBuilder(server)
    conn.request("GET", uri)
    
    req = conn.getresponse()
    
    if int(req.status) == 200 :
        print("지하철 데이터를 가져왔습니다")
        return MapData(req.read())
    else:
        print ("실패했습니다. 다시 시도해보세요")
        return None
    
        
def MapData(strXml):
    
    from xml.etree import ElementTree
    tree = ElementTree.fromstring(strXml)
    itemElements = tree.getiterator("row")
    for item in itemElements:
        CD = item.find("STATION_CD")
        NM = item.find("STATION_NM")
        LB = item.find("LINE_NUM")
        XW = item.find("XPOINT_WGS")
        YW = item.find("YPOINT_WGS")
    print(CD.text,"는",LB.text,"호선의",NM.text,"역입니다")
    import webbrowser
    url = "https://www.google.co.kr/maps/place/37%C2%B029'40.6%22N+127%C2%B003'49.1%22E/@"+XW.text+","+YW.text+",17z"
    webbrowser.open_new(url)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    