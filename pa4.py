import random

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
        self.pages = [None] * 32  # Main memory with 32 pages
        self.page_faults = 0
        self.disk_references = 0
        self.dirty_writes = 0

def simulate_page_replacement(memory, processes, algorithm):
    max_time_units = max(len(process.memory_references) for process in processes)

    for time_unit in range(max_time_units):
        for process in processes:
            if time_unit < len(process.memory_references):  # Check if the current process has enough references
                virtual_address, operation = process.memory_references[time_unit]
                virtual_address = int(virtual_address)  # Convert to integer here

                virtual_page_number = virtual_address // 512
                offset = virtual_address % 512
                page_table_entry = process.page_table.entries[virtual_page_number]

                if not page_table_entry.valid:
                    memory.page_faults += 1

                    if page_table_entry.dirty:
                        memory.disk_references += 2
                        memory.dirty_writes += 1
                        # Write the dirty page back to disk

                    # Load the new page into memory
                    page_table_entry.valid = True
                    page_table_entry.dirty = False
                    page_table_entry.referenced = True
                    # Load the new page from disk

                else:
                    page_table_entry.referenced = True

                # Simulate the read or write operation
                if operation == 'W':
                    page_table_entry.dirty = True

                # Simulate the page replacement algorithm
                if algorithm == 'RAND':
                    victim_page = random.randint(0, 31)
                    # Replace the victim page in memory
                    # Update the corresponding page table entry
                    # Perform any necessary disk operations

                # Implement other page replacement algorithms as needed



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
        simulate_page_replacement(memory, process_objects, algorithm='RAND')

        # Print the simulation results
        print(f"Total Page Faults: {memory.page_faults}")
        print(f"Total Disk References: {memory.disk_references}")
        print(f"Total Dirty Page Writes: {memory.dirty_writes}")


