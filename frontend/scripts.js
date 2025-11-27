const analyzeBtn = document.getElementById('analyzeBtn');
const tasksInput = document.getElementById('tasksInput');
const results = document.getElementById('results');
const messageDiv = document.getElementById('message');
const strategySelect = document.getElementById('strategy');

// Helper: Assign color based on score
function getPriorityClass(score) {
    if (score >= 100) return 'high';
    if (score >= 50) return 'medium';
    return 'low';
}

// Helper: Create table row
function createRow(rank, task) {
    const tr = document.createElement('tr');
    tr.className = getPriorityClass(task.score);
    tr.innerHTML = `
        <td>${rank}</td>
        <td>${task.title}</td>
        <td>${task.due_date || '-'}</td>
        <td>${task.estimated_hours}</td>
        <td>${task.importance}</td>
        <td>${task.dependencies.join(', ') || '-'}</td>
        <td>${task.score}</td>
        <td>${task.explanation}</td>
    `;
    return tr;
}

// Render circular dependency graph using vis-network
function renderDependencyGraph(tasks, cycles) {
    const nodes = tasks.map(task => ({
        id: task.id,
        label: task.title,
        color: cycles.some(c => c.includes(task.id)) ? 'red' : 'lightblue'
    }));

    const edges = [];
    tasks.forEach(task => {
        task.dependencies.forEach(dep => {
            edges.push({ from: task.id, to: dep });
        });
    });

    const container = document.getElementById('dependencyGraph');
    const data = { nodes, edges };
    const options = {
        layout: { hierarchical: true },
        edges: { arrows: 'to' },
        physics: false
    };
    new vis.Network(container, data, options);
}

// Fetch circular dependencies from backend
async function fetchCycles(tasks) {
    try {
        const response = await fetch('http://127.0.0.1:8000/api/tasks/cycles/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(tasks)
        });
        const data = await response.json();
        renderDependencyGraph(tasks, data.cycles);

        if (data.cycles.length > 0) {
            messageDiv.textContent = `⚠ Circular dependencies detected: ${JSON.stringify(data.cycles)}`;
        }
    } catch (error) {
        console.error('Error fetching cycles:', error);
    }
}

// Main analyze button click
analyzeBtn.addEventListener('click', async () => {
    messageDiv.textContent = '';
    results.innerHTML = '';

    let tasks;
    try {
        tasks = JSON.parse(tasksInput.value);
        if (!Array.isArray(tasks)) throw new Error('Input must be a JSON array');
    } catch (err) {
        messageDiv.textContent = 'Invalid JSON: ' + err.message;
        return;
    }

    const payload = {
        tasks: tasks,
        strategy: strategySelect.value
    };

    try {
        // Call analyze API
        const response = await fetch('http://127.0.0.1:8000/api/tasks/analyze/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const errorData = await response.json();
            messageDiv.textContent = 'Error: ' + (errorData.error || JSON.stringify(errorData));
            return;
        }

        const data = await response.json();

        // Sort tasks by score descending
        data.sort((a, b) => b.score - a.score);

        // Display full task list in table
        data.forEach((task, index) => {
            results.appendChild(createRow(index + 1, task));
        });

        // Display top 3 suggestions
        const top3 = data.slice(0, 3);
        let top3Div = document.getElementById('top3');
        if (!top3Div) {
            top3Div = document.createElement('div');
            top3Div.id = 'top3';
            top3Div.style.marginTop = '20px';
            document.querySelector('.container').appendChild(top3Div);
        }
        top3Div.innerHTML = `<h2>Top 3 Tasks You Should Work On Today</h2>`;
        top3.forEach((task, index) => {
            const p = document.createElement('p');
            p.innerHTML = `<strong>${index + 1}. ${task.title}</strong> (Priority Score: ${task.score}) - ${task.explanation}`;
            top3Div.appendChild(p);
        });

        // Fetch and render circular dependency graph
        fetchCycles(tasks);

    } catch (err) {
        messageDiv.textContent = 'Network or server error: ' + err.message;
    }
});
