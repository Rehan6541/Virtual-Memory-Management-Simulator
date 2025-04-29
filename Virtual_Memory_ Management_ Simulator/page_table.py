# page_table.py

class PageTableEntry:
    def __init__(self, frame_number=None, valid=False):
        self.frame_number = frame_number
        self.valid = valid

class PageTable:
    def __init__(self):
        self.entries = {}

    def get_frame(self, page_number):
        entry = self.entries.get(page_number)
        if entry and entry.valid:
            return entry.frame_number
        else:
            return None

    def update_entry(self, page_number, frame_number):
        self.entries[page_number] = PageTableEntry(frame_number, True)

    def get_all_entries(self):
        return self.entries
