from collections import deque

class Gate:
    """
    Implements a ride gate with a regular and fastpass line, 
    serving riders according to a 1 fastpass : 3 regular ratio.
    Empty lines are skipped in the serving cycle.
    """
    
    # Define the serving pattern: F, R, R, R
    # The cycle index will iterate through this list
    SERVICE_PATTERN = ["fastpass", "regular", "regular", "regular"]

    def __init__(self):
        """
        Initializes the queues and the cycle counter.
        """
        self.queues = {
            "regular": deque(),
            "fastpass": deque()
        }
        # Cycle index tracks the position in the SERVICE_PATTERN list.
        # It's initialized to -1 so the first call to _get_next_line 
        # (or serve) starts at index 0 ("fastpass").
        self._cycle_index = -1 

    def arrive(self, line_type: str, rider_id: str):
        """
        Adds a rider to the specified queue.
        :param line_type: "regular" or "fastpass"
        :param rider_id: The unique identifier for the rider.
        """
        if line_type in self.queues:
            self.queues[line_type].append(rider_id)

    def _get_next_line(self) -> str:
        """
        Calculates the next line to serve based on the pattern, 
        handling skips for empty lines. It advances the cycle index.
        :return: The name of the line to serve ("regular" or "fastpass").
        :raises IndexError: If both lines are empty and no one can be served.
        """
        initial_index = (self._cycle_index + 1) % len(self.SERVICE_PATTERN)
        current_index = initial_index

        while True:
            # Determine the line type for the current pattern slot
            line_to_check = self.SERVICE_PATTERN[current_index]

            # Check if that line has riders
            if self.queues[line_to_check]:
                # Found a non-empty line that matches the pattern slot
                self._cycle_index = current_index
                return line_to_check
            
            # Line is empty, so we skip it and move to the next pattern slot
            current_index = (current_index + 1) % len(self.SERVICE_PATTERN)

            # If we've circled back to the starting point, 
            # it means both queues are entirely empty.
            if current_index == initial_index:
                raise IndexError("Both regular and fastpass lines are empty.")

    def serve(self) -> str:
        """
        Serves the next rider based on the pattern and line availability.
        :return: The ID of the rider being served.
        :raises IndexError: If both lines are empty.
        """
        # Determine which line to serve next, advancing the cycle index
        line_to_serve = self._get_next_line()
        
        # Dequeue the rider
        rider_id = self.queues[line_to_serve].popleft()
        return rider_id

    def peek_next_line(self) -> str | None:
        """
        Peeks at the line that would be served *next*, without 
        advancing the cycle or removing a rider.
        :return: "regular", "fastpass", or None if both are empty.
        """
        try:
            # Simulate the next cycle advancement to find the line
            initial_index = (self._cycle_index + 1) % len(self.SERVICE_PATTERN)
            current_index = initial_index
            
            # This logic is almost identical to _get_next_line but 
            # does NOT update self._cycle_index.
            while True:
                line_to_check = self.SERVICE_PATTERN[current_index]

                if self.queues[line_to_check]:
                    return line_to_check
                
                current_index = (current_index + 1) % len(self.SERVICE_PATTERN)

                if current_index == initial_index:
                    return None # Both lines are empty

        except Exception:
            # Catch exceptions like IndexError just in case, though 
            # the loop should handle the empty case by returning None
            return None