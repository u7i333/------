# -*- coding: utf-8 -*-

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
    
    


#주소와 전화번호검색

def ugadURIBuilder(server,**user):
    global Key
    print("------------------------------------------------------------")
    print("1~4호선만 검색이 가능합니다")
    print("------------------------------------------------------------")
    l = input("알고싶은 지하철 호선을 선택해주세요:")
    print("------------------------------------------------------------")
    n = input("알고싶은 지하철 이름(역을 제외하고 입력해주세요 예:신도림 ):")
    print("------------------------------------------------------------")
    f = urllib.parse.quote(n)
    #http://openapi.seoul.go.kr:8088/(인증키)/xml/StationAdresTelno/1/5/2/신정네거리
    str = "http://" + server + "/"+Key+"/xml/StationAdresTelno/1/5/"+l+"/"+f+"/"
    return str
    
    
def ugaddr():
    global server, regKey, conn
    if conn == None :
        connectOpenAPIServer()
    uri = ugadURIBuilder(server)
    conn.request("GET", uri)
    req = conn.getresponse()
    if int(req.status) == 200 :
        print("------------------------------------------------------------")
        print("지하철 데이터를 가져왔습니다")
        print("------------------------------------------------------------")
        return ugaddrData(req.read())
    else:
        print("------------------------------------------------------------")
        print ("실패했습니다. 다시 시도해보세요")
        print("------------------------------------------------------------")
        return None
    
        
def ugaddrData(strXml):

    from xml.etree import ElementTree
    tree = ElementTree.fromstring(strXml)
    itemElements = tree.getiterator("row")
    for item in itemElements:
        
        NM = item.find("STATN_NM")
        AD = item.find("ADRES")
        RD = item.find("RDNMADR")
        TL = item.find("TELNO")
        print("------------------------------------------------------------")
        print("역이름 : ",NM.text)
        print("지번주소 : ",AD.text)
        print("도로명주소 : ",RD.text)
        print("전화번호 : ",TL.text)
        print("------------------------------------------------------------")
    
      
#예술무대정보 검색   

def ugartURIBuilder(server,**user):
    global Key
    print("------------------------------------------------------------")
    l = input("알고싶은 년과 월을 입력해주세요(예:2016-07) =" )
    print("------------------------------------------------------------")
    n = input("알고싶은 일을 입력해주세요(예: 06):")
    print("------------------------------------------------------------")

    #http://openAPI.seoul.go.kr:8088/(인증키)/xml/MetroPerformanceInfo/1/5/2013-07/
    str = "http://" + server + "/"+Key+"/xml/MetroPerformanceInfo/1/5/"+l+"/"+n+"/"
    return str
    
    
def ugart():
    global server, regKey, conn
    if conn == None :
        connectOpenAPIServer()
    uri = ugartURIBuilder(server)
    conn.request("GET", uri)
    req = conn.getresponse()
    if int(req.status) == 200 :
        print("------------------------------------------------------------")
        print("지하철 데이터를 가져왔습니다")
        print("------------------------------------------------------------")
        return ugartData(req.read())
    else:
        print("------------------------------------------------------------")
        print ("실패했습니다. 다시 시도해보세요")
        print("------------------------------------------------------------")
        return None
    
        
def ugartData(strXml):

    from xml.etree import ElementTree
    tree = ElementTree.fromstring(strXml)
    itemElements = tree.getiterator("row")
    print("이 날에 하는 공연")
    for item in itemElements:
        
        NM = item.find("NAME")
        CM = item.find("CMT")
        PL = item.find("PLACE")
        SD = item.find("SDATE")
        ED = item.find("EDATE")
        print("------------------------------------------------------------")
        print("공연제목 또는 음악가이름 : ",NM.text)
        print("공연 간단 설명 : ",CM.text)
        print("장소 : ",PL.text)
        print("시작시간 : ",SD.text)
        print("끝나는 시간 : ",ED.text)
        print("------------------------------------------------------------")           
           
           
           
           
           
#주변정류장검색           
           
def ugbusURIBuilder(server,**user):
    global Key
   
    print("------------------------------------------------------------")
    n = input("알고싶은 지하철의 역코드를 입력해주세요:")
    print("------------------------------------------------------------")
    #http://openAPI.seoul.go.kr:8088/sample/xml/SearchBusSTNByIDService/1/5/0249/
    str = "http://" + server + "/"+Key+"/xml/SearchBusSTNByIDService/1/100/"+n+"/"
    return str
    
    
def ugbus():
    global server, regKey, conn
    if conn == None :
        connectOpenAPIServer()
    uri =ugbusURIBuilder(server)
    conn.request("GET", uri)
    req = conn.getresponse()
    if int(req.status) == 200 :
        print("------------------------------------------------------------")
        print("지하철 데이터를 가져왔습니다")
        print("------------------------------------------------------------")
        return ugbusData(req.read())
    else:
        print("------------------------------------------------------------")
        print ("실패했습니다. 다시 시도해보세요")
        print("------------------------------------------------------------")
        return None
    
        
def ugbusData(strXml):

    from xml.etree import ElementTree
    tree = ElementTree.fromstring(strXml)
    itemElements = tree.getiterator("row")
    for item in itemElements:
        
        NM = item.find("STATION_NM")
        ST = item.find("STNNM")
        SI = item.find("STATIONID")
        print("------------------------------------------------------------")
        print("역이름 : ",NM.text)
        print("버스정류장 이름 : ", ST.text)
        print("버스정류장 ID : ", SI.text)
        print("------------------------------------------------------------")           
    n = input("위치를 검색합니까? (y/n) : ")
    if n == 'y':
        #http://map.naver.com/?type=BUS_STATION&query=15-211버스정류장&enc=utf-8
        import webbrowser
        c =input("버스정류장 ID를 입력해주세요(예 : 15211은  15-211 처럼 검색해야됩니다 ) : ")
        url = "http://map.naver.com/?type=BUS_STATION&query="+c+"버스정류장&enc=utf-8"
        webbrowser.open_new(url)
    


#주요시설건색
           
def ugimpURIBuilder(server,**user):
    global Key
    print("------------------------------------------------------------")
    l = input("알고싶은 지하철역의 역코드를 입력해주세요:")
    print("------------------------------------------------------------")
    #http://openAPI.seoul.go.kr:8088/sample/xml/SearchFacilityByIDService/1/5/0249/
    str = "http://" + server + "/"+Key+"/xml/SearchFacilityByIDService/1/100/"+l+"/"
    return str
    
    
def ugimp():
    global server, regKey, conn
    if conn == None :
        connectOpenAPIServer()
    uri = ugimpURIBuilder(server)
    conn.request("GET", uri)
    req = conn.getresponse()
    if int(req.status) == 200 :
        print("------------------------------------------------------------")
        print("지하철 데이터를 가져왔습니다")
        print("------------------------------------------------------------")
        return ugimpData(req.read())
    else:
        print("------------------------------------------------------------")
        print ("실패했습니다. 다시 시도해보세요")
        print("------------------------------------------------------------")
        return None
    
        
def ugimpData(strXml):

    from xml.etree import ElementTree
    tree = ElementTree.fromstring(strXml)
    itemElements = tree.getiterator("row")
    
    for item in itemElements:
        
        NM = item.find("STATION_NM")
        AN = item.find("AREA_NM")
    
        print("------------------------------------------------------------")
        print("역이름 : ",NM.text)
        print("시설이름 : ",AN.text)
        print("------------------------------------------------------------")
    import webbrowser
    
    #https://www.google.co.kr/maps/place/%EB%AA%A9%EB%8F%999%EB%8B%A8%EC%A7%80%EC%95%84%ED%8C%8C%ED%8A%B8/@37.519265,126.8615711,17z/data=!3m1!4b1!4m5!3m4!1s0x357c9dd681e190ed:0x62ecd7947364f7db!8m2!3d37.5192608!4d126.8637598
    
    print("------------------------------------------------------------")
    
    n = input("위치를 검색해 보시겠습니까?(Y/N) = ")
    print("------------------------------------------------------------")    
    if n == 'y':
        f = input("시설이름을 입력해주세요")
        n = urllib.parse.quote(f)
        url = "https://www.google.co.kr/maps/place/"+n+"/"
        webbrowser.open_new(url)   
           
          

#지명유래


def ugfunURIBuilder(server,**user):
    global Key
   
    print("------------------------------------------------------------")
    print("1~4호선만 검색이 가능합니다")
    print("------------------------------------------------------------")
    l = input("알고싶은 지하철 호선을 선택해주세요:")
    print("------------------------------------------------------------")
    n = input("알고싶은 지하철 이름(역을 제외하고 입력해주세요 예:신도림 ):")
    print("------------------------------------------------------------")
    f = urllib.parse.quote(n)
    #http://openAPI.seoul.go.kr:8088/sample/xml/StationNmfpcOrgnThemaNm/1/5/2/신정네거리/
    str = "http://" + server + "/"+Key+"/xml/StationNmfpcOrgnThemaNm/1/100/"+l+"/"+f+"/"
    return str
    
    
def ugfun():
    global server, regKey, conn
    if conn == None :
        connectOpenAPIServer()
    uri =ugfunURIBuilder(server)
    conn.request("GET", uri)
    req = conn.getresponse()
    if int(req.status) == 200 :
        print("------------------------------------------------------------")
        print("지하철 데이터를 가져왔습니다")
        print("------------------------------------------------------------")
        return ugfunData(req.read())
    else:
        print("------------------------------------------------------------")
        print ("실패했습니다. 다시 시도해보세요")
        print("------------------------------------------------------------")
        return None
    
        
def ugfunData(strXml):

    from xml.etree import ElementTree
    tree = ElementTree.fromstring(strXml)
    itemElements = tree.getiterator("row")
    for item in itemElements:
        
        NM = item.find("STATN_NM")
        ST = item.find("THEMA_NM")
        SI = item.find("NMFPC_ORGN")
        print("------------------------------------------------------------")
        print("역이름 : ",NM.text)
        print("테마  : ", ST.text)
        print("이름의 유래 : ", SI.text)
        print("------------------------------------------------------------")           
    











           
           