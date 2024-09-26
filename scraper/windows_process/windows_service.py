import win32serviceutil
import win32service
import win32event
import psutil
import subprocess


class HRMSService(win32serviceutil.ServiceFramework):
    _svc_name_ = "HRMSService"
    _svc_display_name_ = "HRMS Service Check"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        self.main()

    def check_process_running(self, process_name):
        for process in psutil.process_iter():
            if process.name() == process_name:
                return True
        return False

    def start_application(self, application_path):
        subprocess.Popen(application_path)

    def main(self):
        process_name = "hrms3.exe"
        application_path = "C:/Program Files (x86)/HRMS/hrms3.exe"

        while True:
            if not self.check_process_running(process_name):
                self.start_application(application_path)
                self.log("Started HRMS.")
            else:
                self.log("HRMS is already running.")
            # Check every 60 seconds
            win32event.WaitForSingleObject(self.hWaitStop, 60000)

    def log(self, msg):
        import servicemanager
        servicemanager.LogInfoMsg(str(msg))


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(HRMSService)

# run this application
# python <path_to_script> install
# python service_installer.py install --startup auto --interactive --exe <path_to_python_executable> <path_to_script>

# python service_installer.py install --startup auto --interactive --exe "C:\Python312\python.exe" "D:\python-react\scraper\windows_process\process.py"