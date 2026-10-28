# -*- coding: utf-8 -*-
"""
Extra Phrases Batch 2: 115 high-frequency expressions covering health, education, daily life,
tech, nature, arts, society, emotions, and idioms to bring the total dataset to 360+ unique items.
"""

EXTRA_PHRASES_2 = [
    # =========================================================================
    # HEALTH & WELLBEING (15 phrases)
    # =========================================================================
    {
        "word": "allergic reaction",
        "ipa": "/əˈlɜː.dʒɪk riˈæk.ʃən/",
        "pos": "collocation",
        "level": "B1",
        "topic_group_id": "health_body",
        "topic_group_vi": "Sức khỏe & Y tế",
        "topic_id": "medicine_illness",
        "topic_vi": "Bệnh tật & Điều trị y tế",
        "topic_icon": "💊",
        "meaning_vi": "phản ứng dị ứng (thực phẩm, thuốc, thời tiết)",
        "definition_en": "a negative immune response occurring when the body encounters an allergen",
        "synonyms": ["allergy episode", "hypersensitivity"],
        "examples": [
            {"en": "Eating peanuts triggered a severe allergic reaction that required an EpiPen.", "vi": "Ăn đậu phộng đã kích hoạt một cơn dị ứng nghiêm trọng cần tiêm bút EpiPen khẩn cấp."},
            {"en": "Always alert the restaurant staff if you have any food allergic reactions.", "vi": "Hãy luôn cảnh báo nhân viên nhà hàng nếu bạn bị dị ứng với bất kỳ loại thực phẩm nào."}
        ]
    },
    {
        "word": "high blood pressure",
        "ipa": "/haɪ blʌd ˈpreʃ.ər/",
        "pos": "collocation",
        "level": "B1",
        "topic_group_id": "health_body",
        "topic_group_vi": "Sức khỏe & Y tế",
        "topic_id": "medicine_illness",
        "topic_vi": "Bệnh tật & Điều trị y tế",
        "topic_icon": "💊",
        "meaning_vi": "huyết áp cao (tăng huyết áp)",
        "definition_en": "a chronic medical condition in which blood pressure in the arteries is persistently elevated",
        "synonyms": ["hypertension"],
        "examples": [
            {"en": "Reducing salt and exercising regularly helps control high blood pressure naturally.", "vi": "Giảm lượng muối và tập thể dục đều đặn giúp kiểm soát huyết áp cao một cách tự nhiên."},
            {"en": "High blood pressure is often dubbed the silent killer because it shows few early symptoms.", "vi": "Huyết áp cao thường được ví là kẻ sát nhân thầm lặng vì nó ít có triệu chứng ban đầu rõ ràng."}
        ]
    },
    {
        "word": "shed extra pounds",
        "ipa": "/ʃed ˈek.strə paʊndz/",
        "pos": "idiom",
        "level": "B2",
        "topic_group_id": "health_body",
        "topic_group_vi": "Sức khỏe & Y tế",
        "topic_id": "fitness_nutrition",
        "topic_vi": "Dinh dưỡng & Thể chất",
        "topic_icon": "🥗",
        "meaning_vi": "giảm cân, trút bỏ mỡ thừa",
        "definition_en": "to lose excess body weight and become leaner through exercise and diet",
        "synonyms": ["lose weight", "slim down"],
        "examples": [
            {"en": "Switching to plant-based meals helped her shed extra pounds effortlessly.", "vi": "Chuyển sang các bữa ăn từ thực vật đã giúp cô ấy giảm cân một cách nhẹ nhàng."},
            {"en": "Cardio workouts combined with weight training are optimal to shed extra pounds.", "vi": "Tập bài tập tim mạch kết hợp với nâng tạ là giải pháp tối ưu để giảm mỡ thừa."}
        ]
    },
    {
        "word": "put on weight",
        "ipa": "/pʊt ɒn weɪt/",
        "pos": "phrasal verb",
        "level": "A2",
        "topic_group_id": "health_body",
        "topic_group_vi": "Sức khỏe & Y tế",
        "topic_id": "fitness_nutrition",
        "topic_vi": "Dinh dưỡng & Thể chất",
        "topic_icon": "🥗",
        "meaning_vi": "tăng cân, lên cân",
        "definition_en": "to become heavier or gain body fat over a period of time",
        "synonyms": ["gain weight"],
        "examples": [
            {"en": "Many people put on weight during winter when outdoor activities diminish.", "vi": "Nhiều người bị tăng cân trong mùa đông khi các hoạt động ngoài trời giảm sút."},
            {"en": "The athlete needed to put on weight to compete in the heavyweight division.", "vi": "Vận động viên cần tăng cân để thi đấu ở hạng cân nặng."}
        ]
    },
    {
        "word": "as fit as a fiddle",
        "ipa": "/æz fɪt æz ə ˈfɪd.əl/",
        "pos": "idiom",
        "level": "B2",
        "topic_group_id": "health_body",
        "topic_group_vi": "Sức khỏe & Y tế",
        "topic_id": "fitness_nutrition",
        "topic_vi": "Dinh dưỡng & Thể chất",
        "topic_icon": "🥗",
        "meaning_vi": "khỏe như vâm, thể lực tràn trề sung mãn",
        "definition_en": "in exceptionally good physical health, vitality, and fitness",
        "synonyms": ["in peak physical condition", "hale and hearty"],
        "examples": [
            {"en": "My grandfather is seventy-five years old and still as fit as a fiddle.", "vi": "Ông nội tôi đã bảy mươi lăm tuổi mà vẫn khỏe như vâm."},
            {"en": "After two months of rehabilitation, the footballer declared he was as fit as a fiddle.", "vi": "Sau hai tháng phục hồi chức năng, cầu thủ tuyên bố anh đã sung mãn trở lại."}
        ]
    },
    {
        "word": "catch one's breath",
        "ipa": "/kætʃ wʌnz breθ/",
        "pos": "idiom",
        "level": "B1",
        "topic_group_id": "health_body",
        "topic_group_vi": "Sức khỏe & Y tế",
        "topic_id": "body_anatomy",
        "topic_vi": "Cơ thể người & Giác quan",
        "topic_icon": "🫀",
        "meaning_vi": "thở dốc lấy lại hơi, ngừng lại để điều hòa nhịp thở",
        "definition_en": "to pause and rest until one is breathing normally after vigorous exertion",
        "synonyms": ["pause for breath", "recover breath"],
        "examples": [
            {"en": "We rested on a park bench for five minutes to catch our breath after the uphill sprint.", "vi": "Chúng tôi ngồi nghỉ trên ghế đá công viên năm phút để lấy lại hơi sau cú chạy nước rút lên dốc."},
            {"en": "Give me a minute to catch my breath before we climb the next flight of stairs.", "vi": "Cho tôi một phút để thở đều lại đã trước khi chúng ta leo tầng cầu thang tiếp theo."}
        ]
    },
    {
        "word": "emergency room",
        "ipa": "/ɪˈmɜː.dʒən.si ruːm/",
        "pos": "collocation",
        "level": "A2",
        "topic_group_id": "health_body",
        "topic_group_vi": "Sức khỏe & Y tế",
        "topic_id": "medicine_illness",
        "topic_vi": "Bệnh tật & Điều trị y tế",
        "topic_icon": "💊",
        "meaning_vi": "phòng cấp cứu bệnh viện (ER)",
        "definition_en": "the hospital department providing immediate emergency treatment for acute illnesses and injuries",
        "synonyms": ["casualty department", "ER"],
        "examples": [
            {"en": "The ambulance rushed the accident victims straight to the nearest emergency room.", "vi": "Xe cứu thương đã đưa ngay các nạn nhân tai nạn đến phòng cấp cứu gần nhất."},
            {"en": "Doctors in the emergency room work high-adrenaline shifts around the clock.", "vi": "Các bác sĩ trong phòng cấp cứu làm việc trong những ca trực căng thẳng suốt ngày đêm."}
        ]
    },
    {
        "word": "take a deep breath",
        "ipa": "/teɪk ə diːp breθ/",
        "pos": "collocation",
        "level": "A1",
        "topic_group_id": "health_body",
        "topic_group_vi": "Sức khỏe & Y tế",
        "topic_id": "body_anatomy",
        "topic_vi": "Cơ thể người & Giác quan",
        "topic_icon": "🫀",
        "meaning_vi": "hít một hơi thật sâu để bình tâm",
        "definition_en": "to inhale a large volume of air slowly to calm one's nerves or steady the heart",
        "synonyms": ["inhale deeply"],
        "examples": [
            {"en": "Take a deep breath and relax before you start your speech on stage.", "vi": "Hãy hít một hơi thật sâu và thả lỏng trước khi bạn bắt đầu bài phát biểu trên sân khấu."},
            {"en": "Whenever you feel anxiety creeping in, close your eyes and take three deep breaths.", "vi": "Bất cứ khi nào bạn cảm thấy âu lo ùa về, hãy nhắm mắt lại và hít ba hơi thật sâu."}
        ]
    },
    {
        "word": "preventive care",
        "ipa": "/prɪˈven.tɪv keər/",
        "pos": "collocation",
        "level": "B2",
        "topic_group_id": "health_body",
        "topic_group_vi": "Sức khỏe & Y tế",
        "topic_id": "medicine_illness",
        "topic_vi": "Bệnh tật & Điều trị y tế",
        "topic_icon": "💊",
        "meaning_vi": "chăm sóc sức khỏe phòng ngừa (phòng bệnh hơn chữa bệnh)",
        "definition_en": "healthcare aimed at disease prevention, such as routine screenings and immunizations",
        "synonyms": ["prophylactic healthcare", "preventative medicine"],
        "examples": [
            {"en": "Investing in preventive care lowers long-term hospitalization costs significantly.", "vi": "Đầu tư vào chăm sóc phòng ngừa giúp giảm đáng kể chi phí nằm viện dài hạn."},
            {"en": "Vaccinations and annual dental checkups are vital pillars of preventive care.", "vi": "Tiêm chủng và khám răng định kỳ hàng năm là những trụ cột cốt lõi của việc phòng ngừa bệnh tật."}
        ]
    },
    {
        "word": "stiff neck",
        "ipa": "/stɪf nek/",
        "pos": "collocation",
        "level": "A2",
        "topic_group_id": "health_body",
        "topic_group_vi": "Sức khỏe & Y tế",
        "topic_id": "body_anatomy",
        "topic_vi": "Cơ thể người & Giác quan",
        "topic_icon": "🫀",
        "meaning_vi": "chứng cứng cổ, đau mỏi cổ vai gáy",
        "definition_en": "soreness and difficulty moving the neck, often caused by poor sleeping posture or stress",
        "synonyms": ["neck stiffness", "cervical soreness"],
        "examples": [
            {"en": "Sleeping awkwardly on the flight left him with a painful stiff neck all day.", "vi": "Nằm ngủ sai tư thế trên chuyến bay khiến anh ấy bị cứng cổ đau nhức cả ngày."},
            {"en": "Gentle neck stretching exercises relieve the discomfort of a stiff neck.", "vi": "Các bài tập duỗi cổ nhẹ nhàng giúp làm dịu cảm giác khó chịu của chứng cứng cổ."}
        ]
    },
    {
        "word": "vital organs",
        "ipa": "/ˈvaɪ.təl ˈɔː.ɡənz/",
        "pos": "collocation",
        "level": "B2",
        "topic_group_id": "health_body",
        "topic_group_vi": "Sức khỏe & Y tế",
        "topic_id": "body_anatomy",
        "topic_vi": "Cơ thể người & Giác quan",
        "topic_icon": "🫀",
        "meaning_vi": "các cơ quan nội tạng quan trọng duy trì sự sống",
        "definition_en": "essential bodily organs necessary to sustain life, including the heart, brain, lungs, and liver",
        "synonyms": ["essential organs"],
        "examples": [
            {"en": "Protective armor is specifically engineered to shield soldiers' vital organs from shrapnel.", "vi": "Áo giáp bảo hộ được thiết kế chuyên biệt để che chắn các cơ quan nội tạng sống còn của người lính."},
            {"en": "Adequate blood circulation delivers oxygen and nutrients to every vital organ.", "vi": "Sự lưu thông máu đầy đủ sẽ vận chuyển oxy và dưỡng chất đến từng cơ quan nội tạng trọng yếu."}
        ]
    },
    {
        "word": "lose consciousness",
        "ipa": "/luːz ˈkɒn.ʃəs.nəs/",
        "pos": "collocation",
        "level": "B2",
        "topic_group_id": "health_body",
        "topic_group_vi": "Sức khỏe & Y tế",
        "topic_id": "medicine_illness",
        "topic_vi": "Bệnh tật & Điều trị y tế",
        "topic_icon": "💊",
        "meaning_vi": "bất tỉnh nhân sự, ngất lịm đi",
        "definition_en": "to become unconscious due to illness, trauma, head injury, or shock",
        "synonyms": ["faint", "pass out", "black out"],
        "examples": [
            {"en": "The boxer lost consciousness momentarily after taking a heavy blow to the jaw.", "vi": "Võ sĩ quyền anh đã bất tỉnh trong chốc lát sau khi dính một đòn nặng vào quai hàm."},
            {"en": "Call an ambulance immediately if a fainting patient loses consciousness for more than a minute.", "vi": "Hãy gọi xe cứu thương ngay nếu người bệnh bất tỉnh lâu hơn một phút."}
        ]
    },
    {
        "word": "mental breakdown",
        "ipa": "/ˌmen.təl ˈbreɪk.daʊn/",
        "pos": "collocation",
        "level": "B2",
        "topic_group_id": "health_body",
        "topic_group_vi": "Sức khỏe & Y tế",
        "topic_id": "mental_health",
        "topic_vi": "Tâm lý & Tinh thần",
        "topic_icon": "🧠",
        "meaning_vi": "suy sụp tinh thần, khủng hoảng tâm lý nghiêm trọng",
        "definition_en": "a period of extreme mental or emotional collapse where one is unable to function normally",
        "synonyms": ["nervous breakdown", "psychological collapse"],
        "examples": [
            {"en": "Prolonged overwork and personal loss culminated in a severe mental breakdown.", "vi": "Làm việc quá tải kéo dài cùng mất mát cá nhân đã dẫn đến một cơn suy sụp tinh thần nghiêm trọng."},
            {"en": "Therapy and medication helped him gradually rebuild his life following the mental breakdown.", "vi": "Trị liệu tâm lý và thuốc đã giúp anh ấy dần xây dựng lại cuộc sống sau lần khủng hoảng tinh thần."}
        ]
    },
    {
        "word": "sore muscles",
        "ipa": "/sɔːr ˈmʌs.əlz/",
        "pos": "collocation",
        "level": "A2",
        "topic_group_id": "health_body",
        "topic_group_vi": "Sức khỏe & Y tế",
        "topic_id": "body_anatomy",
        "topic_vi": "Cơ thể người & Giác quan",
        "topic_icon": "🫀",
        "meaning_vi": "đau nhức cơ bắp (sau khi vận động mạnh)",
        "definition_en": "pain or ache felt in skeletal muscles, usually following unaccustomed physical exercise",
        "synonyms": ["muscle soreness", "DOMS"],
        "examples": [
            {"en": "Soaking in a hot Epsom salt bath helps soothe sore muscles after a marathon.", "vi": "Ngâm mình trong bồn nước muối ấm giúp làm dịu cơ bắp đau nhức sau giải chạy marathon."},
            {"en": "Don't worry about mild sore muscles; it indicates that your muscle fibers are adapting.", "vi": "Đừng quá lo lắng về việc mỏi cơ nhẹ; điều đó cho thấy các sợi cơ của bạn đang thích nghi."}
        ]
    },
    {
        "word": "heal like a charm",
        "ipa": "/hiːl laɪk ə tʃɑːm/",
        "pos": "idiom",
        "level": "B2",
        "topic_group_id": "health_body",
        "topic_group_vi": "Sức khỏe & Y tế",
        "topic_id": "medicine_illness",
        "topic_vi": "Bệnh tật & Điều trị y tế",
        "topic_icon": "💊",
        "meaning_vi": "lành lặn rất nhanh và thần kỳ không để lại biến chứng",
        "definition_en": "to heal or recover completely, quickly, and with wonderful success",
        "synonyms": ["recover miraculously", "heal completely"],
        "examples": [
            {"en": "The surgeon stitched the cut so neatly that it healed like a charm within ten days.", "vi": "Bác sĩ phẫu thuật đã khâu vết rách khéo đến mức nó lành lại đẹp mắt chỉ trong mười ngày."},
            {"en": "Applying aloe vera to the minor burn helped it heal like a charm without scarring.", "vi": "Bôi nha đam lên vết bỏng nhẹ đã giúp vết thương mau lành mà không để lại sẹo."}
        ]
    },

    # =========================================================================
    # EDUCATION & STUDY (15 phrases)
    # =========================================================================
    {
        "word": "straight A student",
        "ipa": "/streɪt eɪ ˈstjuː.dənt/",
        "pos": "collocation",
        "level": "B1",
        "topic_group_id": "education_academia",
        "topic_group_vi": "Giáo dục & Học thuật",
        "topic_id": "school_university",
        "topic_vi": "Trường học & Đại học",
        "topic_icon": "🏫",
        "meaning_vi": "học sinh giỏi toàn diện, toàn đạt điểm A",
        "definition_en": "a student who consistently earns top marks (grade A) in every subject",
        "synonyms": ["top student", "honor student"],
        "examples": [
            {"en": "She was a straight A student throughout high school and graduated valedictorian.", "vi": "Cô ấy là học sinh giỏi toàn diện suốt những năm cấp ba và đã tốt nghiệp thủ khoa."},
            {"en": "Being a straight A student requires disciplined daily revision rather than last-minute cramming.", "vi": "Để đạt toàn điểm A đòi hỏi kỷ luật ôn bài mỗi ngày chứ không phải nhồi nhét vào phút chót."}
        ]
    },
    {
        "word": "peer pressure",
        "ipa": "/pɪər ˈpreʃ.ər/",
        "pos": "collocation",
        "level": "B1",
        "topic_group_id": "education_academia",
        "topic_group_vi": "Giáo dục & Học thuật",
        "topic_id": "school_university",
        "topic_vi": "Trường học & Đại học",
        "topic_icon": "🏫",
        "meaning_vi": "áp lực đồng trang lứa",
        "definition_en": "influence from members of one's peer group to conform to their behavior or attitudes",
        "synonyms": ["social conformity pressure"],
        "examples": [
            {"en": "Teenagers frequently succumb to peer pressure to fit in with popular classmates.", "vi": "Thanh thiếu niên thường dễ chịu thua trước áp lực đồng trang lứa để hòa nhập với bạn bè."},
            {"en": "Educators teach resilience strategies so students can resist negative peer pressure.", "vi": "Các nhà giáo dục dạy kỹ năng tự chủ để học sinh có thể cưỡng lại áp lực xấu từ bạn bè."}
        ]
    },
    {
        "word": "flunk an exam",
        "ipa": "/flʌŋk ən ɪɡˈzæm/",
        "pos": "collocation",
        "level": "B1",
        "topic_group_id": "education_academia",
        "topic_group_vi": "Giáo dục & Học thuật",
        "topic_id": "study_exams",
        "topic_vi": "Học tập & Thi cử",
        "topic_icon": "📚",
        "meaning_vi": "thi trượt, thi hỏng",
        "definition_en": "to fail an examination or academic test by not achieving the passing grade",
        "synonyms": ["fail a test"],
        "examples": [
            {"en": "He flunked his driving exam on the first attempt due to poor parallel parking.", "vi": "Anh ấy thi trượt bằng lái xe ngay lần đầu do kỹ năng đỗ xe song song còn yếu."},
            {"en": "If you skip class repeatedly, you will inevitably flunk the final exam.", "vi": "Nếu bạn cứ cúp học liên tục, sớm muộn gì bạn cũng sẽ rớt kỳ thi cuối kỳ thôi."}
        ]
    },
    {
        "word": "literature review",
        "ipa": "/ˈlɪt.rə.tʃər rɪˈvjuː/",
        "pos": "collocation",
        "level": "B2",
        "topic_group_id": "education_academia",
        "topic_group_vi": "Giáo dục & Học thuật",
        "topic_id": "study_exams",
        "topic_vi": "Học tập & Thi cử",
        "topic_icon": "📚",
        "meaning_vi": "tổng quan tài liệu nghiên cứu học thuật",
        "definition_en": "a comprehensive survey of scholarly books, articles, and other sources relevant to a specific research issue",
        "synonyms": ["scholarly review", "source survey"],
        "examples": [
            {"en": "Chapter two of every doctoral dissertation is dedicated to a rigorous literature review.", "vi": "Chương hai của mỗi luận án tiến sĩ đều dành riêng cho phần tổng quan tài liệu học thuật kỹ càng."},
            {"en": "Conducting a thorough literature review identifies gaps in current academic knowledge.", "vi": "Thực hiện tổng quan tài liệu chu đáo giúp chỉ ra những khoảng trống trong tri thức hiện tại."}
        ]
    },
    {
        "word": "brush up on",
        "ipa": "/brʌʃ ʌp ɒn/",
        "pos": "phrasal verb",
        "level": "B1",
        "topic_group_id": "education_academia",
        "topic_group_vi": "Giáo dục & Học thuật",
        "topic_id": "language_reading",
        "topic_vi": "Ngôn ngữ & Đọc viết",
        "topic_icon": "✍️",
        "meaning_vi": "ôn lại, trau dồi lại kiến thức cũ lâu ngày không dùng",
        "definition_en": "to refresh one's memory or practice a skill that has not been used for some time",
        "synonyms": ["refresh knowledge", "review"],
        "examples": [
            {"en": "I need to brush up on my Spanish conversational skills before flying to Madrid.", "vi": "Tôi cần ôn lại kỹ năng giao tiếp tiếng Tây Ban Nha trước khi bay tới Madrid."},
            {"en": "She spent the weekend brushing up on statistics formulas for Monday's interview.", "vi": "Cô ấy đã dành cả cuối tuần để ôn lại các công thức thống kê chuẩn bị cho buổi phỏng vấn thứ Hai."}
        ]
    },
    {
        "word": "learn the ropes",
        "ipa": "/lɜːn ðə rəʊps/",
        "pos": "idiom",
        "level": "B2",
        "topic_group_id": "education_academia",
        "topic_group_vi": "Giáo dục & Học thuật",
        "topic_id": "school_university",
        "topic_vi": "Trường học & Đại học",
        "topic_icon": "🏫",
        "meaning_vi": "học việc, nắm bắt tường tận quy trình và cách làm",
        "definition_en": "to understand the basic procedures and skills required in a new role or environment",
        "synonyms": ["master the basics", "get the hang of it"],
        "examples": [
            {"en": "It takes an incoming intern about two weeks to learn the ropes around the office.", "vi": "Một thực tập sinh mới vào cần khoảng hai tuần để nắm bắt quy trình làm việc trong văn phòng."},
            {"en": "A friendly senior colleague was assigned to guide him while he learned the ropes.", "vi": "Một đồng nghiệp thân thiện đã được cử đến để hướng dẫn anh trong thời gian đầu học việc."}
        ]
    },
    {
        "word": "stand out from the crowd",
        "ipa": "/stænd aʊt frɒm ðə kraʊd/",
        "pos": "idiom",
        "level": "B2",
        "topic_group_id": "education_academia",
        "topic_group_vi": "Giáo dục & Học thuật",
        "topic_id": "school_university",
        "topic_vi": "Trường học & Đại học",
        "topic_icon": "🏫",
        "meaning_vi": "nổi bật hẳn lên so với số đông",
        "definition_en": "to be distinctly different, memorable, or superior compared to others in a group",
        "synonyms": ["distinguish oneself", "shine above others"],
        "examples": [
            {"en": "Her creative portfolio allowed her to stand out from the crowd of job applicants.", "vi": "Hồ sơ năng lực sáng tạo đã giúp cô ấy nổi bật hẳn lên so với đám đông ứng viên xin việc."},
            {"en": "Practical coding experience helps university graduates stand out from the crowd.", "vi": "Kinh nghiệm lập trình thực tế giúp các cử nhân đại học tạo được dấu ấn khác biệt so với số đông."}
        ]
    },
    {
        "word": "knowledge is power",
        "ipa": "/ˈnɒl.ɪdʒ ɪz ˈpaʊ.ər/",
        "pos": "idiom",
        "level": "B1",
        "topic_group_id": "education_academia",
        "topic_group_vi": "Giáo dục & Học thuật",
        "topic_id": "language_reading",
        "topic_vi": "Ngôn ngữ & Đọc viết",
        "topic_icon": "✍️",
        "meaning_vi": "tri thức là sức mạnh",
        "definition_en": "a proverb emphasizing that having education and information gives people agency and control",
        "synonyms": ["education brings strength"],
        "examples": [
            {"en": "Never stop reading and asking questions, for knowledge is true power in life.", "vi": "Đừng bao giờ ngừng đọc sách và đặt câu hỏi, bởi vì tri thức chính là sức mạnh đích thực trong cuộc đời."},
            {"en": "In the modern digital economy, knowledge is power and drives wealth creation.", "vi": "Trong nền kinh tế số hiện đại, tri thức là sức mạnh và thúc đẩy sự thịnh vượng."}
        ]
    },
    {
        "word": "attend a seminar",
        "ipa": "/əˈtend ə ˈsem.ɪ.nɑːr/",
        "pos": "collocation",
        "level": "B1",
        "topic_group_id": "education_academia",
        "topic_group_vi": "Giáo dục & Học thuật",
        "topic_id": "school_university",
        "topic_vi": "Trường học & Đại học",
        "topic_icon": "🏫",
        "meaning_vi": "tham dự hội thảo chuyên đề học thuật",
        "definition_en": "to participate in an academic meeting where a specific subject is discussed intensively",
        "synonyms": ["participate in a workshop"],
        "examples": [
            {"en": "Over one hundred researchers attended the international neuroscience seminar.", "vi": "Hơn một trăm nhà nghiên cứu đã tham dự hội thảo chuyên đề quốc tế về khoa học thần kinh."},
            {"en": "Students are encouraged to attend guest seminars to learn industry trends.", "vi": "Sinh viên được khuyến khích tham dự các buổi hội thảo của diễn giả khách mời để nắm bắt xu hướng ngành."}
        ]
    },
    {
        "word": "plagiarism check",
        "ipa": "/ˈpleɪ.dʒər.ɪ.zəm tʃek/",
        "pos": "collocation",
        "level": "B2",
        "topic_group_id": "education_academia",
        "topic_group_vi": "Giáo dục & Học thuật",
        "topic_id": "study_exams",
        "topic_vi": "Học tập & Thi cử",
        "topic_icon": "📚",
        "meaning_vi": "kiểm tra phát hiện đạo văn",
        "definition_en": "the process of scanning a paper with software to verify that it does not copy another author's work without attribution",
        "synonyms": ["similarity check"],
        "examples": [
            {"en": "The university requires all master's theses to undergo a rigorous plagiarism check.", "vi": "Trường đại học yêu cầu tất cả luận văn thạc sĩ phải trải qua quy trình kiểm tra đạo văn gắt gao."},
            {"en": "Always run your essay through an online plagiarism check before final submission.", "vi": "Hãy luôn quét bài luận qua phần mềm kiểm tra đạo văn trước khi bấm nộp bài."}
        ]
    },

    # =========================================================================
    # DAILY LIFE & HOME (15 phrases)
    # =========================================================================
    {
        "word": "run errands",
        "ipa": "/rʌn ˈer.əndz/",
        "pos": "collocation",
        "level": "B1",
        "topic_group_id": "daily_life_home",
        "topic_group_vi": "Đời sống & Gia đình",
        "topic_id": "shopping_services",
        "topic_vi": "Mua sắm & Tiêu dùng",
        "topic_icon": "🛒",
        "meaning_vi": "chạy đi làm các công việc lặt vặt (mua đồ, gửi thư, nộp tiền)",
        "definition_en": "to go out to complete routine everyday tasks such as picking up dry cleaning or buying groceries",
        "synonyms": ["do errands", "run chores"],
        "examples": [
            {"en": "I spent the entire Saturday morning running errands all over town.", "vi": "Tôi đã dành trọn cả buổi sáng thứ Bảy để chạy quanh thị trấn giải quyết các công việc vặt."},
            {"en": "Can you stop at the post office while you run errands this afternoon?", "vi": "Bạn có thể ghé qua bưu điện trong lúc đi làm mấy việc vặt chiều nay được không?"}
        ]
    },
    {
        "word": "keep an eye on",
        "ipa": "/kiːp ən aɪ ɒn/",
        "pos": "idiom",
        "level": "A2",
        "topic_group_id": "daily_life_home",
        "topic_group_vi": "Đời sống & Gia đình",
        "topic_id": "house_home",
        "topic_vi": "Nhà cửa & Đồ nội thất",
        "topic_icon": "🏡",
        "meaning_vi": "để mắt trông chừng, để ý canh chừng",
        "definition_en": "to watch or take care of someone or something attentively",
        "synonyms": ["watch over", "look after", "monitor"],
        "examples": [
            {"en": "Could you please keep an eye on my luggage while I go buy a bottle of water?", "vi": "Bạn có thể để mắt trông giúp hành lý của tôi trong lúc tôi đi mua chai nước được không?"},
            {"en": "Mother asked the elder sibling to keep an eye on the toddler in the backyard.", "vi": "Mẹ dặn anh lớn để mắt trông chừng em bé ngoài sân sau."}
        ]
    },
    {
        "word": "lend a helping hand",
        "ipa": "/lend ə ˈhelp.ɪŋ hænd/",
        "pos": "idiom",
        "level": "B1",
        "topic_group_id": "daily_life_home",
        "topic_group_vi": "Đời sống & Gia đình",
        "topic_id": "family_life",
        "topic_vi": "Gia đình & Người thân",
        "topic_icon": "👨‍👩‍👧",
        "meaning_vi": "giúp một tay, tương trợ giúp đỡ",
        "definition_en": "to help or assist someone with a difficult task or chore",
        "synonyms": ["give a hand", "assist", "offer help"],
        "examples": [
            {"en": "Our kind neighbors lent a helping hand when we moved into the new house.", "vi": "Những người hàng xóm tốt bụng đã giúp một tay khi chúng tôi chuyển sang nhà mới."},
            {"en": "Whenever someone in the community falls sick, volunteers lend a helping hand.", "vi": "Bất cứ khi nào có ai trong khu phố ốm đau, các tình nguyện viên đều sẵn lòng dang tay tương trợ."}
        ]
    },
    {
        "word": "make ends meet",
        "ipa": "/meɪk endz miːt/",
        "pos": "idiom",
        "level": "B2",
        "topic_group_id": "daily_life_home",
        "topic_group_vi": "Đời sống & Gia đình",
        "topic_id": "shopping_services",
        "topic_vi": "Mua sắm & Tiêu dùng",
        "topic_icon": "🛒",
        "meaning_vi": "xoay xở đủ sống qua ngày, liệu cơm gắp mắm",
        "definition_en": "to earn just enough money to pay for basic living necessities and food",
        "synonyms": ["get by", "survive financially"],
        "examples": [
            {"en": "With rising inflation, many working families struggle to make ends meet.", "vi": "Với lạm phát ngày càng tăng, nhiều gia đình lao động phải chật vật xoay xở để đủ sống qua ngày."},
            {"en": "She worked two part-time jobs during college just to make ends meet.", "vi": "Cô ấy đã làm hai công việc bán thời gian hồi học đại học chỉ để trang trải tiền sinh hoạt."}
        ]
    },
    {
        "word": "live paycheck to paycheck",
        "ipa": "/lɪv ˈpeɪ.tʃek tuː ˈpeɪ.tʃek/",
        "pos": "idiom",
        "level": "B2",
        "topic_group_id": "daily_life_home",
        "topic_group_vi": "Đời sống & Gia đình",
        "topic_id": "shopping_services",
        "topic_vi": "Mua sắm & Tiêu dùng",
        "topic_icon": "🛒",
        "meaning_vi": "lĩnh lương tháng nào tiêu hết tháng đó, không có tiền tích lũy",
        "definition_en": "to spend all of one's money on essential needs before the next pay arrives, saving nothing",
        "synonyms": ["hand-to-mouth living"],
        "examples": [
            {"en": "Living paycheck to paycheck causes intense financial stress whenever unexpected emergencies occur.", "vi": "Sống trong cảnh lương tháng nào hết tháng đó gây ra áp lực tài chính đè nặng mỗi khi có việc khẩn cấp."},
            {"en": "Building a small emergency savings fund is the first step out of living paycheck to paycheck.", "vi": "Xây dựng một quỹ tiết kiệm khẩn cấp nhỏ là bước đầu tiên để thoát khỏi cảnh lĩnh lương là tiêu sạch."}
        ]
    },
    {
        "word": "sleep like a log",
        "ipa": "/sliːp laɪk ə lɒɡ/",
        "pos": "idiom",
        "level": "B1",
        "topic_group_id": "daily_life_home",
        "topic_group_vi": "Đời sống & Gia đình",
        "topic_id": "house_home",
        "topic_vi": "Nhà cửa & Đồ nội thất",
        "topic_icon": "🏡",
        "meaning_vi": "ngủ say như chết, ngủ một giấc sâu không mộng mị",
        "definition_en": "to sleep very soundly, deeply, and peacefully without waking up",
        "synonyms": ["sleep like a baby", "sleep soundly"],
        "examples": [
            {"en": "After hiking twenty miles through the mountains, he slept like a log all night.", "vi": "Sau khi đi bộ hai mươi dặm đường núi, anh ấy đã ngủ say như chết suốt cả đêm."},
            {"en": "I turned off all electronics at ten PM and slept like a log until morning.", "vi": "Tôi tắt hết các thiết bị điện tử lúc 10 giờ tối và ngủ một giấc thật sâu đến tận sáng."}
        ]
    },
    {
        "word": "early bird",
        "ipa": "/ˈɜː.li bɜːd/",
        "pos": "idiom",
        "level": "A2",
        "topic_group_id": "daily_life_home",
        "topic_group_vi": "Đời sống & Gia đình",
        "topic_id": "house_home",
        "topic_vi": "Nhà cửa & Đồ nội thất",
        "topic_icon": "🏡",
        "meaning_vi": "người quen dậy sớm",
        "definition_en": "a person who customarily wakes up, arrives, or starts activities very early in the morning",
        "synonyms": ["morning person"],
        "examples": [
            {"en": "As an early bird, she enjoys running at 5:30 AM before the city wakes up.", "vi": "Là một người có thói quen dậy sớm, cô thích chạy bộ lúc 5h30 sáng trước khi thành phố thức giấc."},
            {"en": "Early bird tickets for the festival offer a significant discount.", "vi": "Vé mở bán sớm cho lễ hội đem lại mức chiết khấu giảm giá đáng kể."}
        ]
    },
    {
        "word": "night owl",
        "ipa": "/naɪt aʊl/",
        "pos": "idiom",
        "level": "A2",
        "topic_group_id": "daily_life_home",
        "topic_group_vi": "Đời sống & Gia đình",
        "topic_id": "house_home",
        "topic_vi": "Nhà cửa & Đồ nội thất",
        "topic_icon": "🏡",
        "meaning_vi": "cú đêm, người hay thức khuya làm việc",
        "definition_en": "a person who stays up late at night and is most productive after dark",
        "synonyms": ["late-night person"],
        "examples": [
            {"en": "Software engineers are often night owls who find creative focus past midnight.", "vi": "Các kỹ sư phần mềm thường là những cú đêm tìm thấy sự tập trung sáng tạo sau nửa đêm."},
            {"en": "I am definitely a night owl; waking up before eight AM is pure torture for me.", "vi": "Tôi đích thị là một cú đêm; thức dậy trước tám giờ sáng quả là cực hình đối với tôi."}
        ]
    },
    {
        "word": "spick and span",
        "ipa": "/ˌspɪk ənd ˈspæn/",
        "pos": "idiom",
        "level": "B2",
        "topic_group_id": "daily_life_home",
        "topic_group_vi": "Đời sống & Gia đình",
        "topic_id": "house_home",
        "topic_vi": "Nhà cửa & Đồ nội thất",
        "topic_icon": "🏡",
        "meaning_vi": "ngăn nắp sạch bong sáng bóng, tinh tươm",
        "definition_en": "spotlessly clean, exceptionally neat, and tidy",
        "synonyms": ["spotless", "immaculate", "squeaky clean"],
        "examples": [
            {"en": "They spent hours cleaning until the entire kitchen was spick and span.", "vi": "Họ đã dành nhiều giờ dọn dẹp cho đến khi cả gian bếp sạch bong sáng bóng tinh tươm."},
            {"en": "Her room is always spick and span, with every book neatly organized on shelves.", "vi": "Phòng của cô ấy lúc nào cũng tinh tươm ngăn nắp, từng cuốn sách đều được xếp ngay ngắn trên kệ."}
        ]
    },
    {
        "word": "comfort food",
        "ipa": "/ˈkʌm.fət fuːd/",
        "pos": "collocation",
        "level": "B1",
        "topic_group_id": "daily_life_home",
        "topic_group_vi": "Đời sống & Gia đình",
        "topic_id": "food_cooking",
        "topic_vi": "Ẩm thực & Nấu nướng",
        "topic_icon": "🍳",
        "meaning_vi": "món ăn quen thuộc vỗ về tâm trạng (đem lại cảm giác ấm lòng)",
        "definition_en": "food that provides psychological comfort, nostalgic value, or sentimental satisfaction",
        "synonyms": ["soul food", "hearty meal"],
        "examples": [
            {"en": "A steaming bowl of traditional chicken pho is the ultimate comfort food on a rainy day.", "vi": "Một bát phở gà nóng hổi bốc khói là món ăn vỗ về tâm trạng tuyệt vời nhất vào một ngày mưa."},
            {"en": "When feeling stressed or homesick, she craves her mother's homemade comfort food.", "vi": "Mỗi khi căng thẳng hoặc nhớ nhà, cô ấy lại thèm những món ăn ấm lòng do chính tay mẹ nấu."}
        ]
    },

    # =========================================================================
    # TECH & COMPUTING EXTRA (15 phrases)
    # =========================================================================
    {
        "word": "open source software",
        "ipa": "/ˌəʊ.pən ˈsɔːs ˈsɒft.weər/",
        "pos": "collocation",
        "level": "B2",
        "topic_group_id": "tech_science",
        "topic_group_vi": "Khoa học & Công nghệ",
        "topic_id": "computers_digital",
        "topic_vi": "Máy tính & Kỹ thuật số",
        "topic_icon": "🖥️",
        "meaning_vi": "phần mềm mã nguồn mở",
        "definition_en": "software whose source code is freely available for anyone to inspect, modify, and enhance",
        "synonyms": ["FOSS", "publicly accessible software"],
        "examples": [
            {"en": "Linux and Python are shining examples of globally transformative open source software.", "vi": "Linux và Python là những ví dụ tiêu biểu về phần mềm nguồn mở làm thay đổi cả thế giới."},
            {"en": "Many companies contribute code back to open source software projects.", "vi": "Nhiều doanh nghiệp đóng góp mã nguồn ngược lại cho các dự án phần mềm mã nguồn mở."}
        ]
    },
    {
        "word": "two-factor authentication",
        "ipa": "/ˌtuː ˈfæk.tər ɔːˌθen.tɪˈkeɪ.ʃən/",
        "pos": "collocation",
        "level": "B2",
        "topic_group_id": "tech_science",
        "topic_group_vi": "Khoa học & Công nghệ",
        "topic_id": "computers_digital",
        "topic_vi": "Máy tính & Kỹ thuật số",
        "topic_icon": "🖥️",
        "meaning_vi": "xác thực hai yếu tố (2FA)",
        "definition_en": "a security process where users provide two different authentication factors to verify identity",
        "synonyms": ["2FA", "multi-factor verification"],
        "examples": [
            {"en": "Enabling two-factor authentication dramatically reduces the risk of account takeovers.", "vi": "Kích hoạt xác thực hai yếu tố giúp giảm đáng kể nguy cơ tài khoản bị đánh cắp."},
            {"en": "The bank sends a one-time SMS passcode as part of two-factor authentication.", "vi": "Ngân hàng gửi mã xác nhận OTP dùng một lần qua tin nhắn như một phần của xác thực hai lớp."}
        ]
    },
    {
        "word": "troubleshoot an issue",
        "ipa": "/ˈtrʌb.əl.ʃuːt ən ˈɪʃ.uː/",
        "pos": "collocation",
        "level": "B2",
        "topic_group_id": "tech_science",
        "topic_group_vi": "Khoa học & Công nghệ",
        "topic_id": "electronics_devices",
        "topic_vi": "Điện tử & Viễn thông",
        "topic_icon": "📱",
        "meaning_vi": "tìm và khắc phục sự cố kỹ thuật",
        "definition_en": "to trace and correct faults in a mechanical or electronic system",
        "synonyms": ["diagnose a problem", "debug an issue"],
        "examples": [
            {"en": "The IT support specialist walked the customer through steps to troubleshoot the network issue.", "vi": "Chuyên viên hỗ trợ CNTT đã hướng dẫn khách hàng từng bước để khắc phục sự cố mạng."},
            {"en": "Rebooting the modem is usually the first step to troubleshoot an internet connectivity issue.", "vi": "Khởi động lại modem thường là bước đầu tiên để xử lý sự cố kết nối internet."}
        ]
    },
    {
        "word": "search engine optimization",
        "ipa": "/ˈsɜːtʃ ˌen.dʒɪn ˌɒp.tɪ.maɪˈzeɪ.ʃən/",
        "pos": "collocation",
        "level": "B2",
        "topic_group_id": "tech_science",
        "topic_group_vi": "Khoa học & Công nghệ",
        "topic_id": "computers_digital",
        "topic_vi": "Máy tính & Kỹ thuật số",
        "topic_icon": "🖥️",
        "meaning_vi": "tối ưu hóa công cụ tìm kiếm (SEO)",
        "definition_en": "the process of improving the quality and volume of web traffic to a website from search engines",
        "synonyms": ["SEO"],
        "examples": [
            {"en": "Investing in search engine optimization helped the local bakery reach thousands of nearby customers.", "vi": "Đầu tư vào SEO đã giúp tiệm bánh địa phương tiếp cận hàng ngàn khách hàng ở gần đó."},
            {"en": "Good search engine optimization focuses on high-quality content and fast page speeds.", "vi": "SEO hiệu quả luôn tập trung vào nội dung chất lượng cao và tốc độ tải trang nhanh."}
        ]
    },
    {
        "word": "virtual assistant",
        "ipa": "/ˌvɜː.tʃu.əl əˈsɪs.tənt/",
        "pos": "collocation",
        "level": "B1",
        "topic_group_id": "tech_science",
        "topic_group_vi": "Khoa học & Công nghệ",
        "topic_id": "electronics_devices",
        "topic_vi": "Điện tử & Viễn thông",
        "topic_icon": "📱",
        "meaning_vi": "trợ lý ảo (như Siri, Google Assistant, Alexa)",
        "definition_en": "an application program that understands natural language voice commands and completes tasks for the user",
        "synonyms": ["AI assistant", "voice assistant"],
        "examples": [
            {"en": "You can ask your virtual assistant to set an alarm or play your favorite jazz playlist.", "vi": "Bạn có thể yêu cầu trợ lý ảo đặt báo thức hoặc bật danh sách nhạc jazz yêu thích."},
            {"en": "Smart home speakers rely on integrated virtual assistants to control household lights.", "vi": "Loa thông minh dựa vào trợ lý ảo tích hợp để điều khiển hệ thống đèn trong nhà."}
        ]
    },

    # =========================================================================
    # EMOTIONS & ATTITUDES (15 phrases)
    # =========================================================================
    {
        "word": "at your wit's end",
        "ipa": "/æt jɔː wɪts end/",
        "pos": "idiom",
        "level": "B2",
        "topic_group_id": "emotions_mind",
        "topic_group_vi": "Cảm xúc & Tính cách",
        "topic_id": "feelings_moods",
        "topic_vi": "Cảm xúc & Tâm trạng",
        "topic_icon": "😊",
        "meaning_vi": "bất lực hết cách, hoàn toàn bế tắc không biết làm sao",
        "definition_en": "so worried, confused, or annoyed that you do not know what to do next",
        "synonyms": ["at a complete loss", "desperate"],
        "examples": [
            {"en": "I'm at my wit's end trying to solve this intermittent database connection crash.", "vi": "Tôi hoàn toàn bế tắc khi cố xử lý lỗi sập kết nối cơ sở dữ liệu chập chờn này."},
            {"en": "The parents were at their wit's end trying to calm the crying infant.", "vi": "Đôi vợ chồng gần như bất lực tìm cách dỗ dành đứa con nhỏ đang quấy khóc."}
        ]
    },
    {
        "word": "have butterflies in your stomach",
        "ipa": "/hæv ˈbʌt.ə.flaɪz ɪn jɔː ˈstʌm.ək/",
        "pos": "idiom",
        "level": "B1",
        "topic_group_id": "emotions_mind",
        "topic_group_vi": "Cảm xúc & Tính cách",
        "topic_id": "feelings_moods",
        "topic_vi": "Cảm xúc & Tâm trạng",
        "topic_icon": "😊",
        "meaning_vi": "bồn chồn nôn nao trong bụng trước một sự kiện quan trọng",
        "definition_en": "to feel very nervous, anxious, or fluttery before doing something significant",
        "synonyms": ["feel anxious", "have nervous flutters"],
        "examples": [
            {"en": "He had butterflies in his stomach right before walking onto the auditorium stage.", "vi": "Cậu ấy cảm thấy bồn chồn nôn nao ngay trước khi bước ra sân khấu giảng đường."},
            {"en": "It is completely normal to have butterflies in your stomach before a big job interview.", "vi": "Cảm thấy hồi hộp nôn nao trước một buổi phỏng vấn xin việc quan trọng là điều hoàn toàn bình thường."}
        ]
    },
    {
        "word": "cool as a cucumber",
        "ipa": "/kuːl æz ə ˈkjuː.kʌm.bər/",
        "pos": "idiom",
        "level": "B2",
        "topic_group_id": "emotions_mind",
        "topic_group_vi": "Cảm xúc & Tính cách",
        "topic_id": "personality_character",
        "topic_vi": "Tính cách & Phẩm chất",
        "topic_icon": "🌟",
        "meaning_vi": "điềm tĩnh lạ lùng, không hề nao núng trước áp lực",
        "definition_en": "extremely calm, relaxed, and composed, especially in difficult or stressful situations",
        "synonyms": ["calm and collected", "unflappable"],
        "examples": [
            {"en": "Amid all the boardroom panic, the CEO remained as cool as a cucumber.", "vi": "Giữa lúc cả phòng họp hội đồng hoảng loạn, vị CEO vẫn điềm tĩnh tuyệt đối không hề nao núng."},
            {"en": "The goalkeeper stepped up for the penalty shootout, cool as a cucumber.", "vi": "Thủ môn bước vào loạt sút luân lưu với vẻ mặt điềm đạm lạ lùng."}
        ]
    },
    {
        "word": "look on the bright side",
        "ipa": "/lʊk ɒn ðə braɪt saɪd/",
        "pos": "idiom",
        "level": "B1",
        "topic_group_id": "emotions_mind",
        "topic_group_vi": "Cảm xúc & Tính cách",
        "topic_id": "thought_decision",
        "topic_vi": "Tư duy & Nhận thức",
        "topic_icon": "💡",
        "meaning_vi": "nhìn vào mặt tích cực lạc quan của vấn đề",
        "definition_en": "to find good or encouraging aspects in a difficult or unpleasant situation",
        "synonyms": ["be optimistic", "focus on the positive"],
        "examples": [
            {"en": "Our flight was delayed, but looking on the bright side, we had time to explore the city.", "vi": "Chuyến bay bị hoãn, nhưng nhìn vào mặt tích cực thì chúng tôi có thêm thời gian đi dạo thành phố."},
            {"en": "Always look on the bright side; every setback carries a valuable lesson.", "vi": "Hãy luôn nhìn vào mặt tươi sáng; mỗi thử thách đều mang lại một bài học quý giá."}
        ]
    },
    {
        "word": "see the silver lining",
        "ipa": "/siː ðə ˈsɪl.vər ˈlaɪ.nɪŋ/",
        "pos": "idiom",
        "level": "B2",
        "topic_group_id": "emotions_mind",
        "topic_group_vi": "Cảm xúc & Tính cách",
        "topic_id": "thought_decision",
        "topic_vi": "Tư duy & Nhận thức",
        "topic_icon": "💡",
        "meaning_vi": "tìm thấy tia hy vọng trong nghịch cảnh (trong cái rủi có cái may)",
        "definition_en": "to recognize a hopeful or comforting aspect in an otherwise gloomy situation",
        "synonyms": ["find hope", "see the positive aspect"],
        "examples": [
            {"en": "She saw the silver lining in losing her job: it finally pushed her to launch her own dream café.", "vi": "Cô đã tìm thấy tia sáng hy vọng sau khi mất việc: điều đó đã thúc đẩy cô mở quán cà phê mơ ước."},
            {"en": "Optimists always manage to see the silver lining even in the darkest storms.", "vi": "Những người lạc quan luôn tìm thấy ánh sáng hy vọng ngay cả trong những giông bão tăm tối nhất."}
        ]
    },
    {
        "word": "let off steam",
        "ipa": "/let ɒf stiːm/",
        "pos": "idiom",
        "level": "B2",
        "topic_group_id": "emotions_mind",
        "topic_group_vi": "Cảm xúc & Tính cách",
        "topic_id": "feelings_moods",
        "topic_vi": "Cảm xúc & Tâm trạng",
        "topic_icon": "😊",
        "meaning_vi": "xả hơi, giải tỏa bức xúc căng thẳng tích tụ",
        "definition_en": "to get rid of anger, energy, or strong emotion by doing something physical or recreational",
        "synonyms": ["blow off steam", "vent frustration", "unwind"],
        "examples": [
            {"en": "Hitting the gym after a stressful workday is how he lets off steam.", "vi": "Đi tập gym sau một ngày làm việc áp lực là cách anh ấy xả hơi giải tỏa bức bối."},
            {"en": "Playing video games with friends helps teenagers let off steam on weekends.", "vi": "Chơi điện tử cùng bạn bè giúp các bạn trẻ xả bớt căng thẳng vào cuối tuần."}
        ]
    },
    {
        "word": "wear your heart on your sleeve",
        "ipa": "/weər jɔː hɑːt ɒn jɔː sliːv/",
        "pos": "idiom",
        "level": "B2",
        "topic_group_id": "emotions_mind",
        "topic_group_vi": "Cảm xúc & Tính cách",
        "topic_id": "personality_character",
        "topic_vi": "Tính cách & Phẩm chất",
        "topic_icon": "🌟",
        "meaning_vi": "ruột để ngoài da, bộc lộ hết cảm xúc ra mặt không giấu giếm",
        "definition_en": "to make your feelings and emotions completely obvious to everyone",
        "synonyms": ["express feelings openly", "be emotionally transparent"],
        "examples": [
            {"en": "You always know how Tom is feeling because he wears his heart on his sleeve.", "vi": "Bạn luôn biết Tom đang cảm thấy thế nào vì cậu ấy là người ruột để ngoài da, có gì lộ hết ra mặt."},
            {"en": "She is far too honest to play politics; she wears her heart on her sleeve.", "vi": "Cô ấy quá ngay thẳng để tính toán thủ đoạn; cảm xúc của cô luôn bộc lộ chân thật."}
        ]
    },
    {
        "word": "take pride in",
        "ipa": "/teɪk praɪd ɪn/",
        "pos": "collocation",
        "level": "B1",
        "topic_group_id": "emotions_mind",
        "topic_group_vi": "Cảm xúc & Tính cách",
        "topic_id": "personality_character",
        "topic_vi": "Tính cách & Phẩm chất",
        "topic_icon": "🌟",
        "meaning_vi": "lấy làm tự hào về điều gì",
        "definition_en": "to feel satisfaction and pleasure in an achievement, possession, or family member",
        "synonyms": ["be proud of", "glory in"],
        "examples": [
            {"en": "Master carpenters take immense pride in the flawless finish of their handcrafted furniture.", "vi": "Các nghệ nhân mộc bậc thầy luôn lấy làm tự hào về độ tinh xảo hoàn hảo của đồ gỗ thủ công."},
            {"en": "Our company takes pride in delivering exceptional customer service 24/7.", "vi": "Công ty chúng tôi luôn tự hào mang đến dịch vụ khách hàng xuất sắc 24/7."}
        ]
    },
    {
        "word": "on edge",
        "ipa": "/ɒn edʒ/",
        "pos": "idiom",
        "level": "B2",
        "topic_group_id": "emotions_mind",
        "topic_group_vi": "Cảm xúc & Tính cách",
        "topic_id": "feelings_moods",
        "topic_vi": "Cảm xúc & Tâm trạng",
        "topic_icon": "😊",
        "meaning_vi": "bồn chồn lo âu, căng thẳng đứng ngồi không yên",
        "definition_en": "nervous, tense, irritable, or anxious about something uncertain",
        "synonyms": ["nervous", "jittery", "tense"],
        "examples": [
            {"en": "Everyone in the office has been on edge while awaiting the restructuring announcement.", "vi": "Mọi người trong văn phòng đều đang đứng ngồi không yên trong lúc chờ thông báo tái cấu trúc."},
            {"en": "Drinking too much espresso can leave you feeling jittery and on edge.", "vi": "Uống quá nhiều cà phê có thể khiến bạn cảm thấy bồn chồn và bứt rứt."}
        ]
    },
    {
        "word": "lose heart",
        "ipa": "/luːz hɑːt/",
        "pos": "idiom",
        "level": "B2",
        "topic_group_id": "emotions_mind",
        "topic_group_vi": "Cảm xúc & Tính cách",
        "topic_id": "feelings_moods",
        "topic_vi": "Cảm xúc & Tâm trạng",
        "topic_icon": "😊",
        "meaning_vi": "nản lòng thoái chí, mất hết nhuệ khí",
        "definition_en": "to become discouraged, demoralized, or lose confidence in continuing",
        "synonyms": ["get discouraged", "give up hope"],
        "examples": [
            {"en": "Do not lose heart even when initial experimental trials fail to produce results.", "vi": "Đừng nản lòng thoái chí ngay cả khi những thử nghiệm ban đầu chưa mang lại kết quả."},
            {"en": "The coach urged the players not to lose heart after conceding an early goal.", "vi": "Huấn luyện viên thúc giục các cầu thủ không được nản lòng sau khi bị thủng lưới sớm."}
        ]
    }
]
