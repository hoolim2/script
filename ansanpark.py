#-*- coding: utf-8 -*-
import urllib.request
import string
import codecs
import smtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

from xml.dom.minidom import *
from tkinter import *
from tkinter import font
import tkinter
import tkinter.messagebox

#메일-----------------------------
global sendMailContent

def sendMail(Sendid, Sendpw, ReviceMail, Subject, Content):
    s = smtplib.SMTP("smtp.gmail.com",587) #SMTP 서버 설정
    s.starttls() #STARTTLS 시작
    s.login( Sendid, Sendpw)
    mail_conts = Content
    messege = MIMEText(mail_conts, _charset='euc-kr')
    messege['Subject'] = Subject
    messege['From'] = Sendid
    messege['To'] = ReviceMail
    s.sendmail( Sendid , ReviceMail, messege.as_string())

#XML추출----------------------------------
def openAPItoXML(server, key):
    openApi = urllib.request.build_opener()
    openApi.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')]
    data = ""
    urldata = server + key
    with openApi.open(urldata) as f:
        data = f.read(9000000).decode('utf-8')
    return data

def addParsingDicList(xmlData, motherData, childData):
    doc = parseString(xmlData)
    siGunGuList = doc.getElementsByTagName(motherData)
    signguCdSize = len(siGunGuList)
    list = []
    for index in range(signguCdSize):
        dataset = siGunGuList[index].getElementsByTagName(childData)
        if  (dataset[0].firstChild):
            list.append(str(dataset[0].firstChild.data))
        else:
            list.append(str("No Data"))
    return list

setter = openAPItoXML("http://data.ansan.go.kr/hub/CityPark?KEY=","8f36a34cf1604ed29ff01310c8f3d917")

PARK_DIV_NM = addParsingDicList(setter , "row", "PARK_NM")
MANAGE_NO = addParsingDicList(setter , "row", "MANAGE_NO")
PARK_SPORTS_FACLT_DTLS = addParsingDicList(setter , "row", "PARK_SPORTS_FACLT_DTLS")
PARK_AMSMT_FACLT_DTLS = addParsingDicList(setter , "row", "PARK_AMSMT_FACLT_DTLS")
PARK_CNVNC_FACLT_DTLS = addParsingDicList(setter , "row", "PARK_CNVNC_FACLT_DTLS")
REFINE_LOTNO_ADDR = addParsingDicList(setter , "row", "REFINE_LOTNO_ADDR")
MANAGE_INST_TELNO = addParsingDicList(setter , "row", "MANAGE_INST_TELNO")

#TkGUI함수----------------------------------------
g_Tk = Tk()
g_Tk.geometry("440x720+750+200")

searchIndex=[]
searchIndexNum = 0

def InitTopText():
    TempFont = font.Font(g_Tk, size=20, weight='bold', family = 'Consolas')
    MainText = Label(g_Tk, font = TempFont,bg='white', text="◆ 안산시 도시공원 검색 ◆")
    MainText.pack()
    MainText.place(x=40)

def InitKeyword_InputLabel():
    global InputLabel
    TempFont = font.Font(g_Tk, size=14, weight='bold', family = 'Consolas')
    InputLabel = Entry(g_Tk,bg='white',relief='flat', font = TempFont, width = 23, borderwidth = 3)
    InputLabel.pack()
    InputLabel.place(x=97, y=52)

def InitSenderadd_InputLabel():
    global sendidLabel
    TempFont = font.Font(g_Tk, size=15, weight='bold', family = 'Consolas')
    sendidLabel = Entry(g_Tk, font = TempFont, width = 20, borderwidth = 4, relief = 'ridge')
    sendidLabel.pack()
    sendidLabel.place(x=130, y=560)

def InitSenderpass_InputLabel():
    global sendpwLabel
    TempFont = font.Font(g_Tk, size=15, weight='bold', family = 'Consolas')
    sendpwLabel = Entry(g_Tk, font = TempFont, width = 20, borderwidth = 4, relief = 'ridge',show="*")
    sendpwLabel.pack()
    sendpwLabel.place(x=130, y=610)

def InitTakeradd_InputLabel():
    global recvidLabel
    TempFont = font.Font(g_Tk, size=15, weight='bold', family = 'Consolas')
    recvidLabel = Entry(g_Tk, font = TempFont, width = 20, borderwidth = 4, relief = 'ridge')
    recvidLabel.pack()
    recvidLabel.place(x=130, y=660)

def InitSearchButton():
    TempFont = font.Font(g_Tk, size=15, weight='bold', family = 'Consolas')
    SearchButton = Button(g_Tk,bg="#48d1cc",fg='white',relief='flat',padx=10,pady=3, font = TempFont, text="검색",  command=SearchButtonAction)
    SearchButton.pack()
    SearchButton.place(x=340, y=45)

def InitMailsendButton():
    TempFont = font.Font(g_Tk, size=12, weight='bold', family = 'Consolas')
    SearchButton = Button(g_Tk,bg="#48d1cc",fg='white',relief='flat',padx=5, font = TempFont, text="Send",  command=SendButtonAction)
    SearchButton.pack()
    SearchButton.place(x=360, y=660)

def InitRightFindButton():
    TempFont = font.Font(g_Tk, size=12, weight='bold', family = 'Consolas')
    rFindButton = Button(g_Tk,bg="#48d1cc",fg='white',relief='flat',padx=5, text="▶",  command=rightIndexButtonAction)
    rFindButton.pack()
    rFindButton.place(x=260, y=510)

def InitLeftFindButton():
    TempFont = font.Font(g_Tk, size=12, weight='bold', family = 'Consolas')
    rFindButton = Button(g_Tk,bg="#48d1cc",fg='white',relief='flat',padx=5, text="◀",  command=leftIndexButtonAction)
    rFindButton.pack()
    rFindButton.place(x=150, y=510)

bg = Canvas ( g_Tk, bg='white',height=720, width=450)
oval = bg.create_polygon(90, 45,350,45, 350, 89,90,89, fill="#48d1cc")
bg.pack()
bg.place(x=0, y=0)

var = IntVar()
RadioParkNM = Radiobutton(g_Tk,borderwidth=4,bg='white', text="공원명", variable=var, value=1)
RadioParkNM.pack()
RadioParkNM.place(x=20, y=35)

RadioFacility = Radiobutton(g_Tk,borderwidth=4,bg='white', text="시설물", variable=var, value=2)
RadioFacility.pack()
RadioFacility.place(x=20, y=55)

RadioAddress = Radiobutton(g_Tk,borderwidth=4,bg='white', text="주소", variable=var, value=3)
RadioAddress.pack()
RadioAddress.place(x=20, y=75)

SendIDLabel = Label(g_Tk,bg='white', text="보내는사람 메일주소")
SendIDLabel.pack()
SendIDLabel.place(x=10, y=565)

SendPWLabel = Label(g_Tk,bg='white', text="보내는사람 PW")
SendPWLabel.pack()
SendPWLabel.place(x=10, y=615)

RcvLabel = Label(g_Tk,bg='white', text="받는사람 메일주소")
RcvLabel.pack()
RcvLabel.place(x=10, y=665)

labelframe = LabelFrame( g_Tk,bg='white', text="검색 결과",width=420,height=440)
labelframe.pack()
labelframe.place(x=10, y=110)

bg1 = Canvas ( g_Tk, bg='#48d1cc',height=10, width=365)
bg1.place(x=30, y=130)

def monitorLabel():
    TempFont = font.Font(g_Tk, size=12, weight='bold', family = 'Consolas')
    indexLabel = Label(g_Tk,bg='white', text=str(searchIndexNum+1) + " / " + str(len(searchIndex)),font=TempFont)
    indexLabel.pack()
    indexLabel.place(x=190, y=512)

def SendButtonAction():
    global sendidLabel
    global sendpwLabel
    global recvidLabel
    global RenderText
    global sendMailContent
    sid = sendidLabel.get()
    spw = sendpwLabel.get()
    rid = recvidLabel.get()
    sendMailContent = searchIndex[searchIndexNum]
    sendMail(sid, spw, rid, "공원정보입니다.", sendMailContent)
    tkinter.messagebox.showinfo("알림", "발송완료")

def SearchButtonAction():
    global SearchListBox
    global searchIndexNum
    searchIndex.clear()
    searchIndexNum = 0
    RenderText.configure(state='normal')
    RenderText.delete(0.0, END)
    if var.get() == 1:
        SearchParkLibrary()
    elif var.get() == 2:
        print("2")
        SearchFacilityLibrary()
    elif var.get() == 3:
        print("3")
        SearchAddressLibrary()
    monitorLabel()
    RenderText.configure(state='disabled')

def InitRenderText():
    global RenderText
    RenderText = Text(g_Tk, width=49, height=27, borderwidth=0, relief='flat')
    RenderText.pack()
    RenderText.place(x=60, y=150)
    RenderText.configure(state='disabled')

#인덱싱 버튼
def rightIndexButtonAction():
    global searchIndexNum
    global RenderText
    RenderText.configure(state='normal')
    RenderText.delete(0.0, END)
    searchIndexNum = (searchIndexNum + 1 +  len(searchIndex)) % len(searchIndex)
    RenderText.insert(INSERT, searchIndex[searchIndexNum])
    monitorLabel()

def leftIndexButtonAction():
    global searchIndexNum
    global RenderText
    RenderText.configure(state='normal')
    RenderText.delete(0.0, END)
    searchIndexNum = (searchIndexNum - 1 + len(searchIndex)) % len(searchIndex)
    RenderText.insert(INSERT, searchIndex[searchIndexNum])
    monitorLabel()

#공원명 검색
def SearchParkLibrary():
    global sendMailContent
    global SearchListBox
    global searchIndexNum
    global ParksDoc
    global InputLabel
    sendMailContent = ""
    keyword = InputLabel.get()
    print("TextBox :",keyword)
    for i in range(0, len(PARK_DIV_NM)):
        if ( PARK_DIV_NM[i].find(keyword) != -1):
            searchIndex.append(str("\n-------------------------------------------\n"
                                   + "공원 이름 : " + PARK_DIV_NM[i] + "\n"
                                   + "관리번호 : " + MANAGE_NO[i] + "\n"
                                   + "스포츠 시설 : " + PARK_SPORTS_FACLT_DTLS[i] + "\n"
                                   + "편의 시설 : " + PARK_CNVNC_FACLT_DTLS[i] + "\n"
                                   + "공원 주소 : " + REFINE_LOTNO_ADDR[i] + "\n"
                                   + "관리 전화번호 : " + MANAGE_INST_TELNO[i] + "\n"
                                   + "-------------------------------------------\n"))
    RenderText.insert(INSERT, searchIndex[searchIndexNum])

#시설물 검색
def SearchFacilityLibrary():
    global SearchListBox
    global ParksDoc
    global searchIndexNum
    global InputLabel
    global sendMailContent
    global searchIndexNum
    sendMailContent = ""
    keyword = InputLabel.get()
    print("TextBox :",keyword)
    for i in range(0, len(PARK_SPORTS_FACLT_DTLS)):
        if (PARK_SPORTS_FACLT_DTLS[i].find(keyword)
                & PARK_AMSMT_FACLT_DTLS[i].find(keyword)
                & PARK_CNVNC_FACLT_DTLS[i].find(keyword) != -1):
            searchIndex.append(str("\n-------------------------------------------\n"
                                   + "공원 이름 : " + PARK_DIV_NM[i] + "\n"
                                   + "관리번호 : " + MANAGE_NO[i] + "\n"
                                   + "스포츠 시설 : " + PARK_SPORTS_FACLT_DTLS[i]+ "\n"
                                   + "편의 시설 : " + PARK_CNVNC_FACLT_DTLS[i] + "\n"
                                   + "공원 주소 : "+ REFINE_LOTNO_ADDR[i] + "\n"
                                   + "관리 전화번호 : " + MANAGE_INST_TELNO[i] + "\n"
                                   + "-------------------------------------------\n"))
    RenderText.insert(INSERT, searchIndex[searchIndexNum])

#주소 검색
def SearchAddressLibrary():
    global SearchListBox
    global ParksDoc
    global InputLabel
    global sendMailContent
    sendMailContent = ""
    keyword = InputLabel.get()
    print("TextBox :",keyword)
    for i in range(0, len(REFINE_LOTNO_ADDR)):
        if ( REFINE_LOTNO_ADDR[i].find(keyword) != -1):
            searchIndex.append(str("\n-------------------------------------------\n"
                                   + "공원 이름 : " + PARK_DIV_NM[i] + "\n"
                                   + "관리번호 : " + MANAGE_NO[i] + "\n"
                                   + "스포츠 시설 : " + PARK_SPORTS_FACLT_DTLS[i] + "\n"
                                   + "편의 시설 : " + PARK_CNVNC_FACLT_DTLS[i] + "\n"
                                   + "공원 주소 : " + REFINE_LOTNO_ADDR[i] + "\n"
                                   + "관리 전화번호 : " + MANAGE_INST_TELNO[i] + "\n"
                                   + "-------------------------------------------\n"))
    RenderText.insert(INSERT, searchIndex[searchIndexNum])

InitTopText()
InitKeyword_InputLabel()
InitSenderadd_InputLabel()
InitSenderpass_InputLabel()
InitTakeradd_InputLabel()
InitSearchButton()
InitRightFindButton()
InitLeftFindButton()
InitMailsendButton()
InitRenderText()

g_Tk.mainloop()

#-------------------dos메뉴
#print("1. Facility Search");
#print("2. Address Search");
#print("3. Name Search");

#inNum = input("input Num : ")

#if ( int(inNum) == int(1)) :
#    search = input("input Data : ")
#    for i in range(0, len(PARK_SPORTS_FACLT_DTLS)):
#        if ( PARK_SPORTS_FACLT_DTLS[i].find(search) != -1):
#            print("\n-------------------------------------------")
#            print("PARK_DIV_NM : " + PARK_DIV_NM[i] )
#            print("MANAGE_NO : " + MANAGE_NO[i] )
#            print("PARK_SPORTS_FACLT_DTLS : " + PARK_SPORTS_FACLT_DTLS[i] )
#            print("PARK_AMSMT_FACLT_DTLS : " + PARK_AMSMT_FACLT_DTLS[i] )
#            print("PARK_CNVNC_FACLT_DTLS : " + PARK_CNVNC_FACLT_DTLS[i] )
#            print("REFINE_LOTNO_ADDR : " + REFINE_LOTNO_ADDR[i] )
#            print("MANAGE_INST_TELNO : " + MANAGE_INST_TELNO[i] )
#            print("-------------------------------------------\n")

#if ( int(inNum) == int(2)) :
#    search = input("input Data : ")
#    for i in range(0, len(REFINE_LOTNO_ADDR)):
#        if ( REFINE_LOTNO_ADDR[i].find(search) != -1):
#            print("\n-------------------------------------------")
#            print("PARK_DIV_NM : " + PARK_DIV_NM[i] )
#            print("MANAGE_NO : " + MANAGE_NO[i] )
#            print("PARK_SPORTS_FACLT_DTLS : " + PARK_SPORTS_FACLT_DTLS[i] )
#            print("PARK_AMSMT_FACLT_DTLS : " + PARK_AMSMT_FACLT_DTLS[i] )
#            print("PARK_CNVNC_FACLT_DTLS : " + PARK_CNVNC_FACLT_DTLS[i] )
#            print("REFINE_LOTNO_ADDR : " + REFINE_LOTNO_ADDR[i] )
#            print("MANAGE_INST_TELNO : " + MANAGE_INST_TELNO[i] )
#            print("-------------------------------------------\n")

#if ( int(inNum) == int(3)) :
#    search = input("input Data : ")
#    for i in range(0, len(PARK_DIV_NM)):
#        if ( PARK_DIV_NM[i].find(search) != -1):
#            print("\n-------------------------------------------")
#            print("PARK_DIV_NM : " + PARK_DIV_NM[i] )
#            print("MANAGE_NO : " + MANAGE_NO[i] )
#            print("PARK_SPORTS_FACLT_DTLS : " + PARK_SPORTS_FACLT_DTLS[i] )
#            print("PARK_AMSMT_FACLT_DTLS : " + PARK_AMSMT_FACLT_DTLS[i] )
#            print("PARK_CNVNC_FACLT_DTLS : " + PARK_CNVNC_FACLT_DTLS[i] )
#            print("REFINE_LOTNO_ADDR : " + REFINE_LOTNO_ADDR[i] )
#            print("MANAGE_INST_TELNO : " + MANAGE_INST_TELNO[i] )
#            print("-------------------------------------------\n")