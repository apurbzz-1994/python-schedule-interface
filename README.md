# python-schedule-interface
A simple GUI for Python's Schedule library

> [!NOTE]
> This repo won't be updated as writing this tool was more of an exercise to learn about trigger-based systems and creating workflows for 
> managing Python scripts for personal use and small teams. I'll for sure be referring to this while building better tools in the future. 

![first version screenshot](/git_assets/main_grab.png)

# Introduction
This small tool built using the [Eel library](https://github.com/python-eel/Eel) and running the [Schedule library](https://github.com/dbader/schedule) under the hood provides a visual, code-free way of periodically running functions within Python modules. 

## Features
- Intuitively displays all Python modules within the directory in a dropdown, and populates all functions within the selected module for scheduling. 
- Schedule functions in `minutes` or `seconds`. 
- Allows for passing arguments to functions with parameters while scheduling for useful workflows. 
- Combine multiple schedule tasks to create a list/flow. Afterwards, `play` and `stop` the flow accordingly, which runs on a sepatate thread. 
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
