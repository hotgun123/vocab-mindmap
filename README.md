# English Quiz - Chrome Extension

Extension hỗ trợ ôn luyện từ vựng tiếng Anh thụ động ngay trong lúc lướt web. Extension hiển thị pop-up ôn tập theo các khoảng thời gian được thiết lập sẵn, với 3 chế độ câu hỏi linh hoạt chống học vẹt và đoán mò.

## 📥 Cách cài đặt (Cài đặt thủ công)
1. Tải toàn bộ thư mục `extension English` về máy tính.
2. Mở trình duyệt Chrome và truy cập vào trang quản lý tiện ích: `chrome://extensions/`
3. Bật chế độ **Developer mode** (Chế độ dành cho nhà phát triển) ở góc trên bên phải.
4. Click vào nút **Load unpacked** (Tải tiện ích đã giải nén).
5. Chọn thư mục `extension English`. Extension sẽ xuất hiện trên trình duyệt của bạn.

---

## 🎯 Hướng dẫn sử dụng
Click vào biểu tượng của Extension trên thanh công cụ để mở giao diện cài đặt (Popup).
- **Khoảng thời gian hiện pop-up:** Cài đặt chu kỳ hiển thị quiz (5 phút, 10 phút, 30 phút, v.v.).
- **Chế độ ôn luyện:**
  - `Từ vựng (Anh -> Việt):` Hiển thị từ tiếng Anh (kèm IPA và phát âm), bạn chọn nghĩa tiếng Việt.
  - `Từ vựng (Việt -> Anh):` Hiển thị nghĩa tiếng Việt, bạn chọn từ tiếng Anh tương ứng.
  - `Câu (Sentence):` Hiển thị câu tiếng Anh hoàn chỉnh, bạn chọn câu dịch tiếng Việt (có các đáp án gây nhiễu).
  - `Trộn ngẫu nhiên (Random):` Trộn tự động các chế độ trên. *(Khuyên dùng)*
- **Nút "Làm Quiz Ngay":** Bấm để ép extension hiện quiz ngay lập tức trên tab hiện tại (lưu ý tab không được là trang `chrome://` hoặc `Cửa hàng Chrome`).

---

## 📝 Hướng dẫn cập nhật và chỉnh sửa từ vựng
Toàn bộ dữ liệu từ vựng nằm trong file: `data/vocabulary.json`. 

### 1. Thêm / Sửa / Xóa từ vựng
Mở file `data/vocabulary.json` bằng text editor (VS Code, Notepad). Dữ liệu có cấu trúc JSON như sau:
```json
{
  "id": "work_verb_1",
  "word": "work",
  "pos": "verb",
  "phonetic": "/wɜːrk/",
  "ipa": "/wɜːk/",
  "definition_en": "to do a job",
  "translation_vi": "làm việc",
  "example_en": "She is working.",
  "difficulty": 1,
  "tags": []
}
```
Bạn có thể sửa `translation_vi`, `example_en` hay bất kỳ trường nào. Sau khi lưu file, vào `chrome://extensions/` nhấn nút **Reload (biểu tượng mũi tên xoay vòng)** của extension để dữ liệu mới được áp dụng.

### 2. Cập nhật IPA tự động (Cho từ mới thêm vào)
Nếu bạn thêm từ mới mà không biết IPA chuẩn, extension có một script tự động gọi API từ điển để điền IPA:
1. Bạn cần cài đặt [Node.js](https://nodejs.org/) trên máy tính.
2. Mở Terminal (CMD / PowerShell) tại thư mục `scripts` (tức là `extension English/scripts`).
3. Chạy lệnh sau:
   ```bash
   node add_ipa.js
   ```
4. Script sẽ tự động quyét file `vocabulary.json` và bổ sung IPA cho những từ chưa có.

---

## ⚙️ Nâng cao: Tùy chỉnh Regex cho phần Dịch câu (Mode 2)
Trong chế độ **Câu (Sentence)**, extension sẽ tách chủ ngữ và thì (tense) từ câu tiếng Anh (`example_en`) để tạo thành khung dịch tiếng Việt (ví dụ: `Cô ấy` + `đang` + `{nghĩa}`). 

Nếu bạn muốn extension dịch chuẩn hơn, hoặc thêm các chủ ngữ/thì mới, hãy chỉnh sửa hàm `extractSentenceFrame` trong file `background.js`:

1. Mở file `background.js`
2. Tìm đến hàm `extractSentenceFrame`:
   ```javascript
   function extractSentenceFrame(sentence_en, target_word) {
     const s = sentence_en.toLowerCase();
     let subject = "Ai đó";
     
     // Thêm hoặc sửa chủ ngữ ở đây
     if (s.includes(" she ") || s.startsWith("she ")) subject = "Cô ấy";
     else if (s.includes(" my father ")) subject = "Bố tôi"; // Ví dụ thêm mới
     
     let tense = "";
     // Thêm hoặc sửa thì (tense) ở đây
     if (s.includes(" is ") || s.includes(" are ") || s.includes(" am ")) tense = "đang";
     else if (s.includes(" will ")) tense = "sẽ";
     else tense = "thì";
   
     return { subject, tense };
   }
   ```
3. Lưu file `background.js` lại.
4. Mở `chrome://extensions/` và nhấn nút **Reload** để áp dụng thay đổi.
