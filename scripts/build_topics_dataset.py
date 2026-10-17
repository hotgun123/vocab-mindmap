import json
import os
import re
import sys
import urllib.parse
import urllib.request
import time
from concurrent.futures import ThreadPoolExecutor

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

VOCAB_PATH = os.path.join(DATA_DIR, 'vocabulary.json')
SYNONYMS_PATH = os.path.join(DATA_DIR, 'synonyms.json')
SENTENCES_PATH = os.path.join(DATA_DIR, 'sentences.json')
OX3_PATH = os.path.join(DATA_DIR, 'oxford_3000.json')
OX5_PATH = os.path.join(DATA_DIR, 'oxford_5000.json')
CACHE_TRANS_PATH = os.path.join(DATA_DIR, 'sentence_translations_cache.json')
OUT_JSON_PATH = os.path.join(DATA_DIR, 'topics_vocabulary.json')
OUT_JS_PATH = os.path.join(DATA_DIR, 'topics_vocab_data.js')

# Load sentence translation cache
trans_cache = {}
if os.path.exists(CACHE_TRANS_PATH):
    try:
        with open(CACHE_TRANS_PATH, 'r', encoding='utf-8') as f:
            trans_cache = json.load(f)
        print(f"Loaded {len(trans_cache)} cached translations.")
    except Exception as e:
        print(f"Could not load cache: {e}")

# Pre-populate cache with existing translations from sentences.json
if os.path.exists(SENTENCES_PATH):
    try:
        with open(SENTENCES_PATH, 'r', encoding='utf-8') as f:
            sentences_pre = json.load(f)
        for s in sentences_pre:
            en = s.get('en', '').strip()
            vi = s.get('vi', '').strip()
            if en and vi and en not in trans_cache:
                trans_cache[en] = vi
        print(f"Total cache after adding sentences.json: {len(trans_cache)}")
    except Exception as e:
        print(f"Error loading sentences.json: {e}")

def translate_sentence(text):
    text = text.strip()
    if not text:
        return ""
    if text in trans_cache:
        return trans_cache[text]
    try:
        url = 'https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=vi&dt=t&q=' + urllib.parse.quote(text)
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=8) as res:
            data = json.loads(res.read().decode('utf-8'))
            vi = ''.join([part[0] for part in data[0] if part[0]])
            trans_cache[text] = vi
            return vi
    except Exception as e:
        return ""

# Topic Groups and Sub-Topics Definitions
TOPIC_GROUPS = [
    {
        "id": "business_work",
        "name_vi": "Kinh doanh & Nghề nghiệp",
        "name_en": "Business & Careers",
        "icon": "💼",
        "topics": [
            {"id": "office_work", "name_vi": "Công sở & Quản lý", "name_en": "Office & Management", "icon": "🏢"},
            {"id": "finance_banking", "name_vi": "Tài chính & Tiền tệ", "name_en": "Finance & Money", "icon": "💰"},
            {"id": "trade_commerce", "name_vi": "Kinh doanh & Bán hàng", "name_en": "Commerce & Sales", "icon": "📈"},
            {"id": "jobs_careers", "name_vi": "Nghề nghiệp & Việc làm", "name_en": "Jobs & Employment", "icon": "🤝"}
        ]
    },
    {
        "id": "tech_science",
        "name_vi": "Khoa học & Công nghệ",
        "name_en": "Science & Technology",
        "icon": "💻",
        "topics": [
            {"id": "computers_digital", "name_vi": "Máy tính & Kỹ thuật số", "name_en": "Computers & Digital", "icon": "🖥️"},
            {"id": "science_research", "name_vi": "Khoa học & Nghiên cứu", "name_en": "Science & Research", "icon": "🔬"},
            {"id": "engineering_industry", "name_vi": "Kỹ thuật & Máy móc", "name_en": "Engineering & Machinery", "icon": "⚙️"},
            {"id": "electronics_devices", "name_vi": "Điện tử & Viễn thông", "name_en": "Electronics & Devices", "icon": "📱"}
        ]
    },
    {
        "id": "education_academia",
        "name_vi": "Giáo dục & Học thuật",
        "name_en": "Education & Academia",
        "icon": "🎓",
        "topics": [
            {"id": "school_university", "name_vi": "Trường học & Đại học", "name_en": "School & University", "icon": "🏫"},
            {"id": "study_exams", "name_vi": "Học tập & Thi cử", "name_en": "Studying & Exams", "icon": "📚"},
            {"id": "language_reading", "name_vi": "Ngôn ngữ & Đọc viết", "name_en": "Language & Literacy", "icon": "✍️"}
        ]
    },
    {
        "id": "health_body",
        "name_vi": "Sức khỏe & Y tế",
        "name_en": "Health & Medicine",
        "icon": "🏥",
        "topics": [
            {"id": "body_anatomy", "name_vi": "Cơ thể người & Giác quan", "name_en": "Body & Senses", "icon": "🫀"},
            {"id": "medicine_illness", "name_vi": "Bệnh tật & Điều trị y tế", "name_en": "Illness & Medical Care", "icon": "💊"},
            {"id": "fitness_nutrition", "name_vi": "Dinh dưỡng & Thể chất", "name_en": "Nutrition & Fitness", "icon": "🥗"},
            {"id": "mental_health", "name_vi": "Tâm lý & Tinh thần", "name_en": "Mental Health & Wellbeing", "icon": "🧠"}
        ]
    },
    {
        "id": "nature_environment",
        "name_vi": "Môi trường & Thiên nhiên",
        "name_en": "Nature & Environment",
        "icon": "🌿",
        "topics": [
            {"id": "weather_seasons", "name_vi": "Thời tiết & Khí hậu", "name_en": "Weather & Climate", "icon": "🌦️"},
            {"id": "animals_wildlife", "name_vi": "Động vật & Sinh vật", "name_en": "Animals & Wildlife", "icon": "🐾"},
            {"id": "plants_nature", "name_vi": "Thực vật & Cây cỏ", "name_en": "Plants & Vegetation", "icon": "🌳"},
            {"id": "geography_earth", "name_vi": "Địa lý, Đất đai & Biển", "name_en": "Geography & Earth", "icon": "🌍"},
            {"id": "environment_ecology", "name_vi": "Môi trường & Sinh thái", "name_en": "Environment & Ecology", "icon": "♻️"}
        ]
    },
    {
        "id": "travel_transport",
        "name_vi": "Du lịch & Giao thông",
        "name_en": "Travel & Transportation",
        "icon": "✈️",
        "topics": [
            {"id": "travel_tourism", "name_vi": "Du lịch & Nghỉ mát", "name_en": "Travel & Tourism", "icon": "🧳"},
            {"id": "vehicles_transport", "name_vi": "Phương tiện & Giao thông", "name_en": "Vehicles & Transport", "icon": "🚗"},
            {"id": "hotel_hospitality", "name_vi": "Khách sạn & Dịch vụ lưu trú", "name_en": "Hotels & Hospitality", "icon": "🏨"},
            {"id": "navigation_places", "name_vi": "Phương hướng & Di chuyển", "name_en": "Directions & Movement", "icon": "🧭"}
        ]
    },
    {
        "id": "daily_life_home",
        "name_vi": "Đời sống & Gia đình",
        "name_en": "Daily Life & Home",
        "icon": "🏠",
        "topics": [
            {"id": "house_home", "name_vi": "Nhà cửa & Đồ nội thất", "name_en": "House & Furniture", "icon": "🏡"},
            {"id": "family_life", "name_vi": "Gia đình & Người thân", "name_en": "Family & Relatives", "icon": "👨‍👩‍👧"},
            {"id": "food_cooking", "name_vi": "Ẩm thực & Nấu nướng", "name_en": "Food & Cooking", "icon": "🍳"},
            {"id": "clothing_fashion", "name_vi": "Trang phục & Thời trang", "name_en": "Clothes & Fashion", "icon": "👗"},
            {"id": "shopping_services", "name_vi": "Mua sắm & Tiêu dùng", "name_en": "Shopping & Services", "icon": "🛒"}
        ]
    },
    {
        "id": "arts_entertainment",
        "name_vi": "Nghệ thuật & Giải trí",
        "name_en": "Arts & Entertainment",
        "icon": "🎨",
        "topics": [
            {"id": "music_cinema", "name_vi": "Âm nhạc & Điện ảnh", "name_en": "Music & Cinema", "icon": "🎵"},
            {"id": "sports_fitness", "name_vi": "Thể thao & Trò chơi", "name_en": "Sports & Games", "icon": "⚽"},
            {"id": "arts_literature", "name_vi": "Văn học & Hội họa", "name_en": "Literature & Fine Arts", "icon": "📖"},
            {"id": "hobbies_celebration", "name_vi": "Sở thích & Lễ hội", "name_en": "Hobbies & Leisure", "icon": "🎉"}
        ]
    },
    {
        "id": "society_law_politics",
        "name_vi": "Xã hội & Pháp luật",
        "name_en": "Society, Law & Politics",
        "icon": "⚖️",
        "topics": [
            {"id": "government_politics", "name_vi": "Chính phủ & Chính trị", "name_en": "Government & Politics", "icon": "🏛️"},
            {"id": "law_justice", "name_vi": "Pháp luật & Tội phạm", "name_en": "Law, Crime & Justice", "icon": "⚖️"},
            {"id": "society_culture", "name_vi": "Xã hội & Cộng đồng", "name_en": "Society & Community", "icon": "🌐"},
            {"id": "military_security", "name_vi": "Quân sự & Quốc phòng", "name_en": "Military & Defense", "icon": "🛡️"}
        ]
    },
    {
        "id": "emotions_mind",
        "name_vi": "Cảm xúc & Tính cách",
        "name_en": "Emotions & Personality",
        "icon": "💭",
        "topics": [
            {"id": "feelings_moods", "name_vi": "Cảm xúc & Tâm trạng", "name_en": "Feelings & Moods", "icon": "😊"},
            {"id": "personality_character", "name_vi": "Tính cách & Phẩm chất", "name_en": "Personality & Character", "icon": "🌟"},
            {"id": "thought_decision", "name_vi": "Tư duy & Nhận thức", "name_en": "Thinking & Ideas", "icon": "💡"}
        ]
    },
    {
        "id": "communication_social",
        "name_vi": "Giao tiếp & Quan hệ",
        "name_en": "Communication & Social",
        "icon": "🗣️",
        "topics": [
            {"id": "conversation_speech", "name_vi": "Giao tiếp & Hội thoại", "name_en": "Conversation & Speech", "icon": "💬"},
            {"id": "social_relations", "name_vi": "Tình bạn & Quan hệ xã hội", "name_en": "Relationships & Friends", "icon": "🤝"}
        ]
    },
    {
        "id": "general_concepts",
        "name_vi": "Khái niệm chung & Đo lường",
        "name_en": "General Concepts & Time",
        "icon": "📐",
        "topics": [
            {"id": "time_calendar", "name_vi": "Thời gian & Lịch trình", "name_en": "Time & Calendar", "icon": "⏳"},
            {"id": "quantity_measurement", "name_vi": "Số lượng & Đo lường", "name_en": "Quantity & Measurement", "icon": "📏"},
            {"id": "actions_change", "name_vi": "Hành động & Biến đổi", "name_en": "Actions & Processes", "icon": "🔄"},
            {"id": "qualities_states", "name_vi": "Trạng thái & Đặc tính", "name_en": "Qualities & States", "icon": "🧩"}
        ]
    }
]

# Topic Keyword Rules for intelligent classification
TOPIC_RULES = {
    "office_work": [r"\boffice\b", r"\bmanage\w*", r"\bboss\b", r"\bstaff\b", r"\bmeeting\b", r"\breport\b", r"\bexecutive\b", r"\bcolleague\b", r"\badmin\w*", r"\bproject\b", r"\bdeadline\b", r"\bworkplace\b", r"\bvăn phòng\b", r"\bquản lý\b", r"\bhội họp\b"],
    "finance_banking": [r"\bbank\w*", r"\bmoney\b", r"\bfinance\w*", r"\bcost\b", r"\bprice\b", r"\btax\w*", r"\bbudget\b", r"\bdebt\b", r"\bloan\b", r"\bcredit\b", r"\bcurrency\b", r"\binvest\w*", r"\beconom\w*", r"\bwealth\b", r"\btiền\b", r"\btài chính\b", r"\bngân hàng\b", r"\bchi phí\b", r"\blãi\b", r"\bvốn\b"],
    "trade_commerce": [r"\bmarket\w*", r"\bsell\w*", r"\bbuy\w*", r"\btrade\b", r"\bcustomer\b", r"\bprofit\b", r"\bproduct\b", r"\bbrand\b", r"\bcommercial\b", r"\bexport\b", r"\bimport\b", r"\bsupply\b", r"\bdemand\b", r"\bdeal\b", r"\bthương mại\b", r"\bbuôn bán\b", r"\blợi nhuận\b"],
    "jobs_careers": [r"\bjob\b", r"\bemploy\w*", r"\bcareer\b", r"\bhire\b", r"\bsalary\b", r"\bwage\b", r"\binterview\b", r"\bworker\b", r"\bprofession\w*", r"\bresign\b", r"\bretire\w*", r"\bviệc làm\b", r"\bnghề nghiệp\b", r"\blương\b", r"\btuyển dụng\b"],
    "computers_digital": [r"\bcomput\w*", r"\bsoftware\b", r"\bhardware\b", r"\bweb\w*", r"\binternet\b", r"\bonline\b", r"\bdigital\b", r"\bdata\b", r"\bcode\b", r"\bprogram\w*", r"\bscreen\b", r"\bclick\b", r"\bfile\b", r"\bnetwork\b", r"\bmáy tính\b", r"\bmạng\b", r"\bdữ liệu\b", r"\bphần mềm\b"],
    "science_research": [r"\bscience\b", r"\bscientific\b", r"\bresearch\w*", r"\bexperiment\b", r"\blaboratory\b", r"\blab\b", r"\btheory\b", r"\bdiscover\w*", r"\bevidence\b", r"\bhypothesis\b", r"\bchemic\w*", r"\bphysic\w*", r"\bkhoa học\b", r"\bnghiên cứu\b", r"\bthí nghiệm\b"],
    "engineering_industry": [r"\bengineer\w*", r"\bmachine\w*", r"\bindustr\w*", r"\bfactory\b", r"\btool\b", r"\bproduce\b", r"\bmanufactur\w*", r"\bequipment\b", r"\bmechanic\w*", r"\bbuild\w*", r"\bkỹ thuật\b", r"\bcông nghiệp\b", r"\bmáy móc\b", r"\bnhà máy\b"],
    "electronics_devices": [r"\belectronic\w*", r"\belectric\w*", r"\bphone\b", r"\bmobile\b", r"\bbattery\b", r"\bdevice\b", r"\bcable\b", r"\bwire\b", r"\bradio\b", r"\bcamera\b", r"\bđiện tử\b", r"\bthiết bị\b", r"\bđiện thoại\b"],
    "school_university": [r"\bschool\b", r"\buniversit\w*", r"\bcollege\b", r"\bstudent\b", r"\bteacher\b", r"\bprofessor\b", r"\bclassroom\b", r"\bcampus\b", r"\blecture\b", r"\btrường học\b", r"\bđại học\b", r"\bhọc sinh\b", r"\bsinh viên\b", r"\bgiáo viên\b"],
    "study_exams": [r"\blearn\w*", r"\bstud\w*", r"\bexam\w*", r"\btest\b", r"\bdegree\b", r"\bgrade\b", r"\bhomework\b", r"\bcourse\b", r"\bdiploma\b", r"\bknowledg\w*", r"\bhọc tập\b", r"\bthi cử\b", r"\bbằng cấp\b", r"\bkiến thức\b"],
    "language_reading": [r"\blanguage\b", r"\bword\b", r"\bgrammar\b", r"\bread\w*", r"\bwrite\w*", r"\bspeak\w*", r"\btext\b", r"\bbook\b", r"\bvocabulary\b", r"\btranslat\w*", r"\bdictionary\b", r"\bngôn ngữ\b", r"\bđọc\b", r"\bviết\b", r"\btừ vựng\b"],
    "body_anatomy": [r"\bbody\b", r"\beye\w*", r"\bhand\w*", r"\bhead\b", r"\bheart\b", r"\bblood\b", r"\bskin\b", r"\bbone\w*", r"\barm\b", r"\bleg\b", r"\bfoot\b", r"\bfeet\b", r"\bface\b", r"\bear\w*", r"\bnose\b", r"\bmouth\b", r"\bhair\b", r"\bcơ thể\b", r"\bmắt\b", r"\btay\b", r"\bchân\b", r"\btim\b", r"\bmáu\b"],
    "medicine_illness": [r"\bdoctor\b", r"\bhospital\b", r"\bpatient\b", r"\bmedicine\b", r"\bill\w*", r"\bsick\w*", r"\bdisease\b", r"\bpain\w*", r"\bhurt\w*", r"\binjur\w*", r"\btreat\w*", r"\bcure\b", r"\bdrug\w*", r"\bclinic\b", r"\bbệnh\b", r"\by tế\b", r"\bbác sĩ\b", r"\bthuốc\b", r"\bđau\b"],
    "fitness_nutrition": [r"\bfitness\b", r"\bexercise\b", r"\bdiet\b", r"\bhealth\w*", r"\bgym\b", r"\bworkout\b", r"\bvitamin\b", r"\bweight\b", r"\bmuscle\b", r"\bsport\b", r"\brunning\b", r"\bdinh dưỡng\b", r"\bsức khỏe\b", r"\btập luyện\b", r"\bthể hình\b"],
    "mental_health": [r"\bmind\b", r"\bmental\b", r"\bstress\b", r"\banxiet\w*", r"\bdepress\w*", r"\brelax\w*", r"\btherapy\b", r"\bpsychol\w*", r"\btâm lý\b", r"\btinh thần\b", r"\bcăng thẳng\b"],
    "weather_seasons": [r"\bweather\b", r"\brain\w*", r"\bsun\w*", r"\bwind\w*", r"\bcloud\w*", r"\bstorm\b", r"\bsnow\w*", r"\btemperature\b", r"\bclimate\b", r"\bspring\b", r"\bsummer\b", r"\bautumn\b", r"\bwinter\b", r"\bhot\b", r"\bcold\b", r"\bthời tiết\b", r"\bmưa\b", r"\bnắng\b", r"\bgió\b", r"\bbão\b", r"\bkhí hậu\b"],
    "animals_wildlife": [r"\banimal\w*", r"\bdog\w*", r"\bcat\w*", r"\bbird\w*", r"\bfish\w*", r"\bhorse\w*", r"\binsect\w*", r"\bwild\w*", r"\bpet\b", r"\bcreature\w*", r"\bbear\b", r"\blion\b", r"\bđộng vật\b", r"\bchó\b", r"\bmèo\b", r"\bchim\b", r"\bcá\b", r"\bthú\b"],
    "plants_nature": [r"\bplant\w*", r"\btree\w*", r"\bflower\w*", r"\bforest\w*", r"\bgrass\b", r"\bgarden\w*", r"\bleaf\b", r"\bleaves\b", r"\bwood\b", r"\bcrop\w*", r"\bfarm\w*", r"\bagricultur\w*", r"\bcây\b", r"\bhoa\b", r"\brừng\b", r"\bcỏ\b", r"\bthực vật\b", r"\bnông nghiệp\b"],
    "geography_earth": [r"\bearth\b", r"\bland\b", r"\bsea\b", r"\bocean\b", r"\briver\b", r"\bmountain\b", r"\bisland\b", r"\blake\b", r"\bbeach\b", r"\bcoast\b", r"\bsoil\b", r"\brock\b", r"\bvalley\b", r"\bđịa lý\b", r"\bđất đai\b", r"\bbiển\b", r"\bđại dương\b", r"\bsông\b", r"\bnúi\b", r"\bđảo\b"],
    "environment_ecology": [r"\benvironment\w*", r"\bpollut\w*", r"\bwaste\b", r"\brecycle\w*", r"\becolog\w*", r"\bconserv\w*", r"\bprotect\w*", r"\bglobal warming\b", r"\bmôi trường\b", r"\bô nhiễm\b", r"\brác\b", r"\btái chế\b"],
    "travel_tourism": [r"\btravel\w*", r"\btrip\b", r"\btour\w*", r"\bvacation\b", r"\bholiday\w*", r"\bvisit\w*", r"\bluggage\b", r"\bpassport\b", r"\bflight\b", r"\bsightsee\w*", r"\bdu lịch\b", r"\bchuyến đi\b", r"\bkỳ nghỉ\b", r"\bhành lý\b"],
    "vehicles_transport": [r"\bcar\w*", r"\bbus\w*", r"\btrain\w*", r"\bplane\w*", r"\bflight\b", r"\bdrive\w*", r"\bdriver\b", r"\btraffic\b", r"\broad\b", r"\bstreet\b", r"\bbicycle\b", r"\bbike\b", r"\bship\b", r"\bboat\b", r"\bxe\b", r"\bgiao thông\b", r"\bđường phố\b", r"\blái xe\b"],
    "hotel_hospitality": [r"\bhotel\w*", r"\broom\b", r"\bguest\b", r"\breserv\w*", r"\bcheck in\b", r"\breception\b", r"\binn\b", r"\bresort\b", r"\bhostel\b", r"\bkhách sạn\b", r"\bphòng\b", r"\bđặt phòng\b", r"\blưu trú\b"],
    "navigation_places": [r"\bmap\b", r"\bdirection\w*", r"\bnorth\b", r"\bsouth\b", r"\beast\b", r"\bwest\b", r"\bleft\b", r"\bright\b", r"\bstraight\b", r"\blocat\w*", r"\bplace\b", r"\bcorner\b", r"\bphương hướng\b", r"\bbản đồ\b", r"\bvị trí\b"],
    "house_home": [r"\bhouse\w*", r"\bhome\b", r"\bkitchen\b", r"\bbath\w*", r"\bbed\w*", r"\bdoor\b", r"\bwindow\b", r"\broof\b", r"\bwall\b", r"\bfloor\b", r"\bfurniture\b", r"\btable\b", r"\bchair\b", r"\bapartment\b", r"\bflat\b", r"\bnhà\b", r"\bphòng\b", r"\bcửa\b", r"\bbàn\b", r"\bghế\b"],
    "family_life": [r"\bfamily\b", r"\bparent\w*", r"\bmother\b", r"\bfather\b", r"\bson\b", r"\bdaughter\b", r"\bbrother\b", r"\bsister\b", r"\bchild\w*", r"\bbaby\b", r"\bhusband\b", r"\bwife\b", r"\bmarry\b", r"\bmarriage\b", r"\bgia đình\b", r"\bcha\b", r"\bmẹ\b", r"\bcon\b", r"\banh em\b", r"\bvợ\b", r"\bchồng\b"],
    "food_cooking": [r"\bfood\b", r"\beat\w*", r"\bdrink\w*", r"\bcook\w*", r"\bmeal\b", r"\bdinner\b", r"\blunch\b", r"\bbreakfast\b", r"\brestaurant\b", r"\bbread\b", r"\bmeat\b", r"\bfruit\b", r"\bvegetable\w*", r"\bsugar\b", r"\btaste\b", r"\băn\b", r"\buống\b", r"\bnấu\b", r"\bmón ăn\b", r"\bbữa\b", r"\bthức ăn\b"],
    "clothing_fashion": [r"\bcloth\w*", r"\bwear\w*", r"\bshirt\b", r"\bdress\w*", r"\bpants\b", r"\btrousers\b", r"\bshoes\b", r"\bhat\b", r"\bcoat\b", r"\bjacket\b", r"\bfashion\b", r"\bstyle\b", r"\bquần áo\b", r"\bmặc\b", r"\bváy\b", r"\bgiày\b", r"\bthời trang\b"],
    "shopping_services": [r"\bshop\w*", r"\bstore\b", r"\bpurchase\b", r"\bprice\b", r"\bpay\w*", r"\bbill\b", r"\bdiscount\b", r"\bcheap\b", r"\bexpensive\b", r"\bsale\b", r"\bmua sắm\b", r"\bchi trả\b", r"\bgiá cả\b", r"\bhóa đơn\b"],
    "music_cinema": [r"\bmusic\w*", r"\bsong\w*", r"\bsing\w*", r"\bfilm\w*", r"\bmovie\w*", r"\bactor\b", r"\bactress\b", r"\btheatre\b", r"\btheater\b", r"\bconcert\b", r"\bcinema\b", r"\bdance\w*", r"\bband\b", r"\bâm nhạc\b", r"\bbài hát\b", r"\bphim\b", r"\bdiễn viên\b", r"\brạp\b"],
    "sports_fitness": [r"\bsport\w*", r"\bgame\w*", r"\bplay\w*", r"\bfootball\b", r"\bsoccer\b", r"\bmatch\b", r"\bball\b", r"\bteam\b", r"\bwin\w*", r"\blose\w*", r"\bscore\b", r"\brace\b", r"\bplayer\b", r"\bthể thao\b", r"\btrò chơi\b", r"\bbóng đá\b", r"\btrận đấu\b", r"\bchiến thắng\b"],
    "arts_literature": [r"\bart\w*", r"\bartist\b", r"\bpaint\w*", r"\bdraw\w*", r"\bmuseum\b", r"\bgallery\b", r"\bpoem\w*", r"\bpoetry\b", r"\bnovel\b", r"\bstory\b", r"\bliterat\w*", r"\bauthor\b", r"\bhội họa\b", r"\bvăn học\b", r"\bvẽ\b", r"\bnghệ thuật\b", r"\btiểu thuyết\b"],
    "hobbies_celebration": [r"\bhobby\b", r"\bparty\b", r"\bfun\b", r"\bcelebrat\w*", r"\bfestival\b", r"\bphoto\w*", r"\bphotograph\w*", r"\bclimb\w*", r"\bfishing\b", r"\bcamp\w*", r"\bsở thích\b", r"\btiệc\b", r"\blễ hội\b", r"\bvui chơi\b"],
    "government_politics": [r"\bgovernment\b", r"\bpolitic\w*", r"\bpresident\b", r"\bminister\b", r"\bparty\b", r"\bparliament\b", r"\belect\w*", r"\bvote\w*", r"\bleader\w*", r"\bnation\w*", r"\bstate\b", r"\bchính phủ\b", r"\bchính trị\b", r"\bbầu cử\b", r"\blãnh đạo\b", r"\bquốc gia\b"],
    "law_justice": [r"\blaw\w*", r"\bcrime\w*", r"\bcriminal\b", r"\bpolice\b", r"\bcourt\b", r"\bjudge\b", r"\bprison\b", r"\bprisoner\b", r"\bpunish\w*", r"\billegal\b", r"\blegal\b", r"\bguilty\b", r"\bpháp luật\b", r"\btội phạm\b", r"\bcảnh sát\b", r"\btòa án\b", r"\btù\b"],
    "society_culture": [r"\bsociety\b", r"\bcommunit\w*", r"\bcultur\w*", r"\btradition\w*", r"\bcustom\b", r"\bpublic\b", r"\bcitizen\b", r"\bhuman\b", r"\bpeople\b", r"\bpopulat\w*", r"\bxã hội\b", r"\bvăn hóa\b", r"\bcộng đồng\b", r"\bngười dân\b"],
    "military_security": [r"\bwar\b", r"\bpeace\b", r"\bmilitary\b", r"\barmy\b", r"\bsoldier\b", r"\bweapon\b", r"\battack\b", r"\bdefen\w*", r"\bguard\b", r"\bsecurity\b", r"\bquân đội\b", r"\bchiến tranh\b", r"\ban ninh\b", r"\bbảo vệ\b"],
    "feelings_moods": [r"\bfeel\w*", r"\bhapp\w*", r"\bsad\w*", r"\bangr\w*", r"\bemotion\w*", r"\blove\b", r"\bhate\b", r"\bfear\b", r"\bworry\b", r"\bglad\b", r"\bjoy\b", r"\bdisappoint\w*", r"\bcảm xúc\b", r"\btâm trạng\b", r"\bvui\b", r"\bbuồn\b", r"\bgiận\b", r"\blo lắng\b"],
    "personality_character": [r"\bkind\b", r"\bbrave\b", r"\bhonest\b", r"\blazy\b", r"\bsmart\b", r"\bclever\b", r"\bpolite\b", r"\brude\b", r"\bshy\b", r"\bcalm\b", r"\bgenerous\b", r"\bpatient\b", r"\btính cách\b", r"\bphẩm chất\b", r"\btốt bụng\b", r"\bdũng cảm\b", r"\blịch sự\b"],
    "thought_decision": [r"\bthink\w*", r"\bthought\b", r"\bidea\b", r"\bdecid\w*", r"\bdecision\b", r"\bconsid\w*", r"\bremember\w*", r"\bforget\b", r"\bbeliev\w*", r"\bknow\w*", r"\breason\b", r"\bsuy nghĩ\b", r"\bý nghĩ\b", r"\bquyết định\b", r"\bnhận thức\b", r"\bnhớ\b"],
    "conversation_speech": [r"\bspeak\w*", r"\btalk\w*", r"\bsay\w*", r"\btell\w*", r"\bconvers\w*", r"\bdiscuss\w*", r"\bargu\w*", r"\bask\w*", r"\banswer\b", r"\bwhisper\b", r"\bshout\b", r"\bexplain\w*", r"\bgiao tiếp\b", r"\bnói\b", r"\btrò chuyện\b", r"\bthảo luận\b", r"\bgiải thích\b"],
    "social_relations": [r"\bfriend\w*", r"\bpartner\b", r"\brelationship\b", r"\btrust\b", r"\bhelp\w*", r"\bmeet\w*", r"\bguest\b", r"\bneighbor\w*", r"\bstranger\b", r"\btình bạn\b", r"\bmối quan hệ\b", r"\bbạn bè\b", r"\bgiúp đỡ\b"],
    "time_calendar": [r"\btime\b", r"\bday\w*", r"\byear\w*", r"\bmonth\w*", r"\bweek\w*", r"\bhour\w*", r"\bminute\w*", r"\bsecond\w*", r"\bmorning\b", r"\bafternoon\b", r"\bevening\b", r"\bnight\b", r"\balways\b", r"\bnever\b", r"\boften\b", r"\bsometimes\b", r"\bearly\b", r"\blate\b", r"\bthời gian\b", r"\bngày\b", r"\bnăm\b", r"\btháng\b", r"\bgiờ\b"],
    "quantity_measurement": [r"\bnumber\w*", r"\bmuch\b", r"\bmany\b", r"\bfew\b", r"\blittle\b", r"\bsize\b", r"\bbig\b", r"\bsmall\b", r"\bmeasur\w*", r"\bweight\b", r"\bheavy\b", r"\blight\b", r"\blong\b", r"\bshort\b", r"\bhigh\b", r"\blow\b", r"\bdeep\b", r"\bsố lượng\b", r"\bđo lường\b", r"\bkích thước\b", r"\bnặng\b", r"\bnhẹ\b"],
    "actions_change": [r"\bstart\w*", r"\bstop\w*", r"\bbegin\w*", r"\bfinish\w*", r"\bchange\w*", r"\bmove\w*", r"\bturn\w*", r"\bbecome\w*", r"\bcreat\w*", r"\bhappen\w*", r"\bcause\w*", r"\baction\w*", r"\bdevelop\w*", r"\bhành động\b", r"\bbiến đổi\b", r"\bbắt đầu\b", r"\bkết thúc\b", r"\bphát triển\b"],
    "qualities_states": [r"\bgood\b", r"\bbad\b", r"\bperfect\b", r"\bsimple\b", r"\bcomplex\b", r"\beasy\b", r"\bdifficult\b", r"\bhard\b", r"\bsafe\b", r"\bdanger\w*", r"\btrue\b", r"\bfalse\b", r"\breal\b", r"\bđặc điểm\b", r"\btính chất\b", r"\btrạng thái\b", r"\btốt\b", r"\bxấu\b"]
}

# Mapping subtopic to group
TOPIC_TO_GROUP = {}
for g in TOPIC_GROUPS:
    for t in g["topics"]:
        TOPIC_TO_GROUP[t["id"]] = {
            "group_id": g["id"],
            "group_name_vi": g["name_vi"],
            "group_name_en": g["name_en"],
            "topic_id": t["id"],
            "topic_name_vi": t["name_vi"],
            "topic_name_en": t["name_en"],
            "topic_icon": t["icon"]
        }

def classify_word(word, definitions_str, translations_str, examples_str):
    search_text = f"{word} {definitions_str} {translations_str} {examples_str}".lower()
    
    scores = {}
    for topic_id, patterns in TOPIC_RULES.items():
        score = 0
        for pat in patterns:
            matches = len(re.findall(pat, search_text))
            score += matches
        if score > 0:
            scores[topic_id] = score
            
    if scores:
        best_topic = max(scores.items(), key=lambda x: x[1])[0]
        return best_topic
    
    # Fallback assignment based on part of speech or word length
    return "qualities_states"

print("Starting vocabulary aggregation & enrichment...")

# 1. Load vocabulary.json
with open(VOCAB_PATH, 'r', encoding='utf-8') as f:
    vocab_raw = json.load(f)
vocab_data = vocab_raw.get('data', [])

# 2. Load Oxford datasets
ox_data = {}
if os.path.exists(OX3_PATH):
    with open(OX3_PATH, 'r', encoding='utf-8') as f:
        ox3 = json.load(f)
        for item in ox3.values():
            w = item.get('word', '').strip().lower()
            if w and w not in ox_data:
                ox_data[w] = item

if os.path.exists(OX5_PATH):
    with open(OX5_PATH, 'r', encoding='utf-8') as f:
        ox5 = json.load(f)
        for item in ox5.values():
            w = item.get('word', '').strip().lower()
            if w and w not in ox_data:
                ox_data[w] = item

# 3. Load Synonyms
synonyms_map = {}
if os.path.exists(SYNONYMS_PATH):
    with open(SYNONYMS_PATH, 'r', encoding='utf-8') as f:
        synonyms_raw = json.load(f)
        for k, syns in synonyms_raw.items():
            # Key might be word_pos_id or word
            base_word = k.split('_')[0].lower()
            if base_word not in synonyms_map:
                synonyms_map[base_word] = set()
            for s in syns[:6]:
                if s.lower() != base_word:
                    synonyms_map[base_word].add(s.lower())

# 4. Group vocabulary entries by word
word_entries = {}
for entry in vocab_data:
    w = entry.get('word', '').strip().lower()
    if not w:
        continue
    word_entries.setdefault(w, []).append(entry)

print(f"Total unique words to process: {len(word_entries)}")

enriched_words = []
sentences_to_translate = set()

for word, entries in word_entries.items():
    # Pick primary entry or first
    primary = next((e for e in entries if e.get('is_primary')), entries[0])
    
    # IPA
    ipa = primary.get('ipa') or primary.get('phonetic') or ""
    if not ipa:
        for e in entries:
            if e.get('ipa') or e.get('phonetic'):
                ipa = e.get('ipa') or e.get('phonetic')
                break
    if not ipa and word in ox_data:
        ipa = ox_data[word].get('phon_n_am') or ox_data[word].get('phon_br') or ""
    
    # Part of speech
    pos = primary.get('pos', '').strip().lower()
    if not pos and word in ox_data:
        pos = ox_data[word].get('type', '').strip().lower()
    if not pos:
        pos = "noun"
        
    # Standardize pos
    if "verb" in pos: pos = "verb"
    elif "noun" in pos: pos = "noun"
    elif "adj" in pos: pos = "adjective"
    elif "adv" in pos: pos = "adverb"
    elif "prep" in pos: pos = "preposition"
    elif "conj" in pos: pos = "conjunction"
    elif "pron" in pos: pos = "pronoun"
    
    # CEFR Level (strictly A1 to C1)
    cefr = "B1" # Default
    if word in ox_data and ox_data[word].get('cefr'):
        raw_cefr = ox_data[word]['cefr'].strip().upper()
        if raw_cefr in ['A1', 'A2', 'B1', 'B2', 'C1']:
            cefr = raw_cefr
    else:
        # Determine from difficulty or word length
        diff = primary.get('difficulty', 1)
        if diff == 1:
            if len(word) <= 4: cefr = "A1"
            elif len(word) <= 6: cefr = "A2"
            else: cefr = "B1"
        else:
            if len(word) >= 9: cefr = "C1"
            else: cefr = "B2"
            
    # Vietnamese Meaning & English Definition
    meaning_vi = primary.get('translation_vi', '').strip()
    all_vis = [e.get('translation_vi', '').strip() for e in entries if e.get('translation_vi')]
    if not meaning_vi and all_vis:
        meaning_vi = all_vis[0]
    # If secondary meanings exist, combine up to 2 distinct meanings
    distinct_vis = []
    for vi in all_vis:
        if vi and vi not in distinct_vis:
            distinct_vis.append(vi)
    if len(distinct_vis) > 1:
        meaning_vi = ", ".join(distinct_vis[:2])
        
    definition_en = primary.get('definition_en', '').strip()
    if not definition_en and word in ox_data:
        definition_en = ox_data[word].get('definition', '').strip()
        
    # Synonyms
    syns = list(synonyms_map.get(word, []))[:4]
    
    # Gather 2-3 Example Sentences
    examples_list = []
    seen_en = set()
    
    # 1. From Cambridge entries
    for e in entries:
        eg = e.get('example_en', '').strip()
        if eg and eg.lower() not in seen_en:
            seen_en.add(eg.lower())
            examples_list.append({"en": eg, "vi": ""})
            if len(examples_list) >= 3:
                break
                
    # 2. From Oxford if needed
    if len(examples_list) < 3 and word in ox_data:
        ox_eg = ox_data[word].get('example', '').strip()
        if ox_eg and ox_eg.lower() not in seen_en:
            seen_en.add(ox_eg.lower())
            examples_list.append({"en": ox_eg, "vi": ""})
            
    # 3. If still needed, look up sentences.json or fallback
    if len(examples_list) < 2:
        # Fallback simple natural sentence
        if pos == "verb":
            fb_eg = f"You should {word} carefully before making a final decision."
        elif pos == "adjective":
            fb_eg = f"This is a very {word} example for your reference."
        elif pos == "noun":
            fb_eg = f"The {word} plays an important role in our daily lives."
        else:
            fb_eg = f"She used the word '{word}' in a clear and natural way."
            
        if fb_eg.lower() not in seen_en:
            seen_en.add(fb_eg.lower())
            examples_list.append({"en": fb_eg, "vi": ""})
            
    # Cap at 2-3 examples
    examples_list = examples_list[:3]
    
    # Mark examples that need translation
    for ex in examples_list:
        en_sent = ex["en"]
        if en_sent in trans_cache:
            ex["vi"] = trans_cache[en_sent]
        else:
            sentences_to_translate.add(en_sent)
            
    # Classify into topic
    all_defs_str = " ".join([e.get('definition_en', '') for e in entries])
    all_vis_str = " ".join(all_vis)
    all_egs_str = " ".join([ex["en"] for ex in examples_list])
    topic_id = classify_word(word, all_defs_str, all_vis_str, all_egs_str)
    topic_info = TOPIC_TO_GROUP.get(topic_id, TOPIC_TO_GROUP["qualities_states"])
    
    enriched_words.append({
        "id": word.replace(" ", "_"),
        "word": word,
        "ipa": ipa,
        "pos": pos,
        "level": cefr,
        "topic_group_id": topic_info["group_id"],
        "topic_group_vi": topic_info["group_name_vi"],
        "topic_group_en": topic_info["group_name_en"],
        "topic_id": topic_info["topic_id"],
        "topic_vi": topic_info["topic_name_vi"],
        "topic_en": topic_info["topic_name_en"],
        "topic_icon": topic_info["topic_icon"],
        "meaning_vi": meaning_vi,
        "definition_en": definition_en,
        "synonyms": syns,
        "examples": examples_list
    })

print(f"Total enriched words prepared: {len(enriched_words)}")
print(f"Sentences needing translation: {len(sentences_to_translate)}")

# Batch translate missing sentences
if sentences_to_translate:
    print(f"Translating {len(sentences_to_translate)} sentences concurrently...")
    sent_list = list(sentences_to_translate)
    
    def worker(sent):
        return sent, translate_sentence(sent)
        
    start_t = time.time()
    with ThreadPoolExecutor(max_workers=16) as executor:
        for idx, (sent, vi_trans) in enumerate(executor.map(worker, sent_list)):
            if (idx + 1) % 500 == 0 or (idx + 1) == len(sent_list):
                print(f"Progress: {idx + 1}/{len(sent_list)} translated in {time.time() - start_t:.1f}s")
                
    # Save updated translation cache
    with open(CACHE_TRANS_PATH, 'w', encoding='utf-8') as f:
        json.dump(trans_cache, f, ensure_ascii=False, indent=2)
    print("Translation cache saved.")

# Fill translations into enriched_words
for item in enriched_words:
    for ex in item["examples"]:
        if not ex["vi"]:
            ex["vi"] = trans_cache.get(ex["en"], "")

# Sort words alphabetically
enriched_words.sort(key=lambda x: x["word"].lower())

# Build topic stats
topic_counts = {}
group_counts = {}
for w in enriched_words:
    tid = w["topic_id"]
    gid = w["topic_group_id"]
    topic_counts[tid] = topic_counts.get(tid, 0) + 1
    group_counts[gid] = group_counts.get(gid, 0) + 1

# Attach word counts to TOPIC_GROUPS
final_topic_groups = []
for g in TOPIC_GROUPS:
    g_copy = dict(g)
    g_copy["count"] = group_counts.get(g["id"], 0)
    g_topics = []
    for t in g["topics"]:
        t_copy = dict(t)
        t_copy["count"] = topic_counts.get(t["id"], 0)
        g_topics.append(t_copy)
    g_copy["topics"] = g_topics
    final_topic_groups.append(g_copy)

# Save JSON dataset
output_data = {
    "version": "1.0",
    "totalWords": len(enriched_words),
    "topicGroups": final_topic_groups,
    "words": enriched_words
}

with open(OUT_JSON_PATH, 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)
print(f"Saved {OUT_JSON_PATH} successfully! Total words: {len(enriched_words)}")

# Save JS dataset for direct local file:// support
with open(OUT_JS_PATH, 'w', encoding='utf-8') as f:
    f.write("// Auto-generated vocabulary by topics dataset\n")
    f.write("window.VOCAB_TOPICS_METADATA = " + json.dumps({
        "version": "1.0",
        "totalWords": len(enriched_words),
        "topicGroups": final_topic_groups
    }, ensure_ascii=False) + ";\n\n")
    f.write("window.VOCAB_WORDS = " + json.dumps(enriched_words, ensure_ascii=False) + ";\n")
print(f"Saved {OUT_JS_PATH} successfully!")

print("\n--- Summary ---")
print(f"Total Words: {len(enriched_words)}")
for g in final_topic_groups:
    print(f"{g['icon']} {g['name_vi']}: {g['count']} words")
