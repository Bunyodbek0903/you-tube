import random
import string
from typing import Dict, List

class ChannelDataGenerator:
    def __init__(self):
        self.channel_names = [
            "TechReview", "GamingZone", "CookingMaster", "TravelVlog", "MusicStudio",
            "FitnessLife", "ArtGallery", "ScienceLab", "ComedyClub", "NewsCenter",
            "SportsHighlights", "MovieReviews", "BookClub", "PhotographyPro", "DIYProjects",
            "HealthTips", "BusinessInsights", "EducationHub", "EntertainmentNow", "LifestyleGuide"
        ]
        
        self.channel_descriptions = [
            "Bizning kanalimizga xush kelibsiz! {topic} haqida ajoyib kontentni ulashamiz.",
            "Eng so'nggi yangiliklar va {topic} haqidagi ma'lumotlar uchun bizga qo'shiling.",
            "Kundalik {topic} kontentingiz. Ko'proq uchun obuna bo'ling!",
            "Siz bilan {topic} dunyosini o'rganamiz. Keling, birga o'rganamiz!",
            "Professional {topic} kontenti - havaskorlar va yangi boshlovchilar uchun.",
            "Bizning mutaxassis jamoamiz bilan {topic} ning eng yaxshisini kashf eting.",
            "{topic} bilan bog'liq hamma narsa uchun sizning kanalingiz.",
            "Kundalik sifatli {topic} kontenti.",
            "{topic} ning eng so'nggi yangiliklarini kuzatib boring.",
            "{topic} ma'lumotlari va ko'ngil ochar dasturlar uchun ishonchli manbaangiz."
        ]
        
        self.topics = [
            "texnologiya", "o'yinlar", "ovqat pishirish", "sayohat", "musiqa", "jismoniy mashqlar", "san'at",
            "fan", "komediya", "yangiliklar", "sport", "filmlar", "kitoblar", "fotografiya",
            "DIY", "sog'liq", "biznes", "ta'lim", "ko'ngil ochar", "hayot tarzi"
        ]
        
        self.categories = [
            "Ta'lim", "Ko'ngil ochar", "Film va animatsiya", "O'yinlar", "Qanday qilish va uslub",
            "Musiqa", "Yangiliklar va siyosat", "Odamlar va bloglar", "Uy hayvonlari va hayvonlar", "Fan va texnologiya",
            "Sport", "Sayohat va tadbirlar", "Komediya", "Avtomobillar va transport vositalari", "Notijorat tashkilotlar va faollik"
        ]
    
    def generate_channel_name(self) -> str:
        """Tasodifiy kanal nomi yaratish"""
        base_name = random.choice(self.channel_names)
        suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=3))
        return f"{base_name}{suffix}"
    
    def generate_channel_description(self) -> str:
        """Tasodifiy kanal tavsifini yaratish"""
        topic = random.choice(self.topics)
        description = random.choice(self.channel_descriptions).format(topic=topic)
        
        # Ba'zi tasodifiy hashtag'lar qo'shish
        hashtags = [f"#{topic}", f"#{random.choice(self.topics)}", f"#{random.choice(self.topics)}"]
        description += f" {' '.join(hashtags)}"
        
        return description
    
    def generate_channel_category(self) -> str:
        """Tasodifiy kanal kategoriyasini yaratish"""
        return random.choice(self.categories)
    
    def generate_channel_data(self) -> Dict[str, str]:
        """To'liq kanal ma'lumotlarini yaratish"""
        return {
            "name": self.generate_channel_name(),
            "description": self.generate_channel_description(),
            "category": self.generate_channel_category(),
            "keywords": self.generate_keywords(),
            "location": self.generate_location()
        }
    
    def generate_keywords(self) -> List[str]:
        """Kanal uchun tasodifiy kalit so'zlarni yaratish"""
        keywords = []
        num_keywords = random.randint(3, 8)
        
        for _ in range(num_keywords):
            topic = random.choice(self.topics)
            keywords.append(topic)
        
        return keywords
    
    def generate_location(self) -> str:
        """Tasodifiy joylashuv yaratish"""
        locations = [
            "Qo'shma Shtatlar", "Birlashgan Qirollik", "Kanada", "Avstraliya", "Germaniya",
            "Fransiya", "Yaponiya", "Janubiy Koreya", "Hindiston", "Braziliya", "Meksika",
            "Ispaniya", "Italiya", "Niderlandiya", "Shvetsiya", "Norvegiya", "Daniya",
            "Finlyandiya", "Shveytsariya", "Avstriya"
        ]
        return random.choice(locations)
    
    def generate_about_section(self) -> Dict[str, str]:
        """Haqida bo'limi ma'lumotlarini yaratish"""
        return {
            "description": self.generate_channel_description(),
            "location": self.generate_location(),
            "website": self.generate_website(),
            "email": self.generate_email(),
            "social_links": self.generate_social_links()
        }
    
    def generate_website(self) -> str:
        """Tasodifiy veb-sayt URL yaratish"""
        domains = ["example.com", "mysite.com", "website.net", "blog.org", "site.io"]
        domain = random.choice(domains)
        return f"https://www.{domain}"
    
    def generate_email(self) -> str:
        """Tasodifiy email yaratish"""
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]
        domain = random.choice(domains)
        return f"{username}@{domain}"
    
    def generate_social_links(self) -> Dict[str, str]:
        """Tasodifiy ijtimoiy tarmoq havolalarini yaratish"""
        social_platforms = ["twitter", "instagram", "facebook", "linkedin", "tiktok"]
        links = {}
        
        for platform in random.sample(social_platforms, random.randint(2, 4)):
            username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
            links[platform] = f"https://{platform}.com/{username}"
        
        return links

class AccountDataGenerator:
    def __init__(self):
        self.first_names = [
            "John", "Jane", "Michael", "Sarah", "David", "Emily", "James", "Lisa",
            "Robert", "Jennifer", "William", "Jessica", "Richard", "Amanda", "Joseph",
            "Nicole", "Thomas", "Stephanie", "Christopher", "Melissa", "Daniel", "Rachel",
            "Matthew", "Laura", "Anthony", "Michelle", "Mark", "Kimberly", "Donald", "Deborah"
        ]
        
        self.last_names = [
            "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
            "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
            "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
            "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson"
        ]
    
    def generate_full_name(self) -> str:
        """Tasodifiy to'liq ism yaratish"""
        first_name = random.choice(self.first_names)
        last_name = random.choice(self.last_names)
        return f"{first_name} {last_name}"
    
    def generate_birth_date(self) -> Dict[str, int]:
        """Tasodifiy tug'ilgan sana yaratish (18+ yosh)"""
        year = random.randint(1980, 2005)
        month = random.randint(1, 12)
        day = random.randint(1, 28)  # Barcha oylar uchun xavfsiz
        return {"year": year, "month": month, "day": day}
    
    def generate_phone_number(self) -> str:
        """Tasodifiy telefon raqami yaratish"""
        area_code = random.randint(200, 999)
        prefix = random.randint(200, 999)
        line_number = random.randint(1000, 9999)
        return f"+1{area_code}{prefix}{line_number}"
    
    def generate_recovery_email(self) -> str:
        """Tiklash email yaratish"""
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]
        domain = random.choice(domains)
        return f"{username}@{domain}"