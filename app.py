from models.elevator import Elevator
from models.user import User
import time
from typing import List

#--------------Initialize elevator and users---------------

building_floors = 40
elevator = Elevator(1, [])

#---------------elevator functionality------------------------------
def move_elevator(num_floors: int, direction: str):
    while num_floors > 0:
        time.sleep(1)
        if direction == "down":
            print(f"Moving down a floor.....--{elevator.curr_floor}--")
            elevator.move_down()
        elif direction == "up":
            print(f"Moving up a floor.....--{elevator.curr_floor}--")
            elevator.move_up()
        num_floors -= 1

def move_to_user(user: User):
    floors_to_user = abs(elevator.curr_floor - user.wait_floor)
    print("Elevator moving to pick up new user")
    if user.wait_floor < elevator.curr_floor:
        move_elevator(floors_to_user, "down")
    elif elevator.curr_floor < user.wait_floor:
        move_elevator(floors_to_user, "up")

def call_elevator(user: User):
    #if the user actually needs to go somewhere
    if user.dest_floor != user.wait_floor:
    #if the user is not on the same floor, move to them
        if user.wait_floor != elevator.curr_floor:
            move_to_user(user)
        #once the elevator has moved to the floor of user (or already was there) pick them up
        print(f"Picking up {user.name}")
        elevator.users.append(user)
    #else it was a false request, don't move to them
    else:
        print("User already at destination floor, pick another floor")

def transport_user(user: User, direction):
    floors_to_dest = abs(user.dest_floor - elevator.curr_floor)
    move_elevator(floors_to_dest, direction)
    elevator.drop_off(user)
    elevator.send_arrival_msg(user, user.dest_floor)
    user.wait_floor = user.dest_floor

def transport_multiple_users(users: List[User], direction):
    for user in users:
        call_elevator(user)
    
    elevator.sort_users(elevator.users, direction, "dest")
    #drop off first user, then work its way up/down
    if elevator.curr_floor > elevator.users[0].dest_floor:
        transport_user(elevator.users[0], "down")
    else:
        transport_user(elevator.users[0], "up")
    
    while elevator.users != []:
        transport_user(elevator.users[0], direction)
        
#---------- Main and User Menus, helper/prompt functions ----------------------------
user_id_count = 1
app_users = []

def show_user_menu(user: User):
    USER_MENU_PROMPT = f"""
---------------------------------------------------------------
*   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *
-------{user.name} user menu----------
1) See current floor of elevator
2) See your current wait floor/destination floor
3) Change your current destination floor
4) Call and ride elevator
5) Back to main menu

Your selection: """
    return USER_MENU_PROMPT

def prompt_create_user():
    global user_id_count
    global app_users
    user_name = input("What is your user name: ")
    user_wait_floor = int(input("What floor are you waiting on (the building is 40 floors): "))
    if user_wait_floor < 1 or user_wait_floor > building_floors:
        print("Floors are 1 to 40, please try making user again")
        return
    user_dest_floor = int(input("What floor do you want to go to?"))
    if user_dest_floor < 1 or user_dest_floor > building_floors:
        print("Floors are 1 to 40, please try making user again")
        return
    user = User(user_id_count, user_name, user_wait_floor, user_dest_floor)
    app_users.append(user)
    user_id_count += 1
    print("User created")

def display_users():
    for user in app_users:
        print("---------------------------")
        print(f"User ID: {user.user_num}\nName: {user.name}\nWaiting on floor: {user.wait_floor}")
        print("---------------------------")

def call_and_ride_elevator(curr_user: User):
    call_elevator(curr_user)
    if curr_user.dest_floor > elevator.curr_floor:
        transport_user(curr_user, "up")
    else:
        transport_user(curr_user, "down")

def get_new_destination_floor(curr_user: User):
    new_dest_floor = int(input("What is your new destination floor: "))
    if new_dest_floor < 1 or new_dest_floor > building_floors:
        print("Floors are 1 to 40, please try entering destination floor again")
        prompt_ride_elevator()
    curr_user.dest_floor = new_dest_floor  

def prompt_ride_elevator():
    curr_user_name = input("Enter the user you would like to ride as by username: ")
    curr_user = look_up_user(curr_user_name)
    if curr_user is None:
        return 
    else:
        while (selection := input(show_user_menu(curr_user))) != "5":
            if selection == "1":
                print(elevator.send_curr_floor_msg())
            elif selection == "2":
                print(curr_user)
            elif selection == "3":
               get_new_destination_floor(curr_user)
            elif selection == "4":
                call_and_ride_elevator(curr_user)
            else:
                print("Invalid input, please try again")
            
        main_menu()

#--------------------------------------------------------------------------------------------------#
#--The current algorithm for the elevator interacting with multiple users is that it starts
#--with an up group, picks everyone up, then drops everyone off. The elevator finds the destination
#--of the first one in the queue by either going up or down, then finishes by dropping everyone else  
#--off on the way up. It then repeats this same order of steps with the down users.
#---------------------------------------------------------------------------------------------------#
def prompt_multiple_users():
    user_arr = []
    while user_name := input("Enter current usernames (or leave empty to stop adding):"):
        added_user = look_up_user(user_name)
        if added_user is not None:
            if added_user.wait_floor == added_user.dest_floor:
                print("User already at destination floor")
                print("Add another user or change user's destination floor")
            else:
                user_arr.append(added_user)

    up_users = [user for user in user_arr if user.wait_floor < user.dest_floor]
    down_users = [user for user in user_arr if user.wait_floor > user.dest_floor]
    
    sorted_up = elevator.sort_users(up_users, "up", "wait")
    if len(sorted_up) != 0:
        transport_multiple_users(sorted_up, "up")
    sorted_down = elevator.sort_users(down_users, "down", "wait")
    if len(sorted_down) != 0:
        transport_multiple_users(sorted_down, "down")    
    
def look_up_user(user_name: str):
    for user in app_users:
        if user_name == user.name:
            return user
    print("User not found")
    
MAIN_MENU_PROMPT = """
---------------------------------------------------------------
*   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *
Welcome to Wills' elevator. This command line application
lets you create any number of users, and have them wait and
ride an elevator. 

Select your option:
1) Create new user
2) See list of users and what floor they are on
3) Solo menu to ride the elevator as a single existing user
4) See current floor of elevator 
5) Run the elevator to pick up/drop off multiple current user
6) Exit

Your selection: """
def main_menu():
    while (selection := input(MAIN_MENU_PROMPT)) != "6":
        if selection == "1":
            prompt_create_user()
        elif selection == "2":
            display_users()
        elif selection == "3":
            prompt_ride_elevator()
        elif selection == "4":
            print(elevator.send_curr_floor_msg())
        elif selection == "5":
            prompt_multiple_users()
        else:
            print("Invalid input, please try again")

#--------- app start-up --------------------
if __name__ == "__main__":
    main_menu()