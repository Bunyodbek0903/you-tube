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
            "Welcome to our channel! We share amazing content about {topic}.",
            "Join us for the latest updates and insights on {topic}.",
            "Your daily dose of {topic} content. Subscribe for more!",
            "Exploring the world of {topic} with you. Let's learn together!",
            "Professional {topic} content for enthusiasts and beginners alike.",
            "Discover the best of {topic} with our expert team.",
            "Your go-to channel for everything {topic} related.",
            "Quality {topic} content delivered daily.",
            "Stay updated with the latest in {topic}.",
            "Your trusted source for {topic} information and entertainment."
        ]
        
        self.topics = [
            "technology", "gaming", "cooking", "travel", "music", "fitness", "art",
            "science", "comedy", "news", "sports", "movies", "books", "photography",
            "DIY", "health", "business", "education", "entertainment", "lifestyle"
        ]
        
        self.categories = [
            "Education", "Entertainment", "Film & Animation", "Gaming", "How-to & Style",
            "Music", "News & Politics", "People & Blogs", "Pets & Animals", "Science & Technology",
            "Sports", "Travel & Events", "Comedy", "Autos & Vehicles", "Nonprofits & Activism"
        ]
    
    def generate_channel_name(self) -> str:
        """Generate random channel name"""
        base_name = random.choice(self.channel_names)
        suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=3))
        return f"{base_name}{suffix}"
    
    def generate_channel_description(self) -> str:
        """Generate random channel description"""
        topic = random.choice(self.topics)
        description = random.choice(self.channel_descriptions).format(topic=topic)
        
        # Add some random hashtags
        hashtags = [f"#{topic}", f"#{random.choice(self.topics)}", f"#{random.choice(self.topics)}"]
        description += f" {' '.join(hashtags)}"
        
        return description
    
    def generate_channel_category(self) -> str:
        """Generate random channel category"""
        return random.choice(self.categories)
    
    def generate_channel_data(self) -> Dict[str, str]:
        """Generate complete channel data"""
        return {
            "name": self.generate_channel_name(),
            "description": self.generate_channel_description(),
            "category": self.generate_channel_category(),
            "keywords": self.generate_keywords(),
            "location": self.generate_location()
        }
    
    def generate_keywords(self) -> List[str]:
        """Generate random keywords for channel"""
        keywords = []
        num_keywords = random.randint(3, 8)
        
        for _ in range(num_keywords):
            topic = random.choice(self.topics)
            keywords.append(topic)
        
        return keywords
    
    def generate_location(self) -> str:
        """Generate random location"""
        locations = [
            "United States", "United Kingdom", "Canada", "Australia", "Germany",
            "France", "Japan", "South Korea", "India", "Brazil", "Mexico",
            "Spain", "Italy", "Netherlands", "Sweden", "Norway", "Denmark",
            "Finland", "Switzerland", "Austria"
        ]
        return random.choice(locations)
    
    def generate_about_section(self) -> Dict[str, str]:
        """Generate about section data"""
        return {
            "description": self.generate_channel_description(),
            "location": self.generate_location(),
            "website": self.generate_website(),
            "email": self.generate_email(),
            "social_links": self.generate_social_links()
        }
    
    def generate_website(self) -> str:
        """Generate random website URL"""
        domains = ["example.com", "mysite.com", "website.net", "blog.org", "site.io"]
        domain = random.choice(domains)
        return f"https://www.{domain}"
    
    def generate_email(self) -> str:
        """Generate random email"""
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]
        domain = random.choice(domains)
        return f"{username}@{domain}"
    
    def generate_social_links(self) -> Dict[str, str]:
        """Generate random social media links"""
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
        """Generate random full name"""
        first_name = random.choice(self.first_names)
        last_name = random.choice(self.last_names)
        return f"{first_name} {last_name}"
    
    def generate_birth_date(self) -> Dict[str, int]:
        """Generate random birth date (18+ years old)"""
        year = random.randint(1980, 2005)
        month = random.randint(1, 12)
        day = random.randint(1, 28)  # Safe for all months
        return {"year": year, "month": month, "day": day}
    
    def generate_phone_number(self) -> str:
        """Generate random phone number"""
        area_code = random.randint(200, 999)
        prefix = random.randint(200, 999)
        line_number = random.randint(1000, 9999)
        return f"+1{area_code}{prefix}{line_number}"
    
    def generate_recovery_email(self) -> str:
        """Generate recovery email"""
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]
        domain = random.choice(domains)
        return f"{username}@{domain}"