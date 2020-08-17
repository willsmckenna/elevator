from typing import List
from .user import User

class Elevator:
    def __init__(self, curr_floor, users: List[User]):
        self.curr_floor = curr_floor
        self.users = users

    def __repr__(self):
        return f"""Elevator is at floor {self.curr_floor} and has {len(self.users)} passengers"""
    
    def move_up(self):
        self.curr_floor += 1

    def move_down(self):
        self.curr_floor -= 1
    
    def send_arrival_msg(self, user: User, dest_floor):
        print(f"Arrived at floor {dest_floor} for {user.name}")
    
    def drop_off(self, user: User):
        self.users.remove(user)
    
    def send_curr_floor_msg(self):
        return f"Elevator is on floor {self.curr_floor}"
    
    # An internal function to sort users in a queue, by their destination floor or wait floor
    def sort_users(self, users: List[User], direction:str, wait_or_dest: str):
        if direction == "up":
            if wait_or_dest == "dest":
                users.sort(key=lambda x: x.dest_floor, reverse=False)
            else:
                users.sort(key=lambda x: x.wait_floor, reverse=False )
            return [user for user in users]
        elif direction == "down":
            if wait_or_dest == "dest":
                users.sort(key=lambda x: x.dest_floor, reverse=True)
            else:
                users.sort(key=lambda x: x.wait_floor, reverse=True)
            return [user for user in users]
    



    



    