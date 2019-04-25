#!/usr/bin/env python
import socket


def get_free_port(remote_ip="localhost"):
    """
    This method will scan all the ports and provide a free port
    :param remote_ip: Host name of server
    :return: Integer - Free Port
    """

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((remote_ip, 0))
    addr, port = s.getsockname()
    s.close()

    return port
