from functools import partial
from config import *
import os
import hashlib
import time
import requests
import smtplib


def download_file(url):
    response = requests.get(url)
    filename = url[url.rfind("/") + 1:]
    print("filename = ", filename)
    if (os.path.isfile(DOWNLOAD_PATH +filename)): 
        print("filename old = ", filename)
        str_timestamp = str(time.time()).replace(".", "_")
        filename = filename.replace(".", str_timestamp+'.')
        print("filename new = ", filename)
    full_file_path = DOWNLOAD_PATH + filename
    print("full path = ", full_file_path)
    with open(full_file_path, 'wb') as f:
        f.write(response.content)
        print("downloaded")
    return full_file_path


def gen_md5_hash(filename):
    with open(filename, 'rb') as f:         
        hash_result = hashlib.md5()
        for buf in iter(partial(f.read, 128), b''):   #redo using chunks
            hash_result.update(buf)
    return hash_result.hexdigest()



def send_result_to_email(email_to, url,  result):
    smtp = smtplib.SMTP(MAIL_SERVER, MAIL_PORT)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(MAIL_USERNAME, MAIL_PASSWORD)
    msg = str('"md5": "' + result + '"')
    msg = 'Subject: {}\n\n{}'.format('MD5 Hash of ' + url, msg)
    print(msg)
    smtp.sendmail(MAIL_USERNAME, email_to, msg)
    smtp.quit()


def remove_file(filename):
    if os.path.isfile(filename):
        os.remove(filename)




