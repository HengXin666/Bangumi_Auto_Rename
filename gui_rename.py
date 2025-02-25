import os
import re
import tkinter as tk
from tkinter import ttk, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES

class RenameApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("番剧批量重命名工具")
        self.geometry("800x600")
        
        # 创建变量
        self.season = tk.StringVar(value="3")
        self.folder_path = tk.StringVar()
        self.preview_data = []
        
        # 创建UI组件
        self.create_widgets()
        
    def create_widgets(self):
        # 季数设置
        ttk.Label(self, text="季数设置:").pack(pady=5)
        season_frame = ttk.Frame(self)
        season_frame.pack()
        ttk.Label(season_frame, text="S").pack(side=tk.LEFT)
        season_entry = ttk.Entry(season_frame, textvariable=self.season, width=3)
        season_entry.pack(side=tk.LEFT)
        ttk.Label(season_frame, text="E").pack(side=tk.LEFT)
        
        # 文件夹拖拽区域
        ttk.Label(self, text="拖拽文件夹到这里:").pack(pady=5)
        self.entry_folder = ttk.Entry(self, textvariable=self.folder_path, width=50)
        self.entry_folder.pack(pady=5)
        
        # 绑定拖拽事件
        self.entry_folder.drop_target_register(DND_FILES)
        self.entry_folder.dnd_bind('<<Drop>>', self.on_drop)
        
        # 预览列表
        self.preview_list = tk.Listbox(self, width=100, height=20)
        self.preview_list.pack(pady=10, expand=True, fill=tk.BOTH)
        
        # 操作按钮
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="刷新预览", command=self.update_preview).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="执行重命名", command=self.do_rename).pack(side=tk.LEFT, padx=5)
        
        # 绑定事件
        self.season.trace_add("write", lambda *_: self.update_preview())
        
    def on_drop(self, event):
        path = event.data.strip().strip("{}")
        if os.path.isdir(path):
            self.folder_path.set(path)
            self.update_preview()
        
    def generate_new_name(self, filename):
        # 匹配第一个[数字]格式
        match = re.search(r'\[(\d+)\]', filename)
        if not match:
            return None
        
        episode_num = match.group(1)
        try:
            episode = f"{int(episode_num):02d}"
        except ValueError:
            return None
        
        season = f"S{self.season.get().zfill(2)}E{episode}"
        new_name = f"{season} - {filename}"
        return new_name
    
    def update_preview(self):
        self.preview_list.delete(0, tk.END)
        self.preview_data.clear()
        
        path = self.folder_path.get()
        if not os.path.isdir(path):
            return
        
        for f in os.listdir(path):
            if os.path.isfile(os.path.join(path, f)):
                new_name = self.generate_new_name(f)
                if new_name:
                    self.preview_list.insert(tk.END, f"原文件名: {f}")
                    self.preview_list.insert(tk.END, f"新文件名: {new_name}")
                    self.preview_list.insert(tk.END, "")
                    self.preview_data.append((f, new_name))
    
    def do_rename(self):
        path = self.folder_path.get()
        if not os.path.isdir(path):
            messagebox.showerror("错误", "请先选择有效文件夹")
            return
        
        success = 0
        for old_name, new_name in self.preview_data:
            try:
                os.rename(
                    os.path.join(path, old_name),
                    os.path.join(path, new_name))
                success += 1
            except Exception as e:
                messagebox.showerror("错误", f"重命名失败: {str(e)}")
                break
        
        messagebox.showinfo("完成", f"成功重命名 {success}/{len(self.preview_data)} 个文件")
        self.update_preview()

if __name__ == "__main__":
    app = RenameApp()
    app.mainloop()