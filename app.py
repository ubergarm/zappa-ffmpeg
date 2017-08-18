import subprocess
from flask import Flask, Response, request, json
from functools import wraps
from typing import List

app = Flask(__name__)


def args_required(*expected_args: str):
    """Confirm expected request args are present"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            for expected_arg in expected_args:
                if not request.args.get(expected_arg, None):
                    return Response(json.dumps({'Error': '{} parameter is required'.format(expected_arg)}),
                                    status=200,
                                    mimetype='application/json')
            return f(*args, **kwargs)
        return wrapper
    return decorator


def stream_shell_cmd(cmd: List[str], mimetype: str, chunksize: int = 16384) -> Response:
    """Returns a streaming flask Response of specified mimetype type given a shell command"""
    def streamer():
        p = subprocess.Popen(cmd,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE)

        while True:
            chunk = p.stdout.read(chunksize)
            if not chunk:
                app.logger.debug(p.stderr.read().decode('utf-8'))
                break
            yield chunk

    return Response(streamer(), 200, mimetype=mimetype)


@app.route('/')
@app.route('/version')
def version():
    cmd = ['bin/ffmpeg', '-version']
    mimetype = 'text/plain'
    return stream_shell_cmd(cmd, mimetype)


# We only need this for local development.
if __name__ == '__main__':
    app.run(debug=False)
