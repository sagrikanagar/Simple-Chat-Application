import tkinter
import warnings

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

warnings.filterwarnings('ignore')

class Client():
    def __init__(self):
        """Constructor function for building the client section of the Chat Server"""
        # Constants
        self.HOST = "127.0.0.1"
        self.PORT = 5000
        self.BUFFER_SIZE = 1024
        self.ADDR = (self.HOST, self.PORT)
        self.SOCK = socket(AF_INET, SOCK_STREAM)
        
        self.application = None
        
        # UI Elements
        self.messages_frame = None
        self.client_message = None
        self.scroll = None
        self.message_list = None
        self.button_label = None
        self.entry_field = None

        # Buttons
        self.send_button = None
        self.smile_emoji = None
        self.frown_emoji = None
        self.quit_button = None
        
        # Thread
        self.receive_thread = None

    def receive_message(self):
        """Function for handling receiving of messages"""
        while True:
            try:
                message = self.SOCK.recv(self.BUFFER_SIZE).decode("utf8")
                self.message_list.insert(tkinter.END, message)
            except OSError:  
                break

    def send_message(self, event=None):
        """Function for handling sending of messages"""
        message = self.client_message.get()
        self.client_message.set("")  
        self.SOCK.send(bytes(message, "utf8"))
        if message == "QUIT":
            self.SOCK.close()
            self.application.destroy()

    def close_window(self, event=None):
        """Function for setting message when closing the window"""
        self.client_message.set("QUIT")
        self.send_message()

    def smileEmoji_button(self, event=None):
        """ Function for Smile Emoji Button"""
        self.client_message.set("=)")    
        self.send_message()

    def frownEmoji_button(self, event=None):
        """ Function for Frown Emoji Button"""
        self.client_message.set("=(")    
        self.send_message()

    def create_chatbox(self):
        self.application = tkinter.Tk()
        self.application.title("Messaging Platform")

        # Added for i3wm
        self.application.attributes('-type', 'dialog')
        self.application.configure(bg='gray')
        
        self.messages_frame = tkinter.Frame(self.application)
        self.client_message = tkinter.StringVar() 
        self.client_message.set("")

        self.scroll = tkinter.Scrollbar(self.messages_frame) 
        self.message_list = tkinter.Listbox(self.messages_frame, height=15, width=70, yscrollcommand=self.scroll.set, foreground="Black", font="Verdana 11", background="White")

        self.scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        
        self.message_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        self.message_list.pack()
        self.messages_frame.pack()

        self.button_label = tkinter.Label(self.application, text="Enter Message:", foreground="Indigo", font='Helvetica 12 bold', background="White")
        self.button_label.pack()

        self.entry_field = tkinter.Entry(self.application, textvariable=self.client_message, foreground="DarkSlateBlue", font='Verdana 11', background="White")
        self.entry_field.bind("<Return>", self.send_message)
        self.entry_field.pack()

        self.send_button = tkinter.Button(self.application, text="Send Message", command=self.send_message, foreground="DarkBlue", font='Calibri 11', background="White")
        self.send_button.pack()

        self.smile_emoji = tkinter.Button(self.application, text="Smile", command=self.smileEmoji_button, foreground="DarkBlue", font='Calibri 11', background="White")
        self.smile_emoji.pack()

        self.frown_emoji = tkinter.Button(self.application, text="Frown", command=self.frownEmoji_button, foreground="DarkBlue", font='Calibri 11', background="White")
        self.frown_emoji.pack()

        self.quit_button = tkinter.Button(self.application, text="Quit", command=self.close_window, foreground="DarkBlue", font='Calibri 11', background="White")
        self.quit_button.pack()

        self.application.protocol("WM_DELETE_WINDOW", self.close_window)

        self.SOCK.connect(self.ADDR)
        self.receive_thread = Thread(target=self.receive_message)
        self.receive_thread.start()
        tkinter.mainloop()

client = Client()
client.create_chatbox()