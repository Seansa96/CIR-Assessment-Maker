# LAN Server Hosting

This document explains how to securely host the CIR Assessment Maker on a local area network (LAN) for a shared study workspace. 

> [!WARNING]
> V1 is a **shared workspace**. All authorized users share the same attempt history, settings, grade logs, and analytics. It does not provide per-user data isolation.

## 1. Setup

### Network and Hostname
Choose a stable IP address or hostname for your server machine. It is highly recommended to configure a DHCP reservation on your router.

### Configure Access Token
Run the utility script to generate a secure hash for your shared token:
```powershell
.\utility_user_scripts\configure_lan_access.ps1
```
This script will output `CIR_ACCESS_TOKEN_HASH` and `CIR_ACCESS_TOKEN_SALT`. Save these values securely.

### Generate Certificate
Since the shared token is sent over the network, HTTPS is mandatory. You must provide a valid TLS certificate (`.pfx` file) for your LAN server. 
You can use `mkcert` or a local CA. 
1. Create a certificate for your server's LAN IP/hostname.
2. Ensure the CA is trusted on the devices that will connect to the server.
3. Save the `.pfx` file and its password.

## 2. Environment Variables

Before starting the server, configure the following environment variables in your terminal session or server profile:

```powershell
$env:CIR_BIND_URL="https://0.0.0.0:5443"
$env:CIR_PUBLIC_ORIGIN="https://cir-study.lan:5443"
$env:CIR_DATA_ROOT="C:\CIR\data"
$env:CIR_KEY_RING_PATH="C:\CIR\keys"
$env:CIR_ACCESS_TOKEN_HASH="..."
$env:CIR_ACCESS_TOKEN_SALT="..."
$env:CIR_CERTIFICATE_PATH="C:\CIR\certs\cir-study.pfx"
$env:CIR_CERTIFICATE_PASSWORD="..."
```

## 3. Publish and Start

Build the self-contained server package by running:
```powershell
.\utility_user_scripts\publish_lan_server.ps1
```

Once the build completes, start the server:
```powershell
.\utility_user_scripts\start_lan_server.ps1
```

## 4. Connecting

On another device connected to the LAN:
1. Open the browser to `https://<server-ip>:5443`.
2. Enter the shared access token at the login gate.
3. You will be authenticated for 12 hours via a secure cookie.

### Important Notes
- **Active Attempts**: In-progress attempts are volatile and reside in process memory. Use the "Save and Quit" action to commit progress to SQLite before restarting the server.
- **Firewall**: Ensure the Windows Defender Firewall is configured to allow inbound TCP traffic on port `5443` (Private Network profile only). Do not expose this port to the internet.
