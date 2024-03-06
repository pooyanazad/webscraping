$(document).ready(function() {
    $('#scrapeForm').submit(function(event) {
        event.preventDefault();
        var url = $('#urlInput').val();
        $.ajax({
            url: '/scrape', // Your Flask endpoint
            type: 'POST',
            data: { url: url },
            success: function(data) {
                $('#dataDisplay').prepend('<p>Scraped Data: ' + JSON.stringify(data) + '</p>');
                // Update chart data here if necessary
            },
            error: function(error) {
                console.log('Error:', error);
            }
        });
    });

    var ctx = document.getElementById('dataChart').getContext('2d');
    var dataChart = new Chart(ctx, {
        type: 'bar', // Choose your chart type
        data: {
            labels: ['Data'], // Update labels based on your data
            datasets: [{
                label: 'Data Visualization',
                data: [0], // Update this with actual data
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});
