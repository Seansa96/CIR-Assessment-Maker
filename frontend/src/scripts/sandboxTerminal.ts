import { Terminal } from 'xterm';
import { FitAddon } from '@xterm/addon-fit';
import * as signalR from '@microsoft/signalr';
import 'xterm/css/xterm.css';

export class SandboxTerminal {
    private terminal: Terminal;
    private fitAddon: FitAddon;
    private connection: signalR.HubConnection;

    constructor(
        private containerElement: HTMLElement,
        private attemptId: string,
        private onCompleted: (attemptId: string) => void
    ) {
        this.terminal = new Terminal({
            cursorBlink: true,
            theme: {
                background: '#1e1e1e',
                foreground: '#cccccc'
            }
        });
        
        this.fitAddon = new FitAddon();
        this.terminal.loadAddon(this.fitAddon);
        
        this.connection = new signalR.HubConnectionBuilder()
            .withUrl("http://localhost:5000/sandbox-hub")
            .withAutomaticReconnect()
            .build();
    }

    public async mount() {
        this.terminal.open(this.containerElement);
        this.fitAddon.fit();

        // Handle terminal resize
        window.addEventListener('resize', () => this.fitAddon.fit());

        // Connect to SignalR
        this.connection.on("ReceiveOutput", (base64Data: string) => {
            const bytes = Uint8Array.from(atob(base64Data), c => c.charCodeAt(0));
            this.terminal.write(bytes);
        });

        this.connection.on("Error", (error: string) => {
            this.terminal.writeln(`\x1b[31m\r\nError: ${error}\x1b[0m`);
        });

        this.terminal.onData((data) => {
            if (this.connection.state === signalR.HubConnectionState.Connected) {
                const base64 = btoa(unescape(encodeURIComponent(data)));
                this.connection.invoke("SendInput", base64);
            }
        });

        this.connection.on("SandboxCompleted", (completedAttemptId: string) => {
            this.terminal.writeln(`\x1b[32m\r\nSandbox completed successfully!\x1b[0m`);
            this.onCompleted(completedAttemptId);
        });

        try {
            await this.connection.start();
            await this.connection.invoke("StartSandbox", this.attemptId);
        } catch (err) {
            console.error("SignalR Connection Error: ", err);
            this.terminal.writeln("\x1b[31m\r\nFailed to connect to the sandbox server.\x1b[0m");
        }
    }

    public dispose() {
        this.connection.stop();
        this.terminal.dispose();
    }
}
