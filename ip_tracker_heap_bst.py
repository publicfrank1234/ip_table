import bisect
from collections import defaultdict
import random
import sys
import timeit
from dataclasses import dataclass, field
import heapq


@dataclass(order=True)
class IpRecord:
    sort_index: int = field(init=False, repr=False)
    ip_address: str
    in_top100: bool = False
    total_hits: int = 0

    def __post_init__(self):
        self.sort_index = self.total_hits

    def inc(self):
        self.total_hits += 1
        self.sort_index += 1


class IpTracker:
    """ This is using binary search in request_handled() to maintain top100 list """

    def __init__(self, n=100):
        """dict: lookup table, e.g. dict[ip] = counts; top100: ordered List, e.g. [(count, ip)]"""
        self.dict = {}  # key: ip; value: IpRecord
        self.top100 = []  # sorted list of top 100 IpRecords
        self.depth = n  # the total n IpRecords; default 100

    def request_handled(self, ip_address):
        """"O(1) insertion of ip address """
        ip_record = self.dict.get(ip_address, IpRecord(ip_address=ip_address))
        ip_record.inc()
        self.dict[ip_address] = ip_record
        if ip_record.in_top100:
            try:
                self.top100.remove(ip_record)
                self.__push_to_top100__(ip_record)
            except:
                print("we got an error")
            return

        if len(self.top100) >= 100:
            if ip_record.total_hits >= self.top100[0].total_hits:
                self.top100[0].in_top100 = False
                ip_record.in_top100 = True
                self.top100[0] = ip_record
                # self.__push_to_top100__(ip_record)
                return
        else:
            ip_record.in_top100 = True
            self.__push_to_top100__(ip_record)
            return

    def __push_to_top100__(self, ip_record):
        ip_record.in_top100 = True
        bisect.insort(self.top100, ip_record)

    def top100(self):
        """"return a list of ips ordered by counts: [(counts, ip)]"""
        return sorted(self.top100)[::-1]

    def clear(self):
        """"reset the memory"""
        self.dict = {}
        self.top100 = []


class IpTrackerHeap:
    """ This is using heap in request_handled() to maintain top100 list """

    def __init__(self, n=10):
        """dict: lookup table, e.g. dict[ip] = counts; top100: ordered List, e.g. [(count, ip)]"""
        self.dict = {}
        self.top100 = []
        self.depth = n

    def request_handled(self, ip_address):
        """"O(1) insertion of ip address """
        ip_record = self.dict.get(ip_address, IpRecord(ip_address=ip_address))
        ip_record.inc()
        self.dict[ip_address] = ip_record
        if ip_record.in_top100:
            heapq.heapify(self.top100)
            return

        if len(self.top100) >= 100:
            if ip_record.total_hits > self.top100[0].total_hits:
                top_item = heapq.heappop(self.top100)
                top_item.in_top100 = False
                ip_record.in_top100 = True
                heapq.heappush(self.top100, ip_record)
                return
        else:
            ip_record.in_top100 = True
            heapq.heappush(self.top100, ip_record)
            return

    def __push_to_top100__(self, ip_record):
        ip_record.in_top100 = True
        bisect.insort(self.top100, ip_record)

    def top100(self):
        """"return a list of ips ordered by counts: [(counts, ip)]"""
        return sorted(self.top100)[::-1]

    def clear(self):
        """"reset the memory"""
        self.dict = {}
        self.top100 = []


def ip_gen(): return ".".join(map(str, (random.randint(0, 255) for _ in range(4))))


if __name__ == "__main__":

    total_ip_numbers = sys.argv[1] if len(sys.argv) > 1 else 20*10**6
    ip_tracker = IpTracker()

    print(f'Test #1 -- ip from 255.255.255.0/24, count = ip[3] \n')
    print(f'\t step1 -- start generating 255.255.255.0/24 ip address \n')
    max_time = 0
    for i in range(256):
        for j in range(i):
            start = timeit.default_timer()
            ip_tracker.request_handled("255.255.255."+str(i))
            max_time = max(max_time, timeit.default_timer() - start)
    print(
        f'\t step1 -- finished !!! worst single-insertion time: {max_time} s \n')
    print(f'\t step2 -- get 100 most visited ip address \n')
    start = timeit.default_timer()
    print(f'\t top100 : {ip_tracker.top100}')
    pass_fail = True
    target = 255
    for i in ip_tracker.top100:
        if i.total_hits == target:
            target -= 1
            continue
        target = False
        break
    print(
        f'\t step2 -- finished !!!  { "Pass" if pass_fail else "Fail" } \n top100 time: {timeit.default_timer() - start} s \n')
    ip_tracker.clear()

    print(f'Test #2 -- random {total_ip_numbers} ips \n')
    print(f'\t step1 -- generate {total_ip_numbers} ip address \n')
    max_time = 0
    total_time = 0
    for i in range(int(total_ip_numbers)):
        random_ip = ip_gen()
        start = timeit.default_timer()
        ip_tracker.request_handled(random_ip)
        duration = timeit.default_timer() - start
        max_time = max(max_time, timeit.default_timer() - start)
        total_time += duration
    print(
        f'\t step1 -- finished !!! worst single-insertion time: {max_time} s \n')
    print(
        f'\t step1 -- finished !!! average single-insertion time: {total_time/total_ip_numbers} s \n')
    print(f'\t step2 -- get 100 most visited ip address \n')
    start = timeit.default_timer()
    print(f'\t top100 : {ip_tracker.top100}')
    print(
        f'\t step2 -- finished !!! top100 time: {timeit.default_timer() - start} s \n')
