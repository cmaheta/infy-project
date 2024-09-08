function previewFile(filename) {
    fetch(`/preview/${filename}`)
        .then(response => response.json())
        .then(data => {
            if (data.content) {
                document.getElementById('fileContent').textContent = data.content;
                document.getElementById('fileModal').style.display = 'block';
            } else {
                alert('Error previewing file: ' + data.error);
            }
        });
}

function deleteFile(fileName) {
    // Show SweetAlert2 confirmation dialog
    Swal.fire({
        title: `Are you sure you want to delete ${fileName}?`,
        showCancelButton: true,
        confirmButtonText: 'Delete',
        cancelButtonText: 'Cancel',
        customClass: {
            title: 'swal2-title'  // Apply custom class to the title
        }
    }).then((result) => {
        if (result.isConfirmed) {
            // Send delete request if confirmed
            fetch(`/delete-file/${fileName}`, {
                method: 'DELETE',
            })
            .then(response => {
                if (response.ok) {
                    Swal.fire(
                        'Deleted!',
                        `${fileName} has been deleted.`,
                        'success'
                    ).then(() => {
                        location.reload();  // Reload the page to update the file list
                    });
                } else {
                    Swal.fire(
                        'Error!',
                        `Failed to delete ${fileName}.`,
                        'error'
                    );
                }
            })
            .catch(error => {
                console.error('Error:', error);
                Swal.fire(
                    'Error!',
                    'An unexpected error occurred.',
                    'error'
                );
            });
        }
    });
}

function closeModal() {
    document.getElementById('fileModal').style.display = 'none';
}

// Close the modal when clicking outside of it
window.onclick = function(event) {
    if (event.target == document.getElementById('fileModal')) {
        document.getElementById('fileModal').style.display = 'none';
    }
}