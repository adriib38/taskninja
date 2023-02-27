/**
 * Metodos para consumir la API desde el navegador.
 */

let btns_done_task = document.querySelectorAll('.btn-done-task');

//Obtener token del usuario
var cookies = document.cookie.split(';');
var tokenUser = null;
for (var i = 0; i < cookies.length; i++) {
    var cookie = cookies[i].trim();
    if (cookie.indexOf('tokenUser=') === 0) {
        tokenUser = cookie.substring('tokenUser='.length, cookie.length);
        break;
    }
}
tokenUser = 'Token ' + tokenUser;

/**
 * Marca una tarea como completada y la mueve a la sección de tareas completadas
 */
function doneTask(id) {
    let section_done_tasks = document.querySelector('#done-tasks');
    //PATCH request with fetch
    fetch('http://127.0.0.1:8000/api/tasks/' + id + '/', {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': tokenUser
        },
        body: JSON.stringify({
            done: true,
            date_done: new Date()   
        })
    })
    .then(response => response.json())
    .then(data => {
        //Ocultar la tarea
        let task = document.querySelector('#task-' + id);
        //Mover la tarea a la sección de tareas completadas

        section_done_tasks.appendChild(task);

        //Cambiar boton de done a undone
        let btn_done_task = document.querySelector('.btn-done-' + id);
        btn_done_task.classList.remove('btn-done');
        btn_done_task.classList.add('btn-undone');
        btn_done_task.innerHTML = 'Undone';
        btn_done_task.setAttribute('onclick', 'undoneTask(' + id + ')');

        try {
            //Cambiar texto estado de la tarea
            let task_status = task.querySelector('#task-status');
            task_status.innerHTML = 'Done';
            task_status.classList.remove('task-status-pending');
            task_status.classList.add('task-status-done');

            //Cambiar emoji
            let task_emoji = task.querySelector('.emoji');
            task_emoji.innerHTML = '✅';
        }catch(error) {
    
        }

    })
    .catch(error => console.log(error));
}

/**
 * Marca una tarea como pendiente y la mueve a la sección de tareas pendientes
 */
function undoneTask(id) {
    let section_undone_tasks = document.querySelector('#undone-tasks');
    //PATCH request with fetch
    fetch('http://127.0.0.1:8000/api/tasks/' + id + '/', {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': tokenUser
        },
        body: JSON.stringify({
            done: false,
            date_done: null
        })
    })
    .then(response => response.json())
    .then(data => {
        //Ocultar la tarea
        let task = document.querySelector('#task-' + id);
        //Mover la tarea a la sección de tareas completadas

        section_undone_tasks.appendChild(task);

        //Cambiar boton de undone a done
        let btn_done_task = document.querySelector('.btn-done-' + id);
        btn_done_task.classList.remove('btn-undone');
        btn_done_task.classList.add('btn-done');
        btn_done_task.innerHTML = 'Done';

        btn_done_task.setAttribute('onclick', 'doneTask(' + id + ')');

        //Cambiar texto estado de la tarea
        try {
            let task_status = task.querySelector('#task-status');
            task_status.innerHTML = 'Pending';
            task_status.classList.remove('task-status-done');
            task_status.classList.add('task-status-pending');

            //Cambiar emoji
            let task_emoji = task.querySelector('.emoji');
            task_emoji.innerHTML = '🕑';
        }catch(error) {
    
        }

    })
    .catch(error => console.log(error));
}

/**
 * Elimina una tarea
 */
function deleteTask(id) {
    //DELETE request with fetch
    fetch('http://127.0.0.1:8000/api/tasks/' + id + '/', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': tokenUser
        }
    })
    .then(data => {
        console.log('Tarea eliminada');
        //Ocultar la tarea
        let task = document.querySelector('#task-' + id);
        task.style.display = 'none';
    }
    )
    .catch(error => console.log(error));
}

/**
 * Elimina un proyecto
 */
function deleteProject(id) {
    //DELETE request with fetch
    fetch('http://127.0.0.1:8000/api/projects/' + id + '/', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': tokenUser
        }
    })
    .then(data => {
        console.log('Proyecto eliminado');
        //Ocultar el proyecto
        let project = document.querySelector('#project-' + id);
        project.style.display = 'none';
    }
    )
    .catch(error => console.log(error));
}

       