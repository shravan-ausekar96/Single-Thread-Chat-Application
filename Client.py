import queue
import socket
import threading
import tkinter as tk

HOST = "127.0.0.1"  # must match the server
PORT = 12345


class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Client")
        self.sock = None
        self.incoming = queue.Queue()

        # ---------- GUI ----------
        self.listbox = tk.Listbox(root, width=50, height=15)
        self.listbox.pack(padx=10, pady=10)

        bottom = tk.Frame(root)
        bottom.pack(padx=10, pady=(0, 10))

        self.entry = tk.Entry(bottom, width=40)
        self.entry.pack(side=tk.LEFT, padx=(0, 5))
        self.entry.bind("<Return>", lambda event: self.send())

        self.send_button = tk.Button(bottom, text="Send", command=self.send)
        self.send_button.pack(side=tk.LEFT)

        # ---------- Networking ----------
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((HOST, PORT))
            self.show(f"[Connected to {HOST}:{PORT}]")
            threading.Thread(target=self.receive_loop, daemon=True).start()
        except ConnectionRefusedError:
            self.sock = None
            self.show("[Could not connect - start server.py first]")

        self.poll_queue()
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def show(self, text):
        self.listbox.insert(tk.END, text)
        self.listbox.yview_moveto(1)

    def send(self):
        message = self.entry.get().strip()
        if not message:
            return
        if self.sock is None:
            self.show("[Not connected]")
            return
        try:
            self.sock.sendall(message.encode("utf-8"))
        except OSError:
            self.show("[Send failed - server disconnected]")
            return
        self.show(f"You: {message}")
        self.entry.delete(0, tk.END)

    def receive_loop(self):  # runs in a background thread
        while True:
            try:
                data = self.sock.recv(1024)
            except OSError:
                break
            if not data:
                self.incoming.put("[Server disconnected]")
                break
            self.incoming.put("Server: " + data.decode("utf-8"))

    def poll_queue(self):
        while not self.incoming.empty():
            self.show(self.incoming.get())
        self.root.after(100, self.poll_queue)

    def close(self):
        if self.sock:
            self.sock.close()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    ChatClient(root)
    root.mainloop()