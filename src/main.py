import numpy as np
import time
import cv2
import os
import argparse
import logging
from config import Config
import lib.androiddebug as connect
import adb_shell


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

    old_count = 0
    time_deltas = []
    start_time = time.time()

    def take_screenshot(device_id, count, adb_path):
        if os.path.exists("screenshot{}.png".format(count)):
            count += 1
        else:
            os.system(
                "{} -s {} shell screencap -p /sdcard/screenshot{}.png".format(adb_path, device_id, count))
            os.system(
                "{} -s {} pull /sdcard/screenshot{}.png".format(adb_path, device_id, count))
        return count

    def display_screenshot(count, old_count=0):
        if os.path.exists("screenshot{}.png".format(count)):
            img = cv2.imread("screenshot{}.png".format(count))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            if count != old_count:
                cv2.imshow("Screenshot", img)
                cv2.waitKey(1)
            old_count = count
            try:
                os.remove("screenshot{}.png".format(count-1))
            except:
                pass
        return old_count

    device_id = "emulator-5554"
    adb_path = "\"C:\Program Files\BlueStacks_nxt\HD-Adb.exe\""
    count = 1

    while True:
        screenshot_start_time = time.time()
        count = take_screenshot(device_id, count, adb_path)
        old_count = display_screenshot(count, old_count)
        screenshot_end_time = time.time()
        time_deltas.append(screenshot_end_time - screenshot_start_time)

        if len(time_deltas) % 10 == 0:
            avg_time_delta = np.mean(time_deltas) * 1000
            print("Average delay between screenshots: {:.2f} ms".format(
                avg_time_delta))
            # convert to fps
            print("Average FPS: {:.2f}".format(1000 / avg_time_delta))
