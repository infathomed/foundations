# Nmap Scans: Foundational + Repeatable (Infathomed)

This document captures a repeatable Nmap workflow that mirrors real-world SOC / analyst practice:
**discover hosts → enumerate ports → identify services → fingerprint OS → run safe scripts → export results**.

> Tip: Always scan only networks/systems you own or have explicit permission to test.

---

## 0) Quick Reference (Most-Used Commands)

### Host discovery (subnet)
nmap -sn 192.168.1.0/24
### Fast Ports     (Top~100)
nmap -F 192.168.1.10
###  Default Ports (Top 1000)
nmap 192.168.1.10
### Full TCP ports (1-65535)
nmap -p- 192.168.1.10
### Service/Version detection
nmap -sV 192.168.1.10
### OS detection (run terminal as admin/root)
nmap -O 192.168.1.10
### "Good coverage" scan (common for labs)
nmap -sS -sV -O 192.168.1.10
### Save results (recommended)
nmap -sS -sV -O 192.168.1.10 -oA outputs/host1
### Host Discovery (Who is alive?)
### ICMP/ARP discovery (best for local LAN)
nmap -sn 192.168.1.0/24
### TCP SYN ping (useful if ICMP blocked)
nmap -sn -PS22,80,443 192.168.1.0/24
### ICMP echo ping (explicit)
nmap -sn -PE 192.168.1.0/24
### No ping (treat host as up; useful if discovery is blocked)
nmap -Pn 192.168.1.10
### Notes:

### -sn = host discovery only (no port scan)

### -Pn can be slower and noisier, but works when ping is blocked
### Port Discovery (What is open?)
### Common ports (top 1000)
nmap 192.168.1.10
### Fast scan (top ~100)
nmap -F 192.168.1.10
### Full TCP port sweep
nmap -p- 192.168.1.10
### Specific ports (targeted)
nmap -p 22,80,443,3389 192.168.1.10
### Top ports (choose count)
nmap --top-ports 200 192.168.1.10
### Scan Types (How to scan TCP/UDP)
### TCP SYN scan (default for privileged/admin)
nmap -sS 192.168.1.10
### TCP connect scan (works without admin)
nmap -sT 192.168.1.10
### UDP scan (slower; often needs tuning)
nmap -sU 192.168.1.10
### TCP + UDP combo (common ports)
nmap -sS -sU -p T:22,80,443,U:53,67,68,123 192.168.1.10
### Service and Version Detection (What software is running?)
### Standard service detection
nmap -sV 192.168.1.10
### More aggressive version detection
nmap -sV --version-intensity 9 192.168.1.10
### Try all probes (can be noisy)
nmap -sV --version-all 192.168.1.10
### OS Detection and Fingerprinting (What OS is it?)
### OS guess
nmap -O 192.168.1.10
### OS + services + SYN scan (strong baseline)
nmap -sS -sV -O 192.168.1.10
### Aggressive scan (includes scripts + traceroute)
nmap -A 192.168.1.10
### Notes:

### OS detection is best when the host has at least one open and one closed port.

### On Windows, run your terminal as Administrator for best results
### Nmap Scripting Engine (NSE) — Safe Recon & Checks
### Default scripts (generally safe)
nmap --script default 192.168.1.10
### “Safe” category scripts
nmap --script safe 192.168.1.10
### Vulnerability category (review results carefully)
nmap --script vuln 192.168.1.10
### Discovery scripts (enumeration)
nmap --script discovery 192.168.1.10
### Tip: Prefer safe + default for employer-facing labs unless you clearly explain scope and permission.
### Performance and Reliability (Timing / Retries)
### Timing templates (0 to 5)
nmap -T3 192.168.1.10
nmap -T4 192.168.1.10
### Set min/max rate (advanced; use carefully)
nmap --min-rate 100 192.168.1.10
### Output and Documentation (Professional habit)

### Create an outputs folder:
mkdir outputs
### Save in all formats (recommended):
nmap -sS -sV -O 192.168.1.10 -oA outputs/host1
### Save subnet discovery:
nmap -sn 192.168.1.0/24 -oA outputs/subnet-discovery
### Formats:

### -oN normal (human-readable)

### -oX XML (tools/SIEM ingestion)

### -oG grepable

### -oA all formats (best for labs)
### A Repeatable Workflow (Do this every time)

### 1 Discover live hosts:
nmap -sn 192.168.1.0/24 -oA outputs/01-discovery
### 2 Quick port check of a target:
nmap -F 192.168.1.10 -oA outputs/02-fast
### 3 Full port scan (TCP):
nmap -p- 192.168.1.10 -oA outputs/03-full-tcp
### 4 Service + OS fingerprint:
nmap -sS -sV -O 192.168.1.10 -oA outputs/04-fingerprint
### 5 Safe scripts:
nmap -sV --script default,safe 192.168.1.10 -oA outputs/05-nse-safe
### Notes / Ethics

### Only scan systems you own or have explicit permission to test.
### Document scope, date/time, and purpose of each scan when saving outputs
## Home Network Discovery - 2026-01-14
**Command** nmap -sn 192.168.1.0/24 -oA nmap/outputs/home-discovery
## Result

## 256 IP addresses scanned

## 0 hosts responded

## Interpretation
## This indicates that host-to-host discovery is blocked on the local network.
## Likely causes include:

## Wireless client isolation

## Guest VLAN

## Router firewall policies

## This is a positive security control that reduces lateral movement risk.

## Router Port Enumeration — 2026-01-15

**Target**
- IP Address: 192.168.4.1
- Asset Type: Network gateway / router
- Vendor Identified via MAC OUI: eero

**Command**

nmap -sT -p 1-1024 192.168.4.1 -oA nmap/outputs/router-enum
Results

## Host is reachable with low latency

## 1022 TCP ports closed (connection refused)

## Open ports:

## 53/tcp (DNS)

## 80/tcp (HTTP)

## Interpretation
The router exposes a minimal and expected attack surface:

## Port 53 indicates local DNS services

## Port 80 indicates a web-based management interface

## All other well-known ports are closed, indicating an enforced default-deny posture

## MAC address vendor identification confirms the device as an eero router, validating asset classification as network infrastructure rather than an endpoint.

## This configuration reduces lateral movement opportunities and limits exposure to common service-based attacks.
---

## Scan 2 – Router Port Enumeration

**Target**
- IP Address: 192.168.4.1
- Asset Type: Network gateway / router

**Command**

nmap -sT -p 1-1024 192.168.4.1 -oA nmap/outputs/router-enum

## Results

## Host reachable with low latency

## 1022 TCP ports closed (connection refused)

## Open ports identified:

## 53/tcp (DNS)

## 80/tcp (HTTP)

## Device Identification

## MAC address OUI resolved to vendor: eero

## Indicates the device is network infrastructure rather than an endpoint

## Security Interpretation
## The router exposes a minimal and expected attack surface. DNS and HTTP services are typical for local name resolution and administrative access. The absence of additional open well-known ports suggests a default-deny firewall posture, which reduces exposure to common service-based attacks and limits lateral movement opportunities.
