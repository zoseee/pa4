import collections
import sys
import random

class Process:
    def __init__(self, process_id):
        self.process_id = process_id
        self.memory_references = []


class Memory:
    def __init__(self):
        self.page_faults = 0
        self.disk_references = 0
        self.dirty_writes = 0

import random

def RAND(processes):
    page_faults = 0
    disk_accesses = 0
    dirty_page_writes = 0

    # System parameters
    main_memory = set()
    page_table = {}
    addressable_physical_pages = 32

    for access in processes:
        process_number, virtual_address, read_or_write = access

        # Extract virtual page number
        vpn = virtual_address >> 9 

        # Check if page is in main memory
        if vpn not in main_memory:
            page_faults += 1
            disk_accesses += 1

            # Check if main memory is full
            if len(main_memory) == addressable_physical_pages:
                # Select a random victim page for replacement
                victim_page = random.choice(list(main_memory))
                main_memory.remove(victim_page)

                # Check if the victim page was dirty
                if page_table[victim_page]['dirty']:
                    disk_accesses += 1  # if dirty plus 2
                    dirty_page_writes += 1

            # Load the new page into main memory
            main_memory.add(vpn)

            # Update page table entry
            page_table[vpn] = {'dirty': False}

            # Check if memory access is write
            if read_or_write == 'W':
                page_table[vpn]['dirty'] = True


    data = f"Total Page Faults: {page_faults}\nTotal Disk References: {disk_accesses}\nTotal Dirty Page Writes: {dirty_page_writes}"
    return data


def FIFO(processes):
    page_faults = 0
    disk_accesses = 0
    dirty_page_writes = 0

    # System parameters
    main_memory = set()
    page_queue = []
    page_table = {}
    addressable_physical_pages = 32

    for access in processes:
        process_number, virtual_address, read_or_write = access

        # Extract virtual page number
        vpn = virtual_address >> 9 

        # Check if page is in main memory
        if vpn not in main_memory:
            page_faults += 1
            disk_accesses += 1

            # Check if main memory is full
            if len(main_memory) == addressable_physical_pages:
                oldest_page = page_queue.pop(0)
                main_memory.remove(oldest_page)

                # Check if the oldest page was dirty
                if page_table[oldest_page]['dirty']:
                    disk_accesses += 1  # if dirty another disk ref
                    dirty_page_writes += 1


            # Load the new page into main memory
            main_memory.add(vpn)
            page_queue.append(vpn)

            # Update page table entry
            page_table[vpn] = {'dirty': False}

            # Check if memory access is write
            if read_or_write == 'W':
                page_table[vpn]['dirty'] = True


    data = f"Total Page Faults: {page_faults}\nTotal Disk References: {disk_accesses}\nTotal Dirty Page Writes: {dirty_page_writes}"
    return data


if __name__ == "__main__":
    
    if len(sys.argv) !=3:
        print("Incorrect Format, Execute as follows: python 'scriptname.py' data.txt <algorithm desired>")
        sys.exit(1)

    inputFile = sys.argv[1]
    algorithm = sys.argv[2]

    try:
        with open(inputFile, 'r') as file:
            input_data = file.read()
            lines = input_data.split('\n')

            processes = []
            for line in lines:
                # Skip empty lines
                if line.strip() == "":
                    continue

                # Split the line into components
                fields = line.split('\t')

                # Ensure the line has exactly three components
                if len(fields) != 3:
                    print(f"Invalid line format: {line}")
                    continue

                # Parse the components
                process_number = int(fields[0])
                virtual_address = int(fields[1])
                operation = fields[2]
                processes.append((process_number, virtual_address, operation))

        if algorithm == 'FIFO':
            result = FIFO(processes)
        elif algorithm == 'RAND':
            result = RAND(processes)
        else:
            print(f"unknown algo")
            sys.exit(1)
        

        # Print the simulation results
        print(result)

    except FileNotFoundError:
        print("File not found. Please make sure the file exists.")
    except Exception as e:
        print(f"An error occurred: {e}")

