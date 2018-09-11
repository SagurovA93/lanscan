#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import ipaddress
import argparse
import re

def get_arguments():

    scan_address = []

    parser = argparse.ArgumentParser(add_help=True)
    #TODO: Добавить справку в help!
    #TODO: Добавить аргументы для step, и timeout параметров!
    parser.add_argument('--address', type=str)
    parser.add_argument('--network', type=str)

    arguments = parser.parse_args()

    if arguments.address != None:
        address_range = []

        # Удаляю пробелы из строки
        arguments.address = re.sub(r'\s+', '', arguments.address, flags=re.UNICODE)
        # Разделяю строку по ',' или ';'
        split_range = re.split(r'[;,]', arguments.address)

        for pair in split_range:

            if not re.search(r'-', pair):
                try:
                    scan_address.append(ipaddress.IPv4Address(pair))

                except ipaddress.AddressValueError:
                    continue

            else:
                pair = re.split(r'[-]', pair)

            try:
                address_range.append(ipaddress.IPv4Address(pair[0]))
                address_range.append(ipaddress.IPv4Address(pair[1]))

            except ipaddress.AddressValueError:
                continue

        while address_range:
            first_address = int(address_range.pop(0))
            try:
                second_address = int(address_range.pop(0))
            except IndexError:
                second_address = 0

            # Переворачиваю пару адресов в порядке возрастания
            if first_address > second_address:
                first_address_temp = first_address
                first_address = second_address
                second_address = first_address_temp

            for address in range(first_address, second_address + 1):
                scan_address.append(ipaddress.IPv4Address(address))

    if arguments.network != None:

        networks = []

        # Разделяю строку по ',' или ';'
        split_range = re.split(r'[;,\s]', arguments.network)

        for element in split_range:
            try:
                networks.append(ipaddress.IPv4Network(element))

            except ipaddress.AddressValueError:
                continue

            except ipaddress.NetmaskValueError:
                continue

        for network in networks:
            network_hosts = list(ipaddress.ip_network(network).hosts())
            if len(network_hosts) != 0:
                for address in network_hosts:
                    scan_address.append(address)

    # Сортирую список и оставляю только уникальные элементы
    scan_address = sorted(list(set(scan_address)))

    return scan_address


if __name__ == "__main__":

    address_to_scan = get_arguments()
    for address in address_to_scan:
        print(address)