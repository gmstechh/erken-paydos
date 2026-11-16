import tkinter as tk
import math
import ctypes

class ErkenPaydosApp:
    def __init__(self, root):
        self.root = root
        
        # Açılıştaki siyah ekranı gizle
        self.root.withdraw()
        
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        self.root.geometry(f"{self.screen_width}x{self.screen_height}+0+0")
        
        self.trans_color = '#abcdef'
        self.root.config(bg=self.trans_color)
        self.root.attributes("-transparentcolor", self.trans_color)
        
        self.canvas = tk.Canvas(root, width=self.screen_width, height=self.screen_height, 
                                bg=self.trans_color, highlightthickness=0)
        self.canvas.pack()
        
        self.mascot_x = -100
        self.shutter_y = 0
        self.walk_speed = 4
        self.step_count = 0
        self.shutter_speed = 6  
        self.throw_t = 0.0
        
        self.has_lasso = True 
        
        self.root.bind("<Escape>", lambda e: self.root.destroy())
        
        # Şeffaflık hazır olunca göster
        self.root.deiconify()
        self.root.after(1000, self.animate_walk_in)

    def draw_character(self, pose="walk", direction=1, hand_y=None):
        self.canvas.delete("mascot")
        x = self.mascot_x
        y = self.screen_height - 60
        
        phase = self.step_count * 0.25
        leg_swing = 0 if pose != "walk" else math.sin(phase) * 25
        arm_swing = 0 if pose != "walk" else math.sin(phase) * 20
        bounce = 0 if pose != "walk" else abs(math.cos(phase)) * 4
        
        y -= bounce

        if pose == "walk":
            left_foot_x, right_foot_x = x - leg_swing, x + leg_swing
            left_hand_x, left_hand_y = x + arm_swing, y - 40
            right_hand_x, right_hand_y = x - arm_swing, y - 40
        elif pose == "stand":
            left_foot_x, right_foot_x = x - 10, x + 10
            left_hand_x, left_hand_y = x - 12, y - 40
            right_hand_x, right_hand_y = x + 12, y - 40
        elif pose == "throw_ready":
            left_foot_x, right_foot_x = x - 10, x + 10
            left_hand_x, left_hand_y = x - 12, y - 180
            right_hand_x, right_hand_y = x + 12, y - 180
        elif pose == "pull":
            left_foot_x, right_foot_x = x - 10, x + 10
            left_hand_x, right_hand_x = x - 12, x + 12
            left_hand_y = right_hand_y = hand_y

        self.canvas.create_line(x-5, y-30, left_foot_x, y+10, width=12, fill="#1565C0", capstyle=tk.ROUND, tags="mascot")
        self.canvas.create_polygon(left_foot_x-8, y+10, left_foot_x+18, y+10, left_foot_x+18, y+18, left_foot_x-8, y+18, fill="#212121", outline="black", tags="mascot")
        self.canvas.create_line(x-5, y-90, left_hand_x, left_hand_y, width=11, fill="#E64A19", capstyle=tk.ROUND, tags="mascot")
        self.canvas.create_oval(left_hand_x-6, left_hand_y-6, left_hand_x+6, left_hand_y+6, fill="#FFCBA4", outline="black", tags="mascot")

        self.canvas.create_rectangle(x-18, y-95, x+18, y-30, fill="#FF5722", outline="black", width=2, tags="mascot")
        self.canvas.create_polygon(x-10, y-95, x+10, y-95, x, y-80, fill="#FFCBA4", outline="black", tags="mascot")

        self.canvas.create_oval(x-22, y-145, x+22, y-95, fill="#FFCBA4", outline="black", width=2, tags="mascot") 
        if direction == 1:
            self.canvas.create_polygon(x-25, y-130, x-20, y-155, x+20, y-150, x+25, y-125, x, y-140, fill="#4E342E", outline="black", tags="mascot") 
            self.canvas.create_oval(x+6, y-130, x+16, y-120, fill="white", outline="black", tags="mascot") 
            self.canvas.create_oval(x+11, y-128, x+15, y-122, fill="black", tags="mascot") 
            self.canvas.create_arc(x+5, y-122, x+16, y-110, start=190, extent=100, style=tk.ARC, width=2, outline="black", tags="mascot")
        else:
            self.canvas.create_polygon(x+25, y-130, x+20, y-155, x-20, y-150, x-25, y-125, x, y-140, fill="#4E342E", outline="black", tags="mascot") 
            self.canvas.create_oval(x-16, y-130, x-6, y-120, fill="white", outline="black", tags="mascot") 
            self.canvas.create_oval(x-15, y-128, x-11, y-122, fill="black", tags="mascot") 
            self.canvas.create_arc(x-16, y-122, x-5, y-110, start=250, extent=100, style=tk.ARC, width=2, outline="black", tags="mascot")

        self.canvas.create_line(x+5, y-30, right_foot_x, y+10, width=12, fill="#1976D2", capstyle=tk.ROUND, tags="mascot")
        self.canvas.create_polygon(right_foot_x-8, y+10, right_foot_x+18, y+10, right_foot_x+18, y+18, right_foot_x-8, y+18, fill="#212121", outline="black", tags="mascot")
        self.canvas.create_line(x+5, y-90, right_hand_x, right_hand_y, width=11, fill="#FF5722", capstyle=tk.ROUND, tags="mascot")
        self.canvas.create_oval(right_hand_x-6, right_hand_y-6, right_hand_x+6, right_hand_y+6, fill="#FFCBA4", outline="black", tags="mascot")

        if self.has_lasso and pose in ["walk", "stand"]:
            coil_y = right_hand_y + 10
            for i in range(4):
                self.canvas.create_oval(right_hand_x - 12, coil_y - 6 + i*4, right_hand_x + 12, coil_y + 6 + i*4, outline="#4E342E", width=4, tags="mascot")
                self.canvas.create_oval(right_hand_x - 12, coil_y - 6 + i*4, right_hand_x + 12, coil_y + 6 + i*4, outline="#8D6E63", width=2, dash=(2,2), tags="mascot")

    def animate_walk_in(self):
        if self.mascot_x < self.screen_width / 2:
            self.mascot_x += self.walk_speed
            self.step_count += 1
            self.draw_character(pose="walk", direction=1)
            self.root.after(15, self.animate_walk_in) 
        else:
            self.draw_character(pose="stand", direction=1)
            self.root.after(300, self.throw_lasso)

    def throw_lasso(self):
        self.throw_t += 0.025 
        if self.throw_t > 1.0: self.throw_t = 1.0
            
        self.canvas.delete("lasso")
        hx, hy = self.mascot_x, self.screen_height - 240
        ty = 30 
        
        ease_y = 1 - (1 - self.throw_t) ** 2
        loop_cx = hx + math.sin(self.throw_t * math.pi) * 250 
        loop_cy = hy + (ty - hy) * ease_y
        
        spin = math.sin(self.throw_t * math.pi * 8) 
        loop_w = 40 + math.sin(self.throw_t * math.pi) * 40 
        loop_h = 15 + spin * 10
        
        mid_x = hx + (loop_cx - hx) * 0.5 + math.sin(self.throw_t * math.pi) * 100
        mid_y = hy + (loop_cy - hy) * 0.5 + 50
        
        self.canvas.create_line(hx, hy, mid_x, mid_y, loop_cx, loop_cy, width=5, fill="#4E342E", smooth=True, tags="lasso")
        self.canvas.create_line(hx, hy, mid_x, mid_y, loop_cx, loop_cy, width=3, fill="#8D6E63", dash=(4,4), smooth=True, tags="lasso")
        
        self.canvas.create_oval(loop_cx - loop_w/2, loop_cy - loop_h/2, loop_cx + loop_w/2, loop_cy + loop_h/2, outline="#4E342E", width=5, tags="lasso")
        self.canvas.create_oval(loop_cx - loop_w/2, loop_cy - loop_h/2, loop_cx + loop_w/2, loop_cy + loop_h/2, outline="#8D6E63", width=3, dash=(4,4), tags="lasso")
        
        knot_x = loop_cx - loop_w/2 + 5
        self.canvas.create_oval(knot_x - 4, loop_cy - 4, knot_x + 4, loop_cy + 4, fill="#3E2723", tags="lasso")
        self.canvas.create_line(knot_x, loop_cy, knot_x - 10, loop_cy + 15, width=3, fill="#4E342E", tags="lasso")

        self.draw_character(pose="throw_ready", direction=1)
        
        if self.throw_t < 1.0:
            self.root.after(15, self.throw_lasso)
        else:
            # BEKLEME SÜRESİ KISALTILDI (1000'den 200'e düştü)
            self.root.after(200, self.pull_shutter)

    def pull_shutter(self):
        if self.shutter_y < self.screen_height:
            self.shutter_y += self.shutter_speed
            
            self.canvas.delete("shutter")
            self.canvas.delete("lasso")
            
            # --- 1. KEPENGİN ZEMİN RENGİ ---
            self.canvas.create_rectangle(0, 0, self.screen_width, self.shutter_y, fill="#2C3136", outline="", tags="shutter")
            
            # --- 2. DOĞRUDAN KEPENGE YAZILMIŞ YAZILAR ---
            center_y = self.shutter_y - (self.screen_height / 2)
            if center_y > -300: 
                self.canvas.create_text(self.screen_width/2, center_y - 80, text="BUGÜN BENİ ÇOK YORDUN.", font=("Arial Black", 40), fill="#ECEFF1", tags="shutter")
                self.canvas.create_text(self.screen_width/2, center_y + 45, text="ERKEN PAYDOS EDİYORUM", font=("Impact", 85), fill="#F44336", tags="shutter")
                self.canvas.create_text(self.screen_width/2 + 450, center_y + 140, text="- ASUS", font=("Impact", 30, "italic"), fill="#90A4AE", anchor="e", tags="shutter")

            # --- 3. KEPENK ÇİZGİLERİ ---
            for i in range(0, int(self.shutter_y), 20):
                self.canvas.create_line(0, i, self.screen_width, i, fill="#181B1E", width=3, tags="shutter") 
                self.canvas.create_line(0, i+2, self.screen_width, i+2, fill="#3E454C", width=1, tags="shutter") 
            
            # --- 4. ALT KİLİT PROFİLİ VE GÜVENLİK BANDI ---
            profile_y = self.shutter_y - 30
            self.canvas.create_rectangle(0, profile_y, self.screen_width, self.shutter_y, fill="#111111", outline="", tags="shutter")
            self.canvas.create_rectangle(0, profile_y, self.screen_width, profile_y + 10, fill="#FFC107", outline="", tags="shutter")
            for x_offset in range(-50, int(self.screen_width) + 100, 40):
                self.canvas.create_polygon(x_offset, profile_y, x_offset + 20, profile_y, 
                                           x_offset + 10, profile_y + 10, x_offset - 10, profile_y + 10, 
                                           fill="#212121", outline="", tags="shutter")
                
            # --- KEMENTİ ÇEKME İŞLEMİ ---
            hy_base = self.screen_height - 60
            max_up = hy_base - 180  
            max_down = hy_base - 40 
            
            current_hand_y = max(max_up, min(max_down, self.shutter_y))
            hx = self.mascot_x
            
            self.canvas.create_line(hx, current_hand_y, hx, self.shutter_y, width=5, fill="#4E342E", tags="lasso")
            self.canvas.create_line(hx, current_hand_y, hx, self.shutter_y, width=3, fill="#8D6E63", dash=(4,4), tags="lasso")
            
            loop_w, loop_h = 80, 20
            self.canvas.create_oval(hx - loop_w/2, self.shutter_y - loop_h/2, hx + loop_w/2, self.shutter_y + loop_h/2, outline="#4E342E", width=5, tags="lasso")
            self.canvas.create_oval(hx - loop_w/2, self.shutter_y - loop_h/2, hx + loop_w/2, self.shutter_y + loop_h/2, outline="#8D6E63", width=3, dash=(4,4), tags="lasso")
            self.canvas.create_oval(hx - loop_w/2 - 4, self.shutter_y - 4, hx - loop_w/2 + 4, self.shutter_y + 4, fill="#3E2723", tags="lasso")

            self.draw_character(pose="pull", direction=1, hand_y=current_hand_y)
            
            self.root.after(20, self.pull_shutter)
        else:
            self.canvas.delete("lasso")
            self.has_lasso = True
            self.root.after(500, self.animate_walk_out)

    def animate_walk_out(self):
        if self.mascot_x > -150:
            self.mascot_x -= self.walk_speed
            self.step_count += 1
            self.draw_character(pose="walk", direction=-1) 
            self.root.after(15, self.animate_walk_out)
        else:
            self.canvas.delete("mascot")
            ctypes.windll.user32.LockWorkStation() 
            self.root.destroy() 

if __name__ == "__main__":
    root = tk.Tk()
    app = ErkenPaydosApp(root)
    root.mainloop()
