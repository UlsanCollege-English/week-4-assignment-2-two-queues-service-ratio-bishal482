from collections import deque

class Gate:
    def __init__(self):
        self.fastpass = deque()
        self.regular = deque()
        # Pattern: F,R,R,R (indexes 0..3)
        self.pattern = ["fastpass", "regular", "regular", "regular"]
        self.ptr = 0  # current index in pattern

    def arrive(self, line, person):
        if line == "fastpass":
            self.fastpass.append(person)
        elif line == "regular":
            self.regular.append(person)
        else:
            raise ValueError("Unknown line type")

    def serve(self):
        # try up to 4 slots to find available
        for _ in range(len(self.pattern)):
            current = self.pattern[self.ptr]
            if current == "fastpass" and self.fastpass:
                rider = self.fastpass.popleft()
                self.ptr = (self.ptr + 1) % len(self.pattern)
                return rider
            elif current == "regular" and self.regular:
                rider = self.regular.popleft()
                self.ptr = (self.ptr + 1) % len(self.pattern)
                return rider
            else:
                # advance pointer and keep checking
                self.ptr = (self.ptr + 1) % len(self.pattern)

        # no one to serve
        raise IndexError("No riders to serve")

    def peek_next_line(self):
        # look ahead through pattern until we find a non-empty line
        for offset in range(len(self.pattern)):
            idx = (self.ptr + offset) % len(self.pattern)
            line = self.pattern[idx]
            if line == "fastpass" and self.fastpass:
                return "fastpass"
            if line == "regular" and self.regular:
                return "regular"
        return None
