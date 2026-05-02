// -----------------------------
// GLOBAL VARIABLES
// -----------------------------
let positiveCount = 0;
let negativeCount = 0;
let neutralCount = 0;

let sentimentChart;
let trendChart;


// -----------------------------
// INIT CHARTS
// -----------------------------
window.onload = function () {

    // PIE CHART
    const ctx = document.getElementById("chart").getContext("2d");

    sentimentChart = new Chart(ctx, {
        type: "pie",
        data: {
            labels: ["Positive", "Negative", "Neutral"],
            datasets: [{
                data: [0, 0, 0]
            }]
        }
    });

    // TREND CHART
    const trendCtx = document.getElementById("trendChart").getContext("2d");

    trendChart = new Chart(trendCtx, {
        type: "line",
        data: {
            labels: [],
            datasets: [
                { label: "Positive", data: [], borderWidth: 2 },
                { label: "Negative", data: [], borderWidth: 2 },
                { label: "Neutral", data: [], borderWidth: 2 }
            ]
        },
        options: {
            responsive: true
        }
    });
};


// -----------------------------
// SINGLE REVIEW ANALYSIS
// -----------------------------
async function analyzeReview() {

    const review = document.getElementById("review").value;

    if (!review) {
        alert("Please enter a review!");
        return;
    }

    document.getElementById("result").innerHTML = "⏳ Analyzing...";

    try {
        const response = await fetch("http://127.0.0.1:8000/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text: review })
        });

        const data = await response.json();

        if (data.error) {
            document.getElementById("result").innerHTML = "❌ " + data.error;
            return;
        }

        // Update result
        document.getElementById("result").innerHTML =
            `Sentiment: ${data.sentiment} <br> Confidence: ${data.confidence}%`;

        // Update counts
        if (data.sentiment.includes("Positive")) positiveCount++;
        else if (data.sentiment.includes("Negative")) negativeCount++;
        else neutralCount++;

        updateDashboard();

    } catch (error) {
        document.getElementById("result").innerHTML =
            "⚠️ Error connecting to backend!";
    }
}


// -----------------------------
// CSV UPLOAD ANALYSIS
// -----------------------------
async function uploadCSV() {

    const fileInput = document.getElementById("csvFile");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select a CSV file!");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    document.getElementById("result").innerHTML = "⏳ Processing CSV...";

    try {
        const response = await fetch("http://127.0.0.1:8000/upload_csv", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (data.error) {
            document.getElementById("result").innerHTML = "❌ " + data.error;
            return;
        }

        // Update counts
        positiveCount += data.positive;
        negativeCount += data.negative;
        neutralCount += data.neutral;

        updateDashboard();

        // UPDATE TREND GRAPH
        const now = new Date().toLocaleTimeString();

        trendChart.data.labels.push(now);
        trendChart.data.datasets[0].data.push(data.positive);
        trendChart.data.datasets[1].data.push(data.negative);
        trendChart.data.datasets[2].data.push(data.neutral);

        trendChart.update();

        // KEYWORDS
        const keywordsList = document.getElementById("keywords");
        keywordsList.innerHTML = "";

        if (data.keywords) {
            data.keywords.forEach(word => {
                const li = document.createElement("li");
                li.innerText = word;
                keywordsList.appendChild(li);
            });
        }

        // INSIGHTS
        if (data.insight) {
            document.getElementById("insights").innerText = data.insight;
        }

        document.getElementById("result").innerHTML =
            "✅ CSV Analysis Completed!";

    } catch (error) {
        document.getElementById("result").innerHTML =
            "⚠️ Error connecting to backend!";
    }
}


// -----------------------------
// UPDATE DASHBOARD
// -----------------------------
function updateDashboard() {

    document.getElementById("posCount").innerText = positiveCount;
    document.getElementById("negCount").innerText = negativeCount;
    document.getElementById("neuCount").innerText = neutralCount;

    sentimentChart.data.datasets[0].data = [
        positiveCount,
        negativeCount,
        neutralCount
    ];

    sentimentChart.update();
}