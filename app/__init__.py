from flask import abort, Flask, Response, request
import fcntl
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
    def generate(file_path):
        try:
            with open(file_path, 'r') as f:
                fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
                for byte in iter(partial(f.read, 65536), ''):
                    yield byte
        except IOError as e:
            print "IOError: %s File: %s" % (e, file_path)
            abort(500)
        except OSError as e:
            print "OSerror: %s File: %s" % (e, file_path)
            abort(500)
        finally:
            os.unlink(file_path)

    fname = request.args.get('f', None)
    if not fname:
        print "Invalid request arguments: %s" % fname
        abort(404)
    print "File Name: %s" % fname

    file_path = os.path.normpath(os.path.join(config.filepath,
            os.path.basename(fname)))
    print "File path: %s" % file_path

    content_disposition = 'attachment; filename="%s"' % (
                fname.encode('utf8'))

    print "Content disposition: %s" % content_disposition

    try:
        sz = str(os.stat(file_path).st_size)
    except OSError as e:
        print "OS error stating file: %s Error: %s Status Code 500" % (
                file_path,
                e)
        abort(500)

    mt = mimetypes.guess_type(file_path)[0]
    if not mt:
        mt = "binary/octet-stream"

    print "File: %s Size: %s Mime Type: %s" % (
            file_path,
            sz,
            mt)

    return Response(
            generate(file_path),
            mimetype=mt,
            headers={"Content-Type:" : mt,
                     "Content-Disposition" : content_disposition,
                     "Content-Length" : sz
                    })

def main():
    app.debug = config.debug
    app.run()

if __name__ == "__main__":
	main()
