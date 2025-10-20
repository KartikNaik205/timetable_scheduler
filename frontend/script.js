const subjects = [];
const apiBase = "http://127.0.0.1:8000";

document.getElementById("subjectForm").addEventListener("submit", (e) => {
    e.preventDefault();
    const name = document.getElementById("subjectName").value.trim();
    const avg = document.getElementById("subjectAverage").value.trim();

    if (name && avg) {
        subjects.push({ name, average: avg });
        displaySubjects();
        e.target.reset();
    }
});

function displaySubjects() {
    const list = document.getElementById("subjectsList");
    list.innerHTML = subjects
        .map(
            (s, i) => `
        <div class="subject-item">
            <strong>${s.name}</strong> — ${s.average}%
            <button onclick="removeSubject(${i})">❌</button>
        </div>`
        )
        .join("");
}

function removeSubject(index) {
    subjects.splice(index, 1);
    displaySubjects();
}

document.getElementById("generateBtn").addEventListener("click", async () => {
    if (subjects.length === 0) {
        alert("Add at least one subject first!");
        return;
    }

    try {
        const response = await fetch(`${apiBase}/generate_timetable`);
        const data = await response.json();

        if (data.timetable) displayTimetable(data.timetable);
        else alert("No timetable generated");
    } catch (err) {
        console.error(err);
        alert("Error connecting to FastAPI backend");
    }
});

function displayTimetable(timetable) {
    const timetableDiv = document.getElementById("timetable");
    timetableDiv.innerHTML = "";

    for (const [day, sessions] of Object.entries(timetable)) {
        let tableHTML = `
            <div class="timetable-day">${day}</div>
            <table class="timetable-table">
                <tr><th>Time</th><th>Subject</th></tr>
                ${sessions
                    .map(
                        (s) => `<tr><td>${s.time}</td><td>${s.subject}</td></tr>`
                    )
                    .join("")}
            </table>
        `;
        timetableDiv.innerHTML += tableHTML;
    }
}
