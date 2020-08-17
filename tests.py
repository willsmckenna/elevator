#----------------------test.py--------------------------------------
#
# Some simple unit tests to check the elevator functionality through
# going through one elevator ride with different user cases.
#
#-------------------------------------------------------------------

from models.elevator import Elevator
from models.user import User
from app import call_elevator, transport_user, transport_multiple_users, elevator


user_1 = User(1, "Wills", 1, 10)
user_2 = User(2, "Jim", 10, 15)
user_3 = User(3, "Fred", 10, 20)
user_4 = User(4, "Sally", 20, 10)
user_5 = User(5, "Janice", 20, 5)
user_6 = User(6, "Bob", 7, 15)
user_7 = User(7, "Mike", 22, 24)
user_8 = User(8, "John", 22, 25)
user_9 = User(9, "Abe", 25, 30)
user_10 = User(10, "Bart", 27, 31)


def test_start():
    assert(elevator.curr_floor == 1)
    assert(len(elevator.users) == 0)

def test_one_user_up():
    call_elevator(user_1)
    assert(len(elevator.users) == 1)
    transport_user(user_1, "up")
    print(elevator.send_curr_floor_msg())
    assert(elevator.curr_floor == 10)
    assert(len(elevator.users) == 0)
    

def test_two_users_up():
    transport_multiple_users([user_2, user_3], "up")
    assert(elevator.curr_floor == 20)
    assert(len(elevator.users) == 0)

def test_two_users_down():
    transport_multiple_users([user_4, user_5], "down")
    assert(elevator.curr_floor == 5)
    assert(len(elevator.users) == 0)

def test_move_to_user_then_up():
    call_elevator(user_6)
    transport_user(user_6, "up")
    assert(elevator.curr_floor == 15)
    assert(len(elevator.users) == 0)

def test_move_to_two_then_up():
    transport_multiple_users([user_7, user_8], "up")
    assert(elevator.curr_floor == 25)

def test_move_to_one_then_pick_up_one():
    transport_multiple_users([user_9, user_10], "up")
    assert(elevator.curr_floor == 31)
    


test_start()
test_one_user_up()
test_two_users_up()
test_two_users_down()
test_move_to_user_then_up()
test_move_to_two_then_up()
test_move_to_one_then_pick_up_one()
print("Tests passed")

