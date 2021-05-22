from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from functools import partial
from shutil import copyfile
import os

WRITE_TXT_FILE = 0  # Save method, write your labels to "labels.txt" file
SPLIT_IN_DIR = 1    # Save method, create data directory to store your labels
DO_BOTH = 2         # Save method, do both WRITE_TXT_FILE and SPLIT_IN_DIR

WRITE_NUMBER = 0    # Write method, write in format: images_name,labels_in_number
WRITE_NAME = 1      # Write method, write in format: images_name,labels_in_name

# Dynamic variables
source_path = "images"  # Where you push your images into
destination_path = "done"   # Where you done images go
list_of_label_names = ["DOG", "CAT", "NOISE"]   # Label names
list_of_label_numbers = [1, 0, -1]  # Label numbers
save_mt = WRITE_TXT_FILE       # Save method
mov_to_done = False     # Move to done directory or not
write_mt = WRITE_NAME   # Write method
clear_txt_file = False  # Clear your "labels.txt" before running


image_list = os.listdir(source_path)


class App(Frame):
    def __init__(self, master=None, src_path=None, img_list=None, des_path=None, labels_list=None, nums_list=None,
                 save_method=2, write_method=0, move_to_done=None, clear_f=False):
        Frame.__init__(self, master)
        self.master = master
        self.src_path = src_path
        self.img_list = img_list
        self.des_path = des_path
        self.labels_list = labels_list
        self.nums_list = nums_list
        self.save_method = save_method
        if self.save_method == 1 or self.save_method == 2:
            self.data_dir_name = "data"
            if self.data_dir_name not in os.listdir():
                os.mkdir(self.data_dir_name)
            for label_dir in self.labels_list:
                if label_dir.lower() not in os.listdir(self.data_dir_name):
                    os.mkdir(self.data_dir_name + "/" + label_dir.lower())

        self.write_method = write_method
        self.move_to_done = move_to_done
        self.clear_f = clear_f
        if self.clear_f:
            with open("labels.txt", "w"):
                pass

        self.pack(fill=BOTH, expand=1)

        self.bg = "#FFE4C4"
        self["bg"] = self.bg

        self.index = 0
        self.choice, self.choice_name = None, None
        self.no_labels = len(self.labels_list)
        self.btn_length = 130
        self.btn_labels_list = []

        self.marx, self.mary = 20, 20
        self.space_bw_btn = (1080 - 2 * self.marx - self.btn_length * self.no_labels) / self.no_labels
        self.lb_space_x, self.lb_space_y = self.space_bw_btn//2, 600
        self.img_label = self.load_img(src_path + "/" + img_list[self.index], self.marx, self.mary)
        self.lb_label = self.add_label("LABELS:", 480, 520, ("Times", "24", "bold"))

        for i in range(len(self.labels_list)):
            action_with_arg = partial(self.btn_label_action, i)
            btn = self.add_button(f"{self.nums_list[i]} ({self.labels_list[i]})", ("Times", "16", "bold"),
                                  (self.space_bw_btn + self.btn_length)*i + self.lb_space_x + self.marx, self.lb_space_y,
                                  "#87CEEB", "black", command=action_with_arg)
            self.btn_labels_list.append(btn)

        self.btn_next = self.add_button("NEXT", ("Times", "16", "bold"), 850, 350, "yellow", "red", command=self.btn_next_action)
        self.btn_finish = self.add_button("FINISH", ("Times", "16", "bold"), 850, 100, "#708090", "#800000", command=self.btn_finish_action)

    def load_img(self, path, x, y):
        img = ImageTk.PhotoImage(Image.open(path).resize((720, 480)))
        label = Label(self, image=img)
        label.image = img
        label.place(x=x, y=y)
        return label

    def add_label(self, text, x, y, font):
        label = Label(self, text=text, font=font, bg=self.bg)
        label.place(x=x, y=y)
        return label

    def add_button(self, text, font, x, y, bg, fg, command=None):
        button = Button(self, text=text, font=font, width=10, height=2, bg=bg, fg=fg, command=command)
        button.place(x=x, y=y)
        return button

    def reset(self):
        self.choice, self.choice_name = None, None
        for btn in self.btn_labels_list:
            btn["bg"] = "#87CEEB"
            btn["fg"] = "black"

    def btn_label_action(self, index):
        self.reset()
        self.choice = self.nums_list[index]
        self.choice_name = self.labels_list[index]
        self.btn_labels_list[index]["bg"] = "green"
        self.btn_labels_list[index]["fg"] = "red"

    def btn_next_action(self):
        if self.choice is None:
            messagebox.showerror("Error", "You have to choose label!")
        else:
            if self.index < len(self.img_list):
                if self.save_method == 0 or self.save_method == 2:
                    with open("labels.txt", "a") as file:
                        if self.write_method == 0:
                            file.write(self.img_list[self.index] + "," + str(self.choice))
                        else:
                            file.write(self.img_list[self.index] + "," + str(self.choice_name.lower()))
                        file.write("\n")
                if self.save_method == 1 or self.save_method == 2:
                    copyfile(self.src_path + "/" + self.img_list[self.index],
                             self.data_dir_name + "/" + self.choice_name.lower() + "/" + self.img_list[self.index])

                if self.move_to_done:
                    os.replace(self.src_path + "/" + self.img_list[self.index], self.des_path + "/" + self.img_list[self.index])

            self.index += 1
            if self.index < len(self.img_list):
                self.img_label = self.load_img(self.src_path + "/" + self.img_list[self.index], self.marx, self.mary)
            else:
                messagebox.showinfo('Infor', "Finish Work!")
                self.master.destroy()
            self.reset()

    def btn_finish_action(self):
        self.master.destroy()


root = Tk()
app = App(root, source_path, image_list, destination_path, list_of_label_names, list_of_label_numbers,
          save_mt, write_mt, mov_to_done, clear_txt_file)
root.wm_title("Image Labeling")
root.geometry("1080x720")
root.resizable(0, 0)
root.mainloop()
