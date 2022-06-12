 
ip_tracker contains a class design and unit test. 

`ip_tracker_heap_bst.py`: the original file. With 20M records, its average `request_handled()` time was in ~1mS and `top100()` was < 10mS. 
However, i saw the worst-case `request_handled()` time goes to 1S. So I tried a few other data structures. 
Eventually, I think this delay may be related with the garabage collections. The average time is still fine. 

`ip_tracker.py`: the file which was simplified. It uses simple data structure. The IP record was using plain tuples instead of dataclass. The `request_handled()` only maintains the hash table and will not do any `top100()` related processing. 


# How to run the program 
`python3 ip_tracker.py `


# Test Cases 
Test #1: 
ip from 255.255.255.0/24, each ip is repeated by the last 8bits. 
for example, 
    255.255.255.255 will be repeated 255 times 
    ...
    255.255.255.0 will be repeated 0 times 
We will check if the repeated time and IP matches the above pattern. If it matches, the test will pass. 

Test #2: 
random 20M IPs. We will check the average `request_handled()`  and `top100()` response time. 


# FAQ

**What would you do differently if you had more time?**
I would do more profile and figure out why the worst-case `request_handled()` time with 20M records is so high ~1s. 
Profiling also shows a lot of time wasted in generating the random IP addresses. Maybe that can be optimized. 
I can also parallelize the caculation using Redis queue. 
Maybe consult others if there is another algorithm. 


**What is the runtime complexity of each function?**
`request_handled()`: O(1). It mostly uses hash table which is O(1). I also tried to use heap and BST tree initially in this call to maintain the ordered top100 list direclty. It uses a binary search or linear search on a fixed length array. So the time complexity is O(100ln(100)) which is approaximated as O(1). 

top100(): it is also approximated as O(1) because it is on a fixed length array. 


**How does your code work?**
The `top100()` runs very fast on even 20M records at 10mS.  
The problem is that `request_handled()` worst-case on 20M records can be 1s. The average time is still pretty low ~1.3mS. 

**What other approaches did you decide not to pursue?**
I tried to use heap and bst tree in `request_handled()` cinitially.
I did some profiling on it. The dataclass I used earlier was having some delays but that is not the problem.  

**How would you test this?**
Test #1: 
ip from 255.255.255.0/24, each ip is repeated by the last 8bits. 
for example, 
    255.255.255.255 will be repeated 255 times 
    ...
    255.255.255.0 will be repeated 0 times 
We will check if the repeated time and IP matches the above pattern. If it matches, the test will pass. 

Test #2: 
random 20M IPs. We will check the average `request_handled()`  and `top100()` response time. 