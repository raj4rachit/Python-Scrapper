import os
import sys
import win32com.client


def create_task(task_name, script_path):
    scheduler = win32com.client.Dispatch('Schedule.Service')
    scheduler.Connect()
    root_folder = scheduler.GetFolder('\\')

    task_def = scheduler.NewTask(0)
    task_def.RegistrationInfo.Description = "Task to run Python script every 5 minutes"

    # Create trigger - run every 5 minutes
    trigger = task_def.Triggers.Create(1)  # 1 means trigger type is Daily
    #trigger.DaysInterval = 1
    trigger.StartBoundary = "2024-04-29T00:00:00"  # Set the start time (adjust as needed)
    trigger.Repetition.Interval = "PT5M"  # PT5M means repeat every 5 minutes

    # Create action - run Python script
    action = task_def.Actions.Create(0)  # 0 means action type is Execute
    action.Path = sys.executable  # Path to Python executable
    action.Arguments = script_path  # Path to your script

    # Register the task
    result = root_folder.RegisterTaskDefinition(
        task_name,  # Task name
        task_def,
        6,  # TaskCreateOrUpdate
        "",  # User credentials (empty for current user)
        "",  # User password (empty for current user)
        3  # Logon type: Interactive session
    )

    if result == 0:
        print("Task created successfully.")
    else:
        print(f"Error creating task. Error code: {result}")


if __name__ == "__main__":
    task_name = "MyPythonTask"
    script_path = r"D:\python-react\scraper\windows_process\process.py"  # Replace with the path to your Python script
    create_task(task_name, script_path)
