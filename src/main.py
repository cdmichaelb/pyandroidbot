import threading
import numpy as np
import time
import cv2
import os
import argparse
import logging
from config import Config
# import lib.androiddebug as connect
# import adb_shell


def setup_logging():
    """
    Configure the logging settings
    """
    logging.basicConfig(
        level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    return logging.getLogger(__name__)


def parse_args():
    """
    Parse command-line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', help='Debug mode')
    return parser.parse_args()


def check_debug_mode(args, logger):
    """
    Check if debug mode is on, and configure logging accordingly
    """
    if args.debug or Config.DEBUG:
        logger.setLevel(logging.DEBUG)
        logger.debug('Debug mode is on')
    else:
        logger.info('Debug mode is off')


def main():
    # Setup logging
    logger = setup_logging()
    # Parse command-line arguments
    args = parse_args()
    # Check if debug mode is on
    check_debug_mode(args, logger)
    # Print the parsed arguments
    print(args)


if __name__ == '__main__':
    main()

# Import necessary modules

# Initialize variables
old_count = 0  # Store the previous screenshot count
time_deltas = []  # Store the time difference between each screenshot
time_deltas2 = []  # Store the time difference between each screenshot
start_time = time.time()  # Store the start time
click_location = None  # Store the location to click
# Define function to take screenshot


def take_screenshot(device_id, count, adb_path):
    # Check if the screenshot file already exists
    if os.path.exists(f"screenshot{count}.png"):
        count += 1
    else:
        # Use adb to take screenshot on the device
        os.system(
            f"{adb_path} -s {device_id} shell screencap -p /sdcard/screenshot{count}.png")
        os.system(
            f"{adb_path} -s {device_id} pull /sdcard/screenshot{count}.png")
    return count

# Define function to display screenshot


def display_screenshot(count, old_count=0):
    # Check if screenshot file exists
    if os.path.exists(f"screenshot{count}.png"):
        # Read the screenshot file
        img = cv2.imread(f"screenshot{count}.png")
        # convert the image to black and white
        try:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
            img = cv2.threshold(
                img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        except:
            pass
        # Display the screenshot if it is a new screenshot
        if count != old_count:
            try:
                cv2.imshow("Screenshot", img)
                cv2.waitKey(1)
            except:
                pass
        old_count = count
    return old_count

# Define function to process screenshot


def process_screenshot(count):
    global old_count
    # Read the screenshot file
    img = cv2.imread(f"screenshot{count}.png")
    # convert the image to black and white
    try:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
        # img = cv2.threshold(
        #     img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    except:
        pass
    # old_count = count
    return img

# Locate image in screenshot


def locate_image(img, template):
    global click_location
    # Get the dimensions of the image
    height, width = template.shape
    # Find the location of the template in the image
    try:
        res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    except:
        return None
    # Get the location of the template
    loc = np.where(res >= 0.9)
    # Draw a rectangle around the template
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img, pt, (pt[0] + width, pt[1] + height), (0, 0, 255), 2)
    # Display the image
    cv2.imshow("Screenshot", img)
    if cv2.waitKey(1) == ord('q'):
        t2.join()
        t1.join()
        exit()
    # Click a random location in the rectangle
    try:
        # randomize the click location within the rectangle
        point_x = np.random.randint(pt[0], pt[0] + width)
        point_y = np.random.randint(pt[1], pt[1] + height)
        print(f"Clicking at {point_x}, {point_y}")
        click_location = (point_x, point_y)

    except:
        return click_location
    return click_location


# Define function to remove old screenshot
def remove_screenshot(count):
    try:
        # Remove the previous screenshot if it exists
        if count > 1 and os.path.exists(f"screenshot{count-1}.png"):
            os.remove(f"screenshot{count-1}.png")
    except Exception as e:
        # Print error if there is an issue removing the file
        print(e)
        pass


# Set the device id and adb path
device_id = "emulator-5554"
adb_path = "\"C:\Program Files\BlueStacks_nxt\HD-Adb.exe\""
count = 1
template = cv2.imread("template.png", 0)
collect = cv2.imread("collect.png", 0)
taskgift = cv2.imread("taskgift.png", 0)
helpimg = cv2.imread("help.png", 0)
ladyloot = cv2.imread("ladyloot.png", 0)
ladylootbox = cv2.imread("ladylootbox.png", 0)
back = cv2.imread("back.png", 0)


# Main loop to continuously take and display screenshots


def main_loop():
    global count
    global old_count
    global adb_path
    global click_location

    while True:
        # Take the screenshot

        count = take_screenshot(device_id, count, adb_path)
        # old_count = display_screenshot(count, old_count)  # Display the screenshot
        # Only process the screenshot if it is a new screenshot

        # Process the screenshot
        # Only process the screenshot if it is a new screenshot
        # print(count, old_count)
        # print(count != old_count)
        if count != old_count or img is None:
            img = process_screenshot(count)

        # img = process_screenshot(count)  # Process the screenshot
        # Locate the image in the screenshot
        # =============Replace with task manager====================
        # click_location = locate_image(img, helpimg)
        # if not click_location:
        #     click_location = locate_image(img, collect)
        # if not click_location:
        #     click_location = locate_image(img, taskgift)
        # if not click_location:
        #     click_location = locate_image(img, template)
        process_tasks(img)
        old_count = count  # Set the old_count to the current count

        remove_screenshot(count)  # Remove the previous screenshot


# Process list of tasks
tasks = [
    ["help", 5, 0],
    ["collect", 6, 0],
    ["taskgift", 7, 0],
    ["ladyloot", 8, 0],
    ["ladylootbox", 9, 0],
    ["template", 10, 0],
    ["back", 11, 0],
]


def process_tasks(img):
    global click_location

    if len(tasks) == 0:
        return
    if len(time_deltas2) > 0:
        if time.time() - time_deltas2[-1] < 1:
            return
    time_deltas.append(time.time())
    for task in tasks:
        if (task[2] == 0) or (time.time() - task[2] >= task[1]):
            # Run task
            print(
                f"Running task {task[0]} because {(time.time() - task[2])} >= {task[1]}")
            # =============Replace with task manager====================
            if task[0] == "help":
                click_location = locate_image(img, helpimg)
                task[2] = time.time()
                break
            if task[0] == "collect":
                click_location = locate_image(img, collect)
                task[2] = time.time()
                break
            if task[0] == "taskgift":
                click_location = locate_image(img, taskgift)
                task[2] = time.time()
                break
            if task[0] == "ladyloot":
                click_location = locate_image(img, ladyloot)
                task[2] = time.time()
                break
            if task[0] == "ladylootbox":
                click_location = locate_image(img, ladylootbox)
                task[2] = time.time()
                break
            if task[0] == "template":
                click_location = locate_image(img, template)
                task[2] = time.time()
                break
            if task[0] == "back":
                click_location = locate_image(img, back)
                task[2] = time.time()
                break
            time.sleep(1)


def click_loop():

    global click_location
    while True:
        # print("click loop", click_location)
        if click_location:
            # Prevent clicking too often
            # if len(time_deltas) > 0:
            #     if time.time() - time_deltas[-1] < 1:
            #         continue
            # time_deltas.append(time.time())

            os.system(
                f"{adb_path} -s {device_id} shell input tap {click_location[0]} {click_location[1]}")
            click_location = None
        time.sleep(1)


# thread click_loop and main_loop
t1 = threading.Thread(target=main_loop)
t2 = threading.Thread(target=click_loop)
t1.start()
t2.start()
