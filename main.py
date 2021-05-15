from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os


class App(Frame):
    def __init__(self, master=None, path=None, img_list=None):
        Frame.__init__(self, master)
        self.master = master
        self.path = path
        self.img_list = img_list
        self.pack(fill=BOTH, expand=1)

        self.index = 0
        self.choice = None

        self.img_label = self.load_img(path + "/" + img_list[self.index], 0, 0)
        self.lb_label = self.add_label("LABELS:", 100, 300)
        self.btn_wrong = self.add_button("0 (WRONG)", 0, 350, command=self.btn_wrong_action)
        self.btn_right = self.add_button("1 (RIGHT)", 100, 350, command=self.btn_right_action)
        self.btn_noise = self.add_button("-1 (NOISE)", 200, 350, command=self.btn_noise_action)
        self.btn_next = self.add_button("NEXT", 400, 350, command=self.btn_next_action)

    def load_img(self, path, x, y):
        img = ImageTk.PhotoImage(Image.open(path).resize((300, 200)))
        label = Label(self, image=img)
        label.image = img
        label.place(x=x, y=y)
        return label

    def add_label(self, text, x, y):
        label = Label(self, text=text)
        label.place(x=x, y=y)
        return label

    def add_button(self, text, x, y, command=None):
        button = Button(self, text=text, width=10, height=2, bg="white", fg="black", command=command)
        button.place(x=x, y=y)
        return button

    def reset(self):
        self.choice = None
        self.btn_wrong["bg"] = "white"
        self.btn_wrong["fg"] = "black"
        self.btn_right["bg"] = "white"
        self.btn_right["fg"] = "black"
        self.btn_noise["bg"] = "white"
        self.btn_noise["fg"] = "black"

    def btn_wrong_action(self):
        self.reset()
        self.choice = 0
        self.btn_wrong["bg"] = "green"
        self.btn_wrong["fg"] = "red"

    def btn_right_action(self):
        self.reset()
        self.choice = 1
        self.btn_right["bg"] = "green"
        self.btn_right["fg"] = "red"

    def btn_noise_action(self):
        self.reset()
        self.choice = -1
        self.btn_noise["bg"] = "green"
        self.btn_noise["fg"] = "red"

    def btn_next_action(self):
        if self.choice is None:
            messagebox.showerror("Error", "You have to choose label!")
        else:
            if self.index < len(self.img_list):
                with open("labels.txt", "a") as file:
                    file.write("\n")
                    file.write(img_list[self.index] + "," + str(self.choice))
                os.replace(self.path + "/" + self.img_list[self.index], "done/" + self.img_list[self.index])

            self.index += 1
            if self.index < len(self.img_list):
                self.img_label = self.load_img(path + "/" + img_list[self.index], 0, 0)
            else:
                messagebox.showinfo("Infor", "Finish Work!")
                self.master.destroy()
            self.reset()


path = "images"
img_list = os.listdir(path)

root = Tk()
app = App(root, path, img_list)
root.wm_title("Tkinter window")
root.geometry("500x500")
root.mainloop()


# khi het anh???