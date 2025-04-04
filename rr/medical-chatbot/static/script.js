function searchDisease() {
    let inputText = document.getElementById("searchInput").value;

    if (!inputText) {
        alert("Please enter a disease or symptom.");
        return;
    }

    document.getElementById("loading").classList.remove("d-none");
    document.getElementById("result").classList.add("hidden");

    fetch("/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query_type: "disease", input_text: inputText })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("loading").classList.add("d-none");
        document.getElementById("result").classList.remove("hidden");

        document.getElementById("diseaseName").innerText = inputText;
        document.getElementById("responseText").innerText = data.response || "No data available.";
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Something went wrong. Please try again.");
    });
}
