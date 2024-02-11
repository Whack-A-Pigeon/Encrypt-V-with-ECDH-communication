# gui.py

from tkinter import Tk, PhotoImage, Label, Entry, Button, messagebox, filedialog

# Encryptiv GUI components
class EncryptiVGUI:

    def __init__(self):

        # GUI
        self.root = Tk()
        self.root.geometry("400x250")
        self.root.title("Encrypti V")
        self.root.resizable(False, False)

        self.backgroundImage = PhotoImage(file = r"C:\Users\whack\OneDrive\Desktop\STUFF\Programming STUFF\Python\Encrypti-V\Client\background.gif")
        self.backgroundLabel = Label(self.root, image = self.backgroundImage)
        self.backgroundLabel.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.welcomeLabel = Label(self.root, text="Welcome to Encrypti V")
        self.welcomeLabel.place(x=150, y=30)

        self.usernameLabel = Label(self.root, text="Username:")
        self.usernameLabel.place(x=50, y=80)

        self.passwordLabel = Label(self.root, text="Password:")
        self.passwordLabel.place(x=50, y=120)

        self.usernameField = Entry(self.root)
        self.usernameField.place(x=140, y=80, width=200, height=25)
        self.passwordField = Entry(self.root, show="*")
        self.passwordField.place(x=140, y=120, width=200, height=25)

        self.loginButton = Button(self.root, text="Login")
        self.loginButton.place(x=140, y=160, width=90, height=30)
        self.registerButton = Button(self.root, text="Register")
        self.registerButton.place(x=250, y=160, width=90, height=30)
        self.encryptFileButton = Button(self.root, text="Encrypt")
        self.decryptFileButton = Button(self.root, text="Decrypt")

        # Hide encrypt and decrypt button initially
        self.hideComponents(1)
    
    # Function to display a message dialog
    def showMessage(self, message):
        messagebox.showinfo("Message", message)

    # Function to hide components
    def hideComponents(self, button_id):
        
        if button_id == 1:
            self.encryptFileButton.place_forget()
            self.decryptFileButton.place_forget()

        if button_id == 2:

            # Buttons to be hidden
            fields = [self.usernameLabel, self.usernameField, self.passwordLabel, self.passwordField, self.loginButton, self.registerButton, self.welcomeLabel]
            
            self.welcomeLabel
            for field in fields:
                field.place_forget()
            
    
    # Function for showing the Encrypt and Decrypt buttons
    def showButtons(self):
        self.encryptFileButton.place(x=100, y=110, width=90, height=30)
        self.decryptFileButton.place(x=210, y=110, width=90, height=30)

    # Function to open dialog to pick file
    def pickFile(self):
        return filedialog.askopenfilename()

    # Function to open a directory picker dialog
    def pickDir(self):
        return filedialog.askdirectory()


    def run(self):
        self.root.mainloop()
