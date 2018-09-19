#!/usr/bin/python3
# -*- coding: utf-8 -*-

import ipaddress
import logging


def get_list_ip(rangeIP, is_str=True):

    result = set()

    # Удаляю пробелы из строки
    rangeIP = rangeIP.replace(' ', '')
    # Разделяю строку по ','
    split_range = rangeIP.split(',')

    for element in split_range:
        try:
            if element.find('-') != -1:
                pair = element.split('-')

                second_address = int(ipaddress.IPv4Address(pair[0]))
                first_address = int(ipaddress.IPv4Address(pair[1]))

                # Переворачиваю пару адресов в порядке возрастания
                if first_address > second_address:
                    first_address, second_address = second_address, first_address

                for address in range(first_address, second_address + 1):
                    result.add(ipaddress.IPv4Address(address))

            elif element.find('/') != -1:
                network = ipaddress.IPv4Network(element)
                network_hosts = list(ipaddress.ip_network(network).hosts())
                result.update(network_hosts)
            else:
                result.add(ipaddress.IPv4Address(element))
        except (ipaddress.AddressValueError, ipaddress.NetmaskValueError, ValueError):
            logging.warning(
                'Неправильно задан ip или network или range ip: %s' % (element))
            continue

    if is_str:
        result = list(map(lambda ip: str(ip), result))

    return result


if __name__ == "__main__":

    # Пример использования
    print(get_list_ip("10.1.0.0-10.1.0.10, 10.1.2.0-10.1.2.25, 10.2.1.2, 10.2.0.0/24"))
