import os
import subprocess
from sirji.messages.output import OutputMessage
from sirji.tools.logger import executor as logger

class SingletonMeta(type):
    """
    This is a metaclass that will be used to create a Singleton class.
    It ensures that only one instance of the Singleton class exists.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        # If an instance of the class does not exist, create one; otherwise, return the existing one.
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Executor(metaclass=SingletonMeta):
    def __init__(self):
        pass

    def _code_folder(self):
        return os.path.join("workspace", "code")

    def create_file(self, input_message):
        # Create code directory if it does not exist
        if not os.path.exists(self._code_folder()):
            logger.info("Executor: Code directory not present. Creating directory")
            os.makedirs(self._code_folder())

        filename = input_message.get("FILENAME")
        content = input_message.get("CONTENT")

        # Construct the full path where the file should be created
        file_path = os.path.join(self._code_folder(), filename)

        logger.info(f"Executor: Creating file: {file_path}")

        try:
            with open(file_path, "w") as file:
                file.write(content)
                return "Done"
        except Exception as e:
            raise IOError(f"Failed to create or write to the file '{file_path}'. Error: {e}")

    # Execute a file
    def execute_file(self, input_message):
        command = input_message.get("COMMAND")
        logger.info(f"Executor: Execute file command: {command}")
        return self.execute_command(command)

    # Install a package
    def install_package(self, input_message):
        command = input_message.get("COMMAND")
        logger.info(f"Executor: Install package command: {command}")
        return self.execute_command(command)

    # Execute a command
    def execute_command(self, command):
        try:
            # Run the command and capture the output and error, if any.
            # shell=True can be a security hazard if command is constructed from external input.
            logger.info(f"Executor: Executing command: {command}")
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
            # If the command was successful, return the output.
            return result.stdout

        except subprocess.CalledProcessError as e:
            # If an error occurred while executing the command, return the error.
            raise subprocess.CalledProcessError(e.returncode, e.cmd, f"Error occurred while executing the command: {e.output}\n{e.stderr}") from e

    def message(self, input_message):
        action = input_message.get("ACTION")
        messageFrom = input_message.get("FROM")
        messageTo = input_message.get("TO")

        logger.info(f"Executor: Received message from {messageFrom} with action: {action}")
        if action == "create-file":
            details = self.create_file(input_message)
        elif action == "execute-file":
            details = self.execute_file(input_message)
        elif action == "install-package":
            details = self.install_package(input_message)
        else:
            raise ValueError(
                f"Unknown action: {action}")

        logger.info("Executor: Preparing output message")

        output_instance = OutputMessage(messageTo)
        output_message = output_instance.generate(messageFrom, { "details": details })

        return output_message;

