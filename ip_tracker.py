import bisect
from collections import defaultdict
import random
import sys
import timeit


class IpTracker:
    """ A class to collect IP data and list the most visited IPs

        _ _ _ 

        method: 
        request_handled() - only use hash table to bucket the ip address by their counts. 
        top100() - loop through the bucked hash table and return a list of most used ips 

    """

    def __init__(self, n=100):
        """
            ip2cnt: lookup table, ip -> counts; 
            cnt2group: cnt -> group of ips with same counts; 
            cnt_set: set of existing cnt buckets 
            depth: default 100
        """
        self.ip2cnt = defaultdict(int)
        self.cnt2group = defaultdict(set)
        self.cnt_set = set()
        self.depth = n

    def request_handled(self, ip_address):
        """"O(1) insertion of ip address """
        ip_counts = self.ip2cnt[ip_address]
        cnt_ip_set = self.cnt2group[ip_counts]

        if ip_address in cnt_ip_set:
            self.cnt2group[ip_counts].remove(ip_address)
            if len(self.cnt2group[ip_counts]) == 0:
                self.cnt_set.remove(ip_counts)
        ip_counts += 1
        self.ip2cnt[ip_address] = ip_counts
        new_cnt_ip_set = self.cnt2group[ip_counts]
        new_cnt_ip_set.add(ip_address)

        if ip_counts not in self.cnt_set:
            #bisect.insort(self.cnt_sorted, ip_counts)
            self.cnt_set.add(ip_counts)

    def top100(self):
        """"return a list of ips ordered by counts """
        res = []
        grp_length = 0
        for cnt in sorted(self.cnt_set)[::-1]:
            cnt_grp = self.cnt2group[cnt]
            grp_length += len(cnt_grp)
            if grp_length < self.depth:
                res += cnt_grp
                continue
            else:
                res += cnt_grp
                return res[:self.depth]
        return res

    def clear(self):
        """"reset the memory"""
        self.ip2cnt = defaultdict(int)
        self.cnt2group = defaultdict(set)
        self.cnt_set = set()
        self.cnt_sorted = []


def ip_gen(): return ".".join(map(str, (random.randint(0, 255) for _ in range(4))))


if __name__ == "__main__":
    total_ip_numbers = sys.argv[1] if len(sys.argv) > 1 else 20*10**6
    ip_tracker = IpTracker()

    print(f'Test #1 -- ip from 255.255.255.0/24, count = ip[3] \n')
    print(f'\t step1 -- start generating 255.255.255.0/24 ip address \n')
    max_time = 0
    for i in range(255, -1, -1):
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
    for i in ip_tracker.top100():
        if i == "255.255.255." + str(target):
            target -= 1
            continue
        pass_fail = False
        break
    print(
        f'\t step2 -- finished !!!  { "Pass" if pass_fail else "Fail" } \n top100 time: {timeit.default_timer() - start} s \n')
    print(f'\t top100 : {ip_tracker.top100()} \n')
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
        total_time += duration
        max_time = max(max_time, duration)
    average_time = total_time / int(total_ip_numbers)
    print(
        f'\t step1 -- finished !!! worst single-insertion time: {max_time} s \n')
    print(
        f'\t step1 -- finished !!! average single-insertion time: {average_time} s \n')
    print(f'\t step2 -- get 100 most visited ip address \n')
    start = timeit.default_timer()
    print(f'\t top100 : {ip_tracker.top100()} \n')
    print(
        f'\t step2 -- finished !!! top100 time: {timeit.default_timer() - start} s \n')
