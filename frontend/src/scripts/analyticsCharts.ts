import Chart from 'chart.js/auto';

export interface CategoryGradeAnalytics {
    categoryId: string;
    categoryTitle: string;
    attemptCount: number;
    averagePercent: number;
    lastPercent?: number;
}

export interface QuestionTypePerformance {
    questionType: string;
    answeredCount: number;
    correctCount: number;
    needsReviewCount: number;
    correctPercent: number;
}

export interface IssueSignalPerformance {
    signalId: string;
    triggerCount: number;
    urgencyScore: number;
    categoryId?: string;
    topicId?: string;
    skillIds: string[];
}

export interface GradeLogEntry {
    attemptId: string;
    assessmentId: string;
    assessmentTitle: string;
    mode: string;
    correctCount: number;
    totalQuestions: number;
    percentScore: number;
    committedAt: string;
}

// Keep track of chart instances to destroy them before re-rendering
const chartInstances: { [canvasId: string]: Chart } = {};

function getChartContext(id: string): CanvasRenderingContext2D | null {
    const canvas = document.getElementById(id) as HTMLCanvasElement;
    return canvas ? canvas.getContext('2d') : null;
}

function destroyChart(id: string) {
    if (chartInstances[id]) {
        chartInstances[id].destroy();
        delete chartInstances[id];
    }
}

export function renderScoresOverTimeChart(canvasId: string, entries: GradeLogEntry[]) {
    destroyChart(canvasId);
    const ctx = getChartContext(canvasId);
    if (!ctx) return;

    if (entries.length === 0) return;

    const sorted = [...entries].sort((a, b) => new Date(a.committedAt).getTime() - new Date(b.committedAt).getTime());
    const labels = sorted.map(e => new Date(e.committedAt).toLocaleDateString());
    const data = sorted.map(e => e.percentScore);

    chartInstances[canvasId] = new Chart(ctx, {
        type: 'line',
        data: {
            labels,
            datasets: [{
                label: 'Committed Score (%)',
                data,
                borderColor: '#10b981',
                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                fill: true,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { min: 0, max: 100 }
            }
        }
    });
}

export function renderCategoryMasteryChart(canvasId: string, categories: CategoryGradeAnalytics[]) {
    destroyChart(canvasId);
    const ctx = getChartContext(canvasId);
    if (!ctx) return;

    if (categories.length === 0) return;

    const labels = categories.map(c => c.categoryTitle);
    const data = categories.map(c => c.averagePercent);

    chartInstances[canvasId] = new Chart(ctx, {
        type: 'radar',
        data: {
            labels,
            datasets: [{
                label: 'Average Score (%)',
                data,
                borderColor: '#6366f1',
                backgroundColor: 'rgba(99, 102, 241, 0.2)',
                pointBackgroundColor: '#6366f1'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    angleLines: { display: true },
                    suggestedMin: 0,
                    suggestedMax: 100
                }
            }
        }
    });
}

export function renderTopIssueSignalsChart(canvasId: string, signals: IssueSignalPerformance[]) {
    destroyChart(canvasId);
    const ctx = getChartContext(canvasId);
    if (!ctx) return;

    if (!signals || signals.length === 0) return;

    const topSignals = signals.slice(0, 8);
    const labels = topSignals.map(s => s.signalId);
    const data = topSignals.map(s => s.triggerCount);

    chartInstances[canvasId] = new Chart(ctx, {
        type: 'bar',
        data: {
            labels,
            datasets: [{
                label: 'Triggers (Frequency)',
                data,
                backgroundColor: '#ef4444',
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
        }
    });
}

export function renderQuestionTypeChart(canvasId: string, questionTypes: QuestionTypePerformance[]) {
    destroyChart(canvasId);
    const ctx = getChartContext(canvasId);
    if (!ctx) return;

    if (questionTypes.length === 0) return;

    const labels = questionTypes.map(q => q.questionType);
    const data = questionTypes.map(q => q.answeredCount);

    chartInstances[canvasId] = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels,
            datasets: [{
                data,
                backgroundColor: [
                    '#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899', '#64748b'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'right' }
            }
        }
    });
}
