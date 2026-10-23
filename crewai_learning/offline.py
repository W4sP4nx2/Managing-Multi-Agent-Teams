"""A temporary network boundary for the offline reference and its verification."""
from contextlib import contextmanager
import ipaddress
import socket
from unittest.mock import patch


@contextmanager
def blocked_network():
    """Reject external DNS/connections; preserve Jupyter's local kernel sockets."""
    attempts = []
    original_connect = socket.socket.connect
    original_connect_ex = socket.socket.connect_ex
    original_getaddrinfo = socket.getaddrinfo

    def local(host):
        if host == "localhost":
            return True
        try:
            return ipaddress.ip_address(host).is_loopback
        except (ValueError, TypeError):
            return False

    def check(host):
        if not local(host):
            attempts.append("external network attempt")
            raise AssertionError("OFFLINE_REFERENCE: external network access blocked")

    def connect(sock, address):
        if isinstance(address, tuple):
            check(address[0])
        return original_connect(sock, address)

    def connect_ex(sock, address):
        if isinstance(address, tuple):
            check(address[0])
        return original_connect_ex(sock, address)

    def getaddrinfo(host, *args, **kwargs):
        if host is not None:
            check(host)
        return original_getaddrinfo(host, *args, **kwargs)

    with patch.object(socket.socket, "connect", connect), \
         patch.object(socket.socket, "connect_ex", connect_ex), \
         patch.object(socket, "getaddrinfo", getaddrinfo):
        yield attempts
