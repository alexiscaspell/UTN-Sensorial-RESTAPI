import errno
import os
import time
from typing import List

import psutil
from flask import Flask
from netifaces import AF_INET, gateways, ifaddresses, interfaces

logger = None


def set_logger(some_logger):
    global logger
    logger = some_logger


def path_join(*args):
    is_first_element=True
    normalized_args = [args[0]]

    for arg in args:
        if is_first_element:
            is_first_element=False
            continue

        if len(arg)>1 and (arg[0]=="/" or arg[0]=="\\"):
            if len(arg)==1:
                arg = ""
            else:
                arg = arg[1:]

        normalized_args.append(arg)

    return os.path.join(*normalized_args)


# BIENVENIDO A NEGROLAND


def make_directory_if_not_exists(path):
    if not os.path.isdir(path):
        intentos = 0

        while intentos < 6:
            intentos = intentos + 1
            try:
                os.makedirs(path)
                break
            except OSError as _:
                time.sleep(1)


class SystemMonitor:
    """Contiene metodos para obtener informacion del sistema en tiempo real."""
    @classmethod
    def memory(cls) -> dict:
        """Fields: (usage_percent)"""
        return {
            'usage_percent': dict(psutil.virtual_memory()._asdict())['percent']
        }

    @classmethod
    def cpu(cls) -> dict:
        """Fields: (usage_percent)"""
        return {'usage_percent': psutil.cpu_percent()}

    @classmethod
    def disk(cls, path: str = '/') -> dict:
        """Fields: (total, used, free, percent)"""
        disk_usage = dict(psutil.disk_usage(path)._asdict())
        return disk_usage

    @classmethod
    def ip4_addresses(cls, interface: str = None):
        ip_list = []
        some_interfaces = [interface
                           ] if interface is not None else interfaces()

        for interface in some_interfaces:
            if AF_INET in ifaddresses(interface):
                for link in ifaddresses(interface)[AF_INET]:
                    ip_list.append(link['addr'])

        return ip_list

    @classmethod
    def ip(cls):
        """Retorna la ip de la pc en la que corre"""
        gws = gateways()
        return cls.ip4_addresses(gws['default'][AF_INET][1])[0]
        # return '127.0.0.1'

    @classmethod
    def status(cls) -> dict:
        """Fields: (memory,cpu,disk)"""
        return {
            'memory': cls.memory(),
            'cpu': cls.cpu(),
            'disk': cls.disk(),
            'ip': cls.ip()
        }


if __name__ == '__main__':
    pass