#!/usr/bin/env python3

import websocket, json
from housepy import config, log

def send(data):
    data = {'pulses': data}
    try:
        data = json.dumps(data)
    except Exception as e:
        log.error("JSON failed: %s" % e)
        return
    try:
        socket = websocket.create_connection("ws://localhost:%s/websocket" % config['server']['port'])
        result = socket.recv()
        log.info(result)
    except Exception as e:
        log.error(e)
        return
    socket.send(data)
    result = socket.recv()
    log.info(result)
    socket.close()

if __name__ == "__main__":
    # pulses = [(1.0, 400), (0.5, 200)]
    # pulses = [(0.2, 200), (0.0, 500), (0.4, 200), (0.0, 500), (0.6, 200), (0.0, 500), (0.8, 200), (0.0, 500), (1.0, 200), (0.0, 500)]
    pulses = [(1.0, 500), (0.0, 500)]
    send(pulses)


    # note that low intensity requires a slightly longer duration (ie, (0.1, 100) wont sound)