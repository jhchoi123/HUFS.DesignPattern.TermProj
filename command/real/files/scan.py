from pathlib import Path

from api import ApiClient
from command import Command
from command.exception import InvalidApiKeyException, InvalidArgumentException
from command.result import CommandResult
from util.json import load_json_from_str
from db import ScanIdDB


class ScanCommand(Command):
    def __init__(self):
        super(ScanCommand, self).__init__()
        self._name = "scan"

    def _execute(self, *args) -> CommandResult:
        client = ApiClient()
        target_endpoint = client.get_endpoint("files", "scan")

        if not self._has_args(1, args):
            raise InvalidArgumentException

        file_path = args[0]

        file_path = Path(file_path).resolve()

        try:
            target_file = file_path.open("rb")
            if target_file is None:
                raise FileNotFoundError

            print("Uploading File...")
            result = client.exec_endpoint(target_endpoint, file=target_file)

            target_file.close()

            if result.status_code == 403:
                raise InvalidApiKeyException

            result = load_json_from_str(result.text)

            try:
                result = result["data"]
                scan_id = result["id"]
                ScanIdDB().add_scan_id(scan_id, str(file_path))
                return CommandResult(True, f"Successfully Upload File.\n"
                                     + f"File Path: {file_path}\n"
                                     + f"Scan ID: {scan_id}\n")
            except KeyError:
                return CommandResult(False, "Error: API Error.")

        except FileNotFoundError:
            return CommandResult(False, "Error: Invalid File Path.")
        except PermissionError:
            return CommandResult(False, "Error: File Permission Denied.")

    def help(self) -> str:
        return "Command: scan / Usage: scan {FILE_PATH}"


class InvalidFilePathException(InvalidArgumentException):
    def __init__(self):
        super(InvalidFilePathException, self).__init__()
