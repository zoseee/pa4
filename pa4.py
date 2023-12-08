class Process:
    def __init__(self, process_id):
        self.process_id = process_id
        self.memory_references = []


class Memory:
    def __init__(self):
        self.page_faults = 0
        self.disk_references = 0
        self.dirty_writes = 0


def FIFO(processes):
    page_faults = 0
    disk_accesses = 0
    dirty_page_writes = 0

    # System parameters
    addressable_physical_pages = 32
    page_size = 512  # Bytes
    virtual_address_bits = 16
    virtual_page_bits = 7
    offset_bits = virtual_address_bits - virtual_page_bits

    for process in processes:
        main_memory = set()
        page_queue = []
        page_table = {i: {'dirty': False, 'reference': False} for i in range(2 ** virtual_page_bits)}

        for access in process.memory_references:
            process_number, virtual_address, read_or_write = access

            # Extract virtual page number and offset
            virtual_page_number = (virtual_address >> offset_bits) & (2 ** virtual_page_bits - 1)
            offset = virtual_address & (2 ** offset_bits - 1)

            # check if page is in main memory
            if virtual_page_number not in main_memory:
                page_faults += 1

                # check if main memory is full
                if len(main_memory) == addressable_physical_pages:
                    oldest_page = page_queue.pop(0)
                    main_memory.remove(oldest_page)

                    # check if oldest page was dirty
                    if page_table[oldest_page]['dirty']:
                        disk_accesses += 2
                        dirty_page_writes += 1
                    else:
                        disk_accesses += 1

                # load the new page into main memory
                main_memory.add(virtual_page_number)
                page_queue.append(virtual_page_number)

                # update page table entry
                page_table[virtual_page_number]['reference'] = True

            # check if memory access is write
            if read_or_write == 'W':
                page_table[virtual_page_number]['dirty'] = True

    data = f"Total Page Faults: {page_faults}\nTotal Disk References: {disk_accesses}\nTotal Dirty Page Writes: {dirty_page_writes}"
    return data


if __name__ == "__main__":
    # Read input from the file and create processes
    try:
        with open('data1.txt', 'r') as file:
            input_data = file.read()
            lines = input_data.split('\n')

            processes = [Process(process_id=i + 1) for i in range(128)]  # Initialize an empty list for each process
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
                processes[process_number - 1].memory_references.append((process_number, virtual_address, operation))

        result = FIFO(processes)

        # Print the simulation results
        print(result)

    except FileNotFoundError:
        print("File not found. Please make sure the file exists.")
    except Exception as e:
        print(f"An error occurred: {e}")

