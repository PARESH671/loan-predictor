async function calculate() {
    const income = document.getElementById('income').value;
    const age = document.getElementById('age').value;
    const credit_score = document.getElementById('credit_score').value;
    const loan_amount = document.getElementById('loan_amount').value;
    const resultDiv = document.getElementById('result');

    resultDiv.innerHTML = "Fibe AI Analyzing Risk...";
    resultDiv.style.display = "block";
    resultDiv.className = "result-box";

    try {
        const response = await fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                income: income, 
                age: age, 
                credit_score: credit_score, 
                loan_amount: loan_amount 
            })
        });

        const data = await response.json();
        resultDiv.innerHTML = "Result: " + data.status;
        resultDiv.className = data.status.includes("Eligible") ? "result-box success" : "result-box fail";
    } catch (error) {
        resultDiv.innerHTML = "Error: Backend Offline";
        resultDiv.className = "result-box fail";
    }
}