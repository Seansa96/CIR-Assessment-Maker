import { Terminal } from 'xterm';
import { FitAddon } from '@xterm/addon-fit';
import * as signalR from '@microsoft/signalr';
import 'xterm/css/xterm.css';

export class SandboxTerminal {
    private terminal: Terminal;
    private fitAddon: FitAddon;
    private connection: signalR.HubConnection;
    private resizeHandler: () => void;
    private resizeObserver: ResizeObserver | null = null;
    private readyForInput = false;
    private warnedInputNotReady = false;

    constructor(
        private containerElement: HTMLElement,
        private attemptId: string,
        private onCompleted: (attemptId: string) => void,
        hubUrl: string = "http://localhost:5000/sandbox-hub"
    ) {
        this.terminal = new Terminal({
            cursorBlink: true,
            // Do NOT set convertEol: true — it interferes with raw PTY control sequences
            theme: {
                background: '#1e1e1e',
                foreground: '#cccccc'
            }
        });
        this.terminal.attachCustomKeyEventHandler((event) => {
            if (event.type === "keydown" && event.ctrlKey && event.key.toLowerCase() === "l") {
                this.terminal.clear();
            }

            return true;
        });

        this.fitAddon = new FitAddon();
        this.terminal.loadAddon(this.fitAddon);

        this.resizeHandler = () => {
            this.fitAddon.fit();
            this.sendResize();
        };
        
        this.connection = new signalR.HubConnectionBuilder()
            .withUrl(hubUrl, { transport: signalR.HttpTransportType.WebSockets })
            .withAutomaticReconnect()
            .build();

        this.connection.onreconnecting((error) => {
            this.readyForInput = false;
            const msg = error?.message ?? "connection lost";
            this.terminal.writeln(`\x1b[33m\r\n[reconnecting] Sandbox connection interrupted: ${msg}\x1b[0m`);
        });

        this.connection.onreconnected(() => {
            this.readyForInput = false;
            this.terminal.writeln("\x1b[33m\r\n[reconnected] Sandbox connection recovered; waiting for sandbox readiness.\x1b[0m");
        });

        this.connection.onclose((error) => {
            this.readyForInput = false;
            const msg = error?.message ?? "connection closed";
            this.terminal.writeln(`\x1b[31m\r\n[closed] Sandbox connection closed: ${msg}\x1b[0m`);
        });
    }

    private sendResize() {
        if (this.connection.state === signalR.HubConnectionState.Connected) {
            const cols = this.terminal.cols;
            const rows = this.terminal.rows;
            this.connection.invoke("ResizeTerminal", cols, rows).catch(() => {});
        }
    }

    public async mount() {
        this.terminal.open(this.containerElement);
        this.fitAddon.fit();

        // Handle terminal resize via window resize
        window.addEventListener('resize', this.resizeHandler);
        this.containerElement.addEventListener('click', () => this.terminal.focus());

        // Also observe the container element itself for size changes
        this.resizeObserver = new ResizeObserver(() => {
            this.fitAddon.fit();
            this.sendResize();
        });
        this.resizeObserver.observe(this.containerElement);

        // Connect to SignalR
        this.connection.on("ReceiveOutput", (base64Data: string) => {
            const binary_string = atob(base64Data);
            const len = binary_string.length;
            const bytes = new Uint8Array(len);
            for (let i = 0; i < len; i++) {
                bytes[i] = binary_string.charCodeAt(i);
            }
            this.terminal.write(bytes);
        });

        this.connection.on("Error", (error: string) => {
            this.terminal.writeln(`\x1b[31m\r\nError: ${error}\x1b[0m`);
        });

        this.connection.on("SandboxStatus", (phase: string, message: string) => {
            this.terminal.writeln(`\x1b[90m[${phase}] ${message}\x1b[0m`);
        });

        this.connection.on("SandboxReady", () => {
            this.readyForInput = true;
            this.warnedInputNotReady = false;
            this.terminal.writeln("\x1b[32m[ready] Sandbox terminal is ready for input.\x1b[0m");
            this.fitAddon.fit();
            this.sendResize();
            this.terminal.focus();
        });

        this.connection.on("SandboxFailed", (phase: string, message: string) => {
            this.readyForInput = false;
            this.terminal.writeln(`\x1b[31m[${phase}] Sandbox failed: ${message}\x1b[0m`);
        });

        this.terminal.onData((data) => {
            if (!this.readyForInput) {
                if (!this.warnedInputNotReady) {
                    this.terminal.writeln("\x1b[33m\r\n[waiting] Sandbox is still starting; input is not ready yet.\x1b[0m");
                    this.warnedInputNotReady = true;
                }
                return;
            }

            if (this.connection.state === signalR.HubConnectionState.Connected) {
                const encoder = new TextEncoder();
                const bytes = encoder.encode(data);
                let binary = '';
                for (let i = 0; i < bytes.byteLength; i++) {
                    binary += String.fromCharCode(bytes[i]);
                }
                const base64 = btoa(binary);
                this.connection.invoke("SendInput", base64).catch((err: any) => {
                    const msg = err?.message ?? String(err);
                    this.terminal.writeln(`\x1b[31m\r\n[input] Failed to send input: ${msg}\x1b[0m`);
                });
            } else {
                this.terminal.writeln(`\x1b[31m\r\n[input] SignalR is ${this.connection.state}; input was not sent.\x1b[0m`);
            }
        });

        // Also send resize events reported by xterm itself (e.g. fitAddon triggers)
        this.terminal.onResize(({ cols, rows }) => {
            if (this.connection.state === signalR.HubConnectionState.Connected) {
                this.connection.invoke("ResizeTerminal", cols, rows).catch(() => {});
            }
        });

        this.connection.on("SandboxCompleted", (completedAttemptId: string) => {
            this.terminal.writeln(`\x1b[32m\r\nSandbox completed successfully!\x1b[0m`);
            this.onCompleted(completedAttemptId);
        });

        try {
            await this.connection.start();
            this.terminal.writeln("\x1b[90mConnecting sandbox...\x1b[0m");
            const cols = this.terminal.cols;
            const rows = this.terminal.rows;
            await this.connection.invoke("StartSandbox", this.attemptId, cols, rows);
            this.terminal.focus();
        } catch (err: any) {
            console.error("SignalR Connection Error: ", err);
            const msg = err?.message ?? String(err);
            this.terminal.writeln(`\x1b[31m\r\nFailed to connect: ${msg}\x1b[0m`);
        }
    }

    public dispose() {
        window.removeEventListener('resize', this.resizeHandler);
        this.resizeObserver?.disconnect();
        void this.connection.stop();
        this.terminal.dispose();
    }
}
