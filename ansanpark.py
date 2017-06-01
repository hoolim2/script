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
g_Tk.geometry("400x700+750+200")

def InitTopText():
    TempFont = font.Font(g_Tk, size=20, weight='bold', family = 'Consolas')
    MainText = Label(g_Tk, font = TempFont, text="[안산시 도시공원 검색]")
    MainText.pack()
    MainText.place(x=40)

def InitSearchListBox():
    global SearchListBox
    ListBoxScrollbar = Scrollbar(g_Tk)
    ListBoxScrollbar.pack()
    ListBoxScrollbar.place(x=300, y=50)

    TempFont = font.Font(g_Tk, size=15, weight='bold', family='Consolas')
    SearchListBox = Listbox(g_Tk, font=TempFont, activestyle='none',
                            width=10, height=1, borderwidth=12, relief='ridge',
                            yscrollcommand = ListBoxScrollbar.set)

    SearchListBox.insert(1, "공원 이름")
    SearchListBox.insert(2, "시설명")
    SearchListBox.insert(3, "주소")
    SearchListBox.pack()
    SearchListBox.place(x=160, y=50)

    ListBoxScrollbar.config(command=SearchListBox.yview)

def InitKeyword_InputLabel():
    global InputLabel
    TempFont = font.Font(g_Tk, size=15, weight='bold', family = 'Consolas')
    InputLabel = Entry(g_Tk, font = TempFont, width = 26, borderwidth = 12, relief = 'ridge')
    InputLabel.pack()
    InputLabel.place(x=10, y=105)

def InitSenderadd_InputLabel():
    global sendidLabel
    TempFont = font.Font(g_Tk, size=15, weight='bold', family = 'Consolas')
    sendidLabel = Entry(g_Tk, font = TempFont, width = 20, borderwidth = 4, relief = 'ridge')
    sendidLabel.pack()
    sendidLabel.place(x=100, y=550)

def InitSenderpass_InputLabel():
    global sendpwLabel
    TempFont = font.Font(g_Tk, size=15, weight='bold', family = 'Consolas')
    sendpwLable = Entry(g_Tk, font = TempFont, width = 20, borderwidth = 4, relief = 'ridge')
    sendpwLable.pack()
    sendpwLable.place(x=100, y=600)

def InitTakeradd_InputLabel():
    global recvidLabel
    TempFont = font.Font(g_Tk, size=15, weight='bold', family = 'Consolas')
    recvidLable = Entry(g_Tk, font = TempFont, width = 20, borderwidth = 4, relief = 'ridge')
    recvidLable.pack()
    recvidLable.place(x=100, y=650)

def InitSearchButton():
    TempFont = font.Font(g_Tk, size=12, weight='bold', family = 'Consolas')
    SearchButton = Button(g_Tk, font = TempFont, text="검색",  command=SearchButtonAction)
    SearchButton.pack()
    SearchButton.place(x=330, y=110)

def InitMailsendButton():
    TempFont = font.Font(g_Tk, size=12, weight='bold', family = 'Consolas')
    SearchButton = Button(g_Tk, font = TempFont, text="Send",  command=SendButtonAction)
    SearchButton.pack()
    SearchButton.place(x=330, y=650)

def SendButtonAction():
    global sendidLabel
    global sendpwLabel
    global recvidLabel
    global RenderText
    global sendMailContent
    sid = sendidLabel.get()
    spw = sendpwLabel.get()
    rid = recvidLabel.get()
    sendMail(sid, spw, rid, "Test", sendMailContent)

def SearchButtonAction():
    global SearchListBox
    RenderText.configure(state='normal')
    RenderText.delete(0.0, END)
    iSearchIndex = SearchListBox.curselection()[0]
    if iSearchIndex == 0:
        SearchParkLibrary()
    elif iSearchIndex == 1:
        print("1")
        SearchFacilityLibrary()
    elif iSearchIndex == 2:
        print("2")
        SearchAddressLibrary()
    RenderText.configure(state='disabled')

def InitRenderText():
    global RenderText
    RenderTextScrollbar = Scrollbar(g_Tk)
    RenderTextScrollbar.pack()
    RenderTextScrollbar.place(x=375, y=200)
    RenderText = Text(g_Tk, width=49, height=27, borderwidth=12, relief='ridge', yscrollcommand=RenderTextScrollbar.set)
    RenderText.pack()
    RenderText.place(x=10, y=160)
    RenderTextScrollbar.config(command=RenderText.yview)
    RenderTextScrollbar.pack(side=RIGHT, fill=BOTH)
    RenderText.configure(state='disabled')

#공원명 검색
def SearchParkLibrary():
    global sendMailContent
    global SearchListBox
    global ParksDoc
    global InputLabel
    sendMailContent = ""
    keyword = InputLabel.get()
    print("TextBox :",keyword)
    for i in range(0, len(PARK_DIV_NM)):
        if ( PARK_DIV_NM[i].find(keyword) != -1): 
            RenderText.insert(INSERT, "\n-------------------------------------------\n")
            RenderText.insert(INSERT, "PARK_DIV_NM : " + PARK_DIV_NM[i] + "\n")
            RenderText.insert(INSERT, "MANAGE_NO : " + MANAGE_NO[i]+ "\n")
            RenderText.insert(INSERT, "PARK_SPORTS_FACLT_DTLS : " + PARK_SPORTS_FACLT_DTLS[i]+ "\n")
            RenderText.insert(INSERT, "PARK_AMSMT_FACLT_DTLS : " + PARK_AMSMT_FACLT_DTLS[i]+ "\n")
            RenderText.insert(INSERT, "PARK_CNVNC_FACLT_DTLS : " + PARK_CNVNC_FACLT_DTLS[i]+ "\n")
            RenderText.insert(INSERT, "REFINE_LOTNO_ADDR : " + REFINE_LOTNO_ADDR[i]+ "\n")
            RenderText.insert(INSERT, "MANAGE_INST_TELNO : " + MANAGE_INST_TELNO[i]+ "\n")
            RenderText.insert(INSERT, "-------------------------------------------\n")
            sendMailContent = sendMailContent + "\n-------------------------------------------\n" + "PARK_DIV_NM : " + PARK_DIV_NM[i] + "\n" +  "MANAGE_NO : " + MANAGE_NO[i]+ "\n" + "PARK_SPORTS_FACLT_DTLS : " + PARK_SPORTS_FACLT_DTLS[i]+ "\n" + "PARK_CNVNC_FACLT_DTLS : " + PARK_CNVNC_FACLT_DTLS[i]+ "\n" + "REFINE_LOTNO_ADDR : " + REFINE_LOTNO_ADDR[i]+ "\n" + "MANAGE_INST_TELNO : " + MANAGE_INST_TELNO[i]+ "\n" + "-------------------------------------------\n"

#시설물 검색
def SearchFacilityLibrary():
    global SearchListBox
    global ParksDoc
    global InputLabel
    global sendMailContent
    sendMailContent = ""
    keyword = InputLabel.get()
    print("TextBox :",keyword)
    for i in range(0, len(PARK_SPORTS_FACLT_DTLS)):
        if ( PARK_SPORTS_FACLT_DTLS[i].find(keyword) != -1):
            RenderText.insert(INSERT, "\n-------------------------------------------\n")
            RenderText.insert(INSERT, "PARK_DIV_NM : " + PARK_DIV_NM[i] + "\n")
            RenderText.insert(INSERT, "MANAGE_NO : " + MANAGE_NO[i]+ "\n")
            RenderText.insert(INSERT, "PARK_SPORTS_FACLT_DTLS : " + PARK_SPORTS_FACLT_DTLS[i]+ "\n")
            RenderText.insert(INSERT, "PARK_AMSMT_FACLT_DTLS : " + PARK_AMSMT_FACLT_DTLS[i]+ "\n")
            RenderText.insert(INSERT, "PARK_CNVNC_FACLT_DTLS : " + PARK_CNVNC_FACLT_DTLS[i]+ "\n")
            RenderText.insert(INSERT, "REFINE_LOTNO_ADDR : " + REFINE_LOTNO_ADDR[i]+ "\n")
            RenderText.insert(INSERT, "MANAGE_INST_TELNO : " + MANAGE_INST_TELNO[i]+ "\n")
            RenderText.insert(INSERT, "-------------------------------------------\n")
            sendMailContent = sendMailContent + "\n-------------------------------------------\n" + "PARK_DIV_NM : " + PARK_DIV_NM[i] + "\n" +  "MANAGE_NO : " + MANAGE_NO[i]+ "\n" + "PARK_SPORTS_FACLT_DTLS : " + PARK_SPORTS_FACLT_DTLS[i]+ "\n" + "PARK_CNVNC_FACLT_DTLS : " + PARK_CNVNC_FACLT_DTLS[i]+ "\n" + "REFINE_LOTNO_ADDR : " + REFINE_LOTNO_ADDR[i]+ "\n" + "MANAGE_INST_TELNO : " + MANAGE_INST_TELNO[i]+ "\n" + "-------------------------------------------\n"

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
            RenderText.insert(INSERT, "\n-------------------------------------------\n")
            RenderText.insert(INSERT, "PARK_DIV_NM : " + PARK_DIV_NM[i] + "\n")
            RenderText.insert(INSERT, "MANAGE_NO : " + MANAGE_NO[i]+ "\n")
            RenderText.insert(INSERT, "PARK_SPORTS_FACLT_DTLS : " + PARK_SPORTS_FACLT_DTLS[i]+ "\n")
            RenderText.insert(INSERT, "PARK_AMSMT_FACLT_DTLS : " + PARK_AMSMT_FACLT_DTLS[i]+ "\n")
            RenderText.insert(INSERT, "PARK_CNVNC_FACLT_DTLS : " + PARK_CNVNC_FACLT_DTLS[i]+ "\n")
            RenderText.insert(INSERT, "REFINE_LOTNO_ADDR : " + REFINE_LOTNO_ADDR[i]+ "\n")
            RenderText.insert(INSERT, "MANAGE_INST_TELNO : " + MANAGE_INST_TELNO[i]+ "\n")
            RenderText.insert(INSERT, "-------------------------------------------\n")
            sendMailContent = sendMailContent + "\n-------------------------------------------\n" + "PARK_DIV_NM : " + PARK_DIV_NM[i] + "\n" +  "MANAGE_NO : " + MANAGE_NO[i]+ "\n" + "PARK_SPORTS_FACLT_DTLS : " + PARK_SPORTS_FACLT_DTLS[i]+ "\n" + "PARK_CNVNC_FACLT_DTLS : " + PARK_CNVNC_FACLT_DTLS[i]+ "\n" + "REFINE_LOTNO_ADDR : " + REFINE_LOTNO_ADDR[i]+ "\n" + "MANAGE_INST_TELNO : " + MANAGE_INST_TELNO[i]+ "\n" + "-------------------------------------------\n"


InitTopText()
InitSearchListBox()
InitKeyword_InputLabel()
InitSenderadd_InputLabel()
InitSenderpass_InputLabel()
InitTakeradd_InputLabel()
InitSearchButton()
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