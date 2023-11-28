import tkinter as tk
import time
import threading
import pygame

# Khởi tạo pygame để phát âm thanh
pygame.init()
pygame.mixer.init()

def play_sound(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(loops=0)

# Biến toàn cục để kiểm tra trạng thái đếm ngược
is_counting_down = False

def update_label(time_str, fg_color="black"):
    label.config(text=time_str, fg=fg_color)

def countdown(time_str):
    global is_counting_down
    is_counting_down = True

    # Chuyển đổi thời gian thành tổng số giây
    minutes, seconds = map(int, time_str.split(':'))
    total_seconds = minutes * 60 + seconds

    # Cập nhật label ngay lập tức trước khi bắt đầu vòng lặp
    update_label(time_str)

    while total_seconds > 0 and is_counting_down:
        time.sleep(1)  # Sleep trước để giảm delay khi nhấn Start
        total_seconds -= 1
        minutes, seconds = divmod(total_seconds, 60)
        time_str = '{:02d}:{:02d}'.format(minutes, seconds)
        update_label(time_str, "red" if total_seconds <= 10 else "black")

        # Phát âm thanh khi còn 10 giây
        if total_seconds == 10:
            play_sound('countdown.mp3')  # Đường dẫn tới file âm thanh đếm ngược của bạn

        window.update()

    if total_seconds == 0 and is_counting_down:
        play_sound('alarm.mp3')  # Đường dẫn tới file âm thanh báo thức của bạn
        update_label("HẾT GIỜ", "red", 60)
        is_counting_down = False

def update_label(time_str, fg_color="black", font_size=80):
    font_style = ('Helvetica', font_size, 'bold')
    label.config(text=time_str, fg=fg_color, font=font_style)

def start_timer():
    # Đọc giá trị thời gian và format lại nếu cần
    time_str = entry.get().strip()
    if len(time_str) == 4:
        time_str = time_str[:2] + ':' + time_str[2:]
    entry.delete(0, tk.END)  # Clear entry after getting the time
    if not is_counting_down:
        threading.Thread(target=countdown, args=(time_str,)).start()

def stop_timer():
    global is_counting_down
    is_counting_down = False
    pygame.mixer.music.stop()  # Dừng âm thanh đang phát

def format_time(event):
    # Tự động thêm dấu ':' sau khi nhập 2 số đầu tiên
    current_text = entry.get()
    if len(current_text) == 2 and not current_text.endswith(':'):
        entry.insert(2, ':')

# Tạo cửa sổ Tkinter
window = tk.Tk()
window.geometry("400x200")
window.title("Chương trình đếm ngược thời gian")  # Thiết lập tên cho cửa sổ chương trình

label = tk.Label(window, text="00:00", font=('Helvetica', 80, 'bold'), bg="white")
label.pack(expand=True)

entry = tk.Entry(window, justify='center', font=('Helvetica', 24), width=7)
entry.pack()
entry.bind('<KeyRelease>', format_time)

# Frame to hold the buttons
button_frame = tk.Frame(window)
button_frame.pack(expand=True)

start_button = tk.Button(button_frame, text="Start", command=start_timer)
stop_button = tk.Button(button_frame, text="Stop", command=stop_timer)
exit_button = tk.Button(button_frame, text="Exit", command=window.destroy)

start_button.pack(side='left', padx=20)
stop_button.pack(side='left')
exit_button.pack(side='left', padx=20)

window.mainloop()
