import os
import sys
import time
import win32serviceutil
import win32service
import win32event
import win32api

class ShutdownService(win32serviceutil.ServiceFramework):
    _svc_name_ = "ShutdownService"
    _svc_display_name_ = "Shutdown Service"
    _svc_description_ = "Shuts down the computer every hour."

    def __init__(self, args):
        # Modify args to include default installation arguments if not provided
        if len(args) == 1:
            args = [sys.executable, __file__, "install"] + args
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        self.main()

    def main(self):
        while True:
            # Wait for 1 hour (3600 seconds)
            time.sleep(300)
            # Shut down the computer
            win32api.InitiateSystemShutdown(None, "Shutting down", 30, True, False)

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(ShutdownService)
