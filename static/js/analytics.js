// Creating the Difficulty Chart
console.log("analytics.js is loaded.");

const ctx = document.getElementById('difficultyChart').getContext('2d');
const scoresData = JSON.parse(document.getElementById('scoresData').textContent);

// Debugging Statement
console.log('Scores Data:', scoresData);

// Gathering Statistics
const labels = scoresData.map(data => data.difficulty.charAt(0).toUpperCase() + data.difficulty.slice(1)); // Capitalizing first letter of difficulty
const totalQuizzes = scoresData.map(data => data.total_quizzes);
const totalScores = scoresData.map(data => data.total_score);
const averageScores = scoresData.map(data => data.average_score);

// Debugging Statements
console.log('Labels:', labels);
console.log('Total Quizzes:', totalQuizzes);
console.log('Total Scores:', totalScores);
console.log('Average Scores:', averageScores);


// Creating Chart
new Chart(ctx, {
    type: 'bar',
    data: {
        labels: labels,
        datasets: [
            {
                label: 'Total Quizzes',
                data: totalQuizzes,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            },
            {
                label: 'Total Scores',
                data: totalScores,
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            },
            {
                label: 'Average Scores',
                data: averageScores,
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }
        ]
    },
    options: {
        responsive: true,
        plugins: {
            legend: { position: 'top' }
        },
        scales: {
            y: { beginAtZero: true }
        }
    }
});


// Creating the Performance Chart
const performanceCtx = document.getElementById('performanceChart').getContext('2d');
const performanceData = JSON.parse(document.getElementById('performanceData').textContent);
const maxQuizzes = JSON.parse(document.getElementById('maxQuizzes').textContent);

// Debugging statements
console.log('Performance Data:', performanceData);
console.log('Max Quizzes:', maxQuizzes);

// Prepare quiz labels for Quiz numbers
const quizLabels = Array.from({ length: maxQuizzes }, (_, i) => `Quiz #${i}`);
console.log('Quiz Labels:', quizLabels);

// Declare difficulty options
const difficulties = ['easy', 'medium', 'hard'];

// Creating datasets for difficulty
const datasets = difficulties.map(difficulty => ({
    label: difficulty.charAt(0).toUpperCase() + difficulty.slice(1),
    data: performanceData[difficulty],
    borderColor: difficulty === 'easy' ? 'rgba(75, 192, 192, 1)' :
                 difficulty === 'medium' ? 'rgba(255, 159, 64, 1)' : 'rgba(153, 102, 255, 1)', // Handling bordercolor options for difficulty
    backgroundColor: difficulty === 'easy' ? 'rgba(75, 192, 192, 0.2)' :
                     difficulty === 'medium' ? 'rgba(255, 159, 64, 0.2)' : 'rgba(153, 102, 255, 0.2)', // Handling backgroundcolor options for difficulty
    spanGaps: true,
    fill: true
}));

// Rendering line chart
new Chart(performanceCtx, {
    type: 'line',
    data: {
        labels: quizLabels,
        datasets: datasets
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
        },
        scales: {
            x: { title: { display: true, text: 'Quiz Number' } },
            y: { title: { display: true, text: 'Score' }, beginAtZero: true }
        }
    }
});
