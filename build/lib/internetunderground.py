# -*- coding: utf-8 -*-
#from temp import *
from http.client import HTTPConnection
from http.server import BaseHTTPRequestHandler, HTTPServer
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import urllib
from subfunc import *



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
    print("------------------------------------------------------------")
    print("1~9: 1~9호선, I: 인천1호선, K: 경의중앙선, B: 분당선, A: 공항철도, G: 경춘선, S:신분당선, SU:수인선")
    print("------------------------------------------------------------")
    n = input("알고싶은 지하철 호선을 선택해주세요:")
    print("------------------------------------------------------------")
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
        print("------------------------------------------------------------")
        print("지하철 데이터를 가져왔습니다")
        print("------------------------------------------------------------")
        return extractUndergroundData(req.read())
    else:
        print("------------------------------------------------------------")
        print ("실패했습니다. 다시 시도해보세요")
        print("------------------------------------------------------------")
        return None
        
def extractUndergroundData(strXml):
    from xml.etree import ElementTree
    tree = ElementTree.fromstring(strXml)
    itemElements = tree.getiterator("row")
    for item in itemElements:
        CD = item.find("STATION_CD")
        NM = item.find("STATION_NM")
        if len(NM.text) > 0 :
           print("------------------------------------------------------------")
           print("역코드 :",CD.text,"역이름:",NM.text)
           print("------------------------------------------------------------")
           
           
# 메일보내기           
           
def SendMail():
    global host, port
    print("------------------------------------------------------------")
    title = str(input ('메일 제목 :'))
    print("------------------------------------------------------------")
    senderAddr = str(input ('보내는 메일 :'))
    print("------------------------------------------------------------")
    passwd = str(input ('비밀번호 입력 :'))
    print("------------------------------------------------------------")
    recipientAddr = str(input ('받는 메일 :'))
    print("------------------------------------------------------------")
    msgtext = str(input ('메일 내용 :'))
    print("------------------------------------------------------------")
    
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
    print("------------------------------------------------------------")
    n = input("알고싶은 역의 역코드를 입력해주세요 : ")
    print("------------------------------------------------------------")
    m = input("요일을 선택해주세요(1:평일 2:토요일 3:일요일,빨간날) : ")
    print("------------------------------------------------------------")
    o = input("상/하행선을 입력해주세요(1:상행선 2:하행선) : ")
    print("------------------------------------------------------------")
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
        print("------------------------------------------------------------")
        print("지하철 데이터를 가져왔습니다")
        print("------------------------------------------------------------")
        return extractTimeListdData(req.read())
    else:
        print("------------------------------------------------------------")
        print ("실패했습니다. 다시 시도해보세요")
        print("------------------------------------------------------------")
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
           print("------------------------------------------------------------")
           print("역코드 :",CD.text,"역이름:",NM.text)
           print("도착시간:",AT.text,"출발시간",LT.text,"시발역",SS.text,"종착역",SE.text)
           print("---------------------------------------------------------------------")
           
           
           
# 개별적인 지하철 검색           
           
def OneURIBuilder(server,**user):
    global Key
    print("------------------------------------------------------------")
    n = input("알고싶은 지하철 이름(역을 제외하고 입력해주세요 예:신도림 ):")
    print("------------------------------------------------------------")
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
        print("------------------------------------------------------------")
        print("지하철 데이터를 가져왔습니다!")
        print("------------------------------------------------------------")
        return extractOneData(req.read())
    else:
        print("------------------------------------------------------------")
        print ("실패했습니다. 다시 시도해보세요")
        print("------------------------------------------------------------")
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
        print(NM.text,"는",LN.text,"호선의 역이면 역코드는 ",CD.text,"입니다.")
        print("--------------------------------------------------------")
        

#지하철 위처검색


def MapURIBuilder(server,**user):
    global Key
    #http://openAPI.seoul.go.kr:8088/(인증키)/xml/SearchLocationOfSTNByIDService/1/5/0335/
    print("------------------------------------------------------------")
    n = input("알고싶은 지하철 역코드:")
    print("------------------------------------------------------------")    
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
        print("------------------------------------------------------------")
        print("지하철 데이터를 가져왔습니다")
        print("------------------------------------------------------------")
        return MapData(req.read())
    else:
        print("------------------------------------------------------------")
        print ("실패했습니다. 다시 시도해보세요")
        print("------------------------------------------------------------")
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
    print(CD.text,"는",LB.text,"호선의",NM.text,"역으로 X좌표는 ",XW.text,"이고 y좌표는 ",YW.text,"입니다.")
    import webbrowser
    url = "https://www.google.co.kr/maps/place/37%C2%B029'40.6%22N+127%C2%B003'49.1%22E/@"+XW.text+","+YW.text+",19z"
    print("------------------------------------------------------------")
    n = input("위치를 검색해 보시겠습니까?(Y/N) = ")
    print("------------------------------------------------------------")    
    if n == 'y':
        webbrowser.open_new(url)
    else:
        print("------------------------------------------------------------")
        print("잘못입력하거나 n를 선택하셨습니다.")
        print("------------------------------------------------------------")
        
        
def information():
    print("========Menu==========")
    print("지하철역 주소와 전화번호 검색:  q")
    print("지하철 예술 무대 정보 검색: w")
    print("역코드로 지하철 주변 버스정류장 검색: e")
    print("역코드로 지하철 주변 주요시설 검색: r")
    print("역별 지명유래 및 테마명(1~4호선만 됩니다. 한번쯤은 봐도 좋아요): t")
    
    menu = str(input ('메뉴를 선택해주세요 :'))
    
    if menu == 'q':
        ugaddr()
    elif menu == 'w':
        ugart()
    elif menu == 'e':
        ugbus()
      
    elif menu == 'r':
        ugimp()
    elif menu == 't':
        ugfun()
  
        
    
           
       

           
    
    
    
    
    
    
    
    
    
    
    
    