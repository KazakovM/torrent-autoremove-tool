from utorrentapi import UTorrentAPI
from time import sleep
import config
import datetime
import json
import shutil

global PORT, LOGIN, PASSWORD, MAXTORRENTS, FREE_SPACE


def culc_free_space():
    total, used, free = shutil.disk_usage("/")
    return round(free / 2**30, 2)

def log(level, message):
    with open('log.txt', 'a', encoding="UTF-8") as file:
        now = datetime.datetime.now()
        file.write(f"[{now}] - {level} - {message}\n")


def loadConfig():
    with open('..\\config.json', 'r', encoding="UTF-8") as file:
        js = json.load(file)
        global PORT, LOGIN, PASSWORD, MAXTORRENTS, FREE_SPACE
        PORT = js["PORT"]
        LOGIN = js["LOGIN"]
        PASSWORD = js["PASSWORD"]
        MAXTORRENTS = js["MAXTORRENTS"]
        FREE_SPACE = js["FREE_SPACE"]


loadConfig()

while True:
    try:
        apiclient = UTorrentAPI(f'http://127.0.0.1:{PORT}/gui', LOGIN, PASSWORD)
        try:
            if apiclient is not None:
                torrents = apiclient.get_list()
                time = 0
                id = 0
                for i, torrent in enumerate(torrents['torrents']):
                    if time == 0 or time > torrent[23]:
                        time = torrent[23]
                        id = i
                if len(torrents['torrents']) > MAXTORRENTS or culc_free_space() < FREE_SPACE:
                    apiclient.removedata(torrents['torrents'][id][0])
                    log("INFO", f"Удаление {torrents['torrents'][id][2]} прошло успешно!")
        except Exception as e:
            log("ERROR", f"Неизвестная ошибка: {e}")

    except Exception as e:
        log("ERROR", f"Ошибка соединения: {e}")
    sleep(60)
