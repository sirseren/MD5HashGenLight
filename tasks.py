from celery import Celery
from utils import download_file, gen_md5_hash, remove_file, send_result_to_email
from config import CELERY_BACKEND_URL, CELERY_BROKER_URL

app = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_BACKEND_URL)


@app.task(track_started=True)
def calc_md5_hash_of_remote_file(url, email_to=''):
    filename = download_file(url)
    hash_result = str(gen_md5_hash(filename))
    remove_file(filename)
    if email_to:
        send_result_to_email(email_to, str(url), hash_result)
    return hash_result, url

