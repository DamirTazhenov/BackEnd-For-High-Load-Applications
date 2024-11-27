import os

from django.core.exceptions import ValidationError

import pyclamd
def scan_file_for_malware(file_path):
    try:
        clamav_file_path = f"/app{file_path.split('/app')[-1]}"
        print(f"Scanning file at: {file_path}")
        print(f"File exists: {os.path.exists(file_path)}")

        cd = pyclamd.ClamdNetworkSocket(host='clamav', port=3310)

        if not cd.ping():
            raise Exception('ClamAV daemon is not running.')

        scan_result = cd.scan_file(clamav_file_path)

        if scan_result:
            return f"Malware detected: {scan_result}"
        return "File is clean."
    except Exception as e:
        return f"Error scanning file: {str(e)}"
