#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import re
import ipaddress
import argparse

def get_arguments():

    scan_address = []

    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('--address', type=str, help="Адреса или диапазоны адресов (через \'-\')")
    parser.add_argument('--network', type=str, help="Адреса сетей для сканирования через \',\'")
    parser.add_argument('-s', '--step', type=int, help="Шаг сканирования в кол-ве адресов за шаг")
    parser.add_argument('-t', '--timeout', type=float, help="Время шага в секундах")
    parser.add_argument('-v', '--verbose', action="store_true", help="Выводит все на stdout")
    parser.add_argument('-S', '--silence', action="store_true", help="Не выводит ничего на stdout")
    parser.add_argument('-e', '--errors', action="store_true", help="Выводит информацию об ошибках на stdout")

    arguments = parser.parse_args()

    if arguments.step != None:
        step = arguments.step
        max_step = 900

        if step > max_step:
            print('Шаг искусственно ограничивается: ', max_step)
            step = max_step

    else:
        step = 200

    if arguments.timeout != None:
        timeout = arguments.timeout
        min_timeout = 1
        if timeout < min_timeout:
            print('Минимальный timeout = 1 секунда')
            timeout = min_timeout

    else:
        timeout = 2

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

    return scan_address, step, timeout, arguments.verbose, arguments.silence, arguments.errors


if __name__ == "__main__":

    address_to_scan = get_arguments()
    for address in address_to_scan:
        print(address)
