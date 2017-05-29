# -*- coding: cp949 -*-
# -*- coding: utf-8 -*-

from xml.etree import ElementTree

##### global
loopFlag = 1
xmlFD = -1
ParksDoc = None


#### Menu  implementation
def printMenu():
    print("Welcome! Park Finder Program (xml version)")
    print("========Menu==========")
    print("Print root: p")
    print("print parklist: b")
    print("empty: e")
    print("Quit program:   q")
    print("==================")


def launcherFunction(menu):
    global ParksDoc
    if menu == 'q':
        QuitParkMgr()
    elif menu == 'p':
        PrintRootName()
    elif menu == 'b':
        PrintParkList(["park_nm"])
    elif menu == 'n':
        keyword = str(input('input keyword to search :'))
        printParkList(SearchParkTitle(keyword))
        print("-----------------------")
        print("-----------------------")
    else:
        print("error : unknow menu key")


#### xml function implementation
def LoadXMLFromFile():
    try:
       dom = ElementTree.parse("ansanpark.xml")  # XML 문서를 파싱합니다.
    except Exception:
         print("loading fail!!!")
    else:
         print("XML Document loading complete")
         return dom
    return None


def ParksFree():
    if checkDocument():
        ParksDoc.unlink()  # minidom 객체 해제합니다.


def QuitParkMgr():
    global loopFlag
    loopFlag = 0
#    ParksFree()


def PrintRootName():
    if checkDocument():
        print(ParksDoc.getroot())


def PrintParkList(tags):
    global ParksDoc
    if not checkDocument():  # DOM이 None인지 검사합니다.
        return None

    for row in ParksDoc.iter("row"):
        print(row.findtext("MANAGE_NO")+"/",row.findtext("PARK_NM")+"/",
              row.findtext("SIGUN_NM")+"/",
              row.findtext("REFINE_LOTNO_ADDR"))

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

def printParkList(plist):
    for res in plist:
        print(res)


def checkDocument():
    global ParksDoc
    if ParksDoc == None:
        print("Error : Document is empty")
        return False
    return True


##### run #####
while (loopFlag > 0):
    printMenu()
    menuKey = str(input('select menu :'))
    ParksDoc = LoadXMLFromFile()
    launcherFunction(menuKey)
else:
    print("Thank you! Good Bye")