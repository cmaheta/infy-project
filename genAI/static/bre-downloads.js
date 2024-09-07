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

function closeModal() {
    document.getElementById('fileModal').style.display = 'none';
}

// Close the modal when clicking outside of it
window.onclick = function(event) {
    if (event.target == document.getElementById('fileModal')) {
        document.getElementById('fileModal').style.display = 'none';
    }
}