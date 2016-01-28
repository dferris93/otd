from flask import abort, Flask, Response, request
from functools import partial
import mimetypes
import os

class ConfigObject(object):
    def __init__(self):
        self.downloadurl = '/otd'
        self.filepath = '/home/dferris/downloads'
        self.debug = False

global config
config = ConfigObject()

app = Flask(__name__)

@app.route(config.downloadurl, methods=['GET'])
def send_file():
    fname = request.args.get('f', None)

    if not fname:
        abort(404)

    file_path = os.path.join(config.filepath, fname)
    print file_path

    def generate(file_path):
        try:
            with open(file_path, 'r') as f:
                for byte in iter(partial(f.read, 65536), ''):
                    yield byte
        except IOError:
            abort(500)
        except OSError:
            abort(500)

        try:
            os.unlink(file_path)
        except OSError:
            abort(500)

    mt = mimetypes.guess_type(file_path)[0]
    if not mt:
        mt = "binary/octet-stream"

    try:
        t = os.stat(file_path)
    except OSError:
        abort(500)

    sz=str(t.st_size)

    return Response(
            generate(file_path),
            mimetype=mt,
            headers={"Content-Type:" : mt,
                     "Content-Disposition" : "attachment;filename=%s" % (
                            fname),
                     "Content-Length" : sz
                    })

def main():
    app.debug = config.debug
    app.run()

if __name__ == "__main__":
    main()
