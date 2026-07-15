using Microsoft.AspNetCore.SignalR;

namespace QuizApp.Api.Hubs;

public class DiagnosticHub : Hub
{
    public async Task StartSandbox(string attemptId)
    {
        await Clients.Caller.SendAsync("ReceiveOutput", Convert.ToBase64String(System.Text.Encoding.UTF8.GetBytes("Connected to Diagnostic Echo Hub!\r\n")));
    }

    public async Task SendInput(string base64Data)
    {
        // Immediately echo back
        await Clients.Caller.SendAsync("ReceiveOutput", base64Data);
    }
}
