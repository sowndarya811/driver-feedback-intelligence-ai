// frontend/script.js

let positiveCount = 0;
let negativeCount = 0;
let neutralCount = 0;
let totalReviews = 0;

let bestReview = "";
let worstReview = "";

/* PIE CHART */

const pieChart = new Chart(
    document.getElementById("pieChart"),
    {
        type: "pie",
        data: {
            labels: [
                "Positive",
                "Negative",
                "Neutral"
            ],
            datasets: [{
                data: [0, 0, 0]
            }]
        }
    }
);

/* LINE CHART */

const lineChart = new Chart(
    document.getElementById("lineChart"),
    {
        type: "line",
        data: {
            labels: [],
            datasets: [{
                label: "Confidence %",
                data: []
            }]
        }
    }
);

/* THEME */

function toggleTheme() {

    document.body.classList.toggle(
        "light"
    );
}

/* ANALYZE */

async function analyzeSentiment() {

    const review =
        document.getElementById(
            "reviewInput"
        ).value;

    if (!review.trim()) {

        alert(
            "Please enter a review"
        );

        return;
    }

    document.getElementById(
        "loadingText"
    ).innerText = "Analyzing...";

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/predict",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    text: review
                })
            }
        );

        const data =
            await response.json();

        document.getElementById(
            "loadingText"
        ).innerText = "";

        document.getElementById(
            "sentimentText"
        ).innerText =
            data.sentiment;

        document.getElementById(
            "confidenceText"
        ).innerText =
            "Confidence: " +
            (data.confidence * 100)
            .toFixed(2) + "%";

        document.getElementById(
            "meterFill"
        ).style.width =
            (data.confidence * 100) + "%";

        let emoji = "😐";

        if (
            data.sentiment ===
            "Positive"
        ) {

            emoji = "😊";

            positiveCount++;

            bestReview = review;

            confetti({
                particleCount: 100,
                spread: 70,
                origin: { y: 0.6 }
            });

            document.getElementById(
                "positiveCountText"
            ).innerText =
                positiveCount;
        }

        else if (
            data.sentiment ===
            "Negative"
        ) {

            emoji = "😡";

            negativeCount++;

            worstReview = review;

            document.getElementById(
                "negativeCountText"
            ).innerText =
                negativeCount;
        }

        else {

            neutralCount++;

            document.getElementById(
                "neutralCountText"
            ).innerText =
                neutralCount;
        }

        document.getElementById(
            "emoji"
        ).innerText = emoji;

        const resultBox =
            document.getElementById(
                "resultBox"
            );

        if (
            data.sentiment ===
            "Positive"
        ) {

            resultBox.style.background =
                "rgba(34,197,94,0.2)";
        }

        else if (
            data.sentiment ===
            "Negative"
        ) {

            resultBox.style.background =
                "rgba(239,68,68,0.2)";
        }

        else {

            resultBox.style.background =
                "rgba(148,163,184,0.2)";
        }

        let insight = "";

        if (
            data.sentiment ===
            "Positive"
        ) {

            insight =
                "Users are highly satisfied with the service.";
        }

        else if (
            data.sentiment ===
            "Negative"
        ) {

            insight =
                "Users are facing issues with the service.";
        }

        else {

            insight =
                "Users have mixed opinions.";
        }

        document.getElementById(
            "aiInsight"
        ).innerText = insight;

        updateCharts(
            data.confidence
        );

        const historyItem =
            `${review} → ${data.sentiment}`;

        const li =
            document.createElement("li");

        li.innerText =
            historyItem;

        document.getElementById(
            "historyList"
        ).appendChild(li);

        let history =
            JSON.parse(
                localStorage.getItem(
                    "sentimentHistory"
                )
            ) || [];

        history.push(historyItem);

        localStorage.setItem(
            "sentimentHistory",
            JSON.stringify(history)
        );

        totalReviews++;

        document.getElementById(
            "reviewCount"
        ).innerText =
            totalReviews;

        /* PERCENTAGES */

        const positivePercent =
        (
            positiveCount /
            totalReviews
        ) * 100;

        const negativePercent =
        (
            negativeCount /
            totalReviews
        ) * 100;

        const neutralPercent =
        (
            neutralCount /
            totalReviews
        ) * 100;

        document.getElementById(
            "positivePercent"
        ).innerText =
            positivePercent.toFixed(1) + "%";

        document.getElementById(
            "negativePercent"
        ).innerText =
            negativePercent.toFixed(1) + "%";

        document.getElementById(
            "neutralPercent"
        ).innerText =
            neutralPercent.toFixed(1) + "%";

        /* SMART SUMMARY */

        document.getElementById(
            "smartSummary"
        ).innerText =

`Best Review:
${bestReview || "No positive review yet"}

Worst Review:
${worstReview || "No negative review yet"}`;

        document.getElementById(
            "resultBox"
        ).scrollIntoView({

            behavior: "smooth"
        });

    }

    catch (error) {

        console.log(error);

        alert(
            "Backend connection error"
        );
    }
}

/* UPDATE CHARTS */

function updateCharts(confidence) {

    pieChart.data.datasets[0].data = [

        positiveCount,

        negativeCount,

        neutralCount
    ];

    pieChart.update();

    lineChart.data.labels.push(

        lineChart.data.labels.length + 1
    );

    lineChart.data.datasets[0].data.push(

        (confidence * 100)
        .toFixed(2)
    );

    lineChart.update();
}

/* VOICE */

function startVoice() {

    const SpeechRecognition =

        window.SpeechRecognition ||

        window.webkitSpeechRecognition;

    if (!SpeechRecognition) {

        alert(
            "Voice recognition not supported"
        );

        return;
    }

    const recognition =
        new SpeechRecognition();

    recognition.lang = "en-US";

    recognition.start();

    recognition.onresult =
        function (event) {

            const transcript =

                event.results[0][0]
                .transcript;

            document.getElementById(
                "reviewInput"
            ).value = transcript;
        };
}

/* DOWNLOAD REPORT */

function downloadReport() {

    const review =
        document.getElementById(
            "reviewInput"
        ).value;

    const sentiment =
        document.getElementById(
            "sentimentText"
        ).innerText;

    const confidence =
        document.getElementById(
            "confidenceText"
        ).innerText;

    if (
        review.trim() === "" ||
        sentiment.trim() === ""
    ) {

        alert(
            "Please analyze review first"
        );

        return;
    }

    const reportText =

`
DRIVER FEEDBACK REPORT

Review:
${review}

Sentiment:
${sentiment}

${confidence}

AI Insight:
${document.getElementById("aiInsight").innerText}
`;

    const blob =
        new Blob(
            [reportText],
            {
                type:
                "text/plain"
            }
        );

    const url =
        URL.createObjectURL(blob);

    const a =
        document.createElement("a");

    a.href = url;

    a.download =
        "AI_Report.txt";

    a.click();
}

/* EXPORT CSV */

function exportCSV() {

    let csvContent =
        "Review,Sentiment\n";

    const historyItems =
        document.querySelectorAll(
            "#historyList li"
        );

    historyItems.forEach(item => {

        const row =
            item.innerText
            .replace(" → ", ",");

        csvContent += row + "\n";
    });

    const blob =
        new Blob(
            [csvContent],
            {
                type: "text/csv"
            }
        );

    const url =
        URL.createObjectURL(blob);

    const a =
        document.createElement("a");

    a.href = url;

    a.download =
        "Sentiment_History.csv";

    a.click();
}

/* CLEAR */

function clearAll() {

    document.getElementById(
        "reviewInput"
    ).value = "";

    document.getElementById(
        "sentimentText"
    ).innerText = "";

    document.getElementById(
        "confidenceText"
    ).innerText = "";

    document.getElementById(
        "emoji"
    ).innerText = "😊";

    document.getElementById(
        "meterFill"
    ).style.width = "0%";

    document.getElementById(
        "aiInsight"
    ).innerText =
        "Waiting for analysis...";
}

/* DATE TIME */

setInterval(() => {

    const now = new Date();

    document.getElementById(
        "dateTime"
    ).innerText =
        now.toLocaleString();

}, 1000);

/* TYPING EFFECT */

const titleText =
"Driver Feedback Intelligence AI";

let i = 0;

function typingEffect() {

    if (
        i < titleText.length
    ) {

        document.getElementById(
            "typingTitle"
        ).innerHTML +=
            titleText.charAt(i);

        i++;

        setTimeout(
            typingEffect,
            100
        );
    }
}

typingEffect();

/* LOAD HISTORY */

window.onload = function () {

    const history =
        JSON.parse(
            localStorage.getItem(
                "sentimentHistory"
            )
        ) || [];

    history.forEach(item => {

        const li =
            document.createElement("li");

        li.innerText = item;

        document.getElementById(
            "historyList"
        ).appendChild(li);
    });
};