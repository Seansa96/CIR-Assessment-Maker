import * as signalR from '@microsoft/signalr';

export function initializeHotReload(hubUrl: string) {
    const connection = new signalR.HubConnectionBuilder()
        .withUrl(hubUrl, { transport: signalR.HttpTransportType.WebSockets })
        .withAutomaticReconnect()
        .build();

    connection.on("AssessmentUpdated", (data) => {
        console.log(`[HotReload] AssessmentUpdated: ${data.assessmentId} (${data.path}). Reloading...`);
        // Simple page reload to reflect new data
        window.location.reload();
    });

    connection.on("AssessmentDeleted", (path) => {
        console.log(`[HotReload] AssessmentDeleted: ${path}. Reloading...`);
        window.location.reload();
    });

    connection.on("AssessmentError", (data) => {
        console.error(`[HotReload] Validation error for ${data.path}:`, data.error);
        // We do not reload the page on error so the user doesn't lose their state and can read the console/diagnostics.
    });

    connection.start().then(() => {
        console.log("[HotReload] Connected to DiagnosticHub for real-time updates.");
    }).catch(err => {
        console.error("[HotReload] Error connecting to DiagnosticHub:", err);
    });
}
