/**
     * function for rendering error messages for cases where an exception is 
     * raised in the Python script
*/

eel.expose(renderErrorMessage);
function renderErrorMessage(data){
    errorMessage = JSON.parse(data).error;
    errorHeading = JSON.parse(data).error_type;
    errorDiv = document.getElementById('error-display');

    allHtml = '';
    
    //add error message to the error div   
    allHtml += `<div class="alert alert-danger alert-dismissible fade show" role="alert">
        <h6 class='alert-heading'>${errorHeading}</h6>
        ${errorMessage}
        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span></button>
        </div>`;

    errorDiv.innerHTML += allHtml;
}


function loadModuleNames(data) {
    let moduleSelectionDiv = document.getElementById('module-selection');
    jsonData = JSON.parse(data);
    allModules = jsonData.modules;

    allHtml = '<p>Please select a <b>Module</b>:</p><select class = "form-control" name="modules" id="modules"><option value="no">No module selected</option>';

    for (let eachModule of allModules) {
        allHtml += `<option value="${eachModule}">${eachModule}</option>`;
    }

    allHtml += '</select>';

    moduleSelectionDiv.innerHTML = allHtml;
    moduleDropDown = document.getElementById('modules');
    //triggering sending module name 
    moduleDropDown.addEventListener('change', sendModuleNameOnModuleSelection);
}


function updateScheduleOptions() {
    let scheduleSelectionDiv = document.getElementById('schedule-selection');
    let selectedFunction = document.getElementById('functions').value;

    if (selectedFunction != "no") {
        allHtml = `<p>Please select a <b>Schedule time</b>:</p><p>"<i>I want to schedule <b>${selectedFunction}()</b>`;
        allHtml += ` to run every <input type="number" min="1" class="form-control form-control-sm mb-2 mr-2 w-25" style = "display: inline;" id="schedule-time"><select class = "form-control form-control-sm mb-2 mr-2 w-50" name="schedule-type" style = "display: inline;" id="schedule-type"><option value="sec">second(s)</option><option value="min">minute(s)</option></select>"</i>`;
        scheduleSelectionDiv.innerHTML = allHtml;

        //enable add task button
        addTaskButton = document.getElementById('add-task-btn');
        addTaskButton.disabled = false;
    }
    else {
        allHtml = `<p>Please select a <b>Schedule time</b>:</p><p>"<i>I want to schedule <b>no functions</b>`;
        allHtml += ` to run every <input type="number" min="1" class="form-control form-control-sm mb-2 mr-2 w-25" style = "display: inline;" id="schedule-time" disabled><select class = "form-control form-control-sm mb-2 mr-2 w-50" name="schedule-type" style = "display: inline;" id="schedule-type" disabled><option value="sec">second(s)</option><option value="min">minute(s)</option></select>"</i>`;
        scheduleSelectionDiv.innerHTML = allHtml;

        //disable add task button
        addTaskButton = document.getElementById('add-task-btn');
        addTaskButton.disabled = true;
    }

}


function loadModuleFunctions(data) {
    let functionSelectionDiv = document.getElementById('function-selection');
    allHtml = '<p>Please select a <b>Function</b> that you would like to schedule:</p><select class = "form-control" name="functions" id="functions">';
    if (data == 'no-select') {
        allHtml += '<option value="no">No functions selected</option>';
    }
    else {
        jsonData = JSON.parse(data);

        if(jsonData.error == 'no'){
            allFunctions = jsonData.functions;

            allHtml += '<option value="no">No functions selected</option>';

            for (let eachFunction of allFunctions) {
                allHtml += `<option value="${eachFunction}">${eachFunction}</option>`;
            }
        }
        else{
            allHtml += '<option value="no">No functions selected</option>';
        }

    }

    allHtml += '</select>';
    functionSelectionDiv.innerHTML = allHtml;
    //calling the function for that first refresh
    updateScheduleOptions();
    functionDropDown = document.getElementById('functions');
    functionDropDown.addEventListener('change', sendFunctionNameOnFunctionSelection);
    functionDropDown.addEventListener('change', updateScheduleOptions);
}

function sendModuleNameOnModuleSelection() {
    let modulesDropdown = document.getElementById('modules');
    let selectedModule = modulesDropdown.value;

    //call to python function to send back module functions data for rendering
    if (selectedModule != "no") {
        eel.send_functions_list(selectedModule)(loadModuleFunctions);
    }
    else {
        loadModuleFunctions('no-select');
    }
}

function updateArgumentTextArea(data){
    jsonData = JSON.parse(data);
    allArguments = jsonData.parameters;
    //grab the textarea reference so that it can be enabled/disabled
    textAreaRef = document.getElementById('func-par');
    argRefDiv = document.getElementById('arg-red');
    //enable the textarea
    textAreaRef.disabled = false;
    textAreaRef.value = " ";

    argRefHtml = '';

    argRefHtml += `<div class="alert alert-info" role="alert">`;

    //add content to textarea label
    if(allArguments.length == 0){
        //disable the textarea if function has no arguments
        textAreaRef.value = " ";
        textAreaRef.disabled = true;
        argRefHtml += 'This function has no parameters';
    }
    else{
        argRefHtml += '<b>Function parameters are: </b>'
        for(let eachArgument of allArguments){
            //no comma for last element
            if(allArguments[allArguments.length - 1] == eachArgument){
                 argRefHtml += `${eachArgument}`;
            }
            else{   
                argRefHtml += `${eachArgument}, `;
            }
        }
    }
    argRefHtml +=  `</div>`;
    argRefDiv.innerHTML = argRefHtml;
}



function sendFunctionNameOnFunctionSelection(){
    let selectedModule = document.getElementById('modules').value;
    let selectedFunction = document.getElementById('functions').value;
    //need a function to process the function argument data
    eel.send_argument_list(selectedFunction, selectedModule)(updateArgumentTextArea);

}


function errorDisplayGoAway(){
    errorDisplay = document.getElementById('error-display');
    errorDisplay.innerHTML = "";
}


//exposing this to eel so that tasks can be rendered on each run 
eel.expose(renderAddedTasks);
function renderAddedTasks(data) {
    jsonPayload = JSON.parse(data);
    allTasks = null;
    removeErrorDiv = true;

    if('remove_error_div' in jsonPayload){
        allTasks = jsonPayload.task_list;
        removeErrorDiv = false;
    }
    else{
        allTasks = jsonPayload;
    }

    if(removeErrorDiv){
        errorDisplayGoAway();
    }    
    
    taskDisplay = document.getElementById('main-display');

    allHtml = '';


    for (let eachTask of allTasks) {
        taskCard = `<div class="card" id="${eachTask['id']}">
                    <div class="card-header">
                      Task ID: ${eachTask['id']}
                      <button type="button" id = "${eachTask['id']}-task-delete" class="btn btn-primary btn-danger float-right delete-task-btn" onclick="deleteTaskOnClick(this)">Delete</button>
                    </div>
                    <div class="card-body">
                      <h5 class="card-title">Module: ${eachTask['module']}</h5>
                       <p class="card-text">Schedule function <b>${eachTask['function']}()</b> to run every <b>${eachTask['set-time']} ${eachTask['set-type']}</b></p>
                       <p>${eachTask['argument-message']}</p> 
                       <p><b>Next Run:</b> ${eachTask['next-runtime']}</p>
                      <button type="button" class="btn btn-warning task-freq" style="margin-top:2em">
                        Script Runs <span class="badge badge-light">${eachTask['freq']}</span>
                      </button>
                    </div>
                    </div>`;
        allHtml += taskCard;
    }

    taskDisplay.innerHTML = allHtml;

}


function deleteTaskOnClick(element) {
    //grab the id
    deleteTaskId = element.id.split("-")[0];
    taskCardToDelete = document.getElementById(deleteTaskId);
    //remove the element
    taskCardToDelete.remove();

    //trigger a python method here to remove the task from the task list
    eel.remove_from_task_list(deleteTaskId);
}


function addTaskOnButtonPress() {
    //need to make a map of data to be sent over to python
    //schedule-time and schedule-type
    selectedModule = document.getElementById('modules').value;
    selectedFunction = document.getElementById('functions').value;
    functionParameters = document.getElementById('func-par').value;
    providedFunctionArguments = functionParameters.split(',');

    argMessage = '';

    //grabbing parameter reference
    argRefDiv = document.getElementById('arg-red');
    divMessage = argRefDiv.firstChild.innerHTML;


    if(divMessage != 'This function has no parameters'){
        argDivMessage = divMessage.split('</b>')[1].split(',');
        for(let ar=0; ar<providedFunctionArguments.length; ar++){
            if(ar == (providedFunctionArguments.length-1)){
                argMessage +=  `<b>${argDivMessage[ar].trim()}</b>: ${providedFunctionArguments[ar].trim()}`;
            }
            else{
                argMessage +=  `<b>${argDivMessage[ar].trim()}</b>: ${providedFunctionArguments[ar].trim()}, `;
            }
            
        }

    }

    setTime = document.getElementById('schedule-time').value;
    setType = document.getElementById('schedule-type').value;

    let task = {
        'module': selectedModule,
        'function': selectedFunction,
        'argument': functionParameters,
        'argument-message': argMessage,
        'set-time': setTime,
        'set-type': setType
    };

    //send over to python for scheduling
    eel.add_to_task_list(JSON.stringify(task))(renderAddedTasks);

}

eel.expose(disableAllDeleteButtons);
function disableAllDeleteButtons(state) {
    allDeleteButtons = document.getElementsByClassName('delete-task-btn');
    if (state == 'play') {
        for (let each of allDeleteButtons) {
            each.disabled = true;
        }
    }
    else {
        for (let each of allDeleteButtons) {
            each.disabled = false;
        }
    }

}


function playAndStop(state) {
    playButton = document.getElementById("play-btn");
    stopButton = document.getElementById("stop-btn");
    addTaskButton = document.getElementById("add-task-btn");
    moduleSelection = document.getElementById("modules");
    functionsDropDown = document.getElementById("functions");
    sTime = document.getElementById("schedule-time");
    sType = document.getElementById("schedule-type");
    if (state == "play") {
        playButton.disabled = true;
        stopButton.disabled = false;
        addTaskButton.disabled = true;
        moduleSelection.disabled = true;
        functionsDropDown.disabled = true;
        sTime.disabled = true;
        sType.disabled = true;

    }
    else if (state == "stop") {
        playButton.disabled = false;
        stopButton.disabled = true;
        addTaskButton.disabled = false;
        moduleSelection.disabled = false;
        functionsDropDown.disabled = false;
        sTime.disabled = false;
        sType.disabled = false;
    }
}


function triggerScheduleTasks() {
    //call python function that does these
    eel.trigger_schedule_tasks();

    //disable the play button during schedule run
    playAndStop('play');
    disableAllDeleteButtons('play')

}

function triggerTaskHalt() {
    eel.trigger_task_halt();
    playAndStop('stop');
    disableAllDeleteButtons('stop')

}

eel.expose(updateTaskFrequency)
function updateTaskFrequency(taskId, freq) {
    //freqNum = document.getElementById(taskId).getElementsByClassName('task-freq')
    //freqNum.innerHTML = freq

    console.log(taskId)
    console.log(freq)
}

//js stuff to do as soon as the whole DOM loads
document.addEventListener("DOMContentLoaded", function (event) {
    eel.send_module_list()(loadModuleNames);
});

//event listener for app close event
window.addEventListener('beforeunload', function (e) {
    //e.preventDefault();
    eel.trigger_task_halt();
});
