from adb_shell import AdbDeviceTcp, AdbDeviceUsb
from adb_shell.auth.sign_pythonrsa import PythonRSASigner


def connect(host, port):
    # Connect to ADB server
    adb_client = AdbDeviceTcp(host, port)
    return adb_client


def devices(adb_client):
    # Get list of all connected devices
    return adb_client.devices()
