
import sys
import random

random.seed(20)

def RAND(processes):
    page_faults = 0
    disk_accesses = 0
    dirty_page_writes = 0
    memory = set()
    page_table = {}
    address_physical = 32

    for access in processes:
        process_number, virtual_address, read_or_write = access

        #get vpn
        vpn = virtual_address >> 9 

        #if not in main memory
        if vpn not in memory:
            page_faults += 1
            disk_accesses += 1

            #if memory is full
            if len(memory) == address_physical:
                #random page
                victim_page = random.choice(list(memory))
                memory.remove(victim_page)

                #if page dirty
                if page_table[victim_page]['dirty']:
                    disk_accesses += 2  # if dirty plus 2
                    dirty_page_writes += 1

            #store new page
            memory.add(vpn)

            #update page table
            page_table[vpn] = {'dirty': False}

            #check if access write
            if read_or_write == 'W':
                page_table[vpn]['dirty'] = True


    data = f"Total Page Faults: {page_faults}\nTotal Disk References: {disk_accesses}\nTotal Dirty Page Writes: {dirty_page_writes}"
    return data

def FIFO(processes):
    page_faults = 0
    disk_accesses = 0
    dirty_page_writes = 0
    memory = set()
    page_queue = []
    page_table = {}
    address_physical = 32

    for access in processes:
        process_number, virtual_address, read_or_write = access

        #get vpn
        vpn = virtual_address >> 9 

        #check if in memory
        if vpn not in memory:
            page_faults += 1
            disk_accesses += 1

            #check if full
            if len(memory) == address_physical:
                replaced_page = page_queue.pop(0) #most recent page
                memory.remove(replaced_page)
                #if replaced page dirty
                if page_table[replaced_page]['dirty']:
                    disk_accesses += 1  # if dirty another disk ref
                    dirty_page_writes += 1
                #memory.remove(replaced_page)
            else:
                replaced_page = None

            memory.add(vpn)
            page_queue.append(vpn)

            #update table
            page_table[vpn] = {'dirty': False}

            #check if write
            if read_or_write == 'W':
                page_table[vpn]['dirty'] = True


    data = f"Total Page Faults: {page_faults}\nTotal Disk References: {disk_accesses}\nTotal Dirty Page Writes: {dirty_page_writes}"
    return data

def LRU(processes):
    page_faults = 0
    disk_accesses = 0
    dirty_page_writes = 0
    memory = set()
    page_order = []
    page_table = {}
    address_physical = 32

    for access in processes:
        process_number, virtual_address, read_or_write = access

        vpn = virtual_address >> 9 

        if vpn not in memory:
            page_faults += 1
            disk_accesses += 1

            if len(memory) == address_physical:
                #least recent page and not dirty, also takes the min as a tiebreaker
                lru_page = min(page_order, key=lambda x: (page_table[x]['last_used'], not page_table[x]['dirty'], x))

                #is lru page dirty
                if page_table[lru_page]['dirty']:
                      # if dirty another disk ref
                    if read_or_write == 'W':
                        dirty_page_writes += 1
                        disk_accesses += 1

                memory.remove(lru_page)
                page_order.remove(lru_page)

            #store new page
            memory.add(vpn)
            page_order.append(vpn)

            #update table
            page_table[vpn] = {'dirty': False, 'last_used': len(page_order)}

            #check write
            if read_or_write == 'W':
                page_table[vpn]['dirty'] = True

        else:
            #if already in memory, update order
            page_order.remove(vpn)
            page_order.append(vpn)
            page_table[vpn]['last_used'] = len(page_order)

            #check write
            if read_or_write == 'W':
                page_table[vpn]['dirty'] = True

    data = f"Total Page Faults: {page_faults}\nTotal Disk References: {disk_accesses}\nTotal Dirty Page Writes: {dirty_page_writes}"
    return data

def PER(processes):
    page_faults = 0
    disk_accesses = 0
    memory = set()
    page_table = {}
    address_physical = 32
    reference_bit_reset = 0
    dirty_page_writes = 0
    for access in processes:
        process_number, virtual_address, read_or_write = access

        vpn = virtual_address >> 9 #get vpn

        if vpn not in memory:
            page_faults += 1
            disk_accesses += 1

            #if mem is full
            if len(memory) == address_physical:

                replacement_order = {
                    #page not in use
                    'unused': set(range(address_physical)) - set(memory),
                    #unreferenced page (reference bit is 0) where the dirty bit is 0
                    'unref_clean': [page for page in memory if not page_table[page]['referenced'] and not page_table[page]['dirty']],
                    #unreferenced page (reference bit is 0) where the dirty bit is 1.
                    'unref_dirty': [page for page in memory if not page_table[page]['referenced'] and page_table[page]['dirty']],
                    #referenced page (reference bit is 1) where the dirty bit is 0.
                    'ref_clean': [page for page in memory if page_table[page]['referenced'] and not page_table[page]['dirty']],
                    #page that is both referenced (reference bit is 1) and dirty (dirty bit is 1).
                    'ref_dirty': [page for page in memory if page_table[page]['referenced'] and page_table[page]['dirty']]
                }

                for x in ('unused', 'unref_clean', 'unref_dirty', 'ref_clean', 'ref_dirty'):
                    pages = replacement_order[x]
                    if pages:
                        #replace lowest numbred page
                        lowest_page = min(pages)

                        #if lowest page is in memory and page table remove
                    if lowest_page in memory and lowest_page in page_table:
                        memory.remove(lowest_page)

                        #check if dirty
                        if page_table[lowest_page]['dirty']:
                            disk_accesses += 1  # if dirty plus 2
                            dirty_page_writes += 1

                        break

            #new page
            memory.add(vpn)

            #update table
            page_table[vpn] = {'dirty': False, 'referenced': True}

            # Check if memory access is write
            if read_or_write == 'W':
                page_table[vpn]['dirty'] = True

        #reference bit logic 
        reference_bit_reset += 1
        if reference_bit_reset == 200: #reset to 0 every 200
            for page in memory:
                page_table[page]['referenced'] = False
            reference_bit_reset = 0

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
                #skip empty line
                if line.strip() == "":
                    continue

                #split into componentns
                fields = line.split('\t')

                #3 components atleast
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
        elif algorithm.upper() == 'PER':
            result = PER(processes)
        else:
            print(f"unknown algo")
            sys.exit(1)
        
        # Print the simulation results
        print(result)

    except FileNotFoundError:
        print("File not found. Please make sure the file exists.")
    except Exception as e:
        print(f"An error occurred: {e}")

