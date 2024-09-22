# python-schedule-interface
A simple GUI for Python's Schedule library

> [!NOTE]
> This repo won't be updated as writing this tool was more of an exercise to learn about trigger-based systems and creating workflows for 
> managing python scripts for personal use and small teams. I'll for sure be referring to this while building better tools in the future. 

![first version screenshot](/git_assets/main_grab.png)

# Introduction
This small tool built using the [Eel library](https://github.com/python-eel/Eel) and running the [Schedule library](https://github.com/dbader/schedule) under the hood provides a visual, code-free way of periodically running functions within Python modules. 

## Features
- Intuitively displays all Python modules within the directory in a dropdown, and populates all functions within the selected module for scheduling. 
- Schedule functions in minutes or seconds. 
- Allows for passing arguments to functions with parameters while scheduling for useful workflows. 
- Combine multiple schedule tasks to create a list/flow. Afterwards, `play` and `stop` the flow, which runs on a sepatate thread. 
- Basic error handling features that display error messages for when a function fails to run. 


