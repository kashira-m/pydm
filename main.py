import sys
import numpy as np
import requests
import threading
import time
import os

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
        filepaths = []
        for i in range(mltimes-1):
            start = dlseq[i] + 1
            end = dlseq[i+1]
            t = threading.Thread(target=downloader,args=(url, start, end, i))
            t.start()
            threads.append(t)
            filepaths.append("C:/Users/mopro/vDownloads/file{}".format(i))
    
        for thread in threads:
            thread.join()

        print("All downloads finished")
    else:
        print("An error occured")

    combine(filepaths, "C:/Users/mopro/vDownloads", "file.rar")


def downloader(url, start, end, num):
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
    'Range': 'bytes={}-{}'.format(start, end)}
    print("downloading:{}-{}".format(start, end))
    r = requests.get(url, headers=header)
    errors = [500, 502, 503]
    while True:
        r = requests.get(url, headers=header, stream=True)

        print("Status Code:{}".format(r.status_code))

        
        if not r.status_code in errors:
            break

        time.sleep(2)

    print("Download Finished:Thread {}".format(num))
    filepath = "C:/Users/mopro/vDownloads/file{}".format(num)
    with open(filepath, mode='wb') as file:
        
        file.write(r.content)
        print("Finished")


def combine(filepaths, opdir, opname):
    """
    op = output
    """
    output = os.path.join(opdir,opname)
    with open(output, mode='ab') as file:
        for filepath in filepaths:
            with open(filepath, mode='rb') as part:
                buff = part.read()
                file.write(buff)

    print("All files combined")



mlreq('http://dl3.downloadly.ir/Files/Software/Internet_Download_Manager_6.38_Build_1_Multilingual_Downloadly.ir.rar',10)