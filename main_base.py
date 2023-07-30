# https://stackoverflow.com/questions/67034284/python-how-to-show-a-transparent-image-in-a-window
from tkinter import Tk, Canvas, PhotoImage, NW

root = Tk()

root.attributes('-transparentcolor','#f0f0f0')

# Image
img = PhotoImage(file="./Yamakaze.png")

# Canvas
canvas = Canvas(root, width=img.width(), height=img.height())
canvas.pack()

# Positioning the Image inside the canvas
canvas.create_image(0, 0, anchor=NW, image=img)

# Starts the GUI
root.mainloop()

# https://python-forum.io/thread-36957.html
# import wx
 
# class Frame(wx.Frame):
 
#     def __init__(self, image, parent=None, id=-1,pos=wx.DefaultPosition, title='wxPython'):
#         temp = image.ConvertToBitmap()
#         size = temp.GetWidth(), temp.GetHeight()
#         wx.Frame.__init__(self, parent, id, title, pos, size)
#         self.bmp = wx.StaticBitmap(parent=self, bitmap=temp)
#         self.SetClientSize(size)
#         self.SetTransparent(100)
 
# class App(wx.App):
#     def OnInit(self):
#         image = wx.Image('Yamakaze.png', wx.BITMAP_TYPE_ANY)
#         self.frame = Frame(image)
#         self.frame.Show()
#         self.SetTopWindow(self.frame)
#         return True
 
# app = App()
# app.MainLoop()