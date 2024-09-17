import eel
import os
import importlib
import inspect
import json
import secrets
import schedule
import time
import datetime
import threading
import traceback
eel.init("web")


# some global variables to keep track of modules getting imported (key refers to the module name)
imported_modules = {}

# list of added tasks
all_tasks = []

# define a stop event
stop_event = threading.Event()
scheduler_thread = None


'''
getting filenames for all python scripts in the directory
'''


def get_module_names():
    script_dir = './'
    all_modules = []

    if os.path.exists(script_dir):
        # look for files with the .py extension
        for each_file in os.listdir(script_dir):
            if each_file.endswith('.py') and each_file != 'main.py':
                # getting rid of the py file extension
                module_name = each_file.split('.')[0]
                all_modules.append(module_name)
    else:
        print('scripts folder not found. please create one and dump all your scripts. Empty list will be returned')
    return all_modules


'''
When passed a module reference, this will return a list of all functions
within that module 
'''


def load_module_functions(module_ref):
    all_attr = dir(module_ref)
    all_functions = [attr for attr in all_attr if inspect.isfunction(
        getattr(module_ref, attr))]
    return all_functions


'''
This grabs all module names and sends over to the frontend 
for populating the first dropdown
'''


@eel.expose
def send_module_list():
    module_list = get_module_names()
    module_dic = {
        'modules': module_list
    }
    modules_to_render = json.dumps(module_dic)
    return modules_to_render


'''
Takes in the name of the selected module and imports it in an object-oriented way - 
creates a reference to the import and stores it in a global dictionary. 

Also sends over functions list to the frontend to render the second dropdown
'''


@eel.expose
def send_functions_list(selected_module):
    module_func = None
    try:
        # create a record in the imported modules dict provided it doesn't already exist
        if selected_module not in imported_modules:
            imported_modules[selected_module] = importlib.import_module(
                selected_module)

        # loading functions associated with selected module
        module_functions = load_module_functions(imported_modules[selected_module])

        module_func = {
            'functions': module_functions,
            'error': 'no'
        }
    except Exception as e:
        error_traceback = traceback.format_exc()
        error_message = f"{e}|{error_traceback}"
        module_func = {
             'functions': [],
             'error': error_message
        }

    to_render = json.dumps(module_func)
    return to_render

'''
For selected function, grab arguments and send to the frontend
'''
@eel.expose
def send_argument_list(selected_function, selected_module):
    # Access the module from the imported_modules dictionary
    module = imported_modules[selected_module]
    
    # Access the function from the module by name (string) if necessary
    func = getattr(module, selected_function)
    
    # Get the signature of the function
    sig = inspect.signature(func)
    
    # Get all parameters from the function signature
    all_parameters = [p for p in sig.parameters]

    json_load = {
        'parameters': all_parameters
    }

    to_render = json.dumps(json_load)
    print(to_render)
    return to_render
    


def refresh_task_view(state):
    # trigger a page refresh on some sort here
    flipped_task_list = sorted(
        all_tasks, key=lambda x: x["set-time"], reverse=False)
    # return the list with new tasks to JS
    to_render = json.dumps(flipped_task_list)
    eel.renderAddedTasks(to_render)
    eel.disableAllDeleteButtons(state)


def main_thread():
    # loading all the modules
    module_list_strings = get_module_names()
    modules = {}
    if len(module_list_strings) != 0:
        for each in module_list_strings:
            modules[each] = importlib.import_module(each)
    else:
        print('No modules returned')

    # loading functions associated with the modules
    for each_module in module_list_strings:
        functions_within = load_module_functions(modules[each_module])
        print(functions_within)


# add to a list of tasks
@eel.expose
def add_to_task_list(task_json):
    '''
    1. create an array called all_tasks
    2. turn the json back to a dictionary
    3. generate an unique identifer (maybe with current time + some kind of hash) to assign to the task
    4. chuck the task with id in all_tasks
    5. print out the results and test!
    '''
    '''
    structure for a task
     let task = {
            'module': selectedModule,
            'function': selectedFunction,
            'argument': providedFunctionArguments,
            'argument-message': argMessage, 
            'set-time': setTime,
            'set-type': setType...min and sec
        };
    '''

    task_to_add = json.loads(task_json)
    # assign unique id to each task
    task_to_add['id'] = secrets.token_hex(4)

    # adding a variable to track the number of times the task ran, starts with zero
    task_to_add['freq'] = 0

    # do come calculations and add a field to denote next run-time
    # current_time = datetime.datetime.now()
    # next_runtime = None

    # if task_to_add['set-type'] == "min":
    #     next_runtime = current_time + datetime.timedelta(minutes = int(task_to_add['set-time']))
    # else:
    #     next_runtime = current_time + datetime.timedelta(seconds = int(task_to_add['set-time']))

    task_to_add['next-runtime'] = "Not Running"

    print(task_to_add)

    # add to all_tasks array
    all_tasks.append(task_to_add)

    # sorting based on smallest time
    flipped_task_list = sorted(
        all_tasks, key=lambda x: x["set-time"], reverse=False)

    # return the list with new tasks to JS
    to_render = json.dumps(flipped_task_list)
    return to_render


@eel.expose
def remove_from_task_list(task_id):
    for each_task in all_tasks:
        if each_task['id'] == task_id:
            all_tasks.remove(each_task)


'''
function wrapper to keep track of function runs and manage UI updates
'''


def handle_function_run(f, task_id, func_pars):
    try:
        # try running this script
        if len(func_pars) == 0:
             execution = f()
        else:
            execution = f(*func_pars)       
    except Exception:
        print('Script execution unsuccessful: ')
        # write this to a file if script is unsuccessful
        traceback.print_exc()
    else:
        # grab the dictionary from list of tasks, should only be one
        task_matching_id = list(
            filter(lambda d: d['id'] == task_id, all_tasks))
        # grab the frequency
        new_freq = task_matching_id[0]['freq'] + 1
        # update frequency
        task_matching_id[0]['freq'] = new_freq
        # determine the next runtime
        # next_runtime = schedule.next_run(task_matching_id[0]['id'])
        # update next runtime
        # task_matching_id[0]['next-runtime'] = next_runtime.strftime('%d-%m-%Y_%H-%M-%S')
        # trigger a page refresh on some sort here
        refresh_task_view('play')


# schedules one task based on dict info
# this is where the main shedule is mentioned
def define_scheduler(task):
    '''
    structure for a task
     let task = {
            'module': selectedModule,
            'function': selectedFunction, 
            'set-time': setTime,
            'set-type': setType...min and sec
        };
    '''
    task_module = imported_modules[task['module']]

    # grabbing the function reference
    task_function = getattr(task_module, task['function'])

    task_function_parameters = []

    #if task function has parameters
    if task['argument'] != " ":
        task_function_parameters = task['argument'].replace(" ", "").split(',')

    if task['set-type'] == 'sec':
        schedule.every(int(task['set-time'])).seconds.do(handle_function_run,
                                                         f=task_function, task_id=task['id'], func_pars=task_function_parameters).tag(task['id'])
    else:
        schedule.every(int(task['set-time'])).minutes.do(handle_function_run,
                                                         f=task_function, task_id=task['id'], func_pars=task_function_parameters).tag(task['id'])


def initial_next_task_runtime_update():
    for each_task in all_tasks:
        next_task_run = schedule.next_run(each_task['id'])
        each_task['next-runtime'] = next_task_run.strftime('%d/%m/%Y %H:%M:%S')
    refresh_task_view('play')


def reset_all_next_runtime():
    for each_task in all_tasks:
        each_task['next-runtime'] = "Task Stopped"
    refresh_task_view('stop')


'''
function to run scheduler with a thread event
'''
def run_schedule(stop_event):
    '''
    1. schedule.next_run() will grab the schedule object that is meant to run next
    2. you can grab more information regarding the next scheduled task from here, possibly tags as well
    3. trigger the JS function based on next runtime

    '''
    next_run_time = None
    while not stop_event.is_set():
        schedule.run_pending()
        initial_next_task_runtime_update()
        next_run = schedule.next_run()
        if next_run and next_run != next_run_time:
            next_run_time = next_run
            print(f"Next scheduled job will run at {
                  next_run.strftime('%Y-%m-%d %H:%M:%S')}")
        time.sleep(1)


'''
Use the scheduler library to schedule all tasks in the all_tasks list
'''


@eel.expose
def trigger_schedule_tasks():

    # set the thread event to false initially
    global stop_event
    if stop_event.is_set():
        stop_event.clear()

    # scheduling everything here
    for each_task in all_tasks:
        define_scheduler(each_task)

    # start the scheduler in a different thread
    global scheduler_thread
    scheduler_thread = threading.Thread(
        target=run_schedule, args=(stop_event,))
    scheduler_thread.start()


@eel.expose
def trigger_task_halt():
    if scheduler_thread is not None:
        stop_event.set()
        scheduler_thread.join()
        # clear all previous jobs
        schedule.clear()
        reset_all_next_runtime()
        # clearing out the task list as well
        #all_tasks.clear()
        #imported_modules.clear()
    else:
        all_tasks.clear()
        imported_modules.clear()
    print('Scheduler has stopped and has been cleared')


def main():
    eel.start("index.html")


if __name__ == "__main__":
    main()
