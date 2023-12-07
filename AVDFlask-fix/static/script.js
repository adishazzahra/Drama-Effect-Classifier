function predict() {
    const formData = new FormData(document.getElementById('predictionForm'));

    fetch('/predict', {
        method: 'POST',
        body: JSON.stringify(Object.fromEntries(formData)),
        headers: {
            'Content-Type': 'application/json',
        },
    })
        .then(response => response.json())
        .then(data => {
            Swal.fire({
                title: 'Prediction Result',
                text: data.prediction_message,
                icon: 'info',
                confirmButtonText: 'OK'
            }).then((result) => {
                if (result.isConfirmed) {
                    document.getElementById('predictionResult').innerText = data.prediction_message;
                    document.getElementById('predictionResult').scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        })
        .catch(error => console.error('Error:', error));
}