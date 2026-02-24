import time
import threading
import random
from pynput.mouse import Button, Controller
from pynput.keyboard import KeyCode
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener

# Used in clicker functions
clicking = False
mouse = Controller()
active_cps = 10
active_left_clicks = 0
active_right_clicks = 0

# Global Settings
toggle_key = KeyCode(char="0")
mouse_held = 1
buttons_enabled = 1
cps_mode = 1
cps_int1 = 10
cps_int2 = 10
run_rng = 0.00

# Main
def main():
    chooseOption()

# Get Option (First Menu)
def chooseOption():
    option = -1
    while (not(option == 1 or option == 2)):
        try:
            print("Selection an option:\n1. Set up new settings\n2. Use saved settings")
            option = int(input())

            if (option == 1):
                print()
                chooseSettings()
            elif (option == 2):
                load()
            else:
                print("Error: Invalid input, enter a selection between 1 and 2\n")
        except (Exception):
            print("Error: Invalid input, enter a selection between 1 and 2\n")

# Edit Settings
def chooseSettings():
    # Keybind
    toggle_input = ""
    global toggle_key
    try:
        while (not(len(toggle_input) == 1)):
            toggle_input = input("Enter a character to be used to toggle the clicker: ")
            if (len(toggle_input) == 1 and not(toggle_input == '\'' or toggle_input == '\"' or toggle_input == '\\')):
                toggle_key = KeyCode(char=toggle_input)
            else:
                print("Error: Only one character should be inputted\n")
    except (Exception):
        print("Error: Invalid character(s) inputted\n")

    print()

    # Mouse Held
    hold_option = -1
    global mouse_held
    while (not(hold_option >= 1 and hold_option <= 2)):
        try:
            print("Should the mouse button(s) be held down to activate the clicker:\n1. Yes\n2. No")
            hold_option = int(input())

            if (hold_option >= 1 and hold_option <= 2):
                mouse_held = hold_option
            else:
                print("Error: Invalid input, enter a selection between 1 and 2\n")
        except (Exception):
            print("Error: Invalid input, enter a selection between 1 and 2\n")

    print()
    
    # Mouse Buttons
    buttons_option = -1
    global buttons_enabled
    while (not(buttons_option >= 1 and buttons_option <= 3)):
        try:
            print("Select which mouse button(s) to use:\n1. Left\n2. Right\n3. Left and Right")
            buttons_option = int(input())

            if (buttons_option >= 1 and buttons_option <= 3):
                buttons_enabled = buttons_option
            else:
                print("Error: Invalid input, enter a selection between 1 and 3\n")
        except (Exception):
            print("Error: Invalid input, enter a selection between 1 and 3\n")

    print()
    
    # CPS Mode
    cps_option = -1
    global cps_mode
    while (not(cps_option >= 1 and cps_option <= 2)):
        try:
            print("Select which CPS mode to use:\n1. Static\n2. Range")
            cps_option = int(input())

            if (cps_option >= 1 and cps_option <= 2):
                cps_mode = cps_option
            else:
                print("Error: Invalid input, enter a selection between 1 and 2\n")
        except (Exception):
            print("Error: Invalid input, enter a selection between 1 and 2\n")

    print()

    # CPS Minimum (or static value)
    cps_1 = -1
    global cps_int1
    while (cps_1 < 0):
        try:
            if (cps_mode == 1):
                cps_1 = int(input("Enter your CPS: "))
            elif (cps_mode == 2):
                cps_1 = int(input("Enter the minimum (lowest) CPS: "))

            if (cps_1 > 0):
                cps_int1 = cps_1
            else:
                print("Error: Invalid input, enter a number above 0\n")
        except (Exception):
            print("Error: Invalid input, enter a number above 0\n")
    
    # CPS Maximum (only runs if range setting is chosen)
    if (cps_mode == 2):
        cps_2 = -1
        global cps_int2
        while (cps_2 < 0):
            try:
                cps_2 = int(input("Enter the maximum (highest) CPS: "))

                if (cps_2 > 0):
                    cps_int2 = cps_2
                else:
                    print("Error: Invalid input, enter a number above 0\n")
            except (Exception):
                print("Error: Invalid input, enter a number above 0\n")
    
    save()

# Save Settings
def save():

    print("\nSaving settings...")
    toggle_key_txt = f"{toggle_key}"
    toggle_key_txt = toggle_key_txt.replace("\'", "")

    try:
        with open("settings.txt", 'w') as file:
            file.write(f"{toggle_key_txt}\n")
            file.write(f"{mouse_held}\n")
            file.write(f"{buttons_enabled}\n")
            file.write(f"{cps_mode}\n")
            file.write(f"{cps_int1}\n")
            file.write(f"{cps_int2}\n")
        
        print("Settings saved to settings.txt!")
        start()
    except (Exception):
        print("An error occurred while saving your settings. Please restart the program.")

# Apply Settings
def load():
    global toggle_key
    global mouse_held
    global buttons_enabled
    global cps_mode
    global cps_int1
    global cps_int2

    print("Loading saved settings...")
    try:
        with open("settings.txt", 'r') as file:
            content = file.readlines()
            content = [item.strip() for item in content]

            # Re-assigns Settings
            toggle_key = KeyCode(char=content[0])
            mouse_held = int(content[1])
            buttons_enabled = int(content[2])
            cps_mode = int(content[3])
            cps_int1 = int(content[4])
            cps_int2 = int(content[5])
            print("Settings loaded!")
            display_settings()
            start()
    except (FileNotFoundError):
        print("Error: File not found. Redirecting to create new settings...")
        chooseSettings()
    except (Exception):
        print("An error occurred while loading your settings. Redirecting to create new settings...")
        chooseSettings()
    
# Display Settings
def display_settings():
    print("\nCurrent Settings:")
    print(f"Toggle Key: {toggle_key}")
    if (mouse_held == 1):
        print("Mouse Held: Yes")
    elif (mouse_held == 2):
        print("Mouse Held: No")
    if (buttons_enabled == 1):
        print("Buttons Enabled: Left")
    elif (buttons_enabled == 2):
        print("Buttons Enabled: Right")
    elif (buttons_enabled == 3):
        print("Buttons Enabled: Left and Right")
    if (cps_mode == 1):
        print("CPS Mode: Static")
        print(f"CPS: {cps_int1}")
    elif (cps_mode == 2):
        print("CPS Mode: Range")
        print(f"Minimum CPS: {cps_int1}")
        print(f"Maximum CPS: {cps_int2}")
    print()

# Starts Clicker
def start():
    global active_cps
    print("Starting...")
    active_cps = cps_int1

    click_thread = threading.Thread(target=clicker)
    click_thread.start()

    if (mouse_held == 1):
        print("Clicker started! Toggle the clicker on and hold down your mouse button to begin.")
    elif (mouse_held == 2):
        print("Clicker started! Toggle the clicker on to begin.")
    print("To disable the clicker, close this window.")

    with KeyboardListener(on_press=toggle_event) as key_listener, \
        MouseListener(on_click=hold_mouse) as mouse_listener:
            key_listener.join()
            mouse_listener.join()
    
# RNG
def cps_rng():
    global active_cps
    active_cps = random.randint(cps_int1, cps_int2)

# Clicker
def clicker():
    global run_rng
    if (cps_mode == 1 and mouse_held == 1): # Static, Mouse Held
        while True:
            if (not(buttons_enabled == 2) and (clicking and active_left_clicks > 0)):
                mouse.click(Button.left, 1)
            if (not(buttons_enabled == 1) and (clicking and active_right_clicks > 0)):
                mouse.click(Button.right, 1)
            time.sleep(round(1 / active_cps, 5))
    elif (cps_mode == 1 and mouse_held == 2): # Static, No Mouse Held
        while True:
            if (not(buttons_enabled == 2) and (clicking)):
                mouse.click(Button.left, 1)
            if (not(buttons_enabled == 1) and (clicking)):
                mouse.click(Button.right, 1)
            time.sleep(round(1 / active_cps, 5))
    elif (cps_mode == 2 and mouse_held == 1): # Range, Mouse Held
        while True:
            if (not(buttons_enabled == 2) and (clicking and active_left_clicks > 0)):
                mouse.click(Button.left, 1)
            if (not(buttons_enabled == 1) and (clicking and active_right_clicks > 0)):
                mouse.click(Button.right, 1)
            time.sleep(round(1 / active_cps, 5))
            run_rng = run_rng + round(1 / active_cps, 5)
            if (run_rng > 1.0):
                run_rng = 0.0
                cps_rng()  
    elif (cps_mode == 2 and mouse_held == 2): # Range, No Mouse Held
        while True:
            if (not(buttons_enabled == 2) and (clicking)):
                mouse.click(Button.left, 1)
            if (not(buttons_enabled == 1) and (clicking)):
                mouse.click(Button.right, 1)
            time.sleep(round(1 / active_cps, 5))
            run_rng = run_rng + round(1 / active_cps, 5)
            if (run_rng > 1.0):
                run_rng = 0.0
                cps_rng()     

# Enable/Disable
def toggle_event(key):
    if key == toggle_key:
        global clicking
        clicking = not clicking
        if (clicking):
            print("Clicker enabled.")
        else:
            print("Clicker disabled.")

# Test for mouse buttons held
def hold_mouse(x, y, button, pressed):
    global active_left_clicks
    global active_right_clicks
    if (button == Button.left):
        if pressed:
            #print("Left mouse button down")
            active_left_clicks = active_left_clicks + 1
        else:
            #print("Left mouse button up")
            active_left_clicks = active_left_clicks - 1
    if (button == Button.right):
        if pressed:
            #print("Right mouse button down")
            active_right_clicks = active_right_clicks + 1
        else:
            #print("Right mouse button up")
            active_right_clicks = active_right_clicks - 1


main()
