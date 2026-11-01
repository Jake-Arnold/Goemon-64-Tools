"""LiveSplit Server protocol, localhost only."""
import socket

class LiveSplit:
    def __init__(self, host="127.0.0.1", port=16834):
        self.host, self.port = host, port
    def _command(self, command: str, needs_response=False):
        # Opening one connection per command avoids stale-state buffering; at 10 Hz
        # it is adequate for a prototype but not an ideal production implementation.
        with socket.create_connection((self.host, self.port), timeout=1) as client:
            client.sendall((command+"\r\n").encode())
            if needs_response:
                client.settimeout(1)
                received = b""
                while b"\n" not in received and len(received) < 4096:
                    chunk = client.recv(1024)
                    if not chunk: break
                    received += chunk
                return received.decode(errors="replace").strip()
    def phase(self):
        return self._command("getcurrenttimerphase", True)
    def split(self):
        return self._command("split")
    def split_index(self):
        return int(self._command("getsplitindex", True))
    def split_count(self):
        return int(self._command("getsplitcount", True))
    def split_name(self, index):
        return self._command(f"getsplitname {index}", True)
    def current_split_name(self):
        return self._command("getcurrentsplitname", True)
