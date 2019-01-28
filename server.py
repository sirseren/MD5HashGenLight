import os

from flask import Flask, jsonify, request
from tasks import calc_md5_hash_of_remote_file
from config import PORT, DOWNLOAD_PATH
from celery import states



#init Flask app
app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)


@app.route('/submit', methods=['POST'])
def submit():
    """ Adds a new task to the hash generation queue
    Returns:
        str: Task's id
    """
    url = request.form.get('url')
    email = request.form.get('email')
    task_id = calc_md5_hash_of_remote_file.delay(url, email)
    return jsonify({'id': str(task_id)}), 201


@app.route('/check', methods=['GET'])
def check():
    """ Check state of task
    Returns:
        str: result of processed task
    """
    task_id = request.args.get('id')

    if not task_id:
        return jsonify({'status': states.FAILURE, 'error': 'Bad task id'}), 404

    result = calc_md5_hash_of_remote_file.AsyncResult(task_id)

    if result.state == "PENDING":
        return 'task does not exist', 404
    elif result.state == "FAILURE":
        return '{"status":"failure"}'
    elif result.state == "STARTED":
        task_status = '{"status":"running"}'

    try:
        hash_value = result.get()[0]
        url = result.get()[1]

    except ValueError as e:
        return {'status': states.FAILURE, 'error': str(e)}, 400

    if result.state == 'SUCCESS':
        return jsonify({'md5': hash_value, 'status': states.SUCCESS, 'url': url})


def validate_settings():
    """ Validate settings values """
    if not os.path.isdir(os.path.abspath(DOWNLOAD_PATH)):
        raise ValueError('DOWNLOAD_PATH must be valid path to existing directory')


if __name__ == '__main__':
    validate_settings()
    app.run(debug=False, port=PORT)