# works fine on my laptop
# while loop exits after the timeout 300 sec is over

import pyautogui
import time
import keyboard
import win32gui
from datetime import datetime

def set_status_available():
    # Open the system tray and click on the MS Teams icon
    pyautogui.press('win')
    time.sleep(1)
    pyautogui.typewrite('Teams')
    time.sleep(1)
    pyautogui.press('enter')

    # Navigate to your profile picture and click on it
    time.sleep(2)
    teams_window = win32gui.FindWindow(None, "Microsoft Teams")
    # if teams_window:
    #     win32gui.SetForegroundWindow(teams_window)
    #     pyautogui.moveTo(100, 100)  # Adjust this to match your Teams window position
    #     pyautogui.click()
    #     time.sleep(1)

    #     # Select "Available" from the status dropdown
    #     pyautogui.press('down')
    #     pyautogui.press('enter')
    #     time.sleep(1)

    #     # Click on the "Available" status to confirm
    #     pyautogui.click()

q_pressed = False  # Global variable

def check_q_press(event):
    global q_pressed  # Declare that we're modifying the global variable
    q_pressed = True
    print(event, 'q pressed. Exiting, wait for a while...')

def main():

    global q_pressed # Declare that we are modifying the global variable 

    keyboard.on_press_key('q', check_q_press) #This registers a callback function that sets the global variable.

    while not q_pressed:
        current_time = datetime.now().strftime("%H:%M")  # Get current time
        print(current_time, '- activating status.')
        set_status_available()
        time.sleep(300)

    print('Exiting...')

if __name__ == "__main__":
    main()