#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import sys
import ipaddress
import argparse

def get_arguments():

    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('--address', type=ipaddress.IPv4Address)
    parser.add_argument('--network', type=ipaddress.IPv4Network)
    parser.add_argument('--address-range', type=str)
    parser.add_argument('--networks', type=str)

    arguments = parser.parse_args()
    print(arguments.address)

    return arguments


if __name__ == "__main__":

    print(get_arguments())
