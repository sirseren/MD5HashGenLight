from flask import Flask, jsonify, request
from tasks import calc_md5_hash_of_remote_file
from config import PORT


#init Flask app
app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)


#routing POST /submit

@app.route('/submit', methods=['POST'])
def post_metod_process():
    url = request.form.get('url')
    email = request.form.get('email')
    id = calc_md5_hash_of_remote_file.delay(url, email)
    return str('{"id":"' + str(id) + '"}')


#routing GET /check

@app.route('/check', methods=['GET'])
def get_method_process():
    task_id = request.args.get('id')
    result = calc_md5_hash_of_remote_file.AsyncResult(task_id)
    state = result.state
    if state == 'SUCCESS':
        task_status = '{"md5":"'+result.get()+'"}'
    elif state == "PENDING":
        return 'task does not exist',404
    elif state == "STARTED":
        task_status = '{"status":"running"}'
    elif state == "FAILURE":
        task_status = '{"status":"failure"}'
    return task_status



#app.run(debug=False, port=PORT)