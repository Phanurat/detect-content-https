import requests
from bs4 import BeautifulSoup
import re  # ใช้สำหรับ Regular Expression

# URL ของเว็บไซต์ที่คุณต้องการดึงข้อมูล
url = "https://ch3plus.com/news/political/morning/435851"  # ใส่ URL ที่คุณต้องการดึงข้อมูล

# ตั้งค่า headers เพื่อระบุ User-Agent
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

# ส่งคำขอ GET ไปยังเว็บไซต์
response = requests.get(url, headers=headers)

# เช็คสถานะของคำขอ
if response.status_code == 200:
    # ใช้ BeautifulSoup เพื่อแยกแยะ HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # ลบโฆษณา (ตัวอย่าง: ลบ <div>, <span>, <script> ที่อาจเป็นโฆษณา)
    # ค้นหาทุกแท็กที่อาจเป็นโฆษณาและลบมัน
    for ad_tag in soup.find_all(['ul', 'span', 'script', 'iframe', 'ins', 'footer', 'header']):
        ad_tag.decompose()  # เอาทั้งแท็กและเนื้อหาภายในออก

    # ลบเนื้อหาจาก class หรือ id ที่อาจจะเป็นโฆษณา
    ad_classes = ['ad-container', 'ads', 'advertisement']  # ตัวอย่างของคลาสที่อาจใช้ในโฆษณา
    ad_ids = ['ad-banner', 'popup-ad']  # ตัวอย่างของไอดีที่อาจใช้ในโฆษณา

    # ลบแท็กที่มี class หรือ id ที่เกี่ยวข้องกับโฆษณา
    for ad_tag in soup.find_all(True, class_=ad_classes):
        ad_tag.decompose()  # ลบแท็กที่มี class ที่เกี่ยวข้องกับโฆษณา

    for ad_tag in soup.find_all(True, id=ad_ids):
        ad_tag.decompose()  # ลบแท็กที่มี id ที่เกี่ยวข้องกับโฆษณา

    # ดึงข้อมูลคอนเท้นต์จากพารากราฟ (p tags) หรือแท็กที่คุณต้องการ
    paragraphs = soup.find_all('p')
    for paragraph in paragraphs:
        text = paragraph.get_text()  # ดึงข้อความจากพารากราฟ
        
        # ใช้ Regular Expression เพื่อลบเนื้อหาที่ตามหลัง '/'
        cleaned_text = re.sub(r'/\S+', '', text)  # ลบทุกอย่างที่ตามหลัง '/'
        
        print(cleaned_text)  # พิมพ์ข้อความที่ถูกทำความสะอาดแล้ว
    
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
