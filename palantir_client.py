import metrics
import connect
import time
import signal
import sys
from functools import partial
import json


def close_metrics(signal, frame, metrics):
    for metric in metrics:
        metric.close()
    sys.exit(0)

if __name__ == '__main__':
    server_ip = '127.0.0.1'
    metric_lst = [
        metrics.Name(),
        metrics.Time(update=2),
        metrics.Uptime(update=2),
        metrics.Kernel(update=86400),
    ]

    sigint_handler = partial(close_metrics, metrics=metric_lst)
    signal.signal(signal.SIGINT, sigint_handler)

    with connect.connection(server_ip) as conn:
        i = 10
        while i > 0:
            message = dict()
            for metric in metric_lst:
                metric.update()
                data = metric.get_data()
                message[data[0]] = data[1]
            message_json = json.dumps(message)
            conn.send(message_json)
            i -= 1
            time.sleep(2)
