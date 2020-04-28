from tkinter import *

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()

    def window_init(self):
        self.master.title('welcome to video-captioning system')
        width, height = self.master.maxsize()
        self.master.geometry("{}x{}".format(width, height))

    def createWidgets(self):
        # fm1
        self.fm1 = Frame(self)
        self.titleLabel = Label(self.fm1, text='video-captioning system')
        self.titleLabel.pack()
        self.fm1.pack(side=TOP)

        # fm2
        self.fm2 = Frame(self)
        self.fm2_left = Frame(self.fm2)
        self.fm2_right = Frame(self.fm2)
        self.fm2_left_top = Frame(self.fm2_left)
        self.fm2_left_bottom = Frame(self.fm2_left)

        self.predictButton = Button(self.fm2_left_top, text='predict sentence')
        self.predictButton.pack(side=LEFT)
        self.predictEntry = Entry(self.fm2_left_top)
        self.predictEntry.pack(side=LEFT)
        self.fm2_left_top.pack(side=TOP)

        self.truthButton = Button(self.fm2_left_bottom, text='ground truth')
        self.truthButton.pack(side=LEFT)
        self.truthEntry = Entry(self.fm2_left_bottom)
        self.truthEntry.pack(side=LEFT)
        self.fm2_left_bottom.pack(side=TOP)

        self.fm2_left.pack(side=LEFT)
        self.nextVideoButton = Button(self.fm2_right, text='next video')
        self.nextVideoButton.pack()
        self.fm2_right.pack(side=LEFT)

        self.fm2.pack(side=TOP)

        # fm3
        self.fm3 = Frame(self)
        load = Image.open('/home/hl/Desktop/lovelyqian/me.jpg')
        print(load)
        render = ImageTk.PhotoImage(load)

        self.img = Label(self.fm3, image=render)
        self.img.image = render
        self.img.pack()
        self.fm3.pack(side=TOP)

if __name__=='__main__':
    app = Application()
    # to do
    app.mainloop()