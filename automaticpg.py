# -*- coding: utf-8 -*-
"""
© 2026 ivanchu.auto. All rights reserved.
自動化語音廣播系統 - 核心控制腳本
"""
import sys
import pygame
import datetime
import time
import schedule
import os

# --- 配置區 ---
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
LOG_FILENAME = "自动广播系统运行日志.txt"

def write_log(message):
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file_path = os.path.join(BASE_PATH, LOG_FILENAME)
    try:
        with open(log_file_path, "a", encoding="utf-8") as f:
            f.write(f"[{now_time}] {message}\n")
    except PermissionError:
        print(f"[{now_time}] [警告] 無法寫入 Log ! 請關閉 Log 檔案。")
    print(f"[{now_time}] {message}")

def speak_pro(audio_filename):
    full_path = os.path.join(BASE_PATH, audio_filename)
    if not os.path.exists(full_path):
        write_log(f"[錯誤] 找不到音訊文件: {audio_filename}")
        return
    
    try:
        write_log(f"開始播放: {audio_filename}")
        pygame.mixer.music.load(full_path)
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play()
        
        # 核心調整：強制等待，不要完全依賴 get_busy() 的自動偵測
        # 給予 1 秒的緩衝讓音訊裝置初始化
        time.sleep(1) 
        
        # 這裡設定等待 30 秒 (或是您 MP3 的長度)
        time.sleep(30)

        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        write_log(f"成功播放完成: {audio_filename}")
    except Exception as e:
        write_log(f"[ERROR] 播放失敗: {e}")

# --- 排程任務 ---
def job_15min():
    write_log(">>> 你的文字")
    speak_pro("你的音乐")

def job_5min():
    write_log(">>> 你的文字")
    speak_pro("你的音乐") 

def setup_schedule(): #这里可以根据自己的需求去更改
    # 星期一和星期二
    for day in ["monday", "tuesday"]:
        getattr(schedule.every(), day).at("17:45").do(job_15min)
        getattr(schedule.every(), day).at("17:55").do(job_5min)
    # 星期三，星期四，星期五和星期六
    for day in ["wednesday", "thursday", "friday", "saturday"]:
        getattr(schedule.every(), day).at("18:04").do(job_15min)
        getattr(schedule.every(), day).at("18:10").do(job_5min)

if __name__ == '__main__':
    write_log("[SYS][START] 系統啟動")
    pygame.mixer.init()
    time.sleep(2)  # 確保音訊系統初始化完成
    setup_schedule()
    write_log("[SYS][READY] 進入監控模式，按 'c' 可結束程式")

    try:
        while True:
            # 自動關機邏輯
            now = datetime.datetime.now()
            if (now.weekday() in [0, 1] and now.hour == 18 and now.minute >= 3) or \
               (now.weekday() in [2, 3, 4, 5] and now.hour == 13 and now.minute >= 57):
                write_log("[SYS][AUTO_EXIT] 準備自動關機")
                pygame.mixer.quit()
                os.system("shutdown /s /f /t 0")
                break
            
            schedule.run_pending()
            
            
            
    except Exception as e:
        write_log(f"[CRITICAL] 異常: {e}")
    finally:
        pygame.mixer.quit()
        write_log("[SYS][OFFLINE] 系統已安全關閉")