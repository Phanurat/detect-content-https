import requests
from bs4 import BeautifulSoup
import re
import tkinter as tk
from tkinter import scrolledtext

def fetch_content():
    url = url_entry.get()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            for tag in soup.find_all(['ul', 'span', 'script', 'iframe', 'ins', 'footer', 'header']):
                tag.decompose()

            ad_classes = ['ad-container', 'ads', 'advertisement']
            ad_ids = ['ad-banner', 'popup-ad']

            for tag in soup.find_all(True, class_=ad_classes):
                tag.decompose()
            for tag in soup.find_all(True, id=ad_ids):
                tag.decompose()

            paragraphs = soup.find_all('p')
            content = ""
            for paragraph in paragraphs:
                text = paragraph.get_text()
                cleaned_text = re.sub(r'/\S+', '', text)
                if cleaned_text.strip():  # ไม่แสดงบรรทัดว่าง
                    content += cleaned_text.strip() + "\n\n"

            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, content)
        else:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, f"ไม่สามารถโหลดหน้าเว็บได้ (Status Code: {response.status_code})")
    except Exception as e:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"เกิดข้อผิดพลาด: {str(e)}")

# สร้างหน้าต่างหลัก
window = tk.Tk()
window.title("Web Scraper GUI")
window.geometry("800x600")

# ช่องกรอก URL
url_label = tk.Label(window, text="กรอก URL ของข่าว:")
url_label.pack(pady=5)

url_entry = tk.Entry(window, width=80)
url_entry.pack(pady=5)
url_entry.insert(0, "https://ch3plus.com/news/political/morning/435851")  # ตัวอย่าง URL

# ปุ่มดึงข้อมูล
fetch_button = tk.Button(window, text="ดึงข้อมูล", command=fetch_content)
fetch_button.pack(pady=10)

# Text area สำหรับแสดงผลลัพธ์
result_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=100, height=25)
result_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

window.mainloop()
