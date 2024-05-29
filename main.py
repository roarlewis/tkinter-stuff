import cv2
import numpy as np
from collections import deque
from moviepy.editor import VideoFileClip
import tkinter as tk
from tkinter import filedialog

class EpicApp:

    filename = ""
    directory = ""

    tint_on = False

    echo_frames = 10
    echo_decay = 0.5

    distort_on = False

    save_name = "new_video"

    def __init__(self):
        global red_scale,blue_scale,green_scale, x_amp_distort_scale, y_amp_distort_scale, user_file_name_box
        self.root = tk.Tk()
        self.root.geometry("800x500")
        self.root.title("LewisVideoSynth")
        header = tk.Label(self.root, text="Lewis's Video Synth", font=('DevLys 010', 30), bg="lightblue", fg="red",
                          width=1000)
        header.pack(padx=20, pady=10)

        import_button = tk.Button(self.root,text="IMPORT FILE", font = ('DevLys 010', 25),bg="lightblue",fg="darkblue",command = self.import_file)
        import_button.place(x=600,y=350)

        directory_button = tk.Button(self.root, text = "SAVE TO", font = ('DevLys 010', 25),bg="lightblue",fg="darkblue",command = self.select_directory)
        directory_button.place(x=600,y=400)

        distort_on_button = tk.Checkbutton(self.root,text="distortion", font = ('DevLys 010', 25),bg="lightblue",fg="darkblue",command=self.change_distort_state)
        distort_on_button.place(x=30,y=450)

        tint_on_button = tk.Checkbutton(self.root,text = "tint", font = ('DevLys 010', 25),bg="lightblue",fg="darkblue", command=self.change_tint_state)
        tint_on_button.place(x=30,y = 250)

        red_scale = tk.Scale(self.root,from_=255, to=-255)
        green_scale = tk.Scale(self.root,from_=255, to=-255)
        blue_scale = tk.Scale(self.root,from_=255, to=-255)

        red_scale.place(x=0,y=100)
        green_scale.place(x=60,y=100)
        blue_scale.place(x=120,y=100)

        red_label = tk.Label(self.root,text="R", font = ('DevLys 010', 20),fg="red")
        red_label.place(x=30,y=210)

        green_label = tk.Label(self.root,text="G", font=('DevLys 010', 20),fg="green")
        green_label.place(x=90, y=210)

        blue_label = tk.Label(self.root,text="B", font=('DevLys 010', 20),fg="blue")
        blue_label.place(x=150, y=210)

        test_button = tk.Button(self.root,text="MAKE VIDEO",font = ('DevLys 010', 25),command = self.change_video, fg="darkblue", bg="lightblue")
        test_button.place(x=600,y=450)

        x_amp_distort_scale = tk.Scale(self.root, from_=10,to=0, resolution=0.1)
        y_amp_distort_scale = tk.Scale(self.root, from_=10, to=0, resolution=0.1)

        x_amp_distort_scale.place(x=30, y=350)
        y_amp_distort_scale.place(x=80, y=350)

        save_as_label = tk.Label(self.root, text="SAVE AS:", font=('DevLys 010', 25), bg="lightblue",
                                           fg="darkblue")
        save_as_label.place(x=225, y=450)

        save_as_label = tk.Label(self.root, text=".mp4", font=('DevLys 010', 25), bg="lightblue",
                                 fg="darkblue")
        save_as_label.place(x=530, y=450)

        def is_valid_char(char):
            # Define what constitutes a valid character for file names
            valid_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_."
            return char in valid_chars

        def validate_entry(char, entry_text):
            if is_valid_char(char):
                return True
            else:
                return False

        vcmd = (self.root.register(validate_entry), '%S', '%P')
        user_file_name_box = tk.Entry(self.root, font=(18),validate="key", validatecommand=vcmd)
        user_file_name_box.place(width = 170, height = 35, x = 350, y = 450)



        self.root.mainloop()

    def import_file(self):
        self.root.filename = filedialog.askopenfilename(title="select a file")

    def select_directory(self):
        self.root.directory = filedialog.askdirectory(title = "choose where u want it saved")

    def change_video(self):
        previous_frames = deque(maxlen=self.echo_frames)
        def apply_warp(frame):
            # Get frame dimensions
            h, w, _ = frame.shape

            # Create a meshgrid of x and y coordinates
            x, y = np.meshgrid(np.arange(w), np.arange(h))

            # Apply warp/distortion effect (e.g., sinusoidal distortion)
            distorted_x = x + x_amp_distort_scale.get() * np.sin(2 * np.pi * y / 30.0)
            distorted_y = y + y_amp_distort_scale.get() * np.cos(2 * np.pi * x / 20.0)

            # Clip distorted coordinates to frame dimensions
            distorted_x = np.clip(distorted_x, 0, w - 1)
            distorted_y = np.clip(distorted_y, 0, h - 1)

            # Map distorted coordinates to original frame
            warped_frame = cv2.remap(frame, distorted_x.astype(np.float32), distorted_y.astype(np.float32),
                                     cv2.INTER_LINEAR)

            return warped_frame

        def apply_echo_effect(self,frame):
            # Add the current frame to the queue
            previous_frames.append(frame)

            # Initialize an empty frame for the effect
            echo_frame = np.zeros_like(frame, dtype=np.float32)

            # Blend each previous frame with the current frame
            for i, prev_frame in enumerate(previous_frames):
                echo_frame += (self.echo_decay ** i) * prev_frame

            # Normalize and convert to uint8
            echo_frame = np.clip(echo_frame, 0, 255).astype(np.uint8)
            return echo_frame

        def apply_color_effect(self,frame):
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Convert back to BGR to apply color tint
            gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

            tinted = gray_bgr + np.array([red_scale.get(), green_scale.get(), blue_scale.get()], dtype=np.uint8)
            return tinted

        def process_frame(frame):
            if self.distort_on:
                frame = apply_warp(frame)
            frame = apply_color_effect(self,frame)
            frame = apply_echo_effect(self,frame)
            return frame

        input_video_path = self.root.filename
        # input_video_path = '/Users/lewislibbywatt/Downloads/IMG_7683.MOV'
        output_video_path = self.root.directory + '/' + user_file_name_box.get() + '.mp4'

        clip = VideoFileClip(input_video_path)
        modified_clip = clip.fl_image(process_frame)
        modified_clip.write_videofile(output_video_path, codec='libx264')

    def print_stuff(self):
        print(self.distort_on)
        print(red_scale.get())
        print(blue_scale.get())
        print(green_scale.get())

    def change_distort_state(self):
        self.distort_on = not self.distort_on

    def change_tint_state(self):
        self.tint_on = not self.tint_on




EpicApp()
