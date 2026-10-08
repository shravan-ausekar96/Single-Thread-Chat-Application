import queue
import socket
import threading
import tkinter as tk

HOST = "127.0.0.1"  # localhost only
PORT = 12345


class ChatServer:
    def __init__(self, root):
        self.root = root
        self.root.title("Server")
        self.conn = None                # becomes the client socket once connected
        self.incoming = queue.Queue()   # background thread -> GUI

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
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # lets you restart the server immediately without "Address already in use"
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((HOST, PORT))
        self.server_socket.listen(1)
        self.show(f"Waiting for a client on {HOST}:{PORT} ...")

        # accept() and recv() block, so they run in a background thread
        threading.Thread(target=self.network_loop, daemon=True).start()

        self.poll_queue()
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    # ---------- helpers ----------
    def show(self, text):
        self.listbox.insert(tk.END, text)
        self.listbox.yview_moveto(1)  # auto-scroll to the newest message

    def send(self):
        message = self.entry.get().strip()
        if not message:
            return
        if self.conn is None:
            self.show("[No client connected yet]")
            return
        try:
            self.conn.sendall(message.encode("utf-8"))
        except OSError:
            self.show("[Send failed - client disconnected]")
            return
        self.show(f"You: {message}")
        self.entry.delete(0, tk.END)

    # ---------- background thread (never touch widgets here) ----------
    def network_loop(self):
        try:
            conn, address = self.server_socket.accept()
        except OSError:
            return  # socket closed while waiting
        self.conn = conn
        self.incoming.put(f"[Client connected from {address[0]}:{address[1]}]")

        while True:
            try:
                data = conn.recv(1024)
            except OSError:
                break
            if not data:  # empty bytes = the other side closed the connection
                self.incoming.put("[Client disconnected]")
                break
            self.incoming.put("Client: " + data.decode("utf-8"))

    # ---------- GUI thread ----------
    def poll_queue(self):
        while not self.incoming.empty():
            self.show(self.incoming.get())
        self.root.after(100, self.poll_queue)  # check again in 100 ms

    def close(self):
        if self.conn:
            self.conn.close()
        self.server_socket.close()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    ChatServer(root)
    root.mainloop()