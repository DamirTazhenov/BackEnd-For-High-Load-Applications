from django.core.exceptions import ValidationError

import pyclamd
def scan_file_for_malware(file_path):
    cd = pyclamd.ClamdUnixSocket()
    if not cd.ping():
        raise Exception('ClamAV daemon is not running.')
    scan_result = cd.scan_file(file_path)
    if scan_result:
        raise ValidationError('The file contains malware.')
