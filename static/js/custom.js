document.addEventListener('DOMContentLoaded', function() {
    const refreshButton = document.getElementById('refresh-dashboard');
    const lastRefreshedTime = document.getElementById('last-refreshed-time');
    const powerbiFrame = document.getElementById('powerbi-frame');

    if (refreshButton && lastRefreshedTime && powerbiFrame) {
        refreshButton.addEventListener('click', function() {
            console.log('Refresh button clicked');
            // Reload the Power BI iframe
            powerbiFrame.src = powerbiFrame.src;

            // Fetch the current timestamp and update the last refreshed time
            axios.post('/refresh_dashboard')
                .then(response => {
                    console.log('Timestamp fetched successfully:', response.data.timestamp);
                    lastRefreshedTime.textContent = response.data.timestamp;
                })
                .catch(error => {
                    console.error('Error fetching refresh timestamp:', error.response || error.message);
                });
        });
    } else {
        console.error('Refresh button, last refreshed time, or powerbiFrame not found');
    }

    const uploadBox = document.getElementById('upload-box');
    const fileInput = document.getElementById('fileInput');
    const uploadStatus = document.getElementById('upload-status');

    uploadBox.addEventListener('click', () => fileInput.click());
    uploadBox.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadBox.classList.add('dragover');
    });
    uploadBox.addEventListener('dragleave', () => uploadBox.classList.remove('dragover'));
    uploadBox.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadBox.classList.remove('dragover');
        handleFiles(e.dataTransfer.files);
    });
    fileInput.addEventListener('change', () => handleFiles(fileInput.files));

    function handleFiles(files) {
        if (files.length > 0) {
            const formData = new FormData();
            for (const file of files) {
                formData.append('file', file);
            }
            axios.post('/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            })
            .then(response => {
                uploadStatus.textContent = response.data.message;
            })
            .catch(error => {
                uploadStatus.textContent = 'Error uploading file: ' + (error.response ? error.response.data.message : error.message);
            });
        } else {
            uploadStatus.textContent = 'No files selected';
        }
    }
});
