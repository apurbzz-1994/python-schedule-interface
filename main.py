import eel
import os
import importlib
import inspect
import json
import secrets
import schedule
import time
from datetime import datetime
eel.init("web")


'''
Writing some notes here for future me:
1. Create a function that saves a map of all the schedule tasks as a dictionary
2. Create a function that takes above dictionary and schedules them accordingly
3. Use a global flag to control a while loop within the scheduler function
4. Use a JS function to toggle the global flag
'''



#some global variables to keep track of modules getting imported (key refers to the module name)
imported_modules = {}

#list of added tasks
all_tasks = []

#flag to play/stop scheduler 
scheduler_running = True

def get_module_names():
    script_dir = './'
    all_modules = []

    if os.path.exists(script_dir):
        #look for files with the .py extension
        for each_file in os.listdir(script_dir):
            if each_file.endswith('.py') and each_file != 'main.py':
                module_name = each_file.split('.')[0] #getting rid of the py file extension
                all_modules.append(module_name)
    else:
        print('scripts folder not found. please create one and dump all your scripts. Empty list will be returned')
    return all_modules



#this grabs all function names
def load_module_functions(module_ref):
    all_attr = dir(module_ref)
    all_functions = [attr for attr in all_attr if inspect.isfunction(getattr(module_ref, attr))]
    return all_functions


@eel.expose
def send_module_list():
    module_list = get_module_names()
    module_dic = {
        'modules': module_list
    }
    modules_to_render = json.dumps(module_dic)
    return modules_to_render

@eel.expose
def send_functions_list(selected_module):
    #create a record in the imported modules dict provided it doesn't already exist
    if selected_module not in imported_modules:
        imported_modules[selected_module] = importlib.import_module(selected_module)

    #loading functions associated with selected module
    module_functions = load_module_functions(imported_modules[selected_module])

    module_func = {
        'functions': module_functions
    }

    to_render = json.dumps(module_func)
    return to_render


def main_thread():
    #loading all the modules
    module_list_strings = get_module_names()
    modules = {}
    if len(module_list_strings) != 0:
        for each in module_list_strings:
            modules[each] = importlib.import_module(each)
    else:
        print('No modules returned')
    

    #loading functions associated with the modules
    for each_module in module_list_strings:
        functions_within = load_module_functions(modules[each_module])
        print(functions_within)


#add to a list of tasks
@eel.expose 
def add_to_task_list(task_json):
    '''
    1. create an array called all_tasks
    2. turn the json back to a dictionary
    3. generate an unique identifer (maybe with current time + some kind of hash) to assign to the task
    4. chuck the task with id in all_tasks
    5. print out the results and test!
    '''

    task_to_add = json.loads(task_json)
    #assign unique id to each task
    task_to_add['id'] = secrets.token_hex(4)

    #add to all_tasks array
    all_tasks.append(task_to_add)

    #sorting based on smallest time
    flipped_task_list = sorted(all_tasks, key=lambda x: x["set-time"], reverse=False)

    #return the list with new tasks to JS
    to_render = json.dumps(flipped_task_list)
    return to_render


#schedules one task based on dict info
def define_scheduler(task):
    '''
    structure for a task
     let task = {
            'module': selectedModule,
            'function': selectedFunction,
            'set-time': setTime,
            'set-type': setType
        };
    '''
    task_module = imported_modules[task['module']]

    #grabbing the function reference 
    task_function = getattr(task_module, task['function'])

    if task['set-type'] == 'sec':
        schedule.every(int(task['set-time'])).seconds.do(task_function)
    else:
        schedule.every(int(task['set-time'])).minutes.do(task_function)



'''
Use the scheduler library to schedule all tasks in the all_tasks list
'''
@eel.expose
def trigger_schedule_tasks():
    #scheduling everything here
    for each_task in all_tasks:
        define_scheduler(each_task)
    
    next_run_time = None

    while True:
        if scheduler_running == True:
            schedule.run_pending()
            next_run = schedule.next_run()
            if next_run and next_run != next_run_time:
                next_run_time = next_run
                print(f"Next scheduled job will run at {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
            time.sleep(1)
        else:
            break

@eel.expose
def trigger_task_halt():
    scheduler_running = False
    print('Scheduler has stopped')
    


def main():
    eel.start("index.html")
            

if __name__ == "__main__":
    main()