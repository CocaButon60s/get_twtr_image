# 最新から最大3200ツイートまでを取得
# conding:utf-8
import json
import urllib.request
from requests_oauthlib import OAuth1Session
from config import *
import os
import time
import sys

TL = "https://api.twitter.com/1.1/statuses/user_timeline.json" # タイムライン

class History_Mng:
    def __init__(self):
        self.__history = [-1, -2, -3]
        self.__p = 0
    def write(self, ID):
        self.__history[self.__p] = ID
        np = self.__p + 1
        if len(self.__history) <= np: self.__p = 0
        else: self.__p = np
    def is_same(self): return len(set(self.__history)) == 1

class Param_Mng:
    def __init__(self, userID, count):
        self.__param = {
            "screen_name": userID,    # 取得したい人のアカウント名(@を除く)
            "count": count,           # 一度に取得したいツイート数(上限200)
            "include_entities": True, # エンティティ(画像や動画など)を含むかどうかを指定
            "exclude_replies": False, # その人が返信しているツイートを含むか
            "include_rts": False      # その人がリツイートしているツイートを含むか
        }
        self.__id_h = History_Mng()
    def update(self, ID):
        self.__id_h.write(ID)
        self.__param.update({"max_id":ID})
    def get_param(self): return self.__param
    def get_endflg(self): return self.__isEnd
    def is_same_id(self): return self.__id_h.is_same()

def saveContents(timeline, folder, param):
    # タイムラインから1ツイート分取得
    for content in timeline:
        param.update(content["id"])
        if "extended_entities" not in content: continue
        if "video_info" in content: continue
        # 1ツイート内に複数画像がある場合もあるため
        for i, img in enumerate(content["extended_entities"]["media"]):
            title   = folder + "/" + content["id_str"] + "_" + str(i) + ".png"
            imgURL  = img["media_url"]
            urllib.request.urlretrieve(imgURL, title)

def main():
    # UI
    userID = input("userID:")
    cnt = int(input("Get Count(MAX 180):"))
    at_once = int(input("Get at Once(MAX 200):"))

    if (cnt > 180) or (cnt < 0): sys.exit()
    if (at_once > 200) or (at_once < 0): sys.exit()
    # パラメータ設定
    param = Param_Mng(userID, at_once)
    # OAuth認証 セッション開始
    twitter = OAuth1Session(CK, CS, AT, AS)
    # 保存するフォルダ
    folder = "./images/" + userID
    # フォルダがない場合は作成する
    if not os.path.exists(folder): os.makedirs(folder)
    for i in range(cnt):
        print(str(i+1) + "回目")
        # タイムライン取得
        res = twitter.get(TL, params=param.get_param())
        timeline = json.loads(res.text)

        saveContents(timeline, folder, param)
        if param.is_same_id():break
        time.sleep(1)

if __name__ == "__main__":
    try: main()
    except Exception as e: print(e)