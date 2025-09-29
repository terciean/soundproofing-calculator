import subprocess
import json
import sys
import time
import requests
import socket
import os

def is_port_open(host, port, timeout=1.0):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False

def check_mcp_server():
    mcp_port = 3034  # Port for MCP server, matches mcp_settings.json
    mcp_host = "127.0.0.1"
    npx_path = os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "nodejs", "npx.cmd")
    if not os.path.exists(npx_path):
        npx_path = os.path.join(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"), "nodejs", "npx.cmd")
    if not os.path.exists(npx_path):
        npx_path = "npx"
    command = [npx_path, "@agentdeskai/browser-tools-mcp@latest"]
    print("PATH environment variable before subprocess:", os.environ.get("PATH"), file=sys.stderr)
    try:
        print("[MCP Health Check] Checking if MCP server is already running...", file=sys.stderr)
        if is_port_open(mcp_host, mcp_port):
            print(f"[MCP Health Check] MCP server detected on port {mcp_port}. Attempting HTTP request...", file=sys.stderr)
            try:
                resp = requests.get(f"http://{mcp_host}:{mcp_port}/", timeout=3)
                output = resp.text.strip()
                success = resp.status_code == 200
                print(f"[MCP Health Check] HTTP request returned status {resp.status_code}.", file=sys.stderr)
                return {"mcp_server_accessible": success, "output": output}
            except Exception as e:
                print(f"[MCP Health Check] HTTP request to running server failed: {e}", file=sys.stderr)
                return {"mcp_server_accessible": False, "error": f"HTTP request failed: {e}"}
        print("[MCP Health Check] MCP server not running. Attempting to start MCP server...", file=sys.stderr)
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        for i in range(60):
            if is_port_open(mcp_host, mcp_port):
                print(f"[MCP Health Check] MCP server started and port {mcp_port} is open after {i*0.5:.1f}s.", file=sys.stderr)
                break
            if i % 5 == 0:
                print(f"[MCP Health Check] Waiting for MCP server to start... ({i*0.5:.1f}s elapsed)", file=sys.stderr)
            time.sleep(0.5)
        else:
            stdout, stderr = proc.communicate(timeout=5)
            proc.terminate()
            print(f"[MCP Health Check] MCP server did not start on port {mcp_port} after 30s.", file=sys.stderr)
            return {"mcp_server_accessible": False, "error": f"MCP server did not start on port {mcp_port}", "stdout": stdout.decode(errors='replace'), "stderr": stderr.decode(errors='replace')}
        try:
            print(f"[MCP Health Check] Attempting HTTP request to MCP server on port {mcp_port}...", file=sys.stderr)
            resp = requests.get(f"http://{mcp_host}:{mcp_port}/", timeout=5)
            output = resp.text.strip()
            success = resp.status_code == 200
            print(f"[MCP Health Check] HTTP request returned status {resp.status_code}.", file=sys.stderr)
        except Exception as e:
            stdout, stderr = proc.communicate(timeout=5)
            proc.terminate()
            print(f"[MCP Health Check] HTTP request to started server failed: {e}", file=sys.stderr)
            return {"mcp_server_accessible": False, "error": f"HTTP request failed: {e}", "stdout": stdout.decode(errors='replace'), "stderr": stderr.decode(errors='replace')}
        stdout, stderr = proc.communicate(timeout=5)
        proc.terminate()
        return {"mcp_server_accessible": success, "output": output, "stdout": stdout.decode(errors='replace'), "stderr": stderr.decode(errors='replace')}
    except Exception as e:
        print(f"[MCP Health Check] Exception occurred: {e}", file=sys.stderr)
        return {"mcp_server_accessible": False, "error": str(e)}

def main():
    print("[MCP Health Check] Starting health check...", file=sys.stderr)
    status = check_mcp_server()
    print("[MCP Health Check] Health check result:", file=sys.stderr)
    print(json.dumps(status, indent=2))

if __name__ == "__main__":
    main()