#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import time
from core import lanscan
from wrapper import get_arguments

if __name__ == "__main__":

    address_pool = get_arguments()
    address_amount = len(address_pool)
    start_time = time.time()

    alive_hosts, dead_hosts, other_errors = lanscan(address_pool, step=200, timeout=2)

    print('\nЗатрачено времени:', round(time.time() - start_time, 3), 'секунд')
    print('Адресов просканировано:', address_amount)
    print('Включенных хостов: ', len(alive_hosts))
    print('Выключенных хостов:', len(dead_hosts))
    print('Ответов с ошибками:', len(other_errors))

    #TODO: молчаливый режим ввести
    #TODO: добавить расчетчик времени сканирования

    if len(other_errors) != 0:
        for error in other_errors:
            print(error)