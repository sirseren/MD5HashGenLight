# MD5HashGenLight
MD5 Hash Generator

### Installation
Before installation please configure [config.py](https://github.com/sirseren/MD5HashGenLight/blob/master/config.py)
```
$ python3.6 -mvenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```
### Starting Redis:
```
$ redis-server
```
### Starting the celery worker:
```
$ celery -A tasks worker -l info -P eventlet
```
### Starting the server:
```
$ python -m server.py
```
### Example:
```
>>>curl -X POST -d "email=user@example.com&url=http://site.com/file.txt" http://localhost:8000/submit
{"id":"0e4fac17-f367-4807-8c28-8a059a2f82ac"}
>>> curl -X GET http://localhost:8000/check?id=0e4fac17-f367-4807-8c28-8a059a2f82ac
{"status":"running"}
>>> curl -X GET http://localhost:8000/check?id=0e4fac17-f367-4807-8c28-8a059a2f82ac
{"md5":"f4afe93ad799484b1d512cc20e93efd1","status":"done","url":"http://site.com/file.txt"}
```
