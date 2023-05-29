let linkDeleteAccount = document.getElementById('link-delete-account');

linkDeleteAccount.addEventListener('click', function (e) {
    //Dialog delete account
    Swal.fire({
        title: 'Are you sure?',
        text: "Your account, tasks and projects will be deleted permanently!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#B84444',
        cancelButtonColor: '#363740',
        confirmButtonText: 'Yes, delete it'
        }).then((result) => {
        if (result.isConfirmed) {
            //Delete account with link
            window.location.href = "/account/delete";
        }
    })
});