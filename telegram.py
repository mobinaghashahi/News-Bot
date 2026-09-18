import requests

def send_telegram_message(chat_id, message, bot_token):
    """
    ارسال پیام به تلگرام
    
    Parameters:
    chat_id (str/int): شناسه چت یا کانال تلگرام
    message (str): متن پیام برای ارسال
    bot_token (str): توکن ربات تلگرام (از @BotFather بگیرید)
    
    Returns:
    bool: True اگر پیام با موفقیت ارسال شد، False در غیر این صورت
    """
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'  # می‌توانید HTML یا Markdown استفاده کنید
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        
        if response.json().get('ok'):
            print("✅ پیام با موفقیت ارسال شد")
            return True
        else:
            print(f"❌ خطا: {response.json()}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ خطای اتصال: {e}")
        return False

def send_telegram_photo(chat_id, image_url, bot_token, caption=""):
    """
    ارسال عکس از لینک به تلگرام
    
    Parameters:
    chat_id (str/int): شناسه چت یا کانال تلگرام
    image_url (str): لینک مستقیم عکس
    bot_token (str): توکن ربات تلگرام
    caption (str): توضیحات زیر عکس (اختیاری)
    
    Returns:
    bool: True اگر عکس با موفقیت ارسال شد، False در غیر این صورت
    """
    # مرحله 1: دانلود عکس از لینک
    try:
        print(f"📥 در حال دانلود عکس از: {image_url}")
        img_response = requests.get(image_url, timeout=30)
        img_response.raise_for_status()
        
        # مرحله 2: ارسال عکس به تلگرام
        url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
        
        # باید عکس را به صورت فایل ارسال کنیم
        files = {
            'photo': ('image.jpg', img_response.content, 'image/jpeg')
        }
        
        data = {
            'chat_id': chat_id,
            'caption': caption
        }
        
        response = requests.post(url, data=data, files=files, timeout=30)
        response.raise_for_status()
        
        if response.json().get('ok'):
            print("✅ عکس با موفقیت ارسال شد")
            return True
        else:
            print(f"❌ خطا در ارسال عکس: {response.json()}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ خطا: {e}")
        return False

def send_telegram_document(chat_id, file_url, bot_token, caption=""):
    """
    ارسال فایل (مستند) از لینک به تلگرام
    
    Parameters:
    chat_id (str/int): شناسه چت یا کانال تلگرام
    file_url (str): لینک مستقیم فایل
    bot_token (str): توکن ربات تلگرام
    caption (str): توضیحات زیر فایل (اختیاری)
    
    Returns:
    bool: True اگر فایل با موفقیت ارسال شد، False در غیر این صورت
    """
    try:
        print(f"📥 در حال دانلود فایل از: {file_url}")
        file_response = requests.get(file_url, timeout=30)
        file_response.raise_for_status()
        
        # ارسال فایل به تلگرام
        url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
        
        files = {
            'document': ('file.jpg', file_response.content)
        }
        
        data = {
            'chat_id': chat_id,
            'caption': caption
        }
        
        response = requests.post(url, data=data, files=files, timeout=30)
        response.raise_for_status()
        
        if response.json().get('ok'):
            print("✅ فایل با موفقیت ارسال شد")
            return True
        else:
            print(f"❌ خطا در ارسال فایل: {response.json()}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ خطا: {e}")
        return False

# تابع کمکی برای ارسال عکس از روی آدرس محلی (فایل روی دیسک)
def send_telegram_photo_from_file(chat_id, file_path, bot_token, caption=""):
    """
    ارسال عکس از فایل محلی به تلگرام
    
    Parameters:
    chat_id (str/int): شناسه چت یا کانال تلگرام
    file_path (str): مسیر فایل عکس روی دیسک
    bot_token (str): توکن ربات تلگرام
    caption (str): توضیحات زیر عکس (اختیاری)
    """
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
        
        with open(file_path, 'rb') as photo_file:
            files = {
                'photo': photo_file
            }
            data = {
                'chat_id': chat_id,
                'caption': caption
            }
            
            response = requests.post(url, data=data, files=files, timeout=30)
            response.raise_for_status()
            
            if response.json().get('ok'):
                print("✅ عکس از فایل محلی با موفقیت ارسال شد")
                return True
            else:
                print(f"❌ خطا: {response.json()}")
                return False
                
    except Exception as e:
        print(f"❌ خطا: {e}")
        return False