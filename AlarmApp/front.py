import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from shared import shared_data, data_lock, flag

class PythonGUIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("3つの入力セル GUI")
        self.root.geometry("500x600")
        
        # 結果保存用リスト
        self.results = []
        
        # メインフレーム
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # タイトル
        title_label = ttk.Label(main_frame, text="3つの入力セル GUI", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # セル1: 1分刻みドロップダウン
        ttk.Label(main_frame, text="使用時間(分):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.cell1_var = tk.StringVar()
        self.cell1_combo = ttk.Combobox(main_frame, textvariable=self.cell1_var, width=25, state="readonly")
        cell1_values = [str(i) for i in range(1, 1441)]  # 1から1440までの1分刻み
        self.cell1_combo['values'] = cell1_values
        self.cell1_combo.grid(row=1, column=1, padx=(10, 0), pady=5)
        
        # セル2: テキスト入力
        ttk.Label(main_frame, text="入力セル2:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.cell2_var = tk.StringVar()
        self.cell2_entry = ttk.Entry(main_frame, textvariable=self.cell2_var, width=30)
        self.cell2_entry.grid(row=2, column=1, padx=(10, 0), pady=5)
        
        # セル3: 1-24ドロップダウン
        ttk.Label(main_frame, text="入力セル3（数値選択）:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.cell3_var = tk.StringVar()
        self.cell3_combo = ttk.Combobox(main_frame, textvariable=self.cell3_var, width=25, state="readonly")
        cell3_values = [str(i) for i in range(1, 25)]
        self.cell3_combo['values'] = cell3_values
        self.cell3_combo.grid(row=3, column=1, padx=(10, 0), pady=5)
        
        # 入力状況表示
        self.status_label = ttk.Label(main_frame, text="入力状況: 0/3 完了", foreground="blue")
        self.status_label.grid(row=4, column=0, columnspan=2, pady=10)
        
        # ボタンフレーム
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        # 送信ボタン
        self.submit_btn = ttk.Button(button_frame, text="送信", command=self.submit_data)
        self.submit_btn.pack(side=tk.LEFT, padx=5)
        
        # クリアボタン
        clear_btn = ttk.Button(button_frame, text="クリア", command=self.clear_data)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # 結果表示エリア
        ttk.Label(main_frame, text="送信結果履歴:").grid(row=6, column=0, sticky=tk.W, pady=(20, 5))
        
        # テキストエリアとスクロールバー
        text_frame = ttk.Frame(main_frame)
        text_frame.grid(row=7, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.result_text = tk.Text(text_frame, height=12, width=50)
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 入力変更時のイベントバインド
        self.cell1_var.trace('w', self.update_status)
        self.cell2_var.trace('w', self.update_status)
        self.cell3_var.trace('w', self.update_status)
        
        # グリッドの重み設定
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(7, weight=1)
    
    def update_status(self, *args):
        """入力状況を更新"""
        filled_count = 0
        if self.cell1_var.get(): filled_count += 1
        if self.cell2_var.get().strip(): filled_count += 1
        if self.cell3_var.get(): filled_count += 1
        
        self.status_label.config(text=f"入力状況: {filled_count}/3 完了")
        
        # 送信ボタンの有効/無効切り替え
        if filled_count == 3:
            self.submit_btn.config(state="normal")
        else:
            self.submit_btn.config(state="disabled")
    
    def submit_data(self):
        """データ送信処理"""
        cell1 = self.cell1_var.get()
        cell2 = self.cell2_var.get().strip()
        cell3 = self.cell3_var.get()
        
        if not cell1 or not cell2 or not cell3:
            messagebox.showwarning("警告", "すべてのセルに入力してください。")
            return
        
        # 結果を保存
        result = {
            "cell1": cell1,
            "cell2": cell2,
            "cell3": cell3,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.results.append(result)
        
        # 結果をテキストエリアに表示
        result_text = f"--- 送信 #{len(self.results)} ---\n"
        result_text += f"時刻: {result['timestamp']}\n"
        result_text += f"セル1: {result['cell1']}\n"
        result_text += f"セル2: {result['cell2']}\n"
        result_text += f"セル3: {result['cell3']}\n"
        result_text += "=" * 30 + "\n\n"
        self.result_text.insert(tk.END, result_text)
        self.result_text.see(tk.END)

        # front.py の中の submit_data() の最後の方
        flag=0
        with data_lock:
            shared_data["latest_result"] = result

        
        print(f"送信されたデータ: {result}")
        messagebox.showinfo("成功", "データが送信されました！")
    
    def clear_data(self):
        """データクリア処理"""
        self.cell1_var.set("")
        self.cell2_var.set("")
        self.cell3_var.set("")
        self.results.clear()
        self.result_text.delete(1.0, tk.END)
        print("データがクリアされました")

def main():
    root = tk.Tk()
    app = PythonGUIApp(root)
    
    print("Python GUIアプリケーションを起動しています...")
    print("3つのセルに入力して、送信ボタンを押してください。")
    
    root.mainloop()

if __name__ == "__main__":
    main()