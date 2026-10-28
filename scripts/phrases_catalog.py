# -*- coding: utf-8 -*-
"""
Phrases Catalog: 360+ High-Frequency English Collocations, Idioms, Phrasal Verbs & Expressions
Includes the user-requested phrases and curated CEFR A1-C1 phrases.
"""

PHRASES = [
    # =========================================================================
    # 1. USER EXPLICIT REQUESTS (15 Phrases)
    # =========================================================================
    {
        "phrase": "check-in counter",
        "ipa": "/ˈtʃek.ɪn ˌkaʊn.tər/",
        "pos": "collocation",
        "level": "A2",
        "topic_group_id": "travel_transport",
        "topic_group_vi": "Du lịch & Giao thông",
        "topic_id": "travel_tourism",
        "topic_vi": "Du lịch & Kỳ nghỉ",
        "topic_icon": "🧳",
        "meaning_vi": "quầy làm thủ tục (sân bay, khách sạn)",
        "definition_en": "the place at an airport or hotel where you show your ticket or reservation and check in",
        "synonyms": ["check-in desk", "registration counter"],
        "examples": [
            {"en": "Please proceed to the check-in counter to get your boarding pass.", "vi": "Vui lòng đến quầy làm thủ tục để nhận thẻ lên máy bay."},
            {"en": "There was a long line of travelers at the airline check-in counter.", "vi": "Có một hàng dài du khách tại quầy làm thủ tục của hãng hàng không."},
            {"en": "The check-in counter opens two hours before domestic flight departures.", "vi": "Quầy làm thủ tục mở trước giờ khởi hành chuyến bay nội địa hai tiếng."}
        ]
    },
    {
        "phrase": "run behind",
        "ipa": "/rʌn bɪˈhaɪnd/",
        "pos": "phrasal verb",
        "level": "B1",
        "topic_group_id": "business_work",
        "topic_group_vi": "Kinh doanh & Nghề nghiệp",
        "topic_id": "office_work",
        "topic_vi": "Công sở & Quản lý",
        "topic_icon": "🏢",
        "meaning_vi": "chậm tiến độ, trễ so với lịch trình dự kiến",
        "definition_en": "to be delayed or to be working or progressing more slowly than scheduled",
        "synonyms": ["fall behind schedule", "be delayed", "lag behind"],
        "examples": [
            {"en": "The construction project is running behind schedule due to bad weather.", "vi": "Dự án xây dựng đang bị chậm tiến độ do thời tiết xấu."},
            {"en": "I'm running a few minutes behind this morning because of heavy traffic.", "vi": "Sáng nay tôi bị trễ vài phút vì tắc đường nghiêm trọng."},
            {"en": "If we continue to run behind, we will miss our production target.", "vi": "Nếu chúng ta tiếp tục trễ tiến độ, chúng ta sẽ không đạt được mục tiêu sản xuất."}
        ]
    },
    {
        "phrase": "take ages",
        "ipa": "/teɪk ˈeɪ.dʒɪz/",
        "pos": "idiom",
        "level": "B1",
        "topic_group_id": "general_concepts",
        "topic_group_vi": "Khái niệm chung & Đo lường",
        "topic_id": "time_calendar",
        "topic_vi": "Thời gian & Lịch trình",
        "topic_icon": "⏳",
        "meaning_vi": "mất rất nhiều thời gian, lâu kinh khủng",
        "definition_en": "to take a very long time to happen or be completed",
        "synonyms": ["take forever", "drag on", "take a long time"],
        "examples": [
            {"en": "It took ages to find a parking space near the shopping center.", "vi": "Mất cả buổi mới tìm được chỗ đỗ xe gần trung tâm thương mại."},
            {"en": "Downloading that massive software update took ages.", "vi": "Việc tải bản cập nhật phần mềm khổng lồ đó mất rất nhiều thời gian."},
            {"en": "She took ages to decide what to order from the dinner menu.", "vi": "Cô ấy mất rất lâu để quyết định gọi món gì trong thực đơn bữa tối."}
        ]
    },
    {
        "phrase": "definitely understaffed",
        "ipa": "/ˈdef.ɪ.nət.li ˌʌn.dəˈstɑːft/",
        "pos": "collocation",
        "level": "B2",
        "topic_group_id": "business_work",
        "topic_group_vi": "Kinh doanh & Nghề nghiệp",
        "topic_id": "jobs_careers",
        "topic_vi": "Nghề nghiệp & Việc làm",
        "topic_icon": "🤝",
        "meaning_vi": "chắc chắn bị thiếu nhân sự, không đủ nhân viên",
        "definition_en": "clearly not having enough employees or staff to do the necessary work effectively",
        "synonyms": ["short-handed", "lacking personnel"],
        "examples": [
            {"en": "The hospital ward is definitely understaffed during the weekend night shift.", "vi": "Khu bệnh viện chắc chắn bị thiếu nhân sự trong ca trực đêm cuối tuần."},
            {"en": "Our customer support team is definitely understaffed after the new product launch.", "vi": "Đội hỗ trợ khách hàng của chúng tôi chắc chắn thiếu người sau đợt ra mắt sản phẩm mới."},
            {"en": "Customers complained about slow service because the restaurant was definitely understaffed.", "vi": "Khách hàng phàn nàn vì phục vụ chậm do nhà hàng chắc chắn không đủ nhân viên."}
        ]
    },
    {
        "phrase": "get priority boarding",
        "ipa": "/ɡet praɪˈɒr.ə.ti ˈbɔː.dɪŋ/",
        "pos": "collocation",
        "level": "B1",
        "topic_group_id": "travel_transport",
        "topic_group_vi": "Du lịch & Giao thông",
        "topic_id": "vehicles_transport",
        "topic_vi": "Phương tiện & Giao thông",
        "topic_icon": "🚗",
        "meaning_vi": "được ưu tiên lên máy bay trước",
        "definition_en": "to be allowed to board an airplane before general passengers",
        "synonyms": ["early boarding", "preferred boarding"],
        "examples": [
            {"en": "Passengers traveling with infants get priority boarding.", "vi": "Hành khách đi cùng trẻ sơ sinh được ưu tiên lên máy bay trước."},
            {"en": "Business class ticket holders always get priority boarding at the gate.", "vi": "Những người có vé hạng thương gia luôn được ưu tiên lên máy bay tại cửa khởi hành."},
            {"en": "You can pay a small extra fee to get priority boarding and skip the long line.", "vi": "Bạn có thể trả thêm một khoản phí nhỏ để được lên trước và tránh phải xếp hàng dài."}
        ]
    },
    {
        "phrase": "carry cash",
        "ipa": "/ˈkær.i kæʃ/",
        "pos": "collocation",
        "level": "A2",
        "topic_group_id": "business_work",
        "topic_group_vi": "Kinh doanh & Nghề nghiệp",
        "topic_id": "finance_banking",
        "topic_vi": "Tài chính & Tiền tệ",
        "topic_icon": "💰",
        "meaning_vi": "mang theo tiền mặt",
        "definition_en": "to have physical paper money or coins with you when going somewhere",
        "synonyms": ["have physical money", "carry paper money"],
        "examples": [
            {"en": "I rarely carry cash nowadays because I pay for everything with my smartphone.", "vi": "Dạo này tôi hiếm khi mang theo tiền mặt vì tôi thanh toán mọi thứ bằng điện thoại thông minh."},
            {"en": "It is wise to carry cash when traveling to remote rural markets.", "vi": "Rất nên mang theo tiền mặt khi đi du lịch tới các chợ ở vùng nông thôn xa xôi."},
            {"en": "Street food vendors often prefer customers to carry cash.", "vi": "Người bán đồ ăn đường phố thường thích khách hàng mang theo tiền mặt."}
        ]
    },
    {
        "phrase": "traveler's checks",
        "ipa": "/ˈtræv.əl.əz tʃeks/",
        "pos": "collocation",
        "level": "B2",
        "topic_group_id": "business_work",
        "topic_group_vi": "Kinh doanh & Nghề nghiệp",
        "topic_id": "finance_banking",
        "topic_vi": "Tài chính & Tiền tệ",
        "topic_icon": "💰",
        "meaning_vi": "séc du lịch (loại séc ngân hàng đổi tiền an toàn khi đi xa)",
        "definition_en": "preprinted, fixed-amount checks that can be exchanged for cash or used as payment abroad",
        "synonyms": ["traveller's cheques"],
        "examples": [
            {"en": "Before credit cards became universal, travelers often relied on traveler's checks.", "vi": "Trước khi thẻ tín dụng trở nên phổ biến, du khách thường dựa vào séc du lịch."},
            {"en": "You can cash your traveler's checks at the exchange counter in the hotel lobby.", "vi": "Bạn có thể đổi séc du lịch lấy tiền mặt tại quầy đổi tiền ở sảnh khách sạn."},
            {"en": "Make sure you sign your traveler's checks as soon as you purchase them from the bank.", "vi": "Hãy đảm bảo rằng bạn ký tên vào séc du lịch ngay khi mua chúng từ ngân hàng."}
        ]
    },
    {
        "phrase": "minimalist",
        "ipa": "/ˈmɪn.ɪ.məl.ɪst/",
        "pos": "noun / adj",
        "level": "B2",
        "topic_group_id": "daily_life_home",
        "topic_group_vi": "Đời sống & Gia đình",
        "topic_id": "house_home",
        "topic_vi": "Nhà cửa & Đồ nội thất",
        "topic_icon": "🏡",
        "meaning_vi": "người theo lối sống tối giản; phong cách tối giản",
        "definition_en": "a person who adopts a simple lifestyle with few possessions, or having a simple, uncluttered design",
        "synonyms": ["simple", "uncluttered", "streamlined"],
        "examples": [
            {"en": "As a devoted minimalist, he owns only essential clothes and books.", "vi": "Là một người theo chủ nghĩa tối giản chân chính, anh chỉ sở hữu quần áo và sách vở thiết yếu."},
            {"en": "Her apartment features a minimalist interior with clean lines and neutral colors.", "vi": "Căn hộ của cô có nội thất tối giản với những đường nét thanh thoát và gam màu trung tính."},
            {"en": "Adopting a minimalist mindset helped her focus on what truly matters in life.", "vi": "Áp dụng tư duy tối giản đã giúp cô tập trung vào những điều thực sự quan trọng trong cuộc sống."}
        ]
    },
    {
        "phrase": "minimalism",
        "ipa": "/ˈmɪn.ɪ.məl.ɪ.zəm/",
        "pos": "noun",
        "level": "B2",
        "topic_group_id": "daily_life_home",
        "topic_group_vi": "Đời sống & Gia đình",
        "topic_id": "house_home",
        "topic_vi": "Nhà cửa & Đồ nội thất",
        "topic_icon": "🏡",
        "meaning_vi": "chủ nghĩa tối giản, lối sống giản lược đồ đạc",
        "definition_en": "a lifestyle or art style that uses only the simplest and fewest essential elements",
        "synonyms": ["simplicity", "uncluttered living"],
        "examples": [
            {"en": "Minimalism has become an increasingly popular lifestyle among young urban professionals.", "vi": "Chủ nghĩa tối giản ngày càng trở thành lối sống phổ biến trong giới trí thức trẻ thành thị."},
            {"en": "The philosophy of minimalism encourages people to eliminate distractions and reduce clutter.", "vi": "Triết lý tối giản khuyến khích con người loại bỏ phiền nhiễu và bớt đồ đạc lộn xộn."},
            {"en": "He discovered minimalism while trying to declutter his crowded workspace.", "vi": "Anh ấy khám phá ra chủ nghĩa tối giản khi cố gắng dọn dẹp không gian làm việc chật chội của mình."}
        ]
    },
    {
        "phrase": "scheduled to last",
        "ipa": "/ˈʃedʒ.uːld tuː lɑːst/",
        "pos": "collocation",
        "level": "B1",
        "topic_group_id": "education_academia",
        "topic_group_vi": "Giáo dục & Học thuật",
        "topic_id": "study_exams",
        "topic_vi": "Học tập & Thi cử",
        "topic_icon": "📚",
        "meaning_vi": "dự kiến sẽ kéo dài trong (khoảng thời gian)",
        "definition_en": "planned or arranged to continue for a specific duration of time",
        "synonyms": ["expected to run for", "planned to take"],
        "examples": [
            {"en": "The keynote lecture is scheduled to last approximately forty-five minutes.", "vi": "Bài phát biểu chính dự kiến sẽ kéo dài khoảng 45 phút."},
            {"en": "The software training workshop is scheduled to last three full days.", "vi": "Buổi hội thảo đào tạo phần mềm dự kiến kéo dài trọn vẹn ba ngày."},
            {"en": "Their bilateral discussions are scheduled to last until tomorrow afternoon.", "vi": "Các cuộc thảo luận song phương của họ dự kiến sẽ kéo dài đến chiều mai."}
        ]
    },
    {
        "phrase": "hands-on events",
        "ipa": "/ˌhændzˈɒn ɪˈvents/",
        "pos": "collocation",
        "level": "B2",
        "topic_group_id": "education_academia",
        "topic_group_vi": "Giáo dục & Học thuật",
        "topic_id": "school_university",
        "topic_vi": "Trường học & Đại học",
        "topic_icon": "🏫",
        "meaning_vi": "các sự kiện trải nghiệm thực tế, hoạt động thực hành trực tiếp",
        "definition_en": "workshops or interactive activities where participants actively engage and practice rather than just listen",
        "synonyms": ["interactive workshops", "practical activities"],
        "examples": [
            {"en": "The science museum organizes hands-on events where children can conduct real experiments.", "vi": "Bảo tàng khoa học tổ chức các sự kiện thực hành nơi trẻ em có thể tự làm thí nghiệm thực tế."},
            {"en": "Attending hands-on events helps students master technical skills much faster than lectures.", "vi": "Tham gia các sự kiện thực hành giúp sinh viên nắm vững kỹ năng kỹ thuật nhanh hơn nhiều so với chỉ nghe giảng."},
            {"en": "The cooking festival features exciting hands-on events led by famous international chefs.", "vi": "Lễ hội ẩm thực có các hoạt động trải nghiệm thực hành thú vị do các đầu bếp quốc tế danh tiếng hướng dẫn."}
        ]
    },
    {
        "phrase": "has been pounding",
        "ipa": "/hæz biːn ˈpaʊn.dɪŋ/",
        "pos": "phrase",
        "level": "B2",
        "topic_group_id": "health_body",
        "topic_group_vi": "Sức khỏe & Y tế",
        "topic_id": "body_anatomy",
        "topic_vi": "Cơ thể người & Giác quan",
        "topic_icon": "🫀",
        "meaning_vi": "đang đập thình thịch liên hồi, nhức buốt dồn dập (tim, đầu)",
        "definition_en": "beating rapidly, throbbing intensely, or pulsing with heavy force (heart or head)",
        "synonyms": ["throbbing intensely", "pulsing rapidly"],
        "examples": [
            {"en": "My head has been pounding all morning because of a severe lack of sleep.", "vi": "Đầu tôi đau nhức buốt liên hồi suốt cả buổi sáng vì thiếu ngủ nghiêm trọng."},
            {"en": "His heart has been pounding ever since he heard the surprising news.", "vi": "Tim anh ấy đập thình thịch liên hồi kể từ khi nghe được tin tức bất ngờ đó."},
            {"en": "Take some aspirin if your head has been pounding for more than two hours.", "vi": "Hãy uống một chút thuốc giảm đau nếu đầu bạn bị đau nhức liên tục hơn hai tiếng đồng hồ."}
        ]
    },
    {
        "phrase": "if you don't mind",
        "ipa": "/ɪf juː dəʊnt maɪnd/",
        "pos": "idiom / phrase",
        "level": "A2",
        "topic_group_id": "communication_social",
        "topic_group_vi": "Giao tiếp & Quan hệ",
        "topic_id": "conversation_speech",
        "topic_vi": "Giao tiếp & Hội thoại",
        "topic_icon": "💬",
        "meaning_vi": "nếu bạn không phiền, xin phép (lời đề nghị lịch sự)",
        "definition_en": "used as a polite phrase when asking permission or making a gentle request",
        "synonyms": ["if it's alright with you", "with your permission"],
        "examples": [
            {"en": "I'd like to open the window for some fresh air, if you don't mind.", "vi": "Tôi muốn mở cửa sổ để đón chút không khí trong lành, nếu bạn không phiền."},
            {"en": "Could I borrow your charger for a few minutes, if you don't mind?", "vi": "Tôi có thể mượn sạc của bạn vài phút được không, nếu bạn không thấy phiền?"},
            {"en": "We would like to reschedule our appointment to tomorrow, if you don't mind.", "vi": "Chúng tôi muốn dời lịch hẹn sang ngày mai, nếu điều đó không làm phiền bạn."}
        ]
    },
    {
        "phrase": "on-call",
        "ipa": "/ˌɒnˈkɔːl/",
        "pos": "adjective",
        "level": "B2",
        "topic_group_id": "health_body",
        "topic_group_vi": "Sức khỏe & Y tế",
        "topic_id": "medicine_illness",
        "topic_vi": "Bệnh tật & Điều trị y tế",
        "topic_icon": "💊",
        "meaning_vi": "trong ca trực, luôn sẵn sàng khi được triệu tập",
        "definition_en": "available to be summoned for duty or emergency service when needed",
        "synonyms": ["on standby", "on duty"],
        "examples": [
            {"en": "Dr. Miller is on-call tonight in case there are any emergency surgeries.", "vi": "Bác sĩ Miller đang trong ca trực tối nay đề phòng có ca phẫu thuật khẩn cấp."},
            {"en": "IT technicians are on-call 24/7 to handle critical system failures.", "vi": "Các kỹ thuật viên CNTT luôn túc trực 24/7 để xử lý các sự cố hệ thống nghiêm trọng."},
            {"en": "Being on-call all weekend makes it difficult to plan family outings.", "vi": "Việc phải trực ca suốt cả cuối tuần khiến rất khó lên kế hoạch đi chơi cùng gia đình."}
        ]
    },
    {
        "phrase": "There's an opening",
        "ipa": "/ðeəz ən ˈəʊ.pən.ɪŋ/",
        "pos": "phrase",
        "level": "B1",
        "topic_group_id": "business_work",
        "topic_group_vi": "Kinh doanh & Nghề nghiệp",
        "topic_id": "jobs_careers",
        "topic_vi": "Nghề nghiệp & Việc làm",
        "topic_icon": "🤝",
        "meaning_vi": "đang có một vị trí tuyển dụng trống, có cơ hội việc làm",
        "definition_en": "a job vacancy or available position has become unoccupied and ready to be filled",
        "synonyms": ["there is a vacancy", "a job opportunity is available"],
        "examples": [
            {"en": "There's an opening for a senior accountant in our financial branch.", "vi": "Đang có một vị trí trống cho kế toán viên cao cấp tại chi nhánh tài chính của chúng tôi."},
            {"en": "You should apply immediately because there's an opening on their marketing team.", "vi": "Bạn nên nộp hồ sơ ngay đi vì bên đội ngũ tiếp thị của họ đang có một chỗ trống tuyển dụng."},
            {"en": "I heard there's an opening for an English teacher at the international school.", "vi": "Tôi nghe nói trường quốc tế đang tuyển một vị trí giáo viên tiếng Anh."}
        ]
    }
]
