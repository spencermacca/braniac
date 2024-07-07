const minValSlider = document.getElementById("minVal");
const maxValSlider = document.getElementById("maxVal");
const minValOutput = document.getElementById("minValOutput");
const maxValOutput = document.getElementById("maxValOutput");

minValSlider.oninput = function() {
    minValOutput.innerText = this.value;
}
maxValSlider.oninput = function() {
    maxValOutput.innerText = this.value;
}

document.getElementById("paramsForm").onsubmit = function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    fetch("/update_params", {
        method: "POST",
        body: formData
    }).then(response => {
        if (!response.ok) {
            alert("Failed to update parameters");
        }
    });
}

document.getElementById("emotionForm").onsubmit = function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    fetch("/process_emotion", {
        method: "POST",
        body: formData
    }).then(response => response.json()).then(data => {
        document.getElementById("emotionResponse").innerText = data.response;
    }).catch(error => {
        alert("Failed to process emotion");
        console.error(error);
    });
}

const eventSource = new EventSource('/audio_feed');
eventSource.onmessage = function(event) {
    const audioData = JSON.parse(event.data);
    const canvas = document.getElementById('audioCanvas');
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.beginPath();
    ctx.moveTo(0, canvas.height / 2);
    audioData.forEach((value, index) => {
        const x = index * canvas.width / audioData.length;
        const y = (canvas.height / 2) + (value / 128.0 * canvas.height / 2);
        ctx.lineTo(x, y);
    });
    ctx.stroke();
}

function startBrain() {
    fetch("/start_brain", { method: "POST" }).then(response => {
        if (!response.ok) {
            alert("Failed to start brain");
        }
    });
}

function stopBrain() {
    fetch("/stop_brain", { method: "POST" }).then(response => {
        if (!response.ok) {
            alert("Failed to stop brain");
        }
    });
}

setInterval(() => {
    fetch("/latest_decision", { method: "GET" }).then(response => response.json()).then(data => {
        document.getElementById("latestDecision").innerText = data.decision;
    }).catch(error => {
        console.error(error);
    });
}, 1000);
