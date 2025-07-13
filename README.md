# YouTube Kanal Yaratish Avtomatizatsiyasi

Bu loyiha Google hisoblarini ishlatib YouTube kanallarini avtomatik yaratish uchun mo'ljallangan. Loyiha xavfsizlik choralari, proxy rotation, captcha yechish va anti-detection texnikalarini o'z ichiga oladi.

## Xususiyatlar

- ✅ Google hisoblariga avtomatik kirish
- ✅ YouTube kanal yaratish
- ✅ Tasodifiy kanal ma'lumotlari generatsiyasi
- ✅ Proxy rotation va IP o'zgartirish
- ✅ User agent rotation
- ✅ Anti-captcha integratsiyasi
- ✅ Cookie management
- ✅ Inson kabi xatti-harakatlar simulyatsiyasi
- ✅ Keng qamrovli logging va monitoring
- ✅ Xavfsizlik choralari

## O'rnatish

### 1. Dasturlarni o'rnatish

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
# Anti-captcha API kaliti (majburiy)
ANTICAPTCHA_API_KEY=your_anticaptcha_api_key_here

# Proxy sozlamalari
USE_PROXY=False
USE_PROXY_API=True
PROXY_TYPE=http
PROXY_TIMEOUT=10000
PROXY_SSL=all
PROXY_ANONYMITY=all
PROXY_COUNTRY=all
```

### 4. Hisoblar faylini yarating

```bash
cp accounts.txt.example accounts.txt
```

`accounts.txt` fayliga Google hisoblaringizni qo'shing:

```
email1@gmail.com:parol1
email2@gmail.com:parol2
email3@gmail.com:parol3
```

### 5. Proxy sozlamalari

Loyiha ProxyScrape API orqali proxy serverlarni avtomatik olish imkoniyatiga ega.

#### API orqali (tavsiya etiladi):

`.env` faylida proxy sozlamalarini o'zgartiring:

```env
USE_PROXY=True
USE_PROXY_API=True
PROXY_TYPE=http
PROXY_TIMEOUT=10000
PROXY_SSL=all
PROXY_ANONYMITY=all
PROXY_COUNTRY=all
```

#### Fayl orqali (fallback):

```bash
cp proxies.txt.example proxies.txt
```

`proxies.txt` fayliga proxy serverlaringizni qo'shing:

```
192.168.1.1:8080
192.168.1.2:3128:foydalanuvchi:parol
```

### 6. User agents faylini yarating (ixtiyoriy)

```bash
cp user_agents.txt.example user_agents.txt
```

### 7. Proxy test qilish

Proxy sozlamalarini test qilish uchun:

```bash
python test_proxy.py
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
3. **Random Delays**: Inson kabi xatti-harakatlar uchun tasodifiy kechikishlar
4. **Anti-detection**: Browser avtomatlashtirish belgilarini olib tashlash
5. **Captcha Solving**: Anti-captcha API orqali captcha yechish
6. **Cookie Management**: Sessiya ma'lumotlarini saqlash

### Loyiha strukturasi

```
youtube-automation/
├── youtube_automation.py      # Asosiy dastur
├── config.py                  # Konfiguratsiya
├── requirements.txt           # Dasturlar
├── .env                      # Muhit o'zgaruvchilari
├── accounts.txt              # Google hisoblar
├── proxies.txt               # Proxy serverlar
├── user_agents.txt           # User agentlar
├── results.json              # Natijalar
├── youtube_automation.log    # Log fayl
└── utils/
    ├── logger.py             # Logging dasturlari
    ├── security.py           # Xavfsizlik choralari
    ├── captcha_solver.py     # Captcha yechish
    └── data_generator.py     # Ma'lumotlar generatsiyasi
```

## Konfiguratsiya

### Muhit o'zgaruvchilari

| O'zgaruvchi | Tavsif | Standart |
|-------------|--------|----------|
| `ANTICAPTCHA_API_KEY` | Anti-captcha API kaliti | - |
| `USE_PROXY` | Proxy ishlatish | False |
| `USE_PROXY_API` | Proxy API ishlatish | True |
| `PROXY_LIST_FILE` | Proxy fayl nomi | proxies.txt |
| `PROXY_TYPE` | Proxy turi (http, https, socks4, socks5) | http |
| `PROXY_TIMEOUT` | Proxy timeout (millisekundlarda) | 10000 |
| `PROXY_SSL` | SSL sozlamalari (yes, no, all) | all |
| `PROXY_ANONYMITY` | Anonimlik darajasi (elite, anonymous, transparent, all) | all |
| `PROXY_COUNTRY` | Mamlakat kodi yoki 'all' | all |
| `HEADLESS` | Headless browser | False |
| `BROWSER_TIMEOUT` | Browser timeout | 30 |
| `MIN_DELAY` | Minimal kechikish | 2 |
| `MAX_DELAY` | Maksimal kechikish | 5 |
| `ACCOUNTS_FILE` | Hisoblar fayli | accounts.txt |
| `RESULTS_FILE` | Natijalar fayli | results.json |
| `LOG_FILE` | Log fayli | youtube_automation.log |

### Fayl formatlari

#### accounts.txt
```
email1@gmail.com:parol1
email2@gmail.com:parol2
```

#### proxies.txt
```
192.168.1.1:8080
192.168.1.2:3128:foydalanuvchi:parol
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
      "details": "Kanal muvaffaqiyatli yaratildi"
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
3. Dasturlar o'rnatilganini tekshiring
4. Internet aloqasini tekshiring

## Litsenziya

Bu loyiha faqat o'quv maqsadlarida yaratilgan. Faqat o'z hisoblaringizda ishlating.