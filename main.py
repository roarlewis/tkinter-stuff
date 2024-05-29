import tkinter as tk

root = tk.Tk()
root.geometry("800x500")
root.title("LewisVideoSynth")

header = tk.Label(root, text="Lewis's Video Synth", font=('DevLys 010', 30),bg="lightblue",fg="red",width=1000)
header.pack(padx=20,pady=10)

root.mainloop()