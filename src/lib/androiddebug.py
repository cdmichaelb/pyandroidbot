import adb_shell


class AndroidDebugBridge:
    def __init__(self, host, port):
        # Initialize ADB client with host and port
        self.adb_client = adb_shell.AdbClient(host, port)

    def devices(self):
        # Get list of all connected devices
        return self.adb_client.devices()

    def device(self, serial):
        # Get specific device by serial number
        return self.adb_client.device(serial)

    def shell(self, serial, command):
        # Execute shell command on device
        return self.device(serial).shell(command)

    def forward(self, serial, local, remote):
        # Forward a local socket to a remote socket
        self.device(serial).forward(local, remote)

    def reverse(self, serial, local, remote):
        # Reverse forward a remote socket to a local socket
        self.device(serial).reverse(local, remote)

    def install(self, serial, apk):
        # Install an apk on the device
        self.device(serial).install(apk)

    def uninstall(self, serial, package):
        # Uninstall a package from the device
        self.device(serial).uninstall(package)

    def push(self, serial, local, remote):
        # Push a file to the device
        self.device(serial).push(local, remote)

    def pull(self, serial, remote, local):
        # Pull a file from the device
        self.device(serial).pull(remote, local)

    def screencap(self, serial, filename):
        # Take a screenshot and save it to a file
        self.device(serial).screencap(filename)

    def screencap_to_stream(self, serial, stream):
        # Take a screenshot and write it to a stream
        self.device(serial).screencap_to_stream(stream)

    def screenrecord(self, serial, filename):
        # Start recording the screen and save it to a file
        self.device(serial).screenrecord(filename)

    def screenrecord_to_stream(self, serial, stream):
        # Start recording the screen and write it to a stream
        self.device(serial).screenrecord_to_stream(stream)

    def open(self, serial, path, mode='r'):
        # Open a file on the device
        self.device(serial).open(path, mode)

    def stat(self, serial, path):
        # Get file status
        self.device(serial).stat(path)

    def list(self, serial, path):
        # List the contents of a directory on the device
        self.device(serial).list(path)
