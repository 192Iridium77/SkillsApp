from tkinter import *
import math
import shelve


class DisplaySkills:
    def __init__(self, skill_obj):  # start with just an object, change it to a list of objects later
        window = Tk()
        window.title("Skillsets")

        # create menu bar
        menubar = Menu(window)
        window.config(menu = menubar)
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label='Exit', command=window.quit)

        # build frames
        frame1 = Frame(window)
        frame1.pack()  # TODO create list of frames

        # Create icon images
        self.icon = PhotoImage(file=skill_obj.image_path)  # TODO images list

        # set IMAGE into the frame
        image = Label(frame1, image=self.icon)  # TODO set image to appropriate list index
        image.grid(row=1, column=1, columnspan=2)

        # Create SKILL label above the exp bar
        self.skillLabel = Label(frame1, text=skill_obj.skill_label, justify=LEFT).grid(row=1, column=3)
        # TODO change text string to iterate skill names

        # Create a LEVEL display under the skill
        Label(frame1, text="lv ").grid(row=2, column=1)
        self.level = IntVar()
        self.levelLabel = Label(frame1, textvariable=self.level).grid(row=2, column=2)

        # create canvas for the exp bar
        self.canvas = Canvas(frame1)
        self.canvas["width"] = 220
        self.canvas["height"] = 40
        self.canvas.grid(row=2, column=3)

        # Create a label that displays current exp total
        self.expPoints = IntVar()
        self.expPoints.set(skill_obj.exp_points)
        Label(frame1, textvariable=self.expPoints).grid(row=1, column=4)

        # Draw exp bar with length set to exp progress
        self.progress = 0  # placeholder
        self.calculateLevel()
        self.processProgress()
        self.canvas.create_line(10, 20, 200, 20, fill="#99CC99", width=6)
        self.progressLevel = self.canvas.create_line(10, 20, self.progress, 20, fill="#009900",
                                                     width=6, tags="progress")

        # Buttons used to MODIFY exp points
        self.plusButton = Button(frame1, text="+", command=self.addExp, repeatdelay=20).grid(row=2, column=4)

        window.mainloop()


    def addExp(self):
        exp = self.expPoints.get()
        exp += 1
        # update everything
        self.expPoints.set(exp)
        self.calculateLevel()
        self.processProgress()

    def calculateLevel(self):
        x = float(self.expPoints.get())
        root = math.sqrt(x)
        self.root = root
        lvlint = int(root)
        self.level.set(lvlint)

    def processProgress(self):
        remainder = self.root % 1
        self.progress = math.floor(remainder * 200)
        self.canvas.delete("progress")
        self.progressLevel = self.canvas.create_line(10, 20, self.progress + 10, 20, fill="#009900",
                                                     width=6, tags="progress")

    def resetExp(self):  # TODO make button for this
        self.expPoints.set(0)

    def access_exp(self):
        return self.expPoints.get()


class Skill:
    def __init__(self, image_path, skill_label, exp_points):
        self.image_path = image_path
        self.skill_label = skill_label
        self.exp_points = exp_points
        # you could make this private, set up accessors/mutators
        # and move it to it's own file

    def retrieve_exp_data(self, exp):
        self.exp_points = exp


def main():
    # coding = Skill("images/coding.png", "Coding", 10)  # you may want a list of skill sets for user to select from
    coding = load_set()  # TODO initial setup for new user
    tk_window = DisplaySkills(coding)
    # retried exp value from tkinter, a stupidly difficult task
    coding.retrieve_exp_data(tk_window.access_exp())
    # save the coding object
    save_set(coding)


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
