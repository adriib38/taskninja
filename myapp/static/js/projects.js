
function clickDeleteProject(projectId){

    //Dialog delete project
    Swal.fire({
        title: 'Delete project?',
        //icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#B84444',
        cancelButtonColor: '#363740',
        confirmButtonText: 'Delete it'
    }).then((result) => {
        if (result.isConfirmed) {
           deleteProject(projectId);
        }
    })
}


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
