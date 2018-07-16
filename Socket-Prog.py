import sys
import pymysql,socket,select,os,webbrowser
import string
from tkinter.ttk import Progressbar
from tkinter import *
from tkinter import messagebox,filedialog
class login:
    def __init__(self,master):

        self.master=master
        self.frame = Frame(self.master, bg="light blue", width=460, height=280, highlightcolor="black", padx=50,
                           pady=10, highlightbackground="black")
        self.footer = Frame(self.master, bg="gray93", width=460, height=35)
        self.header=Frame(self.master,bg="light blue",width=460,height=50,pady=5,padx=45)
        self.header.grid(row=0,sticky="ew")
        self.header.grid_rowconfigure(0, weight=2)
        self.header.grid_columnconfigure(0,weight=1)
        self.header.grid_columnconfigure(2,weight=1)
        self.header.grid_columnconfigure(1,weight=1)
        self.header.grid(row=0, sticky="ew")
        self.frame.grid(row=1,sticky="nsew")

        self.footer.grid(row=2, sticky="nsew")
        self.info = Label(self.footer, text="Made by Nikhil Mulchandani", font="calibri 10 bold  ", pady=10, height=1,
                              fg="blue")
        self.info.pack(fill="both",expand=True)


        # top most frame widgets
        self.source = Button(self.header, text="View Source code", command=self.onclickSource, highlightbackground="grey")
        self.source.pack()
        self.source.flash()

        self.box = LabelFrame(self.frame, height=250, width=200, bd=5, relief="groove")
        self.box.pack()
        self.box.config(highlightbackground="green")

        self.signup=Label(self.box,text="if new user then click signup else sign-in")


        self.user_frame = Frame(self.box, height=100, width=199, bg="white")
        self.user_frame.grid(row=0, sticky="nsew")

        # passwordframe
        self.passFrame = Frame(self.box, height=70, width=199, bg="white")
        self.passFrame.grid(row=1, sticky="nsew")




        self.logintext = Label(self.user_frame, text="Username", fg="black", bg="white")
        self.logintext.grid(row=0, column=0, sticky="w")
        # entry field
        self.username = Entry(self.user_frame, width=21)
        self.username.grid(row=1, column=0, columnspan=2, sticky="e")

        self.passwordtext = Label(self.passFrame, text="Password",bg="white")
        self.passwordtext.grid(row=0, column=0, sticky="w")
        self.password = Entry(self.passFrame, width=21, show="*")
        self.password.grid(row=1, column=0)
        self.ButtonFrame = Frame(self.box,height=70, width=199, bg="white")
        self.ButtonFrame.grid(row=2,sticky="nsew")

        self.server_loginbutton = Button(self.ButtonFrame, text="Server Login",
                                         command=self.onclickServerLogin,width=7,highlightbackground="blue")



        self.server_loginbutton.pack(fill="x")
        #self.server_loginbutton.grid(row=2, column=0)
        self.client_loginbutton = Button(self.ButtonFrame, text="Client Login",
                                         command=self.onclickClientLogin,width=10,highlightbackground="blue")
        self.client_loginbutton.pack(fill="x")

        #self.client_loginbutton.grid(row=2, column=)
        self.quit = Button(self.ButtonFrame, text="Quit", width=7, command=self.destroy,highlightbackground="black")

        #self.quit.grid(row=3, column=0)
        self.quit.pack(fill="x")

        self.heading = Label(self.header, text="CONNECT.IO", font="calibri 26 bold  underline", pady=10, height=1,bg="light blue",fg="red")
        self.heading.pack()

    def onclickSource(self):
        webbrowser.open("https://github.com/nikmul19/Python/blob/master/GUI_TEST/frame_test.py")

    def onclickServerLogin(self):
        db=pymysql.connect("localhost","root","root","test")
        print(sys.argv)
        user=self.username.get()
        user=user.strip(string.whitespace)
        password=self.password.get()
        print(password)
        cursor=db.cursor()
        query="select * from users where name='%s' and password='%s'"%(user,password)
        cursor.execute(query)
        if cursor.rowcount!=0:
            self.logged_in=messagebox.showinfo("login successful","redirecting..")
            flag=True
            self.redirect("SERVER")
        else:
            self.error=messagebox.showerror("Invalid Credentails","please check your username and password")
    def onclickClientLogin(self):
        db=pymysql.connect("localhost","root","root","test")
        print(sys.argv)
        user=self.username.get()
        user=user.strip(string.whitespace)
        password=self.password.get()
        print(password)
        cursor=db.cursor()
        query="select * from users where name='%s' and password='%s'"%(user,password)
        cursor.execute(query)
        if cursor.rowcount!=0:
            self.logged_in=messagebox.showinfo("login successful","redirecting..")
            flag=True
            self.redirect("CLIENT")
        else:
            self.error=messagebox.showerror("Invalid Credentails","please check your username and password")


    def redirect(self,choice):
        self.newWindow = Toplevel(self.master)
        self.newWindow.geometry("320x250")
        if choice=="SERVER":
            self.app = main_window(self.newWindow)
        else:
            self.app=client_window(self.newWindow)
    def destroy(self):
        self.master.destroy()


class main_window:
    def __init__(self,master):
        self.master=master
        self.frame=Frame(self.master,bg="light blue",width=300,height=200,padx=20,pady=50)
        self.frame.grid(row=0,sticky="nsew")
        self.heading = Label(self.frame, text="Server Window", font="calibri 26 bold  underline", pady=10, height=1,
                             bg="light blue", fg="blue")
        self.heading.grid(row=0)
        self.box=LabelFrame(self.frame,width=200,height=200)
        self.box.grid(row=1)
        self.select=Button(self.box,text="Select File",width=10,height=1,command=self.selectFile)
        self.exit=Button(self.box,text="exit",width=10,height=1,command=self.close_all)
        self.retry=Button(self.box,text="Retry ",width=10,height=1,command=self.selectFile)
        self.select.pack()
        self.exit.pack()
        self.file_label = Label(self.box, text="File Uploading", width=20, height=2)
        self.progress = Progressbar(self.box, orient=HORIZONTAL, length=100)

    def selectFile(self):
        self.newFile = ((filedialog.askopenfilename(initialdir="/", title="Select File")))
        if len(self.newFile)==0:
            self.error=messagebox.showerror("No files selected","Select a file to send")
        else:
            self.show=messagebox.showinfo("Files selected","Selected files are "+self.newFile)
            self.server(self.newFile)
    def send_thread(self,c,addr,file):
        print("connectiion from ", addr)
        self.file_label.pack()
        self.progress.pack()
        filename = file.encode()
        self.exit.focus_force()
        flag = True
        filepath = filename
        head, filename = os.path.split(filepath)
        file_obj = open(files, "rb")
        l = file_obj.read(1024)
        i = 1
        self.progress['value'] = int(len(file_obj) / 1024 * i)
        while l:
            print("sending\n")
            c.send(l)
            self.progress['value'] = int(len(file_obj) / 1024 * i)
            l = file_obj.read(1024)
            i += 1
        print("sent")
        self.sent = messagebox.showinfo("successful", "Sent the file Successfully")
        file_obj.close()
        c.close()
        flag = False

    def server(self,files):
        soc=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        soc.connect(("8.8.8.8",1))
        host = soc.getsockname()[0]
        #print(local_ip)
        port = 12345
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        soc.close()
        filename=files.encode()
        self.exit.focus_force()
        flag=True
        self.display_ip=messagebox.showinfo("Sending files","server IP is "+str(host)+" and port is "+str(port))
        while flag:
            self.is_readable=[s]
            self.is_writable=[]
            self.is_error=[]
            count=100
            s.listen(5)
            while count>0:
                r,w,e=select.select(self.is_readable,self.is_writable,self.is_error,1.0)
                if r:
                    c, addr = s.accept()
                    c.settimeout(60)
                    #threading.Thread(target=self.send_thread,args=(c,addr,files)).start()
                    print("connectiion from ", addr)
                    self.file_label.pack()
                    self.progress.pack()
                    filepath=filename
                    head,filename=os.path.split(filepath)
                    #s.send(filename)
                    file = open(files, "rb")
                    l = file.read(1024)
                    i = 1
                    self.progress['value'] = int(len(file) / 1024 * i)
                    while l:
                        print("sending\n")
                        c.send(l)
                        self.progress['value'] = int(len(file) / 1024 * i)
                        l = file.read(1024)
                        i += 1
                    print("sent")
                    
                    self.sent = messagebox.showinfo("successful", "Sent the file Successfully")
                    file.close()
                    c.close()
                    flag = False
                    count=0
                    soc.close()
                    s.close()

                else:
                    count-=1
                    print("still waiting")
                    if count==0:
                        soc.close()
                        self.connection_error=messagebox.showerror("error","no connection")
                        self.retry.pack()

            flag=False
    def close_all(self):
        self.master.destroy()
class client_window:
    def __init__(self,master):
        self.master=master
        self.frame=Frame(self.master,pady=10,padx=10)
        self.frame.pack()
        self.box=LabelFrame(self.frame,width=200,height=200,bg="grey")
        self.box.pack(fill="x")

        self.server_label=Label(self.box,text="Enter Server IP",width=25,height=2)
        self.port_label=Label(self.box,text="Enter server port",width=25,height=2)
        self.server_ip=Entry(self.box)
        self.port=Entry(self.box)
        """self.server_label.grid(row=0,column=0,sticky="w")
        self.port_label.grid(row=2)
        self.server_ip.grid(row=1)
        self.port.grid(row=3)
        """
        self.server_label.pack(side="left",expand=False,fill="x")

        self.server_ip.pack(side="top", expand=True, fill="x")

        self.port_label.pack(side="left",expand=False,fill="x")
        self.port.pack(side="top", expand=True, fill="x")
        self.recieve=Button(self.box,text="Recieve file",command=self.client,width=10)
        self.recieve.pack(side="bottom",expand=False,fill="x")
        self.quit=Button(self.box,text="Quit",command=self.close_all,width=10,bg="light blue")
        self.quit.pack(side="bottom",expand=False,fill="x")

    def client(self):
        host=(self.server_ip.get())
        soc=socket.socket()
        port=int(self.port.get())
        soc.connect((host,port))
        #filename=soc.recv(1024)
        #filename=filename.decode()
        #displayFileName=messagebox.showinfo(title="File To be received",message="Filename is :"+filename)
        saveFile=filedialog.asksaveasfilename(title="enter save as file name")
        file=open(saveFile,"wb")
        bytes=soc.recv(1024)
        while bytes:
            file.write(bytes)
            bytes=soc.recv(1024)
        file.close()
        soc.close()


    def close_all(self):
        self.master.destroy()
def main():
    root = Tk()
    root.title("Socket Programming with Python")
    root.geometry("460x350")
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    app = login(root)
    root.mainloop()
if __name__=="__main__":
    main()
