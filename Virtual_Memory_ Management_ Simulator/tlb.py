# tlb.py

class TLB:
    def __init__(self, size):
        self.size = size
        self.entries = {}
        self.order = []

    def get(self, page_number):
        if page_number in self.entries:
            # Move to end (recently used)
            self.order.remove(page_number)
            self.order.append(page_number)
            return self.entries[page_number]
        return None

    def put(self, page_number, frame_number):
        if len(self.entries) >= self.size:
            # Remove least recently used
            lru_page = self.order.pop(0)
            del self.entries[lru_page]
        self.entries[page_number] = frame_number
        self.order.append(page_number)

    def snapshot(self):
        return self.entries
