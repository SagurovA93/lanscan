#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import time
from core import lanscan
from wrapper import get_arguments

if __name__ == "__main__":

    address_pool, step, timeout, v_mode, S_mode, e_mode = get_arguments()
    address_amount = len(address_pool)
    start_time = time.time()
    
    if (v_mode == True):
        # TODO: аппроксимационная формула для расчета времени нужна.
        print('\nшаг:', step, 'интервал шага:', timeout)
        print(
            'Ожидаемое время сканирования:', 
            round((address_amount / step) * timeout + ((address_amount / step) * timeout) * 0.4, 3), 'секунд', '\n' )
        
    alive_hosts, dead_hosts, other_errors = lanscan(address_pool, step=step, timeout=timeout)

    if S_mode == False:

        for address in alive_hosts:
            print(address, alive_hosts[address]['mac address'], ' ответил через:', alive_hosts[address]['respond time'])

        print('\nЗатрачено времени:', round(time.time() - start_time, 3), 'секунд')
        print('Адресов просканировано:', address_amount)
        print('Включенных хостов: ', len(alive_hosts))
        print('Ответов с ошибками:', len(other_errors), '\n')
    
    if (v_mode == True) or (e_mode == True):
        if len(other_errors) != 0:
            for error in other_errors:
                print(error)
