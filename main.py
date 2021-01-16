import eel, sys, os, shutil
from config import CK, CS
import tweepy
import urllib.request

API = ""
PROC = ""
IS_CANCELED = False
FOLDER = ""


@eel.expose
def py_set_target(id):
    global IS_CANCELED
    global PROC

    IS_CANCELED = False
    PROC = get_image(id)

def get_image(id):
    global FOLDER

    FOLDER = "./images/" + id + "/"
    if not os.path.exists(FOLDER): os.makedirs(FOLDER)
    for j, tweet in enumerate(tweepy.Cursor(API.user_timeline, id=id, include_rts=False).items()):
        if not hasattr(tweet, "extended_entities"): continue
        for i, img in enumerate(tweet.extended_entities["media"]):
            if "video_info" in img: continue
            urllib.request.urlretrieve(img["media_url"], FOLDER + tweet.id_str + "_" + str(i) + ".png")    
        yield j

@eel.expose
def py_get_image():
    if IS_CANCELED == True: return "CANCEL"
    try:
        return PROC.__next__()
    except tweepy.RateLimitError as e:
        print(e)
        return "RATE_LIMIT_ERROR"
    except tweepy.error.TweepError as e:
        print(e)
        ret = ""
        if e.reason == "Twitter error response: status code = 404": ret = "NON_EXIST_USERID"
        else: ret = "ERR"
        shutil.rmtree(FOLDER)
        return ret
    except StopIteration as e:
        print(e)
        return "SUCCESS"
    except Exception as e:
        print(e)
        shutil.rmtree(FOLDER)
        return "ERR"

@eel.expose
def py_cancel():
    global IS_CANCELED
    IS_CANCELED = True


def onCloseWindow(page, sockets):
    print(sockets)
    print(page + 'が閉じられました。プログラムを終了します')
    sys.exit()

def main():
    global API

    API = tweepy.API(tweepy.AppAuthHandler(CK, CS))
    eel.init("web/dist")
    eel.start("index.html", close_callback=onCloseWindow)
    sys.exit()

if __name__ == "__main__":
    main()