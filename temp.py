loopFlag = 1
from internetunderground import *

def printMenu():
    print("\nWelcome! underground Program (xml version)")
    print("========Menu==========")
    print("전체적인 지하철 역 검색:  q")
    print("개별 지하철 역 검색: w")
    print("메일보내기 (임시) : e")
    print("역코드로 열차시간 리스트 출력 = r")
    
    print("프로그램 종료 x")
    
def launcherFunction(menu):
    if menu == 'q':
        UndergroundAllsearch()
        
    elif menu == 'e':
        SendMail()
    elif menu == 'r':
        TimeList()
    elif menu == 'x':
        Quitprogram()
    elif menu == 'w':
        UndergroundOnesearch()
    
def Quitprogram():
    global loopFlag
    loopFlag = 0
    
while(loopFlag > 0):
    printMenu()
    menuKey = str(input ('메뉴를 선택해주세요 :'))
    launcherFunction(menuKey)
else:
    print ("잘가세요")
    