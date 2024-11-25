import json
import random
import os.path


START = "Your House"
FINISH = "Champion Battle!"
ITEM_BAG = []


def main():
    data = json.load(open('custom.json'))
    play_game(data)


def play_game(data):
    """
    This function runs the game, ending it when an appropiriate input is given or when the FINISH room is reached.
    Args:
    Param 1: (dictionary) the nested dictionaries in my world (custom.json file).
    Returns:
    None
    """
    current = random_start(data)
    print('Welcome to the Adventure Game:\n')
    user = input("Enter a username: ")
    save_user_info(user, current)
    current = load_user(user)
    print(describe(data, current))
    while True:  # Use a while loop to check for continuous user inputs. Loop ends when user types 'quit' or 'exit' or when FINISH(ed).
        items(data, current)
        move = input('\nYour move: ').lower()
        print()
        if move == 'quit' or move == 'exit' and current != FINISH:
            break
        if current != FINISH:
            current = move_user(data, current, move)
            print(describe(data, current))
            save_user_info(user, current)
        if current == FINISH:
            delete_user(user)  # The user's info is deleted from the dictionary when they finish the game.
            break


def move_user(data, current, move):
    """
    This function takes the user inputted move and changes the location accordingly. The location is then returned once updated.
    Args:
    Param 1: (dictionary) the nested dictionaries in my world (custom.json file).
    Param 2: (string) the key or "location" that corresponds to another dictionary.
    Param 3: (string) the user input corresponding to a move.
    Returns:
    Either a new location or the current location depending if a valid move was entered.
    """
    while move in ['north', 'east', 'south', 'west']:
        new_location = data[current]['moves'][move]
        return new_location  # Updates the current location.

    return current  # Return the unchanged current location for invalid moves.


def describe(data, current):
    """
    This function takes the current room of the user, and returns a concatenated string of all of the room's info.
    Args:
    Param 1: (dictionary) the nested dictionaries in my world (custom.json file).
    Param 2: (string) the key or "location" that corresponds to another dictionary.
    Returns:
    A concatenated string containing the text, objects, and move options of the current room.
    """
    output_text = ""
    room_text = data[current]['text']
    if current != FINISH:
        output_text += f"{room_text}\n"
        if 'objects' in data[current]:
            output_text += f"You see a {data[current]['objects'][0]['name']}."
        output_text += "\n"
        output_text += 'Your options are:\n'
        for i in data[current]['moves']:
            output_text += f"'{i}' to go to {data[current]['moves'][i]}\n"
    if current == FINISH:
        output_text += room_text
        output_text += "\n"
        output_text += 'Your options are:\n'
    return output_text


def random_start(data):
    """
    This function genereates a random start location (excluding the FINISH room).
    Args:
    Param 1: (dictionary) the nested dictionaries in my world (custom.json file).
    Returns:
    A random starting location is returned.
    """
    length = len(data) - 1  # Get the length of the dictionary - 1 since the last index is the FINISH room.
    random_index = random.randrange(length)  # Choose a random index and use that index to generate a random starting location.
    start_location = list(data.keys())[random_index]
    return start_location


def items(data, current):
    """
    This function checks if there is a special object in the current room, if so, an option is given to the user to pick it up.
    Args:
    Param 1: (dictionary) the nested dictionaries in my world (custom.json file).
    Param 2: (string) the key or "location" that corresponds to another dictionary.
    Returns:
    None
    """
    if len(data[current]) == 3:
        if data[current]['objects'][0]['type'] == 'special':  # Checks if the current room has a special item.
            pick_up = input("Pick up the special item? (yes or no): ").lower()
            if pick_up == 'yes':
                print("Item obtained!")
                ITEM_BAG.append(data[current]['objects'][0]['name'])
        print(f"Current Item(s):{ITEM_BAG}")


def save_user_info(username, current):
    """
    This function creates a json file (if it does not exist) that stores username and location for each unique player.
    Args:
    Param 1: (string) the username entered by the player.
    Param 2: (string) the key or "location" that corresponds to another dictionary.
    Returns:
    None
    """
    if os.path.isfile('location.json'):
        with open('location.json', 'r') as file:
            user_info = json.load(file)
        if username not in user_info.keys():  # If the inputted username is not in the file, then a new key:value pair is created.
            with open('location.json', 'w') as file:
                user_info[username] = current
                json.dump(user_info, file)
        else:  # If the inputted username already exists, then the existing information is just updated.
            with open('location.json', 'w') as file:
                user_info[username] = current
                json.dump(user_info, file)
    else:
        user_info = {}
        user_info[username] = current
        with open('location.json', 'w') as file:
            json.dump(user_info, file)


def load_user(username):
    """
    This function creates a json file (if it does not exist) that stores username and location for each unique player.
    Args:
    Param 1: (string) the username entered by the player.
    Returns:
    The location where the user was previously (if they exist in the dictionary).
    """
    with open('location.json', 'r') as file:
        user_info = json.load(file)
        if username in user_info.keys():  # If the username already exists in the dictionary, then that user's info is loaded.
            current_location = user_info[username]
            return current_location
        

def delete_user(username):
    """
    This function deletes the old user when they reach the FINISH room.
    Args:
    Param 1: (string) the username entered by the player.
    Returns:
    None
    """
    with open('location.json', 'r') as file:
        user_info = json.load(file)
        del user_info[username]
    with open('location.json', 'w') as file:
        json.dump(user_info, file)


if __name__ == '__main__':
    main()
