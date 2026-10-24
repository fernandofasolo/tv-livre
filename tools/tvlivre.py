#!/usr/bin/env python3
"""
TV Livre - helper CLI for LG TVs in Developer Mode.

Commands:
  discover                      Find a TV in Developer Mode on the local network
  pair    --ip IP [--passphrase P]  Download and decrypt the Dev Mode SSH key
  install IPK [--ip IP]         Upload and install an .ipk on the TV
  devmode-status [--ip IP]      Show remaining Developer Mode session time
  devmode-renew  [--ip IP]      Reset the Developer Mode session to 1000 h
  schedule-renew [--ip IP]      (Windows) Create a weekly scheduled task for devmode-renew

The TV IP is remembered in ~/.tvlivre.json after the first successful pair.
"""

import argparse
import json
import os
import socket
import subprocess
import sys
import urllib.request

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

CONFIG_PATH = os.path.expanduser("~/.tvlivre.json")
SSH_DIR = os.path.expanduser("~/.ssh")
RAW_KEY = os.path.join(SSH_DIR, "webos_tv_rsa")
DEC_KEY = os.path.join(SSH_DIR, "webos_tv_rsa_decrypted")
SSH_PORT = "9922"
# The TV's dev sshd only offers legacy ssh-rsa keys.
SSH_OPTS = ["-o", "StrictHostKeyChecking=accept-new",
            "-o", "HostKeyAlgorithms=+ssh-rsa",
            "-o", "PubkeyAcceptedKeyTypes=+ssh-rsa"]
DEVMODE_TOKEN_FILE = "/var/luna/preferences/devmode_enabled"
LGE_SESSION_URL = "https://developer.lge.com/secure/{action}.dev?sessionToken={token}"


def load_config():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def save_config(cfg):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)


def resolve_ip(args):
    ip = getattr(args, "ip", None) or load_config().get("ip")
    if not ip:
        sys.exit("[!] TV IP unknown. Pass --ip or run 'pair' first.")
    return ip


def write_private(path, data):
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "wb") as f:
        f.write(data)
    os.chmod(path, 0o600)


def ssh(ip, remote_cmd, tty=False):
    args = ["ssh", *(["-tt"] if tty else []), *SSH_OPTS, "-p", SSH_PORT, "-i", DEC_KEY,
            f"prisoner@{ip}", remote_cmd]
    return subprocess.run(args, capture_output=True, text=True)


def cmd_discover(args):
    msg = ('M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1900\r\nMAN: "ssdp:discover"\r\n'
           'MX: 2\r\nST: urn:schemas-upnp-org:device:MediaRenderer:1\r\n\r\n').encode()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.settimeout(2.5)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    found = set()
    try:
        sock.sendto(msg, ("239.255.255.250", 1900))
        while True:
            _, addr = sock.recvfrom(4096)
            ip = addr[0]
            if ip in found:
                continue
            found.add(ip)
            probe = socket.socket()
            probe.settimeout(0.3)
            dev = probe.connect_ex((ip, int(SSH_PORT))) == 0
            probe.close()
            print(f"{ip}\t{'Developer Mode ON (port 9922)' if dev else 'media renderer'}")
    except socket.timeout:
        pass
    finally:
        sock.close()
    if not found:
        print("[!] Nothing answered. Is the TV on and on the same network?")


def cmd_pair(args):
    try:
        from cryptography.hazmat.primitives import serialization
    except ImportError:
        sys.exit("[!] Missing dependency: pip install cryptography")
    passphrase = args.passphrase or input("6-character Passphrase shown in the Developer Mode app: ").strip()
    os.makedirs(SSH_DIR, exist_ok=True)
    url = f"http://{args.ip}:9991/webos_rsa"
    print(f"[*] Downloading key from {url} (Key Server must be ON)...")
    with urllib.request.urlopen(url, timeout=5) as resp:
        key_data = resp.read()
    write_private(RAW_KEY, key_data)
    key = serialization.load_pem_private_key(key_data, password=passphrase.encode())
    write_private(DEC_KEY, key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()))
    cfg = load_config()
    cfg["ip"] = args.ip
    save_config(cfg)
    print(f"[+] Paired. Key saved to {DEC_KEY}; TV IP remembered.")


def cmd_install(args):
    ip = resolve_ip(args)
    if not os.path.isfile(args.ipk):
        sys.exit(f"[!] File not found: {args.ipk}")
    remote = "/media/developer/temp/tvlivre-upload.ipk"
    print(f"[*] Uploading {os.path.basename(args.ipk)} to {ip}...")
    res = subprocess.run(["scp", *SSH_OPTS, "-P", SSH_PORT, "-i", DEC_KEY, args.ipk, f"prisoner@{ip}:{remote}"])
    if res.returncode != 0:
        sys.exit("[!] Upload failed.")
    payload = json.dumps({"id": "tvlivre.install", "ipkUrl": remote, "subscribe": True})
    # luna-send-pub needs a TTY to print anything; dev/install streams many
    # progress replies, and the session stays open after the last one.
    res = ssh(ip, f"timeout 60 luna-send-pub -n 30 luna://com.webos.appInstallService/dev/install '{payload}'", tty=True)
    if '"state":"installed"' in res.stdout:
        print("[+] Installed.")
    else:
        print("[!] Install did not reach the 'installed' state:")
        print(res.stdout or res.stderr or "(no output)")
        sys.exit(1)


def read_session_token(ip):
    res = ssh(ip, f"cat {DEVMODE_TOKEN_FILE}")
    token = res.stdout.strip()
    if res.returncode != 0 or not token:
        sys.exit(f"[!] Could not read the Dev Mode session token: {res.stderr.strip()}")
    return token


def lge_session(action, token):
    with urllib.request.urlopen(LGE_SESSION_URL.format(action=action, token=token), timeout=15) as resp:
        return resp.read().decode("utf-8", "replace").strip()


def cmd_devmode_status(args):
    print(lge_session("CheckDevModeSession", read_session_token(resolve_ip(args))))


def cmd_devmode_renew(args):
    print(lge_session("ResetDevModeSession", read_session_token(resolve_ip(args))))
    print("[+] Renewal request sent. Check with 'devmode-status'.")


def cmd_schedule_renew(args):
    if os.name != "nt":
        sys.exit("[!] schedule-renew is Windows-only. On Linux/macOS use cron: "
                 "0 9 * * 1 python3 tools/tvlivre.py devmode-renew")
    ip = resolve_ip(args)
    task = f'"{sys.executable}" "{os.path.abspath(__file__)}" devmode-renew --ip {ip}'
    res = subprocess.run(["schtasks", "/Create", "/F", "/SC", "WEEKLY", "/D", "MON", "/ST", "09:00",
                          "/TN", "TVLivre-DevModeRenew", "/TR", task])
    if res.returncode == 0:
        print("[+] Scheduled task 'TVLivre-DevModeRenew' created (Mondays 09:00).")


def main():
    p = argparse.ArgumentParser(description="TV Livre helper for LG TVs in Developer Mode")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("discover").set_defaults(func=cmd_discover)
    sp = sub.add_parser("pair")
    sp.add_argument("--ip", required=True)
    sp.add_argument("--passphrase")
    sp.set_defaults(func=cmd_pair)
    sp = sub.add_parser("install")
    sp.add_argument("ipk")
    sp.add_argument("--ip")
    sp.set_defaults(func=cmd_install)
    for name, func in (("devmode-status", cmd_devmode_status),
                       ("devmode-renew", cmd_devmode_renew),
                       ("schedule-renew", cmd_schedule_renew)):
        sp = sub.add_parser(name)
        sp.add_argument("--ip")
        sp.set_defaults(func=func)
    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
