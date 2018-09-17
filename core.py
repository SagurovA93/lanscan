#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import re
import socket
import asyncore
import struct
import time
import random
from time import localtime, strftime

def lanscan(address_pool, step=200, timeout=2):

    alive_hosts = {}
    dead_hosts = []
    other_errors = []

    class requester(asyncore.dispatcher):

        def __init__(self, destination_address):
            asyncore.dispatcher.__init__(self)

            self.create_socket()
            self.timeout = timeout
            self.destination_address = destination_address
            self.handle_write()

        def build_icmp_packet(self, icmp_identifier=1, icmp_sequence=1):

            def checksumm(packet):
                sum = 0
                countTo = (len(packet) / 2) * 2
                count = 0
                while count < countTo:
                    thisVal = packet[count + 1] * 256 + packet[count]
                    sum = sum + thisVal
                    sum = sum & 0xFFFFFFFF
                    count = count + 2

                if countTo < len(packet):
                    sum = sum + packet[len(packet) + 1]
                    sum = sum & 0xFFFFFFFF

                sum = (sum >> 16) + (sum & 0xFFFF)
                sum = sum + (sum >> 16)
                answer = ~sum
                answer = answer & 0xFFFF
                answer = answer >> 8 | (answer << 8 & 0xFF00)
                return answer

            icmp_header = struct.pack("!BBHHH", 8, 0, 0, icmp_identifier, icmp_sequence)
            # Данные пакеты - вкладываю время
            icmp_data = struct.pack("d", time.time())
            # Считаю контрольную сумму заголовка и вложенных данных
            icmp_checksum = checksumm(icmp_header + icmp_data)
            # Пересобираю заголовок пакета со значением контрольной суммы
            icmp_header = struct.pack("!BBHHH", 8, 0, icmp_checksum, icmp_identifier, icmp_sequence)
            # Переменная packet - сформированный пакет
            icmp_packet = icmp_header + icmp_data

            return icmp_packet

        def create_socket(self, family=socket.AF_INET, type=socket.SOCK_RAW):
            sock_send = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            sock_send.setblocking(0)
            self.set_socket(sock_send)

        def writable(self):
            pass

        def readable(self):
            self.readable_time = time.time() - self.time_sent

            if (not self.write and (self.timeout < (self.readable_time))):  #
                self.close()

            return not self.write

        def handle_write(self):
            self.connect((self.destination_address, 0))
            self.icmp_identifier = random.randint(1, 60000)
            self.packet = self.build_icmp_packet(self.icmp_identifier, icmp_sequence=1)
            # Время отправки
            self.time_sent = time.time()

            # Буферизуем данные для отправки:
            try:
                sent = self.send(self.packet)
                self.packet = self.packet[sent:]
                self.write = False

            except OSError as os_error:
                print(self.destination_address, ' : ', os_error)
                time.sleep(timeout)
                self.handle_write()

        def handle_read(self):
            packet = self.recv(1024)

            src_address, icmp_type, icmp_code, icmp_cheksum, icmp_identifier, icmp_sequence, time_stamp = self.ip_packet_analayser(
                packet)

            mac_address = self.find_mac_linux(src_address)
            self.timerequest = strftime("%Y-%m-%d %H:%M:%S", localtime())

            if (icmp_type == 0) and (icmp_code == 0) and (self.destination_address == src_address) and (self.icmp_identifier == icmp_identifier):

                self.close()

                alive_hosts[src_address] = {
                    'mac address': mac_address,
                    'respond time': round(time.time() - time_stamp, 5),
                    'checksum': icmp_cheksum,
                    'sequence number': icmp_sequence,
                    'request time': self.timerequest
                }

            elif icmp_type == 3:

                self.close()

                dead_hosts.append({
                    'ip address': self.destination_address,
                    'icmp code': icmp_code,
                    'checksum': icmp_cheksum,
                    'sequence number': icmp_sequence,
                    'request time': self.timerequest
                })

            else:
                other_errors.append({
                    'destination address': self.destination_address,
                    'source address': src_address,
                    'mac address': mac_address,
                    'icmp type': icmp_type,
                    'icmp code': icmp_code,
                    'checksum': icmp_cheksum,
                    'icmp identifier': icmp_identifier,
                    'sequence number': icmp_sequence,
                    'request time': self.timerequest
                })

        def ip_packet_analayser(self, ip_packet):
            ip_address = struct.unpack('!BBBB', ip_packet[12:16])
            src_address = "%d.%d.%d.%d" % (ip_address[0], ip_address[1], ip_address[2], ip_address[3])
            icmp_packet = ip_packet[20:]
            icmp_header = icmp_packet[0:8]
            icmp_type, icmp_code, icmp_cheksum, icmp_identifier, icmp_sequence = struct.unpack("!BBHHH", icmp_header)
            try:
                time_stamp = struct.unpack("d", icmp_packet[8:])[0]
            except:
                time_stamp = 0

            return src_address, icmp_type, icmp_code, icmp_cheksum, icmp_identifier, icmp_sequence, time_stamp

        #TODO: добавить обработку для windows
        def find_mac_linux(self, ip_address):

            ip_address = str(ip_address) + str(' ')
            mac_address = None

            for line in open('/proc/net/arp'):
                if ip_address in line:
                    mac_address = re.search(r"(([A-F\d]{1,2}\:){5}[A-F\d]{1,2})", line.upper()).groups()[0]

            return mac_address

    while address_pool:
        for address in address_pool[:step]:
            requester(destination_address=str(address))
            address_pool.remove(address)
        asyncore.loop(timeout=timeout, use_poll=True)

    return alive_hosts, dead_hosts, other_errors
