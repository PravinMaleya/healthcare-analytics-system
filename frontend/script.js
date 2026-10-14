const API_URL = window.location.origin;

const form = document.getElementById("prediction-form");
const result = document.getElementById("result");
const resultTitle = document.getElementById("result-title");
const resultMessage = document.getElementById("result-message");
const predictButton = document.getElementById("predict-button");

function showMessage(title, message, isError = false) {
    resultTitle.textContent = title;
    resultMessage.textContent = message;
    result.classList.toggle("error", isError);
    result.hidden = false;
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    if (!form.reportValidity()) return;

    const payload = Object.fromEntries(new FormData(form).entries());
    payload.age = Number(payload.age);

    predictButton.disabled = true;
    predictButton.textContent = "Predicting...";
    result.hidden = true;

    try {
        const response = await fetch(`${API_URL}/predict`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (!response.ok) {
            const detail = Array.isArray(data.detail)
                ? "Please check the submitted fields."
                : (data.detail || "The API rejected the request.");

            throw new Error(detail);
        }

        showMessage(
            `Prediction: ${data.predicted_test_result}`,
            "The model returned a prediction successfully."
        );
    } catch (error) {
        const message = error.message === "Failed to fetch"
            ? "Could not reach the API. Check the URL, service status, and CORS settings."
            : error.message;

        showMessage("Prediction failed", message, true);
    } finally {
        predictButton.disabled = false;
        predictButton.textContent = "Predict Result";
    }
});

form.addEventListener("reset", () => {
    result.hidden = true;
    result.classList.remove("error");
    resultTitle.textContent = "";
    resultMessage.textContent = "";
});
