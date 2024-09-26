import os
import sys
import win32serviceutil
import win32service
import win32event
import win32evtlogutil

from windows_service import HRMSService

if __name__ == '__main__':
    if len(sys.argv) > 0:
        # Run as service
        servicename = HRMSService._svc_name_
        try:
            if os.name == 'nt':
                win32serviceutil.HandleCommandLine(HRMSService)
            else:
                print("This script is intended for Windows only.")
        except Exception as e:
            win32evtlogutil.ReportEvent(servicename,
                                         servicename,
                                         "Service failed to start",
                                         win32evtlogutil.Error,
                                         (servicename, str(e)))
    else:
        print("Invalid command line arguments.")
