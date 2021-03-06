import pandas as pd
import time
from datetime import datetime, timedelta,timezone
from getpass import getpass
import csv
import os

#QR코드 인식 프로그램
class QRRecog:
    # init function
    def __init__(self):
        # most recently recognized input
        self.qrInput=0
        # turn ID.csv into pandas
        self.idCsv = pd.read_csv("./ID_sample.csv", encoding='utf-8')
        # ID dictionary
        self.userDict = {}
        # today Date.csv
        self.today =(datetime.now(timezone(timedelta(hours=9)))).strftime('%y%m%d.csv')
        # create today entry list csv
        self.createTodayCsv()
        # turn ID from pandas to dictionary
        self.makeDic()
        
    # create today entry list as csv ? (이게 맞나?)
    def createTodayCsv(self):
        # 만약 today entry list.csv가 있으면 아무것도 하지않음
        if os.path.exists(self.today):
            return
        # 속성 값은 순서대로 [방문시간, 이름, 주소, 연락처] 
        newCsv = pd.DataFrame(columns=["entryTime","Name","address","phoneNumber"])
        # 오늘 날짜로 csv 파일 생성
        newCsv.to_csv(self.today,index=False)

    # make ID dictionary 
    def makeDic(self):
        # change ID from pandas to dictionary
        self.userDict = self.idCsv.set_index('ID').T.to_dict('list')

    # write information to today entry list
    def writeCsv(self,time,name,address,phoneNum):
        # open today entry list(csv)
        f = open(self.today,'a',newline='')
        wr=csv.writer(f)
        # write information
        wr.writerow([time,name,address,phoneNum])
        # save
        f.close()

    # ID recognization
    def qrCodeInput(self):
        print("-"*32)
        self.qrInput  = int(getpass("QR코드를 인식해주세요. : "))
        print("-"*32)

        # if input is in ID dictionary
        if self.qrInput in self.userDict:
            # 현재 시간
            curTime = (datetime.now(timezone(timedelta(hours=9)))).strftime('%H시%M분%S초')
            # input에 맞는 ID 정보
            info = self.userDict[self.qrInput]
            name = info[0]
            address =info[1]
            phoneNum = info[2]
            
            # input에 맞는 info를 today entry list에 쓰고 저장
            self.writeCsv(curTime,name,address,phoneNum)

            print("인식되었습니다.\n")
            print("{} 님 \n".format(name)) #이름 표시
            print("{} 입장\n".format(curTime)) #현재 시간 표시
        elif self.qrInput==990126:
            self.showID()    
        # else
        else : 
            print("다시 입력해주십시오.\n")
        print("-"*32)
        print("\n")

    def showID(self):
        print(self.idCsv)

    # 프로그램을 계속 실행
    
    def recognization(self):
        while True:
            self.qrCodeInput()

if __name__ == "__main__":
    QR=QRRecog()
    QR.recognization()
