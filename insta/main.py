import pyautogui
import pyperclip
import time
import os
import sys
import easyocr
import re
import platform
import numpy
import cv2
import random
import datetime
import instaloader

import tkinter
from tkinter import *
from tkinter import messagebox
import threading



#画面初期化
def init():
  global root
  root = tkinter.Tk()
  root.geometry('415x170')
  root.title("InstaTool")

  global btngetuser
  btngetuser = tkinter.Button(text="ユーザ抽出", command=UserGetDef)
  btngetuser.place(x=170, y=60)

  global btnsndmsg
  btnsndmsg = tkinter.Button(text="DM送信", command=sndClick)
  btnsndmsg.place(x=170, y=110)

  root.mainloop()


def getpath():
    pf = platform.system()
    if pf == 'Windows':
        return "."
    elif pf == 'Darwin':
        return os.path.realpath(os.path.dirname(sys.argv[0]))

def readTxt(pth):
    f = open(pth, 'r', encoding='UTF-8')
    datalist = list(map(lambda x: str(x).replace("\n",""), f.readlines()))
    f.close()
    return datalist

def readAccountConf(pth):
    accountIDPWlist = []
    with open(pth, 'r') as file:
        for line in file:
            # 行をカンマで分割し、リストに追加
            # strip()で改行を削除
            accountIDPWlist.append(line.strip().split(','))
    return accountIDPWlist

def ChangeAccount(ID, PW):
    #その他ボタン遷移
    friicon = pyautogui.locateOnScreen(getpath() + '/icons/OtherBottun.png' , confidence=0.7)
    pyautogui.moveTo(friicon, duration=2)
    pyautogui.click(friicon)
    time.sleep(2)

    #ログアウト遷移
    friicon = pyautogui.locateOnScreen(getpath() + '/icons/LogoutBottun.png' , confidence=0.7)
    pyautogui.moveTo(friicon, duration=2)
    pyautogui.click(friicon)
    time.sleep(5)

    #ID入力欄まで遷移
    pyautogui.press('tab')
    pyautogui.press('tab')

    #ID&PW入力
    pyperclip.copy(ID)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    pyautogui.press('tab')
    pyperclip.copy(PW)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)

    #ログイン
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('enter')
    time.sleep(10)

    #メッセージボタンクリック
    friicon = pyautogui.locateOnScreen(getpath() + '/icons/msgbtn.png' , confidence=0.7)
    pyautogui.moveTo(friicon, duration=1)
    pyautogui.click(friicon)
    time.sleep(2)


#DMテンプレート読込
def readTmpTxt():
    
    f = open(os.path.realpath(os.path.dirname(sys.argv[0])) + r'/template.txt', encoding="utf-8")
    global template
    global template123
    template = f.read()
    f.close()

def writeTxt(pth, arr, mode):
    f = open(pth, mode)
    for i in range(len(arr)):
            f.write(arr[i] + '\n')
    f.close()


def dupdel(p1):
  ret = []
  for i in range(len(p1)):
     dup = False
     for j in range(len(ret)):
        if(p1[i] == ret[j]):
           dup = True
           break
                     
     if(dup==False):
           ret.append(p1[i])
  
  return ret

def randPos():
    
    x = random.randint(0, 1000)
    y = random.randint(0, 1000)

    return [x, y]

def wait1min(start):
    dtbreak = start + datetime.timedelta(minutes=1)
    curdt = datetime.datetime.now()
    while(dtbreak > curdt):
        curdt = datetime.datetime.now()

def randPlay(mode):
    
    #
    friicon = pyautogui.locateOnScreen(getpath() + '/icons/home.png' , confidence=0.8)
    pyautogui.moveTo(friicon, duration=1)
    pyautogui.click(friicon)
    time.sleep(3)

    if mode==0:
        friicon = pyautogui.locateOnScreen(getpath() + '/icons/find.png' , confidence=0.8)
    else:
        friicon = pyautogui.locateOnScreen(getpath() + '/icons/reel.png' , confidence=0.8)

    pyautogui.moveTo(friicon, duration=1)
    pyautogui.click(friicon)
    xoffset = random.randint(0, 200) + 900
    pyautogui.moveTo(x=xoffset, y=friicon.top, duration=1)
    time.sleep(7)

    rotate = random.randint(2, 10)
    height = random.randint(1, 3)
    stop = random.randint(0, 8)
    for i in range(rotate):
        pyautogui.scroll(-1000 * height)
        time.sleep(stop)
    
    
    friicon = pyautogui.locateOnScreen(getpath() + '/icons/msgbtn.png' , confidence=0.7)
    pyautogui.moveTo(friicon, duration=1)
    pyautogui.click(friicon)
    time.sleep(2)


#ユーザ抽出step1
def getClick():
 
  btngetuser["state"] = "disable"
  btnsndmsg["state"] = "disable"
  root.title("[ユーザ抽出中]")
  t = threading.Thread(target=getWrap)
  t.start()

#ユーザ抽出step2
def getWrap():
  
  global extunlist
  extunlist = readTxt(getpath() + '/in.txt')

  for i in range(len(extunlist)):
    if(extunlist[i] != ""):
       extractProc(extunlist[i])

  extunlist = readTxt(getpath() + '/out.txt')
  extunlist = dupdel(extunlist)
  writeTxt(getpath() + '/out.txt', extunlist, 'w')
  
  btngetuser["state"] = "normal"
  btnsndmsg["state"] = "normal"
  messagebox.showinfo("", "ユーザ抽出完了")

#ユーザ抽出step3
def extractProc(un):

    #初期位置決定のため　応答時間があるため3秒以下は難しい
    friicon = pyautogui.locateOnScreen(getpath() + '/icons/search.png' , confidence=0.7)
    pyautogui.click(friicon, duration=1)
    time.sleep(3)

    friicon = pyautogui.locateOnScreen(getpath() + '/icons/search2.png' , confidence=0.7)
    pyautogui.moveTo(friicon, duration=1)
    pyperclip.copy(un)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)

    pyautogui.keyDown('down')
    pyautogui.keyUp('down')
    time.sleep(1)

    #再検索用スリープタイム
    pyautogui.keyDown('enter')
    pyautogui.keyUp('enter')
    time.sleep(1)

    try:
        pos = pyautogui.locateOnScreen(getpath() + '/icons/follower.png' , confidence=0.8)
        pyautogui.moveTo(pos, duration=1)
        time.sleep(1)
        pyautogui.click(pos)
        time.sleep(3)


        imgcnt = 0
        for i in range(2):
            curloopcnt = 0
            scrollcnt = random.randint(25,60)

            friicon = pyautogui.locateOnScreen(getpath() + '/icons/search3.png' , confidence=0.8)
            tx = friicon.left + 220
            ty = friicon.top + 80
            pyautogui.moveTo(x=tx, y=ty, duration=1)

            while(True):
                pyautogui.screenshot(getpath() + "/imgs/" + str(imgcnt) + ".png",  region=(600,420,400,500))

                previmg = None
                curimg = None
                if(imgcnt > 0):
                    previmg = cv2.imread(getpath() + "/imgs/" + str(imgcnt-1) + ".png")
                    curimg = cv2.imread(getpath() + "/imgs/" + str(imgcnt) + ".png")

                imgcnt = imgcnt + 1
                time.sleep(random.randint(3,8))
                pyautogui.scroll(-500)
                
                if(imgcnt > 1 and numpy.array_equal(previmg, curimg) == True):
                    break

                if(curloopcnt > scrollcnt):
                    break

                curloopcnt = curloopcnt + 1
                time.sleep(3)

            if(i==0):
                #pyautogui.moveTo(x=1750, y=500, duration=1)
                #pyautogui.click(x=1750, y=500)
                pos = pyautogui.locateOnScreen(getpath() + '/icons/close.png' , confidence=0.8)
                pyautogui.moveTo(pos, duration=1)
                time.sleep(1)
                pyautogui.click(pos)
                time.sleep(3)
                pos = pyautogui.locateOnScreen(getpath() + '/icons/follow.png' , confidence=0.8)
                pyautogui.moveTo(pos, duration=1)
                time.sleep(1)
                pyautogui.click(pos)
                time.sleep(3)


        #pyautogui.moveTo(x=1750, y=500, duration=1)
        #pyautogui.click(x=1750, y=500)
        pos = pyautogui.locateOnScreen(getpath() + '/icons/close.png' , confidence=0.8)
        pyautogui.moveTo(pos, duration=1)
        time.sleep(1)
        pyautogui.click(pos)

        reader = easyocr.Reader(['en'], gpu=True)

        # OCRを実行したい画像のパス
        image_paths = [str(i) +".png" for i in range(imgcnt)]
        # 画像を開く
        unames = []
        for item in image_paths:
            results = reader.readtext(getpath() + "/imgs/" + item)
            # 結果を出力
            for (bbox, text, prob) in results:
                if(' ' not in text and len(text) > 3):
                    unames.append('@' + text)

            os.remove(getpath() + "/imgs/" + item)

        writeTxt(getpath() + '/out.txt', unames, 'a')
    except Exception as e:
        pass


#DM送信step1
def sndClick():
 
  btngetuser["state"] = "disable"
  btnsndmsg["state"] = "disable"
  root.title("[DM送信中]")
  t = threading.Thread(target=sendWrap)
  t.start()

#DM送信step2
def sendWrap():
  global sendlist
  sendlist = readTxt(getpath() + '/send.txt')
  readTmpTxt()

  global accountList
  accountList = readAccountConf(getpath() + '/accountInfo.txt')

  playflgs = []
  playmindelay = []

  """一時措置
  for i in range(6):
    playflgs.append(False)
    playmindelay.append(random.randint(1,5))

  startdt = datetime.datetime.now()
  nextplaydt =  startdt + datetime.timedelta(minutes=playmindelay[0])
　"""

  for i in range(len(sendlist)):
    if(sendlist[i] != ""):
        sendProc(sendlist[i], i)
    if(i != 0 and i % 50 == 0):
        ListNum = i // 50
        accountID = accountList[ListNum][0]
        accountPW = accountList[ListNum][1]

        ChangeAccount(accountID, accountPW)
    
    """
    curdt = datetime.datetime.now()
    for j in range(6):
        if(playflgs[j] == False and curdt > nextplaydt):
            randPlay(random.randint(0,1))
            playflgs[j] = True
            nextplaydt =  startdt + datetime.timedelta(minutes=((10 * (j + 1)) + playmindelay[j]))
            break
    """


  btngetuser["state"] = "normal"
  btnsndmsg["state"] = "normal"
  root.title("InstaTool")
  messagebox.showinfo("お知らせ","DM送信完了")

#DM送信step3
def sendProc(un, idx):

    startdt = datetime.datetime.now()

    if(idx == 0):
        friicon = pyautogui.locateOnScreen(getpath() + '/icons/msgbtn.png' , confidence=0.7)
        pyautogui.moveTo(friicon, duration=1)
        pyautogui.click(friicon)
        time.sleep(2)

    friicon = pyautogui.locateOnScreen(getpath() + '/icons/msgsbtn.png' , confidence=0.7)
    pyautogui.moveTo(friicon, duration=2)
    pyautogui.click(friicon)
    time.sleep(2)

    """キーボード操作で可能なためコメントアウト
    friicon = pyautogui.locateOnScreen(getpath() + '/icons/usersinpt.png' , confidence=0.7)
    pyautogui.moveTo(friicon, duration=1)
    time.sleep(5)
    """

    pyperclip.copy(un)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(2)

    #ユーザの存在チェックを実施する　いなかった場合スキップ
    try:
        UserCheckFlg = pyautogui.locateOnScreen(getpath() + '/icons/UserExistCheck.png' , confidence=0.7)
        time.sleep(1)
        pyautogui.press('tab')
        time.sleep(0.5)
        pyautogui.press('enter')
        writeTxt(getpath() + '/miss.txt', [un], 'a')
        time.sleep(3)
        
    except Exception as e:
        pyautogui.press('tab')
        #pyautogui.keyUp('tab')
        time.sleep(0.5)
        pyautogui.press('enter')
        #pyautogui.keyUp('enter')
        time.sleep(0.5)
        pyautogui.press('tab')
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(2)


        #ここからテンプレート文を読み込み貼り付け
        #pyautogui.click(friicon)
        #画面左上に移動
        pyautogui.moveTo(10,10)
        pyperclip.copy(template)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        #貼り付けたテンプレートを送信
        pyautogui.press('enter')  


        writeTxt(getpath() + '/sentUsers.txt', [un], 'a')
        time.sleep(3)
    

    """
    #ここからテンプレート文を読み込み貼り付け
    #pyautogui.click(friicon)
    pyperclip.copy(template)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)
    #貼り付けたテンプレートを送信
    pyautogui.press('enter')
    time.sleep(0.5)
    #適当な場所に移動
    rpos = randPos()
    pyautogui.moveTo(rpos[0], rpos[1], duration=1)
    """

    """実装が機能していないためコメントアウト
    try:
        friicon = pyautogui.locateOnScreen(getpath() + '/icons/next.png' , confidence=0.8)
        pyautogui.moveTo(friicon, duration=3)
        pyautogui.click(friicon)
        time.sleep(3)

        friicon = pyautogui.locateOnScreen(getpath() + '/icons/msgarea.png' , confidence=0.8)
        pyautogui.moveTo(friicon, duration=2)
        pyautogui.click(friicon)
        pyperclip.copy(template)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(3)

        friicon = pyautogui.locateOnScreen(getpath() + '/icons/submit.png' , confidence=0.8)
        pyautogui.moveTo(friicon, duration=2)
        pyautogui.click(friicon)
        time.sleep(3)

        #適当な場所に移動
        rpos = randPos()
        pyautogui.moveTo(rpos[0], rpos[1], duration=1)

    except Exception as e:
        writeTxt(getpath() + '/miss.txt', [un], 'a')
    """

def UserGetDef():
    loader = instaloader.Instaloader()

    # テキストファイルのパス
    file_path = 'login_user.txt'  # 拡張子は任意です

    # ファイルを読み込む
    with open(file_path, mode='r', encoding='utf-8') as file:
        line = file.readline().strip()  # 1行だけ読み込む
        data = line.split(',')  # カンマで分割

    loader.login(data[0], data[1])

    id = readAccountConf(getpath() + '/getUser.txt')

    #指定したIDのprofileオブジェクトを作成
    profile = instaloader.Profile.from_username(loader.context, "hyuu_to1023")#id:フォロワーを取得したいアカウントのユーザーID

    #指定したIDのフォロワーを全件取得
    followers = profile.get_followers()

    #ユーザーIDを出力する
    for follower in followers:
        print(follower.username)
        with open(getpath() + '/send.txt', mode='a', encoding='utf-8') as file:
            print("@"+follower.username, file=file)  # ファイルに書き込む

    messagebox.showinfo("", "ユーザ抽出完了")

#エントリーポイント
if __name__ == "__main__":
  
  if len(sys.argv) == 1:
    init()
  else:
    getWrap()


