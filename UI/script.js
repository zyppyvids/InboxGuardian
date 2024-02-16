async function evaluateText() {
    const textInput = document.getElementById('text-input');
    const text = textInput.value;

    if (text.trim() === "") {
        alert("Please enter text before evaluating.");
        return;
    }

    const response = await fetch(`http://localhost:8000/api/evaluate?text=${text}`);
    const result = await response.json();

    displayResult(result);

    // Clear the text input on click
    textInput.value = "";
}

function displayResult(result) {
    const resultContainer = document.getElementById('result-container');
    const resultInfo = document.createElement('div');
    resultInfo.className = result.result ? 'result-info true' : 'result-info false';
    resultInfo.innerHTML = `
        <p>${result.text}</p>
    `;
    resultContainer.appendChild(resultInfo);
}