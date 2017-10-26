# This version is meant to iterate through a series of skills and display them in separate frames
# had to work around tkinter so that it would assign the correct command to each button, thus there is
# a 6 item limit to the number of skills, though it's possible to add more, I don't think it's necessary.

from tkinter import *
import math
import shelve
import time
import os.path
import pygame


class DisplaySkills:
    def __init__(self, skill_obj_list):
        window = Tk()
        window.title("Skillsets")

        # create menu bar
        menubar = Menu(window)
        window.config(menu = menubar)
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label='Exit', command=window.quit)

        # build frames
        frame_list = []
        icon_list = []
        self.exp_points_list = []
        self.forms_list = []
        self.level_list = []
        self.canvas_list = []
        for i in range(len(skill_obj_list)):
            frame_list.append(Frame(window))
            frame_list[i].pack()

            # Create icon images
            icon_list.append(PhotoImage(file=skill_obj_list[i].image_path))

            # set IMAGE into the frame
            Label(frame_list[i], image=icon_list[i]).grid(row=1, column=1, columnspan=2)

            # Create SKILL label above the exp bar
            Label(frame_list[i], text=skill_obj_list[i].skill_label,
                                    justify=LEFT).grid(row=1, column=3)

            # Create a LEVEL display under the skill
            Label(frame_list[i], text="lv ").grid(row=2, column=1)
            self.level_list.append(IntVar())
            Label(frame_list[i], textvariable=self.level_list[i]).grid(row=2, column=2)

            # create canvas for the exp bar
            self.canvas_list.append(Canvas(frame_list[i]))
            self.canvas_list[i]["width"] = 440
            self.canvas_list[i]["height"] = 80
            self.canvas_list[i].grid(row=2, column=3)

            # Create a label that displays current exp total
            self.exp_points_list.append(IntVar())
            self.exp_points_list[i].set(skill_obj_list[i].exp_points)
            Label(frame_list[i],
                  textvariable=self.exp_points_list[i]).grid(row=1, column=4,
                                                             columnspan=2)

            # retrieve the form value so you can display correct image
            self.forms_list[i].append(IntVar())
            self.forms_list[i].set(skill_obj_list[i].form)

            # Draw exp bar with length set to exp progress
            self.progress = 0  # placeholder
            self.calculateLevel(i)
            self.processProgress(i)
            self.canvas_list[i].create_line(20, 40, 400, 40, fill="#99CC99",
                                            width=8)
            self.canvas_list[i].create_line(20, 40, self.progress, 40, fill="#009900",
                                                         width=8, tags="progress")

        # Buttons used to MODIFY exp points, has to be done outside of loop otherwise tkinter sets each
        # button parameter to i = 3
        try:
            Button(frame_list[0], text="+", command= lambda :
                   self.addExp(0)).grid(row=2, column=5)
            Button(frame_list[1], text="+", command= lambda :
                   self.addExp(1)).grid(row=2, column=5)
            Button(frame_list[2], text="+", command= lambda :
                   self.addExp(2)).grid(row=2, column=5)
            Button(frame_list[3], text="+", command= lambda :
                   self.addExp(3)).grid(row=2, column=5)
            Button(frame_list[4], text="+", command= lambda :
                   self.addExp(4)).grid(row=2, column=5)
            Button(frame_list[5], text="+", command= lambda :
                   self.addExp(5)).grid(row=2, column=5)
        except IndexError:
            pass

        try:
            Button(frame_list[0], text="-", command= lambda : self.takeExp(0)).grid(row=2, column=4)
            Button(frame_list[1], text="-", command= lambda : self.takeExp(1)).grid(row=2, column=4)
            Button(frame_list[2], text="-", command= lambda : self.takeExp(2)).grid(row=2, column=4)
            Button(frame_list[3], text="-", command= lambda : self.takeExp(3)).grid(row=2, column=4)
            Button(frame_list[4], text="-", command= lambda : self.takeExp(4)).grid(row=2, column=4)
            Button(frame_list[5], text="-", command= lambda : self.takeExp(5)).grid(row=2, column=4)
        except IndexError:
            pass

        pygame.mixer.init()
        window.mainloop()


    def addExp(self, i):
        try:
            up_sound = pygame.mixer.Sound("sounds/up.wav")
        except:
            raise UserWarning("Sound file not found.")
        up_sound.set_volume(0.4)
        up_sound.play()

        self.logger()
        exp = self.exp_points_list[i].get()
        exp += 1
        # update everything
        self.exp_points_list[i].set(exp)
        self.calculateLevel(i)
        self.processProgress(i)
        self.determineForm(i)

    def takeExp(self, i):
        try:
            down_sound = pygame.mixer.Sound("sounds/down.wav")
        except:
            raise UserWarning("Sound file not found.")
        down_sound.set_volume(0.4)
        down_sound.play()

        self.logger()
        exp = self.exp_points_list[i].get()
        exp -= 1
        # update everything
        self.exp_points_list[i].set(exp)
        self.calculateLevel(i)
        self.processProgress(i)

    def logger(self):
        #if os.path.isfile("log.txt"):
            #log_file = open('log.txt', 'r')
            #date = time.
            # TODO finish writing date adding
        # create logging file if not present and append data to it if it's
        # there
        if not os.path.isfile("log.txt"):
            log_file = open('log.txt', 'w')
            entry = time.strftime('%d-%m-%Y | %I:%M:%S %p |') + "\n"
            log_file.write(entry)
            log_file.close()
        else:
            log_file = open('log.txt', 'a')
            entry = time.strftime('%d-%m-%Y | %I:%M:%S %p |') + "\n"
            log_file.write(entry)
            log_file.close()

    def calculateLevel(self, i):
        x = float(self.exp_points_list[i].get())
        root = math.sqrt(x)
        self.root = root
        lvlint = int(root)
        self.level_list[i].set(lvlint)

    def determineForm(self, i):
        remainder = self.root % 1
        this_form = self.forms_list[i].get() # should return 0, 1, 2
        lvl = int(self.root)
        if remainder == 0 and lvl <= 19:
            this_form = 0
        elif remainder == 0 and 19 < lvl < 39:  # TODO make these numbers
        # intrinsic
            this_form = 1
        else:
            this_form = 2
        # sanity check:
        print(this_form)

    def processProgress(self, i):
        remainder = self.root % 1
        self.progress = math.floor(remainder * 400)
        self.canvas_list[i].delete("progress")
        self.canvas_list[i].create_line(20, 40, self.progress + 20, 40,
                                        fill="#009900", width=8, tags="progress")

    def resetExp(self, i):  # TODO set up a menu option to implement this
        self.exp_points_list[i].set(0)

    def access_exp(self, i):
        return self.exp_points_list[i].get()


class Skill:
    def __init__(self, image_path, skill_label, exp_points, form):
        self.image_path = image_path
        self.skill_label = skill_label
        self.exp_points = exp_points
        self.form = form # 0, 1, 2

    def retrieve_exp_data(self, exp):
        self.exp_points = exp

    def retrieve_form(self, form):
        self.form = form



def main():
    try:
        skill_obj_list = load_set()
    except KeyError:
        coding = Skill("images/snek.png", "Coding", 764, 0)
        physics = Skill("images/chimpit.png", "Physics", 414, 0)
        chemistry = Skill("images/alkalion.png", "Chemistry", 391, 0)
        maths = Skill("images/fitale.png", "Maths", 504, 0)

        skill_obj_list = [coding, physics, chemistry, maths]

    tk_window = DisplaySkills(skill_obj_list)
    # retrieve exp value from tkinter, a stupidly difficult task
    # this can only be done while the window is closing
    for i in range(len(skill_obj_list)):
        skill_obj_list[i].retrieve_exp_data(tk_window.access_exp(i))
    # save the coding object
    save_set(skill_obj_list)


def save_set(skill_set):
    shelf_file = shelve.open('object_data')
    shelf_file['skills'] = skill_set
    shelf_file.close()


def load_set():
    shelf_file = shelve.open('object_data')
    stored_list = shelf_file['skills']
    shelf_file.close()

    return stored_list


main()
