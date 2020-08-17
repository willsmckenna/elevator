from typing import List

class User:
    def __init__(self, user_num, name, wait_floor, dest_floor):
        self.user_num = user_num
        self.name = name
        self.wait_floor = wait_floor
        self.dest_floor = dest_floor

    def __repr__(self):
        if self.wait_floor == self.dest_floor:
            return f"----{self.name} is waiting at floor {self.wait_floor} (no new destination received)---"
        else:
            return f"""----{self.name} is waiting for the elevator at floor {self.wait_floor}, going to {self.dest_floor}---"""
    

    
