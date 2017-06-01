from tkinter import *
from tkinter import font
from xml.etree import ElementTree
import tkinter.messagebox

g_Tk = Tk()
g_Tk.geometry("400x600+750+200")
DataList = []


def printParkList(plist):
    for res in plist:
        print(res)

def checkDocument():
    global ParksDoc
    if ParksDoc == None:
        print("Error : Document is empty")
        return False
    return True

def SearchParkTitle(keyword):
    global ParksDoc
    retlist = []
    if not checkDocument():
        return None

    try:
        tree = ElementTree.fromstring(str(ParksDoc.toxml()))
    except Exception:
        print("Element Tree parsing Error : maybe the xml document is not corrected.")
        return None

    parkElements = tree.getiterator("park name")
    for item in parkElements:
        strTitle = item.find("PARK_NM")
        if (strTitle.text.find(keyword) >= 0):
            retlist.append((item.attrib["ISBN"], strTitle.text))

    return retlist

def LoadXMLFromFile():
    try:
       dom = ElementTree.parse("ansanpark.xml")  # XML 문서를 파싱합니다.
    except Exception:
         print("loading fail!!!")
    else:
         print("XML Document loading complete")
         return dom
    return None

def InitTopText():
    TempFont = font.Font(g_Tk, size=20, weight='bold', family = 'Consolas')
    MainText = Label(g_Tk, font = TempFont, text="[안산시 도시공원 검색]")
    MainText.pack()
    MainText.place(x=20)

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

def InitInputLabel():
    global InputLabel
    TempFont = font.Font(g_Tk, size=15, weight='bold', family = 'Consolas')
    InputLabel = Entry(g_Tk, font = TempFont, width = 26, borderwidth = 12, relief = 'ridge')
    InputLabel.pack()
    InputLabel.place(x=10, y=105)


def InitSearchButton():
    TempFont = font.Font(g_Tk, size=12, weight='bold', family = 'Consolas')
    SearchButton = Button(g_Tk, font = TempFont, text="검색",  command=SearchButtonAction)
    SearchButton.pack()
    SearchButton.place(x=330, y=110)


def SearchButtonAction():
    global SearchListBox
    RenderText.configure(state='normal')
    RenderText.delete(0.0, END)
    print("선택된 조건 번호 : ",SearchListBox.curselection())
    iSearchIndex = SearchListBox.curselection()[0]
    if iSearchIndex == 0:
        SearchLibrary()
    elif iSearchIndex == 1:
        SearchLibrary()
    elif iSearchIndex == 2:
        SearchLibrary()
    RenderText.configure(state='disabled')

def SearchLibrary():
    global SearchListBox
    global ParksDoc
    global InputLabel

    keyword = InputLabel.get()
    print("TextBox :",keyword)
    if(keyword != NONE):
        if SearchListBox.curselection()[0] == 0:
            pass
    for row in ParksDoc.iter("row"):
        RenderText.insert(INSERT, "[")
        RenderText.insert(INSERT, row.findtext("MANAGE_NO"))
        RenderText.insert(INSERT, "] ")
        RenderText.insert(INSERT, "공원 이름: ")
        RenderText.insert(INSERT, row.findtext("PARK_NM"))
        RenderText.insert(INSERT, "\n")
        if (row.findtext("PARK_SPORTS_FACLT_DTLS") != None):
            RenderText.insert(INSERT, "공원시설: ")
            RenderText.insert(INSERT, row.findtext("PARK_SPORTS_FACLT_DTLS"))
            RenderText.insert(INSERT, "\n")
        RenderText.insert(INSERT, "주소: ")
        RenderText.insert(INSERT, row.findtext("REFINE_LOTNO_ADDR"))
        RenderText.insert(INSERT, "\n\n")


def InitRenderText():
    global RenderText
    RenderTextScrollbar = Scrollbar(g_Tk)
    RenderTextScrollbar.pack()
    RenderTextScrollbar.place(x=375, y=200)
    TempFont = font.Font(g_Tk, size=10, family='Consolas')
    RenderText = Text(g_Tk, width=49, height=27, borderwidth=12, relief='ridge', yscrollcommand=RenderTextScrollbar.set)
    RenderText.pack()
    RenderText.place(x=10, y=215)
    RenderTextScrollbar.config(command=RenderText.yview)
    RenderTextScrollbar.pack(side=RIGHT, fill=BOTH)
    RenderText.configure(state='disabled')

ParksDoc = LoadXMLFromFile()
InitTopText()
InitSearchListBox()
InitInputLabel()
InitSearchButton()
InitRenderText()
g_Tk.mainloop()