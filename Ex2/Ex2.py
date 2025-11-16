import tkinter as tk                    
from tkinter import messagebox          
import random                           
import os                              

# this function just grabs all the jokes from the txt file
def load_jokes():
    jokes = []                          # empty list where i put every joke
    
    # sometimes python looks in the wrong folder so i check two places just in case
    paths = [
        "randomJokes.txt",                                      # normal way
        os.path.join(os.path.dirname(__file__), "randomJokes.txt")  # the safe way
    ]
    
    file_location = None                # gonna remember where the file actually is
    for p in paths:                     # check both spots
        if os.path.exists(p):           # if the file is there
            file_location = p           # cool we found it
            break                       # stop looking
    
    # if still cant find the file anywhere
    if not file_location:
        messagebox.showerror("Missing File", 
            "bro where is randomJokes.txt??\nput it in the same folder as this file pls")
        return jokes                    # give back nothing so program knows it failed
    
    # now actually try to read the file
    try:
        with open(file_location, "r", encoding="utf-8") as f:   # open the file
            for line in f:              # go through every line
                line = line.strip()     # remove extra spaces and newlines
                if not line or "?" not in line:   # skip empty lines or lines with no ?
                    continue            # next line please
                
                # split the joke into question and answer
                if "? " in line:        # some jokes have space after the ?
                    q, a = line.split("? ", 1)   # split it properly
                else:                   # some dont have space
                    q, a = line.split("?", 1)
                    
                q = q.strip() + "?"     # make sure the question ends with ?
                a = a.strip()           # clean up the answer
                jokes.append((q, a))    # add this joke to my list
    except:                         # if anything goes wrong
        messagebox.showerror("Error", "couldnt open the jokes file man :(")
        return jokes                # return empty so program stops
        
    return jokes                    # finally give back all the jokes

# main app thingy
class JokeApp:
    def __init__(self, root):
        self.root = root            # save the window
        self.root.title("Alexa, tell me a Joke!")   # title at the top
        self.root.geometry("660x520")   # made it big enough so nothing gets cut
        self.root.configure(bg="#fffff0")   # background color kinda cream
        self.root.resizable(False, False)   # dont let people stretch it
        
        # load all jokes when it starts
        self.jokes = load_jokes()   # get the jokes
        if not self.jokes:          # if no jokes loaded
            self.root.destroy()     # just close everything
            return                  # stop here
            
        self.setup = ""             # current joke question
        self.punchline = ""         # current joke answer
        
        self.create_widgets()       # make all the buttons and stuff
        self.get_new_joke()         # show one joke right away
        
    def create_widgets(self):
        # big title at the top
        tk.Label(self.root, text="Alexa, tell me a Joke!",
                font=("Arial", 26, "bold"), bg="#fffff0", fg="#d63031")\
                .pack(pady=20)      # put it on screen
        
        # big orange button to get a joke
        self.main_btn = tk.Button(self.root, text="Alexa tell me a Joke",
                                 font=("Arial", 16, "bold"), bg="#e17055", fg="white",
                                 width=28, height=2, command=self.get_new_joke)
        self.main_btn.pack(pady=15)     # place it
        
        # where the joke question shows
        self.setup_label = tk.Label(self.root, text="", font=("Arial", 18),
                                   wraplength=620, justify="center",
                                   bg="#fffff0", fg="#2d3436")
        self.setup_label.pack(pady=30)  # lots of space
        
        # where the punchline shows (hidden at first)
        self.punch_label = tk.Label(self.root, text="", font=("Arial", 17, "italic"),
                                   wraplength=620, justify="center",
                                   bg="#fffff0", fg="#e17055")
        self.punch_label.pack(pady=10)  # small space
        
        # frame for the two buttons in the middle
        mid_frame = tk.Frame(self.root, bg="#fffff0")
        mid_frame.pack(pady=20)     # space above
        
        # show punchline button
        tk.Button(mid_frame, text="Show Punchline", font=("Arial", 13, "bold"),
                 bg="#00b894", fg="white", width=18,
                 command=self.reveal_punchline).pack(side="left", padx=30)
        
        # next joke button
        tk.Button(mid_frame, text="Next Joke", font=("Arial", 13, "bold"),
                 bg="#0984e3", fg="white", width=18,
                 command=self.get_new_joke).pack(side="left", padx=30)
        
        # QUIT BUTTON - locked at bottom so it NEVER disappears
        quit_btn = tk.Button(self.root, text="Quit", font=("Arial", 14, "bold"),
                            bg="#d63031", fg="white", width=12,
                            command=self.root.quit)
        quit_btn.place(relx=0.5, rely=0.92, anchor="center")  # stays at bottom center forever
        
    # when you want a new joke
    def get_new_joke(self):
        self.setup, self.punchline = random.choice(self.jokes)  # pick random one
        self.setup_label.config(text=self.setup)    # show question
        self.punch_label.config(text="")            # hide old answer
        self.main_btn.config(state="disabled")      # cant spam the button
        
    # when you click show punchline
    def reveal_punchline(self):
        self.punch_label.config(text=self.punchline)  # show the funny part
        self.main_btn.config(state="normal")          # let them get new joke again


if __name__ == "__main__":
    root = tk.Tk()             
    app = JokeApp(root)        
    root.mainloop()             