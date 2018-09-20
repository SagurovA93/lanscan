#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import core
import argparse

from sys import exit
from utils import get_list_ip


def lanscan(rangeIP, step=200, timeout=2):
    array_ip = get_list_ip(rangeIP)

    return core.lanscan(array_ip, step, timeout)


if __name__ == "__main__":

    # Аргументы командной строки
    parser = argparse.ArgumentParser(description='Сканер сети', add_help=True)
    parser.add_argument('rangeIP', metavar='IP', type=str, help='IP адресс, диапазоны адресов (через \'-\'), '
                                                                'адреса сетей для сканирования. Разделитель \',\'. '
                                                                'Например: 10.1.0.1, 10.1.0.2-10.1.0.10, 10.1.10.1.0/24')
    parser.add_argument('-s', '--step', type=int, default=200, help='Шаг сканирования в кол-ве адресов за шаг'
                                                                    '(default: %(default)s, min: 1, max: 900)')
    parser.add_argument('-t', '--timeout', type=int, default=1, help="Время шага в секундах (default: %(default)s, min: 1, max: ...)")
    parser.add_argument('-v', '--verbose', action="store_true", help="Выводит все на stdout")
    parser.add_argument('-S', '--silence', action="store_false", help="Не выводит ничего на stdout")
    parser.add_argument('-e', '--errors',  action="store_true", help="Выводит информацию об ошибках на stdout")
    args = parser.parse_args()

    address_pool   = get_list_ip(args.rangeIP)
    address_amount = len(address_pool)

    v_mode  = args.verbose
    s_mode  = args.silence
    e_mode  = args.errors
    step    = args.step
    timeout = args.timeout

    start_time = time.time()

    if (v_mode == True):
        # TODO: аппроксимационная формула для расчета времени нужна.
        print('\nшаг:', step, 'интервал шага:', timeout)
        print(
            'Ожидаемое время сканирования:',
            round((address_amount / step) * timeout + ((address_amount / step) * timeout) * 0.4, 3), 'секунд', '\n')
    try:
        alive_hosts, dead_hosts, other_errors = core.lanscan(address_pool, step=step, timeout=timeout)

    except PermissionError:
        print('Нужны права администратора')
        exit(1)


    if s_mode:

        for address in sorted(alive_hosts):
            print(address,
                  alive_hosts[address]['mac address'],
                  ' ответил через:', alive_hosts[address]['respond time']
                  )

        print('\nЗатрачено времени:', round(
            time.time() - start_time, 3), 'секунд')
        print('Адресов просканировано:', address_amount)
        print('Включенных хостов: ', len(alive_hosts))
        print('Ответов с ошибками:', len(other_errors), '\n')

    if (v_mode == True) or (e_mode == True):
        if len(other_errors) != 0:
            for error in other_errors:
                print(error)
