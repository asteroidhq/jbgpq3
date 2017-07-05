from jbgpq3 import app
import logging
from logging.handlers import SysLogHandler
import syslog

if __name__ == '__main__':
    handler = SysLogHandler(address='/var/run/syslog', facility='local1')
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)s: [%(levelname)s] %(message)s')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    app.run(debug=True, port=5010, host='::')

