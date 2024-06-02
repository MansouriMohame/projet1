document.getElementById('predictionForm').addEventListener('submit', function(e) {
    e.preventDefault();

    let formData = {
        CODE_INTERNE_ARTICLE: document.getElementById('CODE_INTERNE_ARTICLE').value,
        LIBELLE_ARTICLE_x: document.getElementById('LIBELLE_ARTICLE_x').value,
        LIBFRS: document.getElementById('LIBFRS').value,
        MARQUE: document.getElementById('MARQUE').value,
        LIB_RAY: document.getElementById('LIB_RAY').value,
        LIB_SSFAM: document.getElementById('LIB_SSFAM').value,
        temperature: document.getElementById('temperature').value,
        year: document.getElementById('year').value,
        month: document.getElementById('month').value,
        day: document.getElementById('day').value
    };

    fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('result').innerText = `Predicted Price: ${data.prediction}`;
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('result').innerText = 'An error occurred. Please try again.';
        });
});