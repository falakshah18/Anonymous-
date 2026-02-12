async function scanURL() {

    const url = document.getElementById("urlInput").value.trim();
    const resultBox = document.getElementById("resultBox");

    if (!url) {
        resultBox.innerText = "Please enter a valid URL.";
        return;
    }

    resultBox.innerText = "Scanning...";

    try {
        const response = await fetch("http://127.0.0.1:8000/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ url: url })
        });

        // Check if backend returned error
        if (!response.ok) {
            throw new Error("Server error");
        }

        const data = await response.json();

        // Color based on risk level
        let riskColor = "green";

        if (data.risk_level.includes("HIGH")) {
            riskColor = "red";
        } else if (data.risk_level.includes("MEDIUM")) {
            riskColor = "orange";
        }

        resultBox.innerHTML = `
            <strong>Risk Score:</strong> ${data.risk_score} <br>
            <strong>Risk Level:</strong> 
            <span style="color:${riskColor}; font-weight:bold;">
                ${data.risk_level}
            </span><br><br>
            <strong>Threats:</strong><br>
            ${data.threats_detected.length > 0
                ? data.threats_detected.map(t => "• " + t).join("<br>")
                : "No major threats detected."}
            <br><br>
            <strong>Recommendation:</strong> ${data.recommendation}
        `;

    } catch (error) {
        resultBox.innerText = "Backend not connected or server error.";
    }
}
