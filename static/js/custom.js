document.addEventListener('DOMContentLoaded', function() {
    const uploadBox = document.getElementById('upload-box');
    const fileInput = document.getElementById('fileInput');
    const uploadStatus = document.getElementById('upload-status');

    if (uploadBox && fileInput && uploadStatus) {
        uploadBox.addEventListener('click', () => fileInput.click());

        uploadBox.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadBox.classList.add('dragover');
        });

        uploadBox.addEventListener('dragleave', () => {
            uploadBox.classList.remove('dragover');
        });

        uploadBox.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadBox.classList.remove('dragover');
            const files = e.dataTransfer.files;
            handleFiles(files);
        });

        fileInput.addEventListener('change', (e) => {
            const files = e.target.files;
            handleFiles(files);
        });

        function handleFiles(files) {
            const formData = new FormData();
            for (let i = 0; i < files.length; i++) {
                formData.append('files', files[i]);
            }

            flashOrangeBorder();
            setStatusText('Uploading files...');
            clearStatusClasses();

            axios.post('/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            }).then(response => {
                console.log('Files uploaded successfully');
                stopFlashingBorder();
                uploadBox.classList.add('upload-success');
                setStatusText('Files uploaded successfully');
            }).catch(error => {
                console.error('Error uploading files', error);
                stopFlashingBorder();
                uploadBox.classList.add('upload-failed');
                setStatusText('Error uploading files');
            });
        }

        function flashOrangeBorder() {
            uploadBox.classList.add('flashing');
        }

        function stopFlashingBorder() {
            uploadBox.classList.remove('flashing');
        }

        function setStatusText(text) {
            uploadStatus.textContent = text;
        }

        function clearStatusClasses() {
            uploadBox.classList.remove('upload-success', 'upload-failed');
        }
    }
});
