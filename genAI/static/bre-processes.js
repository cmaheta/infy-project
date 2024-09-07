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