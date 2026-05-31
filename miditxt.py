import os
import mido
import tkinter as tk
from tkinter import filedialog, messagebox
from mido import MidiFile, MidiTrack, Message, MetaMessage

class MidiTextConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("miditxt转换器")
        self.root.geometry("900x700")
        self.root.configure(bg="#000000")
        
        # 语言文本数据字典
        self.lang_dict = {
            "ZH": {
                "title": " 🕹️  ■ □ ■  miditxt转换器  ■ □ ■  👾 ",
                "input_frame": " ❖ [ 输入与转换 ] TEXT ➔ MIDI ❖ ",
                "extract_frame": " ❖ [ 提取与导出 ] MIDI ➔ TEXT ❖ ",
                "btn_import": "▲ [ 1. 导入本地 .txt 文件 ] ▲",
                "btn_convert": "● [ 2. 将上方文本 ➔ .mid 文件 ] ●",
                "btn_export": "◆ [ 选择本地 .mid ➔ 提取并导出 .txt ] ◆",
                "btn_help": "❓ [ 帮助说明 ]",
                "warning_no_data": "没有合法的 MIDI 音符数据！",
                "success_midi": "MIDI 文件生成成功。",
                "success_txt": "文本文件保存成功。",
                "err_read": "读取失败: ",
                "err_convert": "转换失败: ",
                "help_title": "■□■ 使用说明 ■□■",
                "help_text": "【TEXT ➔ MIDI】\n1. 点击 [ IMPORT .TXT ] 导入或在左框贴入文本。\n2. 点击 [ CONVERT TO .MID ] 导出标准 MIDI 文件。\n\n【MIDI ➔ TEXT】\n1. 点击 [ EXPORT MIDI TO .TXT ] 选择 MIDI 文件。\n2. 软件会自动提取核心音符，在右框预览并提示保存为 .txt。\n\n【底层机制】\n* 时基统一锁死为 480 Ticks/Beat，自动注入 120 BPM 速度元数据，完美对齐宿主格子，防止错位与丢小节。"
            },
            "EN": {
                "title": " 🕹️  ■ □ ■  miditxt_converter  ■ □ ■  👾 ",
                "input_frame": " ❖ [ INPUT ] TEXT ➔ MIDI ❖ ",
                "extract_frame": " ❖ [ EXTRACT ] MIDI ➔ TEXT ❖ ",
                "btn_import": "▲ [ 1. IMPORT .TXT FILE ] ▲",
                "btn_convert": "● [ 2. CONVERT TEXT TO .MID ] ●",
                "btn_export": "◆ [ EXPORT MIDI TO .TXT FILE ] ◆",
                "btn_help": "❓ [ HELP ]",
                "warning_no_data": "No valid MIDI data found.",
                "success_midi": "MIDI file generated successfully.",
                "success_txt": "Text file saved successfully.",
                "err_read": "Read failed: ",
                "err_convert": "Conversion failed: ",
                "help_title": "■□■ INSTRUCTIONS ■□■",
                "help_text": "[TEXT ➔ MIDI]\n1. Click [ IMPORT .TXT ] or paste raw text into the left panel.\n2. Click [ CONVERT TO .MID ] to export a standard MIDI file.\n\n[MIDI ➔ TEXT]\n1. Click [ EXPORT MIDI TO .TXT ] and select a local .mid file.\n2. The core notes will be extracted for preview and exported to .txt.\n\n[CORE ENGINE]\n* Timebase is locked at 480 Ticks/Beat with a 120 BPM tempo meta-tag to prevent any missing bars or synchronization shifting in DAWs."
            },
            "JA": {
                "title": " 🕹️  ■ □ ■  miditxt変換器  ■ □ ■  👾 ",
                "input_frame": " ❖ [ 入力と変換 ] TEXT ➔ MIDI ❖ ",
                "extract_frame": " ❖ [ 抽出と出力 ] MIDI ➔ TEXT ❖ ",
                "btn_import": "▲ [ 1. .txt ファイルをインポート ] ▲",
                "btn_convert": "● [ 2. テキストを .mid に変換 ] ●",
                "btn_export": "◆ [ .mid を選択 ➔ .txt に抽出して保存 ] ◆",
                "btn_help": "❓ [ ヘルプ ]",
                "warning_no_data": "有効なMIDIデータが見つかりません。",
                "success_midi": "MIDIファイルが正常に生成されました。",
                "success_txt": "テキストファイルが正常に保存されました。",
                "err_read": "読み込み失敗: ",
                "err_convert": "変換失敗: ",
                "help_title": "■□■ 使用説明 ■□■",
                "help_text": "【TEXT ➔ MIDI】\n1. [ IMPORT .TXT ] をクリックするか、左枠にテキストを貼り付けます。\n2. [ CONVERT TO .MID ] をクリックしてMIDIファイルを出力します。\n\n【MIDI ➔ TEXT】\n1. [ EXPORT MIDI TO .TXT ] をクリックし、.mid ファイルを選択します。\n2. 核心ノートを自動抽出し、右枠でプレビューしながら .txt で保存します。\n\n【コアメカニズム】\n* タイムベースは 480 Ticks/Beat に固定され、120 BPM のテンポが自動注入されます。DAWのグリッドに完全に一致し、ズレや小節の消失を防ぎます。"
            }
        }
        
        self.current_lang = "ZH"

        # ---------------- 顶层控制面板（语言 + 帮助） ----------------
        top_bar = tk.Frame(root, bg="#000000")
        top_bar.pack(fill="x", padx=15, pady=5)
        
        # 语言切换按钮组
        lang_frame = tk.Frame(top_bar, bg="#000000")
        lang_frame.pack(side="left")
        
        self.btn_zh = tk.Button(lang_frame, text="[ ZH ]", command=lambda: self.switch_language("ZH"), bg="#000000", fg="#FFFF00", font=("Consolas", 9, "bold"), bd=1, relief="solid", cursor="hand2")
        self.btn_zh.pack(side="left", padx=2)
        
        self.btn_en = tk.Button(lang_frame, text="[ EN ]", command=lambda: self.switch_language("EN"), bg="#000000", fg="#FFFFFF", font=("Consolas", 9, "bold"), bd=1, relief="solid", cursor="hand2")
        self.btn_en.pack(side="left", padx=2)
        
        self.btn_ja = tk.Button(lang_frame, text="[ JA ]", command=lambda: self.switch_language("JA"), bg="#000000", fg="#FFFFFF", font=("Consolas", 9, "bold"), bd=1, relief="solid", cursor="hand2")
        self.btn_ja.pack(side="left", padx=2)
        
        # 帮助说明按钮
        self.btn_help = tk.Button(top_bar, text="", command=self.toggle_help_panel, bg="#000000", fg="#00FF00", font=("Consolas", 9, "bold"), bd=1, relief="solid", cursor="hand2")
        self.btn_help.pack(side="right")

        # 游戏风格主标题
        self.top_lbl = tk.Label(root, text="", fg="#FFFF00", bg="#000000", font=("Consolas", 12, "bold"))
        self.top_lbl.pack(pady=5)

        # ----------------- 帮助说明面板（默认隐藏） -----------------
        self.help_panel = tk.LabelFrame(root, text="", padx=10, pady=10, bg="#000000", fg="#00FF00", font=("Consolas", 10, "bold"), bd=2, relief="groove")
        self.txt_help_content = tk.Label(self.help_panel, text="", fg="#00FF00", bg="#000000", font=("Consolas", 9, "bold"), justify="left", anchor="w")
        self.txt_help_content.pack(fill="x")
        self.help_visible = False

        # 主工作容器
        main_frame = tk.Frame(root, bg="#000000")
        main_frame.pack(fill="both", expand=True, padx=15, pady=5)
        
        # =================【左半部分：TXT ➔ MIDI】=================
        self.left_frame = tk.LabelFrame(main_frame, text="", padx=10, pady=10, bg="#000000", fg="#0022FF", font=("Consolas", 10, "bold"), bd=2, relief="groove")
        self.left_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        self.btn_import_txt = tk.Button(self.left_frame, text="", command=self.import_text_file, bg="#000000", fg="#FF9800", activebackground="#FF9800", activeforeground="#000000", font=("Consolas", 9, "bold"), bd=1, relief="solid", cursor="hand2")
        self.btn_import_txt.pack(fill="x", pady=2)
        
        self.txt_input = tk.Text(self.left_frame, bg="#000000", fg="#FFFFFF", font=("Consolas", 10), bd=1, relief="solid", undo=True, insertbackground="#FFFFFF")
        self.txt_input.pack(fill="both", expand=True, pady=5)
        self.txt_input.insert("1.0", "note_on note=60 vel=90 time=0\nnote_off note=60 vel=0 time=480\nnote_on note=64 vel=90 time=0\nnote_off note=64 vel=0 time=480")
        
        self.btn_to_midi = tk.Button(self.left_frame, text="", command=self.text_to_midi, bg="#000000", fg="#FFFF00", activebackground="#FFFF00", activeforeground="#000000", font=("Consolas", 10, "bold"), pady=8, bd=1, relief="solid", cursor="hand2")
        self.btn_to_midi.pack(fill="x", pady=5)

        # =================【右半部分：MIDI ➔ TXT】=================
        self.right_frame = tk.LabelFrame(main_frame, text="", padx=10, pady=10, bg="#000000", fg="#0022FF", font=("Consolas", 10, "bold"), bd=2, relief="groove")
        self.right_frame.pack(side="right", fill="both", expand=True, padx=5)
        
        self.txt_output = tk.Text(self.right_frame, bg="#000000", fg="#00FF00", font=("Consolas", 10), bd=1, relief="solid", insertbackground="#00FF00")
        self.txt_output.pack(fill="both", expand=True, pady=5)
        
        self.btn_to_text = tk.Button(self.right_frame, text="", command=self.midi_to_text_and_save, bg="#000000", fg="#FF0000", activebackground="#FF0000", activeforeground="#000000", font=("Consolas", 10, "bold"), pady=8, bd=1, relief="solid", cursor="hand2")
        self.btn_to_text.pack(fill="x", pady=5)

        # 初始化显示语言
        self.update_ui_text()

    def switch_language(self, lang):
        """切换语系并刷新界面"""
        self.current_lang = lang
        # 联动修改高亮控制台颜色
        self.btn_zh.config(fg="#FFFF00" if lang == "ZH" else "#FFFFFF")
        self.btn_en.config(fg="#FFFF00" if lang == "EN" else "#FFFFFF")
        self.btn_ja.config(fg="#FFFF00" if lang == "JA" else "#FFFFFF")
        self.update_ui_text()

    def update_ui_text(self):
        """刷新所有界面UI文字"""
        data = self.lang_dict[self.current_lang]
        self.top_lbl.config(text=data["title"])
        self.left_frame.config(text=data["input_frame"])
        self.right_frame.config(text=data["extract_frame"])
        self.btn_import_txt.config(text=data["btn_import"])
        self.btn_to_midi.config(text=data["btn_convert"])
        self.btn_to_text.config(text=data["btn_export"])
        self.btn_help.config(text=data["btn_help"])
        self.help_panel.config(text=data["help_title"])
        self.txt_help_content.config(text=data["help_text"])

    def toggle_help_panel(self):
        """控制帮助面板的展开与隐藏"""
        if self.help_visible:
            self.help_panel.pack_forget()
            self.help_visible = False
        else:
            self.help_panel.pack(fill="x", padx=20, pady=5, before=self.left_frame.master)
            self.help_visible = True

    # ----------------- TXT ➔ MIDI -----------------
    def import_text_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if not file_path: return
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.txt_input.delete("1.0", tk.END)
            self.txt_input.insert("1.0", content)
        except Exception as e:
            messagebox.showerror("ERROR", f"{self.lang_dict[self.current_lang]['err_read']}{e}")

    def text_to_midi(self):
        raw_text = self.txt_input.get("1.0", tk.END).strip()
        if not raw_text or "note_" not in raw_text:
            messagebox.showwarning("WARNING", self.lang_dict[self.current_lang]["warning_no_data"])
            return
            
        out_path = filedialog.asksaveasfilename(defaultextension=".mid", filetypes=[("MIDI Files", "*.mid")])
        if not out_path: return
            
        try:
            out_mid = MidiFile(ticks_per_beat=480)
            track = MidiTrack()
            out_mid.tracks.append(track)
            
            target_bpm = 120
            microseconds_per_beat = int(60000000 / target_bpm)
            track.append(MetaMessage('set_tempo', tempo=microseconds_per_beat, time=0))
            
            for line in raw_text.split('\n'):
                line = line.strip()
                if not line or ('note_on' not in line and 'note_off' not in line): 
                    continue
                
                msg_type = 'note_on' if 'note_on' in line else 'note_off'
                note, velocity, time = 60, 64, 0
                
                for part in line.split():
                    if 'note=' in part: note = int(part.split('=')[1])
                    elif 'vel=' in part or 'velocity=' in part: velocity = int(part.split('=')[1])
                    elif 'time=' in part: time = int(part.split('=')[1])
                        
                track.append(Message(
                    msg_type, 
                    note=max(0, min(127, note)), 
                    velocity=max(0, min(127, velocity)), 
                    time=max(0, time)
                ))
                
            out_mid.save(out_path)
            messagebox.showinfo("SUCCESS", self.lang_dict[self.current_lang]["success_midi"])
        except Exception as e: 
            messagebox.showerror("ERROR", f"{self.lang_dict[self.current_lang]['err_convert']}{e}")

    # ----------------- MIDI ➔ TXT -----------------
    def midi_to_text_and_save(self):
        file_path = filedialog.askopenfilename(filetypes=[("MIDI Files", "*.mid *.midi")])
        if not file_path: return
            
        try:
            mid = MidiFile(file_path)
            text_events = []
            
            origin_tpb = mid.ticks_per_beat
            scale_factor = 480.0 / origin_tpb
            
            for track in mid.tracks:
                for msg in track:
                    if msg.type in ['note_on', 'note_off']:
                        scaled_time = int(round(msg.time * scale_factor))
                        text_events.append(f"{msg.type} note={msg.note} vel={msg.velocity} time={scaled_time}")
            
            text_content = "\n".join(text_events)
            
            self.txt_output.delete("1.0", tk.END)
            self.txt_output.insert("1.0", text_content)
            
            out_txt_path = filedialog.asksaveasfilename(
                defaultextension=".txt", 
                filetypes=[("Text Files", "*.txt")],
                title="Save Text File"
            )
            
            if out_txt_path:
                with open(out_txt_path, "w", encoding="utf-8") as f:
                    f.write(text_content)
                messagebox.showinfo("SUCCESS", self.lang_dict[self.current_lang]["success_txt"])
                
        except Exception as e: 
            messagebox.showerror("ERROR", f"{self.lang_dict[self.current_lang]['err_read']}{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MidiTextConverterApp(root)
    root.mainloop()