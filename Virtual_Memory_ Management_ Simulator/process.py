# process.py

import random

class Process:
    def __init__(self, max_page_number):
        self.max_page_number = max_page_number

    def generate_memory_request(self):
        # Random page access
        return random.randint(0, self.max_page_number)
