# pa4


Virtual Memory Simulation Tool
This project is a virtual memory simulation tool that implements and analyzes various page replacement algorithms. The tool reads a series of memory references from an input file, simulating the behavior of processes interacting with virtual memory. The implemented page replacement algorithms include Random (RAND), First in First Out (FIFO), Least Recently Used (LRU), and Periodic Reference Reset (PER).

Input File Format
The input file contains a series of memory references, with each line having three values separated by a space:

Process number (integer)
Memory reference (address) - 16-bit virtual address space (0 to 65535)
Operation type: "R" for Read or "W" for Write
Page Table Organization
1-level page tables
Virtual address: (virtual page number, offset)
Each page is 512 bytes (2^9), and the virtual address space is 64KB (2^16)
Page table entries include a dirty bit and a reference bit
Memory Organization
32 addressable physical pages in main memory
Physical memory size: 32 pages * 512 bytes/page = 16KB
Implemented Page Replacement Algorithms
Random (RAND):

Victim page selected randomly.
First in First Out (FIFO):

Oldest page in memory gets replaced.
Least Recently Used (LRU):

Least recently used page in memory gets replaced.
If two pages have the same last used time unit, replace the one that is not dirty.
If both pages are dirty or neither is dirty, replace the lower-numbered page.
Periodic Reference Reset (PER):

Reference bit is set to 1 whenever a page is referenced.
After every 200 memory references, all reference bits are set to 0.
Page replacement order:
Unused page (early in simulation)
Unreferenced page with dirty bit = 0
Unreferenced page with dirty bit = 1
Referenced page with dirty bit = 0
Referenced page with dirty bit = 1
Lowest numbered page in each category for deterministic results.
Statistics Tracked
The simulation keeps track of three statistics:

Total number of page faults
Total number of disk references
Total number of dirty page writes
How to Run
Provide an input file (e.g., data1.txt, data2.txt).
Choose a page replacement algorithm (RAND, FIFO, LRU, PER).
Run the simulation tool.
Example:
python virtual_memory_simulator.py data1.txt RAND
