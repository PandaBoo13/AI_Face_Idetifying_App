from Detector import main_app
from create_classifier import train_classifer
from create_dataset import start_capture
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox,PhotoImage
names = set()


class MainUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        global names
        with open("nameslist.txt", "r") as f:
            x = f.read()
            z = x.rstrip().split(" ")
            for i in z:
                names.add(i)
        self.title_font = tkfont.Font(family='Helvetica', size=16, weight="bold")
        self.title("Face Recognizer")
        self.resizable(False, False)
        self.geometry("500x250")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.active_name = None
        container = tk.Frame(self)
        container.grid(sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("StartPage")

    def show_frame(self, page_name):
            frame = self.frames[page_name]
            frame.tkraise()

    def on_closing(self):

        if messagebox.askokcancel("Quit", "Are you sure?"):
            global names
            f =  open("nameslist.txt", "a+")
            for i in names:
                    f.write(i+" ")
            self.destroy()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="pink")  # Đặt màu nền hồng cho Frame
        self.controller = controller

        render = PhotoImage(file='homepagepic.png')
        img = tk.Label(self, image=render, bg="pink")  # Đặt nền hồng cho label ảnh
        img.image = render
        img.grid(row=0, column=1, rowspan=4, sticky="nsew")

        label = tk.Label(self, text="        Home Page        ", font=self.controller.title_font, fg="#263942", bg="pink")  # Thêm bg
        label.grid(row=0, sticky="ew")

        button1 = tk.Button(self, text="   Sign up  ", fg="#ffffff", bg="#263942", command=lambda: self.controller.show_frame("PageOne"))
        button2 = tk.Button(self, text="   Check a User  ", fg="#ffffff", bg="#263942", command=lambda: self.controller.show_frame("PageTwo"))
        button3 = tk.Button(self, text="Quit", fg="#263942", bg="#ffffff", command=self.on_closing)

        button1.grid(row=1, column=0, ipady=3, ipadx=7)
        button2.grid(row=2, column=0, ipady=3, ipadx=2)
        button3.grid(row=3, column=0, ipady=3, ipadx=32)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Are you sure?"):
            global names
            with open("nameslist.txt", "w") as f:
                for i in names:
                    f.write(i + " ")
            self.controller.destroy()


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="pink")
        self.controller = controller

        # Label và Entry cho Tên
        tk.Label(self, text="Enter the name", fg="#263942", font='Helvetica 12 bold', bg="pink").grid(row=0, column=0, pady=10, padx=5, sticky="e")
        self.user_name = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.user_name.grid(row=0, column=1, pady=10, padx=10)

        # Label và Entry cho Mã sinh viên
        tk.Label(self, text="Student ID", fg="#263942", font='Helvetica 12 bold', bg="pink").grid(row=1, column=0, pady=10, padx=5, sticky="e")
        self.student_id = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.student_id.grid(row=1, column=1, pady=10, padx=10)

        # Label và Entry cho Mã lớp
        tk.Label(self, text="Class ID", fg="#263942", font='Helvetica 12 bold', bg="pink").grid(row=2, column=0, pady=10, padx=5, sticky="e")
        self.class_id = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.class_id.grid(row=2, column=1, pady=10, padx=10)

        # Các nút chức năng
        self.buttoncanc = tk.Button(self, text="Cancel", bg="#ffffff", fg="#263942", command=lambda: controller.show_frame("StartPage"))
        self.buttonext = tk.Button(self, text="Next", fg="#ffffff", bg="#263942", command=self.start_training)
        self.buttonclear = tk.Button(self, text="Clear", command=self.clear, fg="#ffffff", bg="#263942")

        self.buttoncanc.grid(row=3, column=0, pady=10, ipadx=5, ipady=4)
        self.buttonext.grid(row=3, column=1, pady=10, ipadx=5, ipady=4)
        self.buttonclear.grid(row=3, column=2, pady=10, ipadx=5, ipady=4)

    def start_training(self):
        global names

        name = self.user_name.get().strip()
        sid = self.student_id.get().strip()
        cid = self.class_id.get().strip()

        # Kiểm tra các trường có rỗng không
        if not name or not sid or not cid:
            messagebox.showerror("Error", "All fields are required!")
            return

        # Kiểm tra trường hợp đặc biệt
        full_info = f"{name}_{sid}_{cid}"  # Gom 3 thông tin lại

        if full_info == "None_None_None":
            messagebox.showerror("Error", "Invalid input: None_None_None")
            return
        elif full_info in names:
            messagebox.showerror("Error", "User already exists!")
            return

        # Thêm vào tập và chuyển trang
        names.add(full_info)
        self.controller.active_name = full_info
        
        # Cập nhật lại các trang sau khi thay đổi thông tin
       # self.controller.frames["PageTwo"].refresh_names()  # Cập nhật thông tin ở PageTwo
        self.controller.frames["PageThree"].update_info()  # Cập nhật thông tin ở PageThree
        
        self.controller.show_frame("PageThree")  # Chuyển sang PageThree

    def clear(self):
        self.user_name.delete(0, 'end')
        self.student_id.delete(0, 'end')
        self.class_id.delete(0, 'end')
class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="pink")
        self.controller = controller
        
        # Label và Entry cho Tên
        tk.Label(self, text="Enter your name", fg="#263942", font='Helvetica 12 bold').grid(row=0, column=0, padx=10, pady=10)
        self.user_name = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.user_name.grid(row=0, column=1, pady=10, padx=10)

        # Label và Entry cho Mã sinh viên
        tk.Label(self, text="Student ID", fg="#263942", font='Helvetica 12 bold').grid(row=1, column=0, padx=10, pady=10)
        self.student_id = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.student_id.grid(row=1, column=1, pady=10, padx=10)

        # Label và Entry cho Mã lớp
        tk.Label(self, text="Class ID", fg="#263942", font='Helvetica 12 bold').grid(row=2, column=0, padx=10, pady=10)
        self.class_id = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.class_id.grid(row=2, column=1, pady=10, padx=10)
        
        # Các nút chức năng
        self.buttoncanc = tk.Button(self, text="Cancel", command=lambda: controller.show_frame("StartPage"), bg="#ffffff", fg="#263942")
        self.buttonclear = tk.Button(self, text="Clear", command=self.clear, fg="#ffffff", bg="#263942")
        self.buttonext = tk.Button(self, text="Next", command=self.next_foo, fg="#ffffff", bg="#263942")

        self.buttoncanc.grid(row=3, column=0, pady=10, ipadx=5, ipady=4)
        self.buttonext.grid(row=3, column=1, pady=10, ipadx=5, ipady=4)
        self.buttonclear.grid(row=3, column=2, pady=10, ipadx=5, ipady=4)

    def next_foo(self):
        # Lấy giá trị nhập vào
        name = self.user_name.get().strip()
        sid = self.student_id.get().strip()
        cid = self.class_id.get().strip()

        # Kiểm tra các trường có rỗng không
        if not name or not sid or not cid:
            messagebox.showerror("Error", "All fields are required!")
            return

        # Gom thông tin lại để làm tham số cho PageFour
        full_info = f"{name}_{sid}_{cid}"

        # Lưu thông tin này vào controller để sử dụng ở PageFour
        self.controller.active_name = full_info

        # Chuyển đến PageFour
        self.controller.show_frame("PageFour")  

    def clear(self):
        self.user_name.delete(0, 'end')
        self.student_id.delete(0, 'end')
        self.class_id.delete(0, 'end')

class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="pink")
        self.controller = controller
        self.numimglabel = tk.Label(self, text="Number of images captured = 0", font='Helvetica 12 bold', fg="#263942", bg="pink")
        self.numimglabel.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)

        self.capturebutton = tk.Button(self, text="Capture Data Set", fg="#ffffff", bg="#263942", command=self.capimg)
        self.trainbutton = tk.Button(self, text="Train The Model", fg="#ffffff", bg="#263942", command=self.trainmodel)
        self.capturebutton.grid(row=1, column=0, ipadx=5, ipady=4, padx=10, pady=20)
        self.trainbutton.grid(row=1, column=1, ipadx=5, ipady=4, padx=10, pady=20)

        # Label hiển thị thông tin người dùng
        self.user_info_label = tk.Label(self, text="User info: ", font='Helvetica 12 bold', fg="#263942", bg="pink")
        self.user_info_label.grid(row=2, column=0, columnspan=2, pady=10)

    def capimg(self):
        self.numimglabel.config(text=str("Captured Images = 0 "))
        messagebox.showinfo("INSTRUCTIONS", "We will Capture 300 pics of your Face.")
        x = start_capture(self.controller.active_name)
        self.controller.num_of_images = x
        self.numimglabel.config(text=f"Number of images captured = {x}")

    def trainmodel(self):
        if self.controller.num_of_images < 300:
            messagebox.showerror("ERROR", "Not enough Data, Capture at least 300 images!")
            return
        train_classifer(self.controller.active_name)
        messagebox.showinfo("SUCCESS", "The model has been successfully trained!")
        self.controller.show_frame("PageFour")

    def update_info(self):
        # Cập nhật thông tin người dùng
        self.user_info_label.config(text=f"User info: {self.controller.active_name}")


class PageFour(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="pink")
        self.controller = controller

        label = tk.Label(self, text="Face Recognition", font='Helvetica 16 bold',  bg="pink")
        label.grid(row=0, column=0, sticky="ew")
        
        # Thêm nút "Face Recognition" để nhận diện khuôn mặt
        button1 = tk.Button(self, text="Face Recognition", command=self.openwebcam, fg="#ffffff", bg="#263942")
        # Nút "Go to Home Page" để quay lại trang chủ
        button4 = tk.Button(self, text="Go to Home Page", command=lambda: self.controller.show_frame("StartPage"), bg="#ffffff", fg="#263942")
        
        button1.grid(row=1, column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        button4.grid(row=1, column=1, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)

    def openwebcam(self):
        # Lấy thông tin đã gom từ PageOne
        active_name = self.controller.active_name  # Chuỗi gom từ PageOne
        
        # Gọi hàm main_app và truyền tham số active_name
        main_app(active_name)



app = MainUI()
app.iconphoto(True, tk.PhotoImage(file='icon.ico'))
app.mainloop()

