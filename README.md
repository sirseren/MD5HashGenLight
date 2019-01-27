# MD5HashGenLight
MD5 Hash Generator

### Installation
```
$ python3.6 -mvenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```
### Starting Redis:
```
$ redis-server
```

Starting the celery worker:
```
$ celery -A tasks worker -l info -P eventlet
```
