import sys

file_path = 'c:/Users/SeanS/Downloads/cir_app/frontend/src/pages/index.astro'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace renderAnalyticsDashboard in loadGrades
content = content.replace(
    '        gradeSummary.innerHTML = renderAnalyticsDashboard(analytics, summary.entries);',
    '        updateAnalyticsDashboard();'
)

# Replace renderAnalyticsDashboard in setupGradeLogInteractions
content = content.replace(
    '              gradeSummary.innerHTML = renderAnalyticsDashboard(state.analytics, state.gradeLogEntries);',
    '              updateAnalyticsDashboard();'
)

# Define updateAnalyticsDashboard at the end of renderAnalyticsDashboard
old_return = '        return `\n          <div class="grade-log-full-width">'
new_return = '''      function updateAnalyticsDashboard() {
        if (!state.analytics) return;
        gradeSummary.innerHTML = renderAnalyticsDashboard(state.analytics, state.gradeLogEntries);
        
        if (state.activeAnalyticsCategory === null) {
          renderScoresOverTimeChart("chart-scores-over-time", state.gradeLogEntries);
          renderCategoryMasteryChart("chart-category-mastery", state.analytics.categories);
          renderTopIssueSignalsChart("chart-issue-signals", state.analytics.issueSignals || []);
          renderQuestionTypeChart("chart-question-types", state.analytics.questionTypes);
        }
      }

        return `
          <div class="grade-log-full-width">'''

content = content.replace(old_return, new_return)

# Update the HTML block in renderAnalyticsDashboard
old_html = '''                  <div class="analytics-table-grid">
                    ${renderCategoryAnalyticsTable(analytics.categories)}
                    ${renderQuestionTypeAnalyticsTable(analytics.questionTypes)}
                  </div>
                  <details class="grade-ledger-details" style="margin-top: 2rem;">
                    <summary>View Raw Grade Ledger</summary>
                    ${renderCommittedEntries(entries)}
                  </details>'''

new_html = '''                  <div class="analytics-charts-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 2rem;">
                    <div class="chart-container" style="position: relative; height: 250px; background: var(--surface); padding: 1rem; border-radius: var(--radius-md); border: 1px solid var(--border);">
                        <canvas id="chart-scores-over-time"></canvas>
                    </div>
                    <div class="chart-container" style="position: relative; height: 250px; background: var(--surface); padding: 1rem; border-radius: var(--radius-md); border: 1px solid var(--border);">
                        <canvas id="chart-category-mastery"></canvas>
                    </div>
                    <div class="chart-container" style="position: relative; height: 250px; background: var(--surface); padding: 1rem; border-radius: var(--radius-md); border: 1px solid var(--border);">
                        <canvas id="chart-issue-signals"></canvas>
                    </div>
                    <div class="chart-container" style="position: relative; height: 250px; background: var(--surface); padding: 1rem; border-radius: var(--radius-md); border: 1px solid var(--border);">
                        <canvas id="chart-question-types"></canvas>
                    </div>
                  </div>

                  <details class="grade-ledger-details" style="margin-top: 2rem;">
                    <summary>View Category Data</summary>
                    <div class="analytics-table-grid">
                      ${renderCategoryAnalyticsTable(analytics.categories)}
                    </div>
                  </details>
                  
                  <details class="grade-ledger-details" style="margin-top: 1rem;">
                    <summary>View Question Type Data</summary>
                    <div class="analytics-table-grid">
                      ${renderQuestionTypeAnalyticsTable(analytics.questionTypes)}
                    </div>
                  </details>

                  <details class="grade-ledger-details" style="margin-top: 1rem;">
                    <summary>View Raw Grade Ledger</summary>
                    ${renderCommittedEntries(entries)}
                  </details>'''

content = content.replace(old_html, new_html)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Success')
