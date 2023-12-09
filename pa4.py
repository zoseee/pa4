import collections
import sys
import random

def RAND(processes):
    page_faults = 0
    disk_accesses = 0
    dirty_page_writes = 0

    memory = set() 
    page_table = {}
    addressable_physical_pages = 32

    for access in processes:
        process_number, virtual_address, read_or_write = access

        # Extract virtual page number
        vpn = virtual_address >> 9 

        # Check if page is in main memory
        if vpn not in memory:
            page_faults += 1
            disk_accesses += 1

            # Check if main memory is full
            if len(memory) == addressable_physical_pages:
                # Select a random victim page for replacement
                victim_page = random.choice(list(memory))

                # Check if the victim page was dirty
                if page_table[victim_page]['dirty']:
                    disk_accesses += 1  # if dirty plus 2
                    dirty_page_writes += 1
                
                memory.remove(victim_page)

            # Load the new page into main memory
            memory.add(vpn)

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
    memory = set()
    page_queue = []
    page_table = {}
    addressable_physical_pages = 32

    for access in processes:
        process_number, virtual_address, read_or_write = access

        # Extract virtual page number
        vpn = virtual_address >> 9 

        # Check if page is in main memory
        if vpn not in memory:
            page_faults += 1
            disk_accesses += 1

            # Check if main memory is full
            if len(memory) == addressable_physical_pages:
                replaced_page = page_queue.pop(0)

                #if replaced page diry
                if page_table[replaced_page]['dirty']:
                    disk_accesses += 1  # if dirty another disk ref
                    dirty_page_writes += 1


                # Load the new page into main memory
                memory.remove(replaced_page)
            else:
                replaced_page = None

            memory.add(vpn)
            page_queue.append(vpn)

            # Update page table entry
            page_table[vpn] = {'dirty': False}

            # Check if memory access is write
            if read_or_write == 'W':
                page_table[vpn]['dirty'] = True


    data = f"Total Page Faults: {page_faults}\nTotal Disk References: {disk_accesses}\nTotal Dirty Page Writes: {dirty_page_writes}"
    return data

def LRU(processes):
    page_faults = 0
    disk_accesses = 0
    dirty_page_writes = 0

    # System parameters
    memory = set()
    page_order = []
    page_table = {}
    addressable_physical_pages = 32

    for access in processes:
        process_number, virtual_address, read_or_write = access

        # Extract virtual page number
        vpn = virtual_address >> 9 

        # Check if page is in main memory
        if vpn not in memory:
            page_faults += 1
            disk_accesses += 1

            # Check if main memory is full
            if len(memory) == addressable_physical_pages:
                # Find the least recently used page
                lru_page = page_order.pop(0)

                # Check if the lru_page was dirty
                if page_table[lru_page]['dirty']:
                      # if dirty another disk ref
                    if read_or_write == 'W':
                        dirty_page_writes += 1
                        disk_accesses += 1

                memory.remove(lru_page)

            # Load the new page into main memory
            memory.add(vpn)
            page_order.append(vpn)

            # Update page table entry
            page_table[vpn] = {'dirty': False}

            # Check if memory access is write
            if read_or_write == 'W':
                page_table[vpn]['dirty'] = True

        else:
            # If page is already in main memory, update its usage order
            page_order.remove(vpn)
            page_order.append(vpn)

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

        if algorithm.upper() == 'FIFO':
            result = FIFO(processes)
        elif algorithm.upper() == 'RAND':
            result = RAND(processes)
        elif algorithm.upper() == 'LRU':
            result = LRU(processes)
        else:
            print(f"unknown algo")
            sys.exit(1)
        

        # Print the simulation results
        print(result)

    except FileNotFoundError:
        print("File not found. Please make sure the file exists.")
    except Exception as e:
        print(f"An error occurred: {e}")

