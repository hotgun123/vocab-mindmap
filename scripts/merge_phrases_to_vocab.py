# -*- coding: utf-8 -*-
"""
Master Merger Script:
Combines existing 3,145 single words with 360+ curated phrases & collocations.
Tags every item with `is_phrase: false` (for words) or `is_phrase: true` (for phrases).
Recalculates topicGroup counts and topic counts.
Saves to data/topics_vocabulary.json and data/topics_vocab_data.js.
"""

import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
DATA_DIR = os.path.join(BASE_DIR, 'data')
VOCAB_JSON_PATH = os.path.join(DATA_DIR, 'topics_vocabulary.json')
VOCAB_JS_PATH = os.path.join(DATA_DIR, 'topics_vocab_data.js')

# Import phrase datasets
from scripts.phrases_data.travel_phrases import TRAVEL_PHRASES
from scripts.phrases_data.business_phrases import BUSINESS_PHRASES
from scripts.phrases_data.daily_phrases import DAILY_PHRASES
from scripts.phrases_data.education_phrases import EDUCATION_PHRASES
from scripts.phrases_data.health_phrases import HEALTH_PHRASES
from scripts.phrases_data.communication_phrases import COMMUNICATION_PHRASES
from scripts.phrases_data.tech_phrases import TECH_PHRASES
from scripts.phrases_data.nature_phrases import NATURE_PHRASES
from scripts.phrases_data.arts_phrases import ARTS_PHRASES
from scripts.phrases_data.society_phrases import SOCIETY_PHRASES
from scripts.phrases_data.emotions_phrases import EMOTIONS_PHRASES
from scripts.phrases_data.general_phrases import GENERAL_PHRASES
from scripts.phrases_data.extra_phrases import EXTRA_PHRASES
from scripts.phrases_data.extra_phrases_2 import EXTRA_PHRASES_2
from scripts.phrases_data.extra_phrases_3 import EXTRA_PHRASES_3
from scripts.phrases_catalog import PHRASES

# Additional iconic English collocations & idioms to guarantee >365 items
BONUS_PHRASES = [
    {
        "word": "rain cats and dogs",
        "ipa": "/reɪn kæts ænd dɒɡz/",
        "pos": "idiom",
        "level": "A2",
        "topic_group_id": "nature_environment",
        "topic_group_vi": "Môi trường & Thiên nhiên",
        "topic_id": "weather_seasons",
        "topic_vi": "Thời tiết & Khí hậu",
        "topic_icon": "🌦️",
        "meaning_vi": "mưa như trút nước, mưa tầm tã",
        "definition_en": "to rain very heavily and continuously",
        "synonyms": ["pour down", "bucket down"],
        "examples": [
            {"en": "We had to cancel the picnic because it was raining cats and dogs outside.", "vi": "Chúng tôi phải hủy buổi dã ngoại vì bên ngoài trời đang mưa như trút nước."},
            {"en": "Don't forget your raincoat; the forecast says it will rain cats and dogs.", "vi": "Đừng quên áo mưa nhé; dự báo thời tiết nói hôm nay trời sẽ mưa tầm tã đấy."}
        ]
    },
    {
        "word": "bite off more than you can chew",
        "ipa": "/baɪt ɒf mɔːr ðæn juː kæn tʃuː/",
        "pos": "idiom",
        "level": "B2",
        "topic_group_id": "general_concepts",
        "topic_group_vi": "Khái niệm chung & Đo lường",
        "topic_id": "actions_change",
        "topic_vi": "Hành động & Biến đổi",
        "topic_icon": "🔄",
        "meaning_vi": "ôm đồm quá nhiều việc vượt quá khả năng gánh vác",
        "definition_en": "to take on a commitment or task that is far too big or difficult to handle",
        "synonyms": ["overcommit", "overextend oneself"],
        "examples": [
            {"en": "Taking on three client projects simultaneously was biting off more than he could chew.", "vi": "Nhận ba dự án khách hàng cùng lúc quả là ôm đồm quá sức đối với anh ấy."},
            {"en": "Be honest about your bandwidth so you don't bite off more than you can chew.", "vi": "Hãy thành thật về thời gian của mình để không gánh việc quá sức."}
        ]
    },
    {
        "word": "better late than never",
        "ipa": "/ˈbet.ər leɪt ðæn ˈnev.ər/",
        "pos": "idiom",
        "level": "A1",
        "topic_group_id": "general_concepts",
        "topic_group_vi": "Khái niệm chung & Đo lường",
        "topic_id": "time_calendar",
        "topic_vi": "Thời gian & Lịch trình",
        "topic_icon": "⏳",
        "meaning_vi": "muộn còn hơn không bao giờ làm",
        "definition_en": "it is preferable to arrive or do something late than not at all",
        "synonyms": ["eventual arrival is good"],
        "examples": [
            {"en": "He started learning computer programming at forty-five—better late than never!", "vi": "Anh ấy bắt đầu học lập trình máy tính ở tuổi bốn mươi lăm—muộn còn hơn không bao giờ!"},
            {"en": "Thank you for sending the signed agreement; better late than never.", "vi": "Cảm ơn bạn đã gửi bản hợp đồng có chữ ký; đến muộn vẫn tốt hơn là không gửi."}
        ]
    },
    {
        "word": "keep your fingers crossed",
        "ipa": "/kiːp jɔː ˈfɪŋ.ɡəz krɒst/",
        "pos": "idiom",
        "level": "B1",
        "topic_group_id": "emotions_mind",
        "topic_group_vi": "Cảm xúc & Tính cách",
        "topic_id": "feelings_moods",
        "topic_vi": "Cảm xúc & Tâm trạng",
        "topic_icon": "😊",
        "meaning_vi": "cầu chúc may mắn, hy vọng mọi chuyện suôn sẻ",
        "definition_en": "to hope or wish strongly for good fortune or a successful outcome",
        "synonyms": ["wish for luck", "hope for the best"],
        "examples": [
            {"en": "I'm keeping my fingers crossed that you receive the scholarship offer.", "vi": "Tôi đang cầu chúc may mắn để bạn nhận được học bổng đó."},
            {"en": "Keep your fingers crossed while the judges deliberate on the final scores.", "vi": "Hãy cầu chúc may mắn trong lúc ban giám khảo cân nhắc điểm số chung cuộc."}
        ]
    },
    {
        "word": "on the fence",
        "ipa": "/ɒn ðə fens/",
        "pos": "idiom",
        "level": "B2",
        "topic_group_id": "emotions_mind",
        "topic_group_vi": "Cảm xúc & Tính cách",
        "topic_id": "thought_decision",
        "topic_vi": "Tư duy & Nhận thức",
        "topic_icon": "💡",
        "meaning_vi": "lưỡng lự chưa quyết định, đứng giữa hai ngả",
        "definition_en": "undecided, neutral, or hesitating between two opposing choices or opinions",
        "synonyms": ["undecided", "hesitant", "vacillating"],
        "examples": [
            {"en": "Many independent voters remain on the fence regarding the tax reform proposal.", "vi": "Nhiều cử tri độc lập vẫn đang lưỡng lự chưa quyết định về đề xuất cải cách thuế."},
            {"en": "I'm still on the fence about whether to study law or business administration.", "vi": "Tôi vẫn đang phân vân đứng giữa ngã ba đường xem nên học luật hay quản trị kinh doanh."}
        ]
    },
    {
        "word": "burn the midnight oil",
        "ipa": "/bɜːn ðə ˈmɪd.naɪt ɔɪl/",
        "pos": "idiom",
        "level": "B2",
        "topic_group_id": "education_academia",
        "topic_group_vi": "Giáo dục & Học thuật",
        "topic_id": "study_exams",
        "topic_vi": "Học tập & Thi cử",
        "topic_icon": "📚",
        "meaning_vi": "thức khuya chong đèn làm việc/học bài thâu đêm",
        "definition_en": "to read, study, or work late into the night",
        "synonyms": ["work late", "stay up late"],
        "examples": [
            {"en": "Medical students often burn the midnight oil preparing for anatomy practicals.", "vi": "Sinh viên y khoa thường xuyên thức khuya học bài thâu đêm để chuẩn bị cho kỳ thi giải phẫu."},
            {"en": "The legal defense team burned the midnight oil examining evidence files.", "vi": "Đội ngũ luật sư bào chữa đã làm việc thâu đêm suốt sáng để nghiên cứu hồ sơ chứng cứ."}
        ]
    },
    {
        "word": "throw in the towel",
        "ipa": "/θrəʊ ɪn ðə ˈtaʊ.əl/",
        "pos": "idiom",
        "level": "B2",
        "topic_group_id": "general_concepts",
        "topic_group_vi": "Khái niệm chung & Đo lường",
        "topic_id": "actions_change",
        "topic_vi": "Hành động & Biến đổi",
        "topic_icon": "🔄",
        "meaning_vi": "nhận thua, bỏ cuộc, đầu hàng",
        "definition_en": "to abandon an effort, admit defeat, or quit trying",
        "synonyms": ["give up", "surrender", "quit"],
        "examples": [
            {"en": "After five grueling sets, the exhausted tennis player refused to throw in the towel.", "vi": "Sau năm hiệp đấu nghẹt thở, tay vợt mệt nhoài vẫn kiên quyết không chịu bỏ cuộc."},
            {"en": "Never throw in the towel on your aspirations after a single setback.", "vi": "Đừng bao giờ từ bỏ hoài bão của mình chỉ sau một lần vấp ngã."}
        ]
    },
    {
        "word": "call the shots",
        "ipa": "/kɔːl ðə ʃɒts/",
        "pos": "idiom",
        "level": "B2",
        "topic_group_id": "business_work",
        "topic_group_vi": "Kinh doanh & Nghề nghiệp",
        "topic_id": "office_work",
        "topic_vi": "Công sở & Quản lý",
        "topic_icon": "🏢",
        "meaning_vi": "nắm quyền chỉ đạo, là người ra quyết định chính",
        "definition_en": "to be in charge, have the final authority, or make the major decisions",
        "synonyms": ["be in charge", "run the show"],
        "examples": [
            {"en": "As managing director, she is the one who ultimately calls the shots.", "vi": "Là giám đốc điều hành, cô ấy là người nắm quyền quyết định cuối cùng."},
            {"en": "Investors may fund the company, but founders prefer to call the shots on product design.", "vi": "Các nhà đầu tư có thể rót tiền, nhưng các nhà sáng lập muốn tự quyết định về thiết kế sản phẩm."}
        ]
    },
    {
        "word": "water under the bridge",
        "ipa": "/ˈwɔː.tər ˈʌn.də ðə brɪdʒ/",
        "pos": "idiom",
        "level": "B2",
        "topic_group_id": "communication_social",
        "topic_group_vi": "Giao tiếp & Quan hệ",
        "topic_id": "social_relations",
        "topic_vi": "Tình bạn & Quan hệ xã hội",
        "topic_icon": "🤝",
        "meaning_vi": "chuyện cũ đã qua như nước chảy qua cầu, không nên bận tâm nữa",
        "definition_en": "past events or disagreements that are finished and cannot be altered, so should be forgotten",
        "synonyms": ["past history", "forgiven and forgotten"],
        "examples": [
            {"en": "We had bitter arguments in the past, but all that is water under the bridge now.", "vi": "Trong quá khứ chúng tôi từng cãi vã gay gắt, nhưng giờ mọi chuyện đã trôi qua như nước chảy qua cầu."},
            {"en": "Let's shake hands and treat former rivalries as water under the bridge.", "vi": "Hãy bắt tay nhau và xem những hiềm khích trước đây chỉ là dĩ vãng đã qua."}
        ]
    },
    {
        "word": "face the music",
        "ipa": "/feɪs ðə ˈmjuː.zɪk/",
        "pos": "idiom",
        "level": "B2",
        "topic_group_id": "communication_social",
        "topic_group_vi": "Giao tiếp & Quan hệ",
        "topic_id": "conversation_speech",
        "topic_vi": "Giao tiếp & Hội thoại",
        "topic_icon": "💬",
        "meaning_vi": "chấp nhận đối mặt với hậu quả, chịu trách nhiệm cho lỗi lầm",
        "definition_en": "to confront and accept the unpleasant consequences of one's actions",
        "synonyms": ["accept consequences", "take responsibility"],
        "examples": [
            {"en": "He broke the client contract and now he has to go in and face the music.", "vi": "Anh ấy đã phá vỡ hợp đồng khách hàng và giờ anh phải vào đối mặt với hậu quả."},
            {"en": "Instead of evading blame, mature leaders stand up and face the music.", "vi": "Thay vì trốn tránh trách nhiệm, những người lãnh đạo trưởng thành luôn đứng lên chịu trách nhiệm."}
        ]
    },
    {
        "word": "on cloud nine",
        "ipa": "/ɒn klaʊd naɪn/",
        "pos": "idiom",
        "level": "B1",
        "topic_group_id": "emotions_mind",
        "topic_group_vi": "Cảm xúc & Tính cách",
        "topic_id": "feelings_moods",
        "topic_vi": "Cảm xúc & Tâm trạng",
        "topic_icon": "😊",
        "meaning_vi": "lâng lâng trong hạnh phúc, sung sướng ngập tràn",
        "definition_en": "in a state of supreme happiness, elation, or bliss",
        "synonyms": ["in seventh heaven", "overjoyed", "blissful"],
        "examples": [
            {"en": "Ever since she welcomed her baby girl, she has been floating on cloud nine.", "vi": "Kể từ khi đón bé gái chào đời, cô ấy luôn lâng lâng trong niềm hạnh phúc ngập tràn."},
            {"en": "The artist was on cloud nine when his debut album shot straight to number one.", "vi": "Nghệ sĩ sung sướng như ở trên chín tầng mây khi album đầu tay vươn thẳng lên vị trí số một."}
        ]
    },
    {
        "word": "stand your ground",
        "ipa": "/stænd jɔː ɡraʊnd/",
        "pos": "idiom",
        "level": "B2",
        "topic_group_id": "emotions_mind",
        "topic_group_vi": "Cảm xúc & Tính cách",
        "topic_id": "personality_character",
        "topic_vi": "Tính cách & Phẩm chất",
        "topic_icon": "🌟",
        "meaning_vi": "giữ vững lập trường, không nao núng nhượng bộ",
        "definition_en": "to maintain one's position or opinion resolutely against criticism or pressure",
        "synonyms": ["hold firm", "remain steadfast"],
        "examples": [
            {"en": "Despite aggressive opposition, the community leader stood his ground firmly.", "vi": "Bất chấp sự phản đối gay gắt, người lãnh đạo cộng đồng vẫn kiên quyết giữ vững lập trường."},
            {"en": "Stand your ground during negotiations if you know the proposal is fair and accurate.", "vi": "Hãy giữ vững lập trường trong cuộc đàm phán nếu bạn biết đề xuất đó là công bằng và chính xác."}
        ]
    },
    {
        "word": "tip of the iceberg",
        "ipa": "/tɪp əv ðiː ˈaɪs.bɜːɡ/",
        "pos": "idiom",
        "level": "B2",
        "topic_group_id": "general_concepts",
        "topic_group_vi": "Khái niệm chung & Đo lường",
        "topic_id": "qualities_states",
        "topic_vi": "Trạng thái & Đặc tính",
        "topic_icon": "🧩",
        "meaning_vi": "phần nổi của tảng băng chìm (chỉ là phần nhỏ của vấn đề khổng lồ)",
        "definition_en": "a small, visible part of a much larger, concealed problem or complex situation",
        "synonyms": ["surface symptom"],
        "examples": [
            {"en": "The reported accounting errors are merely the tip of the iceberg in this financial scandal.", "vi": "Các sai sót kế toán được báo cáo chỉ là phần nổi của tảng băng chìm trong vụ bê bối tài chính này."},
            {"en": "Initial customer complaints were just the tip of the iceberg regarding the software flaw.", "vi": "Những lời phàn nàn ban đầu của khách hàng mới chỉ là phần nổi của một lỗi phần mềm nghiêm trọng."}
        ]
    },
    {
        "word": "ahead of time",
        "ipa": "/əˈhed əv taɪm/",
        "pos": "idiom",
        "level": "A2",
        "topic_group_id": "general_concepts",
        "topic_group_vi": "Khái niệm chung & Đo lường",
        "topic_id": "time_calendar",
        "topic_vi": "Thời gian & Lịch trình",
        "topic_icon": "⏳",
        "meaning_vi": "trước thời hạn, làm trước thời gian quy định",
        "definition_en": "earlier than expected or before the scheduled deadline",
        "synonyms": ["in advance", "early"],
        "examples": [
            {"en": "He finished writing the quarterly summary three days ahead of time.", "vi": "Anh ấy đã viết xong bản tổng kết quý trước thời hạn ba ngày."},
            {"en": "Booking train tickets ahead of time guarantees seat reservations and cheaper rates.", "vi": "Đặt vé tàu trước thời gian quy định đảm bảo giữ được chỗ ngồi và có giá vé rẻ hơn."}
        ]
    },
    {
        "word": "at the end of the day",
        "ipa": "/æt ðiː end əv ðə deɪ/",
        "pos": "idiom",
        "level": "B1",
        "topic_group_id": "general_concepts",
        "topic_group_vi": "Khái niệm chung & Đo lường",
        "topic_id": "qualities_states",
        "topic_vi": "Trạng thái & Đặc tính",
        "topic_icon": "🧩",
        "meaning_vi": "suy cho cùng, xét đến cùng, chung quy lại",
        "definition_en": "used when considering what is the most important aspect after all factors are evaluated",
        "synonyms": ["ultimately", "when all is said and done"],
        "examples": [
            {"en": "At the end of the day, client satisfaction is the only metric that truly matters.", "vi": "Suy cho cùng, sự hài lòng của khách hàng là thước đo duy nhất thực sự quan trọng."},
            {"en": "You can debate strategies endlessly, but at the end of the day results speak.", "vi": "Bạn có thể tranh luận chiến lược không hồi kết, nhưng chung quy lại kết quả mới là câu trả lời."}
        ]
    }
]

print("Loading existing topics_vocabulary.json...")
with open(VOCAB_JSON_PATH, 'r', encoding='utf-8') as f:
    vocab_data = json.load(f)

existing_words = [w for w in vocab_data.get('words', []) if not w.get('is_phrase', False)]
print(f"Loaded {len(existing_words)} existing single words.")

# Ensure existing single words have is_phrase: False
for w in existing_words:
    w['is_phrase'] = False

# Aggregate all phrases
all_phrase_sources = [
    PHRASES,
    TRAVEL_PHRASES, BUSINESS_PHRASES, DAILY_PHRASES, EDUCATION_PHRASES,
    HEALTH_PHRASES, COMMUNICATION_PHRASES, TECH_PHRASES, NATURE_PHRASES,
    ARTS_PHRASES, SOCIETY_PHRASES, EMOTIONS_PHRASES, GENERAL_PHRASES,
    EXTRA_PHRASES, EXTRA_PHRASES_2, EXTRA_PHRASES_3, BONUS_PHRASES
]

seen_phrases = set()
formatted_phrases = []

for p_list in all_phrase_sources:
    for item in p_list:
        raw_word = (item.get('word') or item.get('phrase', '')).strip()
        if not raw_word:
            continue
        norm_key = raw_word.lower()
        if norm_key in seen_phrases:
            continue
        seen_phrases.add(norm_key)

        p_id = "phrase_" + norm_key.replace(" ", "_").replace("'", "").replace("-", "_").replace(".", "").replace("/", "_")
        g_id = item.get('topic_group_id', 'general_concepts')
        t_id = item.get('topic_id', 'qualities_states')

        formatted_phrase = {
            "id": p_id,
            "word": raw_word,
            "ipa": item.get('ipa', ''),
            "pos": item.get('pos', 'phrase'),
            "level": item.get('level', 'B1'),
            "topic_group_id": g_id,
            "topic_group_vi": item.get('topic_group_vi', 'Khái niệm chung & Đo lường'),
            "topic_group_en": item.get('topic_group_en', g_id.replace("_", " ").title()),
            "topic_id": t_id,
            "topic_vi": item.get('topic_vi', 'Trạng thái & Đặc tính'),
            "topic_en": item.get('topic_en', t_id.replace("_", " ").title()),
            "topic_icon": item.get('topic_icon', '💬'),
            "meaning_vi": item.get('meaning_vi', ''),
            "definition_en": item.get('definition_en', ''),
            "synonyms": item.get('synonyms', []),
            "examples": item.get('examples', []),
            "is_phrase": True
        }
        formatted_phrases.append(formatted_phrase)

print(f"Generated {len(formatted_phrases)} unique high-quality phrases.")

# Verify all 15 user requested phrases exist
USER_REQUESTS = [
    'check-in counter', 'run behind', 'take ages', 'definitely understaffed',
    'get priority boarding', 'carry cash', "traveler's checks", 'minimalist',
    'minimalism', 'scheduled to last', 'hands-on events', 'has been pounding',
    "if you don't mind", 'on-call', "there's an opening"
]

all_phrase_words = {p['word'].lower() for p in formatted_phrases}
missing_user_reqs = [r for r in USER_REQUESTS if r.lower() not in all_phrase_words]
if missing_user_reqs:
    print(f"WARNING: Missing user phrases: {missing_user_reqs}")
else:
    print("SUCCESS: All 15 user-requested phrases are fully present and verified!")

# Combine words and phrases
all_items = existing_words + formatted_phrases
total_count = len(all_items)
print(f"Total vocabulary items (words + phrases): {total_count}")

# Recalculate topicGroup and topic counts
# Mapping topic_id -> counts
topic_counts = {}
group_counts = {}

for it in all_items:
    gid = it.get('topic_group_id')
    tid = it.get('topic_id')
    is_p = it.get('is_phrase', False)

    if gid not in group_counts:
        group_counts[gid] = {'total': 0, 'words': 0, 'phrases': 0}
    group_counts[gid]['total'] += 1
    if is_p:
        group_counts[gid]['phrases'] += 1
    else:
        group_counts[gid]['words'] += 1

    if tid not in topic_counts:
        topic_counts[tid] = {'total': 0, 'words': 0, 'phrases': 0}
    topic_counts[tid]['total'] += 1
    if is_p:
        topic_counts[tid]['phrases'] += 1
    else:
        topic_counts[tid]['words'] += 1

# Update topicGroups in vocab_data
for g in vocab_data['topicGroups']:
    gid = g['id']
    gc = group_counts.get(gid, {'total': 0, 'words': 0, 'phrases': 0})
    g['wordCount'] = gc['total']
    g['singleWordsCount'] = gc['words']
    g['phrasesCount'] = gc['phrases']

    for t in g.get('topics', []):
        tid = t['id']
        tc = topic_counts.get(tid, {'total': 0, 'words': 0, 'phrases': 0})
        t['wordCount'] = tc['total']
        t['singleWordsCount'] = tc['words']
        t['phrasesCount'] = tc['phrases']

vocab_data['totalWords'] = total_count
vocab_data['singleWordsCount'] = len(existing_words)
vocab_data['phrasesCount'] = len(formatted_phrases)
vocab_data['words'] = all_items

print(f"Saving updated vocabulary to {VOCAB_JSON_PATH}...")
with open(VOCAB_JSON_PATH, 'w', encoding='utf-8') as f:
    json.dump(vocab_data, f, ensure_ascii=False, indent=2)

print(f"Saving updated topics_vocab_data.js to {VOCAB_JS_PATH}...")
js_content = f"""// Auto-generated Topics Vocabulary Dataset
// Total Items: {total_count} ({len(existing_words)} Single Words + {len(formatted_phrases)} Phrases & Collocations)
window.VOCAB_WORDS = {json.dumps(all_items, ensure_ascii=False)};
window.VOCAB_TOPICS_METADATA = {{
  totalWords: {total_count},
  singleWordsCount: {len(existing_words)},
  phrasesCount: {len(formatted_phrases)},
  topicGroups: {json.dumps(vocab_data['topicGroups'], ensure_ascii=False)}
}};
"""

with open(VOCAB_JS_PATH, 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"Done! Successfully generated {len(formatted_phrases)} phrases. Total database items: {total_count}")
