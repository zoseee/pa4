import random
from collections import deque  # Import deque for FIFO


random.seed(42)

class PageTableEntry:
    def __init__(self):
        self.valid = False
        self.dirty = False
        self.referenced = False

class PageTable:
    def __init__(self):
        self.entries = [PageTableEntry() for _ in range(128)]

class Process:
    def __init__(self, process_id):
        self.process_id = process_id
        self.page_table = PageTable()
        self.memory_references = []

class Memory:
    def __init__(self):
        self.pages = [PageTableEntry() for _ in range(32)] 
        self.page_faults = 0
        self.disk_references = 0
        self.dirty_writes = 0
        self.page_order = deque()  # Initialize the deque for FIFO

def fifo_algo(processed_data):
    data = "" 
    page_faults = 0
    disk_accesses = 0
    dirty_page_writes = 0

    # data structures
    main_memory = set()
    page_queue = []
    page_table = {}

    for access in processed_data:
        process_number, memory_reference, read_or_write = access

        # calculate virtual page # and offset
        virtual_page_number = memory_reference >> 0
        offset = memory_reference & 0x1FF

        # check if page is in main memory
        if virtual_page_number not in main_memory:
            page_faults += 1

            # check if main memory is full
            if len(main_memory) == addressable_physical_pages:
                oldest_page = page_queue.pop(0)
                main_memory.remove(oldest_page)

                #check if oldest page was dirty
                if page_table[oldest_page]['dirty']:
                    disk_accesses += 2
                    dirty_page_writes += 1
                else:
                    disk_accesses += 1

            # load the new page in the main memory
            main_memory.add(virtual_page_number)
            page_queue.append(virtual_page_number)

            #update page table enttry
            page_table[virtual_page_number] = {'dirty': False, 'reference': True}

        #check if memory access is write
        if read_or_write == 'W':
            page_table[virtual_page_number]['dirty'] = True

    data = f"Total Page Faults: {page_faults}\nTotal Disk References: {disk_accesses}\nTotal Dirty Page Writes: {dirty_page_writes}"
    return data

def simulate_page_replacement(memory, processes, algorithm):
    max_time_units = max(len(process.memory_references) for process in processes)

    for time_unit in range(max_time_units):
        for process in processes:
            if time_unit < len(process.memory_references):  # Check if the current process has enough references
                virtual_address, operation = process.memory_references[time_unit]
                virtual_address = int(virtual_address)  # Convert to integer here

                
                virtual_page_number = (virtual_address >> 9) % 32


                offset = virtual_address % 512
                page_table_entry = process.page_table.entries[virtual_page_number]

                if not page_table_entry.valid:
                    memory.page_faults += 1

                    if page_table_entry.dirty:
                        memory.disk_references += 1
                        memory.dirty_writes += 1
                        # Write the dirty page back to disk

                    # Load the new page into memory
                    memory.pages[virtual_page_number] = PageTableEntry()
                    page_table_entry = memory.pages[virtual_page_number]
                    page_table_entry.valid = True
                    page_table_entry.dirty = False
                    page_table_entry.referenced = True
                    # Load the new page from disk

                else:
                    page_table_entry.referenced = True

                # Simulate the read or write operation
                if operation == 'W':
                    page_table_entry.dirty = True

                
                if algorithm == 'RAND':
                    victim_page = random.randint(0, 31)
                    victim_page_entry = memory.pages[victim_page]
                    
                    if victim_page_entry.dirty:
                        memory.disk_references += 1
                        memory.dirty_writes += 1
                        # Write the dirty page back to disk

                    # Update the corresponding page table entry
                    process.page_table.entries[virtual_page_number] = victim_page_entry
                    victim_page_entry.valid = True
                    victim_page_entry.dirty = False
                    victim_page_entry.referenced = True
                    # Load the new page from disk

                elif algorithm == 'FIFO':
                    if memory.page_order:    

                        oldest_page = memory.page_order.popleft()
                        oldest_page_entry = memory.pages[oldest_page]

                        if oldest_page_entry.dirty:
                            memory.disk_references += 1
                            memory.dirty_writes += 1
                            # Write the dirty page back to disk

                        # Update the corresponding page table entry
                        process.page_table.entries[virtual_page_number] = oldest_page_entry
                        oldest_page_entry.valid = True
                        oldest_page_entry.dirty = False
                        oldest_page_entry.referenced = True
                        # Load the new page from disk

                    # Update the page order for both algorithms
                memory.page_order.append(virtual_page_number)





if __name__ == "__main__":
    # Read input from the file and create processes
    try:
        with open('data1.txt', 'r') as file:
            lines = file.readlines()
            processes = [[] for _ in range(128)]  # Initialize an empty list for each process

            for line in lines:
                process_id, virtual_address, operation = map(str.strip, line.split())
                process_id = int(process_id)
                virtual_address = int(virtual_address)
                processes[process_id - 1].append((virtual_address, operation))

    except FileNotFoundError:
        print("File not found. Please make sure the file exists.")
        processes = []

    # ...

    # Continue with the simulation if processes are successfully loaded
    if processes:
        # Convert the list of processes into a list of Process instances
        process_objects = [Process(process_id=i + 1) for i in range(len(processes))]
        for process_obj, process_data in zip(process_objects, processes):
            process_obj.memory_references = process_data


        # Initialize memory and processes
        memory = Memory()

        # Simulate page replacement with a specific algorithm
        simulate_page_replacement(memory, process_objects, algorithm='FIFO')

        # Print the simulation results
        print(f"Total Page Faults: {memory.page_faults}")
        print(f"Total Disk References: {memory.disk_references}")
        print(f"Total Dirty Page Writes: {memory.dirty_writes}")


