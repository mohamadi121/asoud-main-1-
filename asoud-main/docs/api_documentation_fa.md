# 📋 مستندات API سیستم Conditional Content Delivery - آسود

## 🎯 **نمای کلی سیستم**

سیستم Conditional Content Delivery به طور هوشمندانه تشخیص می‌دهد که درخواست از **اپ آسود** می‌آید یا از **مرورگر وب**، و بر اساس آن پاسخ مناسب را ارائه می‌دهد:

- **اپ آسود**: پاسخ JSON API 
- **مرورگر وب**: صفحه HTML کارت ویزیت

---

## 🔗 **Endpoint اصلی**

### **VisitCard API**
```
GET /{business_id}
Host: {business_id}.asoud.ir
```

**مثال:**
```
GET /
Host: shop123.asoud.ir
```

---

## 🔍 **تشخیص نوع کلاینت (Client Detection)**

سیستم از روش‌های زیر برای تشخیص نوع کلاینت استفاده می‌کند:

### **🔸 Headers مورد بررسی:**

#### **برای اپ آسود:**
```http
User-Agent: AsoudApp/1.0 Flutter/3.0
Accept: application/json
X-ASOUD-APP: true
X-FLUTTER-APP: true
X-MOBILE-APP: true
```

#### **برای مرورگر:**
```http
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
```

### **🔸 User-Agent Patterns:**

#### **پترن‌های تشخیص اپ آسود:**
- `asoud`
- `flutter`
- `dart`
- `http/\d\.\d` (مانند http/1.1)
- `okhttp`

#### **پترن‌های تشخیص مرورگر:**
- `mozilla`
- `chrome`
- `safari`
- `firefox`
- `edge`
- `opera`
- `webkit`

---

## 📊 **Response Formats**

### **🔸 پاسخ برای اپ آسود (JSON)**

#### **موفق:**
```json
{
  "success": true,
  "code": 200,
  "data": {
    "business_id": "shop123",
    "name": "فروشگاه تست",
    "slogan": "بهترین کیفیت",
    "description": "توضیحات فروشگاه...",
    "logo_img": "https://domain.com/media/logos/logo.jpg",
    "contact": {
      "first_mobile_number": "09123456789",
      "second_mobile_number": "09987654321",
      "telephone": "02112345678",
      "email": "info@shop.com",
      "messenger_ids": {
        "telegram": "shopusername",
        "instagram": "shopinsta"
      }
    },
    "location": {
      "address": "تهران، خیابان ولیعصر، پلاک ۱۲۳",
      "latitude": "35.6892",
      "longitude": "51.3890",
      "city": "تهران"
    }
  }
}
```

#### **خطا - فروشگاه یافت نشد:**
```json
{
  "success": false,
  "code": 404,
  "error": "Market not found"
}
```

#### **خطا - سرور:**
```json
{
  "success": false,
  "code": 500,
  "error": "Internal server error"
}
```

### **🔸 پاسخ برای مرورگر (HTML)**

#### **موفق:**
```html
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <title>فروشگاه تست - کارت ویزیت دیجیتال آسود</title>
    <!-- کارت ویزیت کامل با طراحی responsive -->
</head>
<body>
    <!-- محتوای کارت ویزیت -->
</body>
</html>
```

#### **خطا - فروشگاه یافت نشد:**
```html
<!DOCTYPE html>
<html>
    <!-- صفحه خطای 404 با طراحی زیبا -->
</html>
```

---

## 🧪 **نحوه تست API**

### **🔸 تست با cURL:**

#### **درخواست از اپ آسود:**
```bash
curl -H "User-Agent: AsoudApp/1.0 Flutter/3.0" \
     -H "Accept: application/json" \
     -H "X-ASOUD-APP: true" \
     https://shop123.asoud.ir
```

#### **درخواست از مرورگر:**
```bash
curl -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
     -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
     https://shop123.asoud.ir
```

### **🔸 تست با JavaScript (در اپ):**

#### **Flutter/Dart:**
```dart
final response = await http.get(
  Uri.parse('https://shop123.asoud.ir'),
  headers: {
    'User-Agent': 'AsoudApp/1.0 Flutter/3.0',
    'Accept': 'application/json',
    'X-ASOUD-APP': 'true',
  },
);

final data = json.decode(response.body);
if (data['success']) {
  // استفاده از data['data']
}
```

#### **JavaScript (در مرورگر):**
```javascript
fetch('https://shop123.asoud.ir', {
  headers: {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
  }
})
.then(response => response.text())
.then(html => {
  // HTML کارت ویزیت دریافت شد
});
```

---

## 🗂️ **ساختار Database Models**

### **🔸 Market Model:**
```python
- business_id: CharField (unique)
- name: CharField
- slogan: CharField (optional)
- description: TextField (optional)
- logo_img: ImageField (optional)
```

### **🔸 MarketContact Model (OneToOne با Market):**
```python
- first_mobile_number: CharField (optional)
- second_mobile_number: CharField (optional)
- telephone: CharField (optional)
- email: EmailField (optional)
- messenger_ids: JSONField (برای telegram/instagram)
```

### **🔸 MarketLocation Model (OneToOne با Market):**
```python
- address: TextField (optional)
- latitude: DecimalField (optional)
- longitude: DecimalField (optional)
- city: CharField (optional)
```

---

## ⚙️ **Logic Flow سیستم**

```
درخواست وارد می‌شود
        ↓
بررسی User-Agent و Headers
        ↓
    ┌─────────────┐      ┌─────────────┐
    │ اپ آسود؟    │  یا  │ مرورگر؟     │
    └─────────────┘      └─────────────┘
           ↓                    ↓
    ┌─────────────┐      ┌─────────────┐
    │ JSON Response│      │HTML Response│
    └─────────────┘      └─────────────┘
```

### **🔸 شرایط تشخیص:**

1. **اگر `is_asoud_app` و `not is_web_browser`** → JSON Response
2. **اگر `is_web_browser`** → HTML Response  
3. **در غیر این صورت** → JSON Response (پیش‌فرض)

---

## 🚀 **Features اضافی**

### **🔸 کارت ویزیت HTML شامل:**
- طراحی responsive مناسب موبایل و دسکتاپ
- نقشه تعاملی OpenStreetMap
- لینک‌های مستقیم تلگرام و اینستاگرام
- قابلیت Share کارت ویزیت
- فونت فارسی Vazirmatn
- طراحی dark theme مطابق آسود

### **🔸 Error Handling:**
- خطاهای مجزا برای JSON و HTML
- صفحات خطای زیبا برای مرورگرها
- پیام‌های خطای مناسب برای اپ

### **🔸 Security:**
- بررسی دقیق User-Agent patterns
- Validation مناسب business_id
- Error handling امن

---

## 📝 **نکات مهم برای Frontend Developers**

### **🔸 برای توسعه‌دهندگان اپ آسود:**
1. **همیشه header های مناسب ارسال کنید**
2. **Accept: application/json اجباری است**
3. **User-Agent شامل flutter یا asoud باشد**
4. **بررسی success field در response**

### **🔸 برای توسعه‌دهندگان وب:**
1. **مرورگرها به طور خودکار تشخیص داده می‌شوند**
2. **HTML کامل با CSS و JavaScript دریافت می‌کنید**
3. **قابلیت Share و Map به طور خودکار کار می‌کند**

### **🔸 مشترک:**
1. **business_id باید معتبر باشد**
2. **از HTTPS استفاده کنید**
3. **Subdomain pattern: {business_id}.asoud.ir**

---

## 🆘 **Troubleshooting**

### **🔸 مشکلات رایج:**

#### **1. JSON به جای HTML دریافت می‌کنم:**
**راه حل:** User-Agent مرورگر شما patterns مناسب ندارد.

#### **2. HTML به جای JSON دریافت می‌کنم:**
**راه حل:** Headers مناسب اپ را ارسال کنید.

#### **3. 404 Error:**
**راه حل:** business_id را بررسی کنید.

### **🔸 Debug Headers:**
```bash
# بررسی headers ارسالی
curl -v https://shop123.asoud.ir
```

---

## 📞 **پشتیبانی**

برای سوالات فنی و پشتیبانی:
- **تیم فنی آسود**
- **ایمیل:** support@asoud.ir
- **مستندات کامل:** [لینک مستندات]

---

*این مستندات برای نسخه فعلی سیستم Conditional Content Delivery آسود تهیه شده است.*