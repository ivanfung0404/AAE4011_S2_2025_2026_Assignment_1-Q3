#!/usr/bin/env python3
import rospy
import rosbag
import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from ultralytics import YOLO

class VehicleDetectionApp:
    def __init__(self, root, bag_path, topic_name):
        self.root = root
        self.root.title("Vehicle Detector Dashboard")
        self.root.geometry("1280x720")
        self.root.resizable(True, True)
        
        # Apply Modern Theme
        self.style = ttk.Style(self.root)
        self.style.theme_use('clam')
        self.configure_styles()
        
        self.bag_path = bag_path
        self.topic_name = topic_name
        
        print("Loading YOLO model...")
        self.model = YOLO('yolov8n.pt')
        
        # State variables
        self.frames = []  
        self.total_frames = 0
        self.current_frame_idx = 0
        self.is_playing = False
        self.after_id = None
        
        self.load_bag_into_memory()
        self.setup_ui()
        
        if self.total_frames > 0:
            self.process_and_show_frame(0)

    def configure_styles(self):
        """Setup ultra-modern dark theme colors and fonts"""
        BG_MAIN = "#121212"
        BG_SIDEBAR = "#1E1E1E"
        BG_BOTTOM = "#181818"
        ACCENT = "#00A2FF"
        TEXT_LIGHT = "#FFFFFF"
        TEXT_MUTED = "#A0A0A0"
        
        self.root.configure(bg=BG_MAIN)
        
        # Frame Styles
        self.style.configure('Main.TFrame', background=BG_MAIN)
        self.style.configure('Sidebar.TFrame', background=BG_SIDEBAR)
        self.style.configure('Bottom.TFrame', background=BG_BOTTOM)
        
        # Label Styles
        self.style.configure('Header.TLabel', background=BG_SIDEBAR, foreground=ACCENT, font=("Segoe UI", 16, "bold"))
        self.style.configure('SubHeader.TLabel', background=BG_SIDEBAR, foreground=TEXT_MUTED, font=("Segoe UI", 10, "bold"))
        
        self.style.configure('FrameText.TLabel', background=BG_SIDEBAR, foreground=TEXT_LIGHT, font=("Segoe UI", 12))
        self.style.configure('FrameNum.TLabel', background=BG_SIDEBAR, foreground=ACCENT, font=("Segoe UI", 14, "bold"))
        
        self.style.configure('BigNumTitle.TLabel', background=BG_SIDEBAR, foreground=TEXT_LIGHT, font=("Segoe UI", 12))
        self.style.configure('BigNum.TLabel', background=BG_SIDEBAR, foreground="#FFB900", font=("Segoe UI", 36, "bold"))
        
        self.style.configure('StatusPlay.TLabel', background=BG_SIDEBAR, foreground="#00FF41", font=("Segoe UI", 11, "bold"))
        self.style.configure('StatusStop.TLabel', background=BG_SIDEBAR, foreground="#F44336", font=("Segoe UI", 11, "bold"))
        
        # Button & Slider
        self.style.configure('Play.TButton', font=("Segoe UI", 11, "bold"), padding=6)
        self.style.configure('TScale', background=BG_BOTTOM, troughcolor="#333333")

    def load_bag_into_memory(self):
        print("Pre-loading rosbag into memory... Please wait.")
        bag = rosbag.Bag(self.bag_path, 'r')
        for topic, msg, t in bag.read_messages(topics=[self.topic_name]):
            self.frames.append(msg.data)
        bag.close()
        self.total_frames = len(self.frames)
        print(f"Loaded {self.total_frames} frames.")

    def setup_ui(self):
        # Bottom side: Control Panel
        self.control_frame = ttk.Frame(self.root, height=70, style='Bottom.TFrame')
        self.control_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.btn_play = ttk.Button(self.control_frame, text="▶ PLAY", style='Play.TButton', command=self.toggle_play, width=10)
        self.btn_play.pack(side=tk.LEFT, padx=25, pady=15)
        
        self.slider = ttk.Scale(self.control_frame, from_=1, to=self.total_frames, orient=tk.HORIZONTAL)
        self.slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=20, pady=20)
        
        self.slider.bind("<ButtonRelease-1>", self.on_slider_release)
        self.slider.bind("<ButtonPress-1>", self.on_slider_press)

        # Right side: Sidebar Dashboard
        self.stats_frame = ttk.Frame(self.root, width=360, style='Sidebar.TFrame')
        self.stats_frame.pack(side=tk.RIGHT, fill=tk.Y)
        self.stats_frame.pack_propagate(False) 
        
        self.inner_stats = ttk.Frame(self.stats_frame, style='Sidebar.TFrame')
        self.inner_stats.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Title
        ttk.Label(self.inner_stats, text="SYSTEM DASHBOARD", style='Header.TLabel').pack(anchor="w", pady=(0, 5))
        self.lbl_status = ttk.Label(self.inner_stats, text="● PAUSED", style='StatusStop.TLabel')
        self.lbl_status.pack(anchor="w", pady=(0, 20))
        
        ttk.Separator(self.inner_stats, orient='horizontal').pack(fill='x', pady=10)
        
        # Frame Counter Box
        frame_box = ttk.Frame(self.inner_stats, style='Sidebar.TFrame')
        frame_box.pack(fill=tk.X, pady=10)
        ttk.Label(frame_box, text="FRAME", style='SubHeader.TLabel').pack(anchor="w")
        self.lbl_frame_count = ttk.Label(frame_box, text=f"0 / {self.total_frames}", style='FrameNum.TLabel')
        self.lbl_frame_count.pack(anchor="w", pady=2)
        
        ttk.Separator(self.inner_stats, orient='horizontal').pack(fill='x', pady=10)
        
        # Big Target Number
        ttk.Label(self.inner_stats, text="TOTAL VEHICLES", style='BigNumTitle.TLabel').pack(anchor="center", pady=(10, 0))
        self.lbl_vehicle_count = ttk.Label(self.inner_stats, text="0", style='BigNum.TLabel')
        self.lbl_vehicle_count.pack(anchor="center", pady=(0, 10))
        
        ttk.Separator(self.inner_stats, orient='horizontal').pack(fill='x', pady=10)
        
        # Terminal-Style Detection Log
        ttk.Label(self.inner_stats, text="TARGET LOG", style='SubHeader.TLabel').pack(anchor="w", pady=(10, 5))
        
        self.txt_detections = tk.Text(self.inner_stats, height=12, width=30, 
                                      font=("Consolas", 11), bg="#0A0A0A", fg="#00FF41", 
                                      bd=0, highlightthickness=1, highlightbackground="#333333", 
                                      padx=10, pady=10)
        self.txt_detections.pack(fill=tk.BOTH, expand=True, pady=5)

        # Left side: Video Frame
        self.video_frame = ttk.Frame(self.root, style='Main.TFrame')
        self.video_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        self.video_label = tk.Label(self.video_frame, bg="#000000")
        self.video_label.pack(expand=True)

    def process_and_show_frame(self, index):
        if index >= self.total_frames:
            if self.is_playing:
                self.toggle_play() 
            return
            
        raw_data = self.frames[index]
        np_arr = np.frombuffer(raw_data, np.uint8)
        cv_img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        
        small_img = cv2.resize(cv_img, (880, 660))
        results = self.model(small_img, classes=[2, 3, 5, 7], imgsz=480, verbose=False)
        annotated_frame = results[0].plot()
        
        boxes = results[0].boxes
        current_detections = len(boxes)
        
        # Update Terminal Text Log smoothly
        self.txt_detections.delete(1.0, tk.END)
        if current_detections > 0:
            for box in boxes:
                cls_id = int(box.cls[0].item())
                conf = float(box.conf[0].item())
                class_name = self.model.names[cls_id].upper()
                
                # Format perfectly aligned text: "► CAR           85.2%"
                log_entry = f"► {class_name:<12} {conf*100:>6.1f}%\n"
                self.txt_detections.insert(tk.END, log_entry)
        else:
            self.txt_detections.insert(tk.END, "\n  [ NO TARGETS ACQUIRED ]")
            
        self.lbl_frame_count.config(text=f"{index + 1} / {self.total_frames}")
        self.lbl_vehicle_count.config(text=f"{current_detections}")
        
        self.slider.set(index + 1)
        
        rgb_image = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_image)
        tk_image = ImageTk.PhotoImage(image=pil_image)
        
        self.video_label.imgtk = tk_image
        self.video_label.configure(image=tk_image)
        self.current_frame_idx = index

    def play_loop(self):
        if self.is_playing:
            next_idx = self.current_frame_idx + 1
            if next_idx < self.total_frames:
                self.process_and_show_frame(next_idx)
                self.after_id = self.root.after(10, self.play_loop)
            else:
                self.toggle_play()

    def toggle_play(self):
        if self.is_playing:
            self.is_playing = False
            self.btn_play.config(text="▶ PLAY")
            self.lbl_status.config(text="● PAUSED", style='StatusStop.TLabel')
            if self.after_id:
                self.root.after_cancel(self.after_id)
                self.after_id = None
        else:
            if self.current_frame_idx >= self.total_frames - 1:
                self.current_frame_idx = -1 
                
            self.is_playing = True
            self.btn_play.config(text="⏸ PAUSE")
            self.lbl_status.config(text="● PLAYING", style='StatusPlay.TLabel')
            self.play_loop()

    def on_slider_press(self, event):
        if self.is_playing:
            self.toggle_play()

    def on_slider_release(self, event):
        target_frame = int(self.slider.get()) - 1
        if target_frame != self.current_frame_idx:
            self.process_and_show_frame(target_frame)

if __name__ == '__main__':
    rospy.init_node('vehicle_detector_node', anonymous=True)
    bag_path = '/mnt/c/Users/ivanf/Downloads/2026-02-23-15-58-29.bag'
    topic_name = '/hikcamera/image_1/compressed'
    
    root = tk.Tk()
    app = VehicleDetectionApp(root, bag_path, topic_name)
    root.mainloop()
