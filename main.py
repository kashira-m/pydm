import sys
import numpy as np
import requests
import threading
import time

from PyQt5.QtWidgets import QApplication, QLabel


def mlreq(url, mltimes):
    """
    header format to download part of file
    header = {'Range':'bytes=0-X'}

    """
    header = requests.head(url)
    print(header.headers)
    if header.headers.get('Accept-Ranges'):
        dlseq = np.linspace(-1, int(header.headers['Content-Length']), mltimes, dtype=int)
        threads = []
        for i in range(mltimes-1):
            start = dlseq[i] + 1
            end = dlseq[i+1]
            t = threading.Thread(target=downloader,args=(url, start, end, i))
            t.start()
            threads.append(t)
    
        for thread in threads:
            thread.join()

        print("All downloads finished")
    else:
        print("An error occured")
        
def downloader(url, start, end, num):
    header = {'Range': 'bytes={}-{}'.format(start, end)}
    print("downloading:{}-{}".format(start, end))
    r = requests.get(url, headers=header)

    while True:
        r = requests.get(url, headers=header)

        print("Status Code:{}".format(r.status_code))
        if r.status_code == 203:
            break

    print("Download Finished:Thread {}".format(num))
    filepath = "C:/Users/mopro/vDownloads/file{}".format(num)
    with open(filepath, mode='wb') as file:
        print(r.content[100]," ", num)

mlreq('http://dl3.downloadly.ir/Files/Software/Internet_Download_Manager_6.38_Build_1_Multilingual_Downloadly.ir.rar',10)