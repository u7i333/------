# -*- coding: utf-8 -*-
#from temp import *
from http.client import HTTPConnection
from http.server import BaseHTTPRequestHandler, HTTPServer
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

conn = None
server = "openAPI.seoul.go.kr:8088"
Key = '507546756775376939356151527963'

host = "smtp.gmail.com"
port = "587"

def userURIBuilder(server,**user):
    global Key
    print("1~9: 1~9호선, I: 인천1호선, K: 경의중앙선, B: 분당선, A: 공항철도, G: 경춘선, S:신분당선, SU:수인선")
    n = input("알고싶은 지하철 호선을 선택해주세요:")
    str = "http://" + server + "/"+Key+"/xml/SearchSTNBySubwayLineService/1/100/"+n+"/"
    return str
    
def connectOpenAPIServer():
    global conn, server
    conn = HTTPConnection(server)
    
def UndergroundAllsearch():
    global server, regKey, conn
    if conn == None :
        connectOpenAPIServer()
    uri = userURIBuilder(server)
    conn.request("GET", uri)
    
    req = conn.getresponse()
    
    if int(req.status) == 200 :
        print("Underground data downloading complete!")
        return extractUndergroundData(req.read())
    else:
        print ("OpenAPI request has been failed!! please retry")
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
           
def SendMail():
    global host, port
    title = str(input ('메일 제목 :'))
    senderAddr = str(input ('보내는 메일 :'))
    recipientAddr = str(input ('받는 메일 :'))
    msgtext = str(input ('메일 내용 :'))
    passwd = str(input ('비밀번호 입력 :'))
    
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
        print("Underground data downloading complete!")
        return extractTimeListdData(req.read())
    else:
        print ("OpenAPI request has been failed!! please retry")
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
           