# python-schedule-interface
A simple GUI for the Python Schedule library

> [!NOTE]
> This repository won't be updated as writing this tool was more of an exercise to learn about trigger-based systems and creating 
> workflows for managing Python scripts for personal use and small teams.

![first version screenshot](/git_assets/main_grab.png)

# Introduction
This small tool built using the [Eel library](https://github.com/python-eel/Eel) and running the [Schedule library](https://github.com/dbader/schedule) under the hood provides a visual, code-free way of periodically running functions within Python modules. 

## Features
- Intuitively displays all Python modules within the directory in a dropdown, and populates all functions within the selected module for scheduling. 
- Schedule functions in `minutes` or `seconds`. 
- Allows for passing arguments to functions with parameters while scheduling for useful workflows. 
- Combine multiple schedule tasks to create a list/flow. Afterwards, `play` and `stop` the flow accordingly, which runs on a sepatate thread.
- Runs locally on your machine, no servers needed.  
- Basic error handling features that display error messages for when a function fails to run. 

## How to run
1. Install the latest version of Python from [https://www.python.org/downloads](https://www.python.org/downloads/), ensuring that you've added Python to your `PATH` (more on this here: [https://realpython.com/add-python-to-path](https://realpython.com/add-python-to-path/)). 

2. Clone this repository in your machine or download the project files via `Code > Download ZIP`. It is recommended to use a Python virtual environment (like [venv](https://docs.python.org/3/library/venv.html)) so that all modules and dependencies can be housed neatly in one place.

3. Open your terminal and `cd` to the repository directory and run the following command:

    ```
    pip install -r requirements.txt
    ```

    This will install all necessary modules. 

4. To run the application, open a terminal, `cd` to the correct directory and run the following command:

    ```
    python3 main.py
    ```

    Depending on your system, you may need to use `python` or `python3` in the above command. 

    This will launch the dashboard. 


# Workflow
1. Place all your Python module files/scripts in the same directory as this project's `main.py` file. 

> [!NOTE]
> It's recommended that you have your Python scripts modularised and broken down into functions that can be scheduled. 
> If you're using a `if __name__ == "__main__":` statement in your script, you'll have to remove that and schedule the `main()`
> function via the tool instead (or create a `main()` function if not present). This is because the tool imports the selected Python 
> module to access its functions and we want to prevent unwanted script execution at this stage. 

2. Launch the tool. You'll see all the files you've just added in the first drop-down:

![modules dropdown](/git_assets/workflow_1.png)
<img src="/git_assets/workflow_1.png" width="588" height="186" />

3. On selecting a module, the second drop-down will be populated with module functions:

![modules dropdown](/git_assets/workflow_2.png)
<img src="/git_assets/workflow_2.png" width="588" height="186" />

4. On selecting a function, if it accepts arguments, you can input them here, separated by commas for multiple arguments. For example, the function being scheduled here will take a CSV file of course codes and will grab the student count for each from a Learning Management System. In this case, the function's argument is the filename of the CSV:
 
 ![argument input](/git_assets/workflow_3.png)

 5. Set a frequency for the schedule. You're able to set this in `minutes` or `seconds`. 

 6. Once ready, click on the `Add Schedule Task` button to add a scheduling task to the list/flow. 

 7. In a similar manner, create as many tasks as needed. You're also able to remove tasks from the list by clicking the `Delete` button 
 on the top right corner of each task. 

 8. Once your schedule list is ready, hit `Play` to run the scheduler. This will periodically run the tasks based on the frequencies previously set. The GUI will update you on the **"number of total script runs"** and **"time for next script run"** for each of the tasks:

 ![first version screenshot](/git_assets/workflow_4.png)

 9. To halt the flow, click on th `Stop` button. To resume the flow, hit `Play` again. 


# Common errors

## 'No Module' error

![first version screenshot](/git_assets/error_1.png)

**Description:** This implies that the Python script from which you're trying to schedule a function is making use of a module that hasn't been installed yet, but has been imported in the script. You'll experience this error while the tool attempts to load the functions. 

**Fix:** Install the required module(s) using `pip`. 


## Function errors

![first version screenshot](/git_assets/error_2.png)

**Description:** The tool will catch any error that the scheduled functions may throw and render a corresponding error message.  

**Fix:** Determine which task's function is throwing an error by checking the task ID in the error message's heading, and fix the script accordingly. 


