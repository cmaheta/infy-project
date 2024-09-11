// Get the wrapper that holds the file inputs
let wrapper = document.getElementById('fileInputsWrapper');

// Add click event listener to the "+" button
document.getElementById('addFolderBtn').addEventListener('click', function () {
    const inputFields = wrapper.getElementsByClassName('file-field input-field');

    // Check if there's more than one div to avoid removing all inputs
    if (inputFields.length < 5) {
        // Create a new div for the new input element
        let newMainDiv = document.createElement('div');
        newMainDiv.className = 'file-field input-field';

        // Create a new input element
        let newInput1 = document.createElement('input');
        newInput1.type = 'file';
        newInput1.name = 'files[]';
        newInput1.id = 'fileInput';

        // Create a label for the input
        let newInnerDiv1 = document.createElement('div');
        newInnerDiv1.className = 'btn';
        newInnerDiv1.innerHTML = '<span>File</span>';
        // Append the input to the label
        newInnerDiv1.appendChild(newInput1);

        let newInnerDiv2 = document.createElement('div');
        newInnerDiv2.className = "file-path-wrapper";
        let newInput2 = document.createElement('input');
        newInput2.className = "file-path";
        newInput2.type = 'text';
        newInput2.placeholder = 'Choose mainframe code';
        newInnerDiv2.appendChild(newInput2);

        newMainDiv.appendChild(newInnerDiv1);
        newMainDiv.appendChild(newInnerDiv2);

        // Append the new input wrapper to the main wrapper
        wrapper.appendChild(newMainDiv);
    }
});

document.getElementById('removeFolderBtn').addEventListener('click', function () {
    // Get all file-field input-field divs
    const inputFields = wrapper.getElementsByClassName('file-field input-field');

    // Check if there's more than one div to avoid removing all inputs
    if (inputFields.length > 1) {
        wrapper.removeChild(inputFields[inputFields.length - 1]);
    }
});

function convertFilename(filename) {
    // Use a regular expression to find the number inside parentheses and replace it
    return filename.replace(/\s*\((\d+)\)\s*/, '_$1').replace(/\s+/g, '_');
}

let intervalId = null;

function checkStatus() {
    fetch('/check_status')
        .then(response => response.json())
        .then(data => {
            // Update the status and message on the web page
            const progressBar = document.getElementById('progress-bar');
            const message = document.getElementById('message');

            const current_progress = progressBar.innerText;
            updated_progress = parseInt(current_progress) + 5;
            if (updated_progress <= 90) {
                progressBar.style.width = `${updated_progress}%`;
                progressBar.innerText = `${updated_progress}`;
                message.innerText = data.message;
            }

            // Stop polling when progress reaches 100%
            if (data.progress === 100) {
                clearInterval(intervalId);
                progressBar.style.width = `${data.progress}%`;
                progressBar.innerText = `${data.progress}`;
                message.innerText = data.message;
                var show_downloads_div = document.getElementById("show_downloads_div");
                show_downloads_div.style.display = "block";
                const process_btn = document.getElementById('process-btn');
                process_btn.disabled = false;
                populateFileList();
            }
        })
        .catch(error => {
            console.error('Error fetching status:', error);
        });
}

function startProcess() {
    const progressBar = document.getElementById('progress-bar');
    const message = document.getElementById('message');
    progressBar.style.width = `10%`;
    progressBar.innerText = `10`;
    message.innerText = 'Uploading files to process...';

    //reset buttons and data
    const process_btn = document.getElementById('process-btn');
    process_btn.disabled = true;
    const deletedFilesDiv = document.getElementById('deleted_files');
    deletedFilesDiv.textContent = '';
    var progress_bar_div = document.getElementById("progress_bar_div");
    progress_bar_div.style.display = "block";
    var progress_bar_div = document.getElementById("show_downloads_div");
    progress_bar_div.style.display = "none";
    

    intervalId = setInterval(checkStatus, 5000);
    const formData = new FormData();
    const fileInput = document.getElementById('fileInput');

    for (const file of fileInput.files) {
        formData.append('files[]', file);
    }
    const selectedProcessType = document.querySelector('input[name="process-type"]:checked').value;
    formData.append('process-type', selectedProcessType);

    fetch('/ai-processes', { method: 'POST', body: formData })
        .then(response => response.json())
        .then(data => {
            console.log('Process started');
        })
        .catch(error => {
            console.error('Error starting process:', error);
        });
}

function populateFileList() {
    const fileInput = document.getElementById('fileInput');
    const fileList = document.getElementById('fileList');
    const deletedFilesDiv = document.getElementById('deleted_files');
    const deletedFiles = deletedFilesDiv.textContent ? deletedFilesDiv.textContent.split(',') : [];

    fileList.innerHTML = ''; // Clear the list before adding new items

    for (const file of fileInput.files) {
        if (!deletedFiles.includes(file.name)) {
            secure_file_name=convertFilename(file.name)
            const listItem = document.createElement('li');
            listItem.innerHTML = `
            <a style="font-size: large;" href="/ai-download-file/${secure_file_name}" download style="font-size: large;">
                ${file.name}
            </a>
            <button style="margin-left: 20px;" type="button" class="btn waves-effect waves-light"
                onclick="previewFile('${file.name}')">Preview</button>
            <button style="margin-left: 20px;" type="button" class="btn waves-effect waves-light"
                onclick="deleteFile('${file.name}')">Delete</button>
        `;
            fileList.appendChild(listItem);
        }
    }
}

function previewFile(filename) {
    secure_file_name=convertFilename(filename)
    fetch(`/preview/${secure_file_name}`)
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
            const formData = new FormData();
            const selectedProcessType = document.querySelector('input[name="process-type"]:checked').value;
            formData.append('process-type', selectedProcessType);
            secure_file_name=convertFilename(fileName)
            fetch(`/delete-file/${secure_file_name}`, {
                method: 'POST',
                body: formData
            })
                .then(response => {
                    if (response.ok) {
                        Swal.fire(
                            'Deleted!',
                            `${fileName} has been deleted.`,
                            'success'
                        ).then(() => {
                            // Add the deleted filename to the hidden div
                            const deletedFilesDiv = document.getElementById('deleted_files');
                            const currentDeletedFiles = deletedFilesDiv.textContent ? deletedFilesDiv.textContent.split(',') : [];
                            currentDeletedFiles.push(fileName);
                            deletedFilesDiv.textContent = currentDeletedFiles.join(',');
                            populateFileList();
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
window.onclick = function (event) {
    if (event.target == document.getElementById('fileModal')) {
        document.getElementById('fileModal').style.display = 'none';
    }
}

// Attach click event to the start button
document.getElementById('process-btn').addEventListener('click', startProcess);