import subprocess
import psutil
import schedule
import time

def check_process_running(process_name):
    for process in psutil.process_iter():
        if process.name() == process_name:
            return True
    return False

def start_application(application_path):
    subprocess.Popen(application_path)


def terminate_process(process_name):
    for process in psutil.process_iter():
        if process.name() == process_name:
            process.terminate()


def main():
    process_name = "hrms3.exe"
    application_path = "C:/Program Files (x86)/HRMS/hrms3.exe"  # Replace with the path to your application

    if check_process_running(process_name):
        print(f"{process_name} is already running. Terminating and restarting.")
        terminate_process(process_name)

    start_application(application_path)
    print(f"Started {process_name}.")


# Schedule the main function to run every 5 minutes
schedule.every(1).minutes.do(main)

# Run the scheduler continuously
while True:
    schedule.run_pending()
    time.sleep(1)  # Sleep for 1 second to avoid high CPU usage

#
# if __name__ == "__main__":
#     main()
