import subprocess
import platform

def check_process_running(process_name):
    command = f"pgrep -x {process_name}"
    try:
        subprocess.check_output(command, shell=True)
        return True
    except subprocess.CalledProcessError:
        return False

def start_application(application_path):
    subprocess.Popen(["open", application_path])

def main():
    process_name = "hrms3"
    application_path = "/Applications/HRMS/hrms3.app"  # Replace with the path to your application

    if not check_process_running(process_name):
        start_application(application_path)
        print(f"Started {process_name}.")
    else:
        print(f"{process_name} is already running.")

if __name__ == "__main__":
    main()
