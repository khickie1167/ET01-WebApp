document.getElementById('refresh-dashboard').addEventListener('click', function() {
    var iframe = document.getElementById('powerbi-frame');
    iframe.src = iframe.src; // Refresh the iframe
    updateTimestamp();
});

function updateTimestamp() {
    var now = new Date();
    var formattedTime = now.toLocaleString(); // Format the current time
    document.getElementById('last-refreshed-time').innerText = formattedTime;
}

// Initialize the timestamp on page load
document.addEventListener('DOMContentLoaded', function() {
    updateTimestamp();
});
