# memory_manager.py

class MemoryManager:
    def __init__(self, total_frames):
        self.total_frames = total_frames
        self.frames = [None] * total_frames
        self.free_frames = list(range(total_frames))

    def allocate_frame(self, page_number):
        if self.free_frames:
            frame = self.free_frames.pop(0)
            self.frames[frame] = page_number
            return frame, False  # No replacement
        else:
            # FIFO Replacement
            replaced_frame = 0
            old_page = self.frames[replaced_frame]
            self.frames[replaced_frame] = page_number
            return replaced_frame, True

    def memory_snapshot(self):
        return self.frames
