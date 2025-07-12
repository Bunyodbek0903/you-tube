# YouTube Channel Creation Automation

Bu loyiha Google hisoblarini ishlatib YouTube kanallarini avtomatik yaratish uchun mo'ljallangan. Loyiha xavfsizlik choralari, proxy rotation, captcha yechish va anti-detection texnikalarini o'z ichiga oladi.

## Xususiyatlar

- ✅ Google hisoblariga avtomatik kirish
- ✅ YouTube kanal yaratish
- ✅ Random kanal ma'lumotlari generatsiya qilish
- ✅ Proxy rotation va IP o'zgartirish
- ✅ User agent rotation
- ✅ Anti-captcha integratsiyasi
- ✅ Cookie management
- ✅ Human-like behavior simulation
- ✅ Comprehensive logging va monitoring
- ✅ Xavfsizlik choralari

## O'rnatish

### 1. Dependencies o'rnatish

```bash
pip install -r requirements.txt
```

### 2. Chrome browser o'rnatish

Chrome browser o'rnatilgan bo'lishi kerak. WebDriver avtomatik o'rnatiladi.

### 3. Konfiguratsiya

`.env` faylini yarating:

```bash
cp .env.example .env
```

Kerakli sozlamalarni to'ldiring:

```env
# Anti-captcha API key (majburiy)
ANTICAPTCHA_API_KEY=your_anticaptcha_api_key_here

# Proxy sozlamalari
USE_PROXY=False
PROXY_LIST_FILE=proxies.txt

# Browser sozlamalari
HEADLESS=False
BROWSER_TIMEOUT=30

# Delay sozlamalari (sekundlarda)
MIN_DELAY=2
MAX_DELAY=5
```

### 4. Hisoblar faylini yarating

```bash
cp accounts.txt.example accounts.txt
```

`accounts.txt` fayliga Google hisoblaringizni qo'shing:

```
email1@gmail.com:password1
email2@gmail.com:password2
email3@gmail.com:password3
```

### 5. Proxy faylini yarating (ixtiyoriy)

```bash
cp proxies.txt.example proxies.txt
```

`proxies.txt` fayliga proxy serverlaringizni qo'shing:

```
192.168.1.1:8080
192.168.1.2:3128:username:password
```

### 6. User agents faylini yarating (ixtiyoriy)

```bash
cp user_agents.txt.example user_agents.txt
```

## Ishlatish

### Asosiy ishlatish

```bash
python youtube_automation.py
```

### Xavfsizlik choralari

Loyiha quyidagi xavfsizlik choralarini o'z ichiga oladi:

1. **Proxy Rotation**: Har bir sessiya uchun boshqa proxy ishlatish
2. **User Agent Rotation**: Har bir sessiya uchun boshqa user agent
3. **Random Delays**: Human-like behavior uchun random kechikishlar
4. **Anti-detection**: Browser automation belgilarini olib tashlash
5. **Captcha Solving**: Anti-captcha API orqali captcha yechish
6. **Cookie Management**: Sessiya ma'lumotlarini saqlash

### Loyiha strukturasi

```
youtube-automation/
├── youtube_automation.py      # Asosiy dastur
├── config.py                  # Konfiguratsiya
├── requirements.txt           # Dependencies
├── .env                      # Environment variables
├── accounts.txt              # Google hisoblar
├── proxies.txt               # Proxy serverlar
├── user_agents.txt           # User agents
├── results.json              # Natijalar
├── youtube_automation.log    # Log fayl
└── utils/
    ├── logger.py             # Logging utilities
    ├── security.py           # Xavfsizlik choralari
    ├── captcha_solver.py     # Captcha yechish
    └── data_generator.py     # Ma'lumotlar generatsiyasi
```

## Konfiguratsiya

### Environment Variables

| O'zgaruvchi | Tavsif | Default |
|-------------|--------|---------|
| `ANTICAPTCHA_API_KEY` | Anti-captcha API kaliti | - |
| `USE_PROXY` | Proxy ishlatish | False |
| `PROXY_LIST_FILE` | Proxy fayl nomi | proxies.txt |
| `HEADLESS` | Headless browser | False |
| `BROWSER_TIMEOUT` | Browser timeout | 30 |
| `MIN_DELAY` | Minimal delay | 2 |
| `MAX_DELAY` | Maksimal delay | 5 |
| `ACCOUNTS_FILE` | Hisoblar fayli | accounts.txt |
| `RESULTS_FILE` | Natijalar fayli | results.json |
| `LOG_FILE` | Log fayli | youtube_automation.log |

### Fayl formatlari

#### accounts.txt
```
email1@gmail.com:password1
email2@gmail.com:password2
```

#### proxies.txt
```
192.168.1.1:8080
192.168.1.2:3128:username:password
http://192.168.1.3:8080
socks5://192.168.1.4:1080
```

#### user_agents.txt
```
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36...
```

## Natijalar

Dastur ishlagandan so'ng quyidagi fayllar yaratiladi:

- `results.json`: Barcha natijalar
- `youtube_automation.log`: Batafsil loglar

### Natija format

```json
{
  "start_time": "2024-01-01T12:00:00",
  "total_accounts": 10,
  "successful": 8,
  "failed": 2,
  "accounts": [
    {
      "timestamp": "2024-01-01T12:05:00",
      "email": "user1@gmail.com",
      "success": true,
      "details": "Channel created successfully"
    }
  ]
}
```

## Xavfsizlik

⚠️ **Muhim**: Bu dastur faqat o'z hisoblaringiz uchun ishlatilishi kerak. Boshqalarning hisoblarini buzish qonuniy emas.

### Tavsiya etilgan xavfsizlik choralari:

1. **2FA yoqish**: Barcha Google hisoblarda 2FA yoqing
2. **Kuchli parollar**: Kuchli va unique parollar ishlating
3. **Proxy ishlatish**: IP manzilingizni yashirish uchun proxy ishlating
4. **Cheklangan ishlatish**: Bir vaqtda juda ko'p hisob ishlatmang
5. **Monitoring**: Hisoblaringizni muntazam tekshiring

## Xatoliklar

### Keng tarqalgan xatoliklar

1. **Chrome driver xatosi**: Chrome browser o'rnatilganligini tekshiring
2. **Captcha xatosi**: Anti-captcha API kalitini to'g'ri kiriting
3. **Login xatosi**: Hisob ma'lumotlarini to'g'ri kiriting
4. **Proxy xatosi**: Proxy serverlar ishlayotganini tekshiring

### Debug

Log faylini tekshiring:
```bash
tail -f youtube_automation.log
```

## Yordam

Muammolar bo'lsa:
1. Log faylini tekshiring
2. Konfiguratsiyani tekshiring
3. Dependencies o'rnatilganini tekshiring
4. Internet aloqasini tekshiring

## Litsenziya

Bu loyiha faqat o'quv maqsadlarida yaratilgan. Faqat o'z hisoblaringizda ishlating.