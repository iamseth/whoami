import timeit
import socket
import random
import platform

from flask import Flask, request, Response

app = Flask(__name__)


@app.route("/")
def index():
    headers, remote_addr = request.headers, request.remote_addr

    def generate():
        yield f"Hostname: {platform.node()}\n"
        yield f"Remote Addr: {remote_addr}\n"

        for iface in socket.getaddrinfo(socket.gethostname(), None):
            yield f"IP: {iface[4][0]}\n"

        for header in headers:
            field, value = header
            yield f"{field}: {value}\n"

    return Response(generate())


@app.route("/live")
def liveness_probe():
    return "we are live"


@app.route("/ready")
def readiness_probe():
    return "we are ready"


@app.route("/work")
def work():
    try:
        iterations = int(request.args.get("i", "100"))
    except ValueError:
        return "invalid iterations", 400

    start_time = timeit.default_timer()
    for _ in range(iterations):
        random.randint(0, 128)
    elapsed = timeit.default_timer() - start_time
    return f"time elapsed: {elapsed}s"
