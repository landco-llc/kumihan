Hướng dẫn này giải thích cách sử dụng {{brand}} với ChatGPT và Codex.

> **Về phiên bản v{{version}}**
> Đây là phiên bản để bạn thử cài đặt trong môi trường của mình. Hoạt động trên từng công cụ chưa được kiểm chứng đầy đủ, nên một số bước có thể không chạy như mong đợi.

## 1. Chọn cách cài đặt

| Nơi bạn muốn sử dụng | Cách khuyến nghị |
| --- | --- |
| ChatGPT (nếu có thể tải kỹ năng lên) | [A. Thêm từng kỹ năng một](#a) |
| ChatGPT (nếu muốn đăng ký làm plugin riêng của bạn) | [B. Đăng ký tất cả dưới dạng plugin](#b) |
| Codex (dùng trên máy tính) | [C. Sao chép thư mục](#c) |

Mỗi **kỹ năng** (skill) là một chức năng; **plugin** là gói gộp cả bốn kỹ năng.

## 2. Tải tệp xuống

Các tệp có trên [trang phát hành]({{release}}). Nhấp vào liên kết để tải tệp ZIP xuống.

**Plugin (gồm cả bốn kỹ năng)**

- {{plugin_link}}

**Kỹ năng (từng kỹ năng riêng)**

{{skills_list}}

## A. Thêm kỹ năng vào ChatGPT

Dùng cách này nếu giao diện ChatGPT của bạn có mục “Skills” và tùy chọn tải lên.

1. Chọn một tệp ZIP kỹ năng và tải lên.
2. Kiểm tra nội dung hiển thị rồi thêm kỹ năng.
3. Lặp lại các bước trên cho từng kỹ năng bạn cần.

**Lưu ý**

- Không dùng được ZIP plugin với cách này. Hãy dùng ZIP của từng kỹ năng.
- Chỉ đính kèm tệp vào cuộc trò chuyện thì không cài đặt được kỹ năng.
- Nếu không thấy mục này, có thể gói dịch vụ hoặc ứng dụng của bạn chưa hỗ trợ. Xem [hướng dẫn chính thức của OpenAI](https://learn.chatgpt.com/docs/build-skills).

## B. Đăng ký plugin trong ChatGPT

Cách này gộp cả bốn kỹ năng và đăng ký thành plugin riêng của bạn.

1. Mở cuộc trò chuyện mới trong ChatGPT và chọn `@plugin-creator`.
2. Đính kèm tệp ZIP plugin.
3. Gửi yêu cầu như sau:

   > Hãy đăng ký gói này thành plugin riêng tư chỉ dành cho tôi. Đừng gửi nó lên thư mục công khai.

4. Sau khi đăng ký xong, **{{display}}** sẽ xuất hiện trong Plugins, ở mục “Personal” hoặc “Created by me”.
5. Cài đặt nếu cần, rồi bật plugin trong một cuộc trò chuyện mới.

**Lưu ý**

- Plugin có thể được đăng ký vào không gian làm việc của nhóm. Nếu chỉ muốn dùng riêng, hãy kiểm tra nơi lưu trước khi đăng ký.
- Tính năng này có thể không dùng được tùy theo gói dịch vụ hoặc cài đặt không gian làm việc. Xem thêm [Build plugins](https://learn.chatgpt.com/docs/build-plugins) và [Plugins](https://learn.chatgpt.com/docs/plugins).
- Plugin đăng ký theo cách này chỉ dùng được trong tài khoản của bạn và không xuất hiện trong thư mục công khai.

## C. Sao chép thư mục kỹ năng cho Codex

Giải nén ZIP kỹ năng, bạn sẽ có thư mục như `{{first}}`. Hãy sao chép thư mục này vào vị trí mà Codex đọc kỹ năng.

| Phạm vi sử dụng | Nơi sao chép đến |
| --- | --- |
| Chỉ dùng trong một dự án | `.agents/skills/` bên trong dự án |
| Dùng cho mọi dự án | `~/.agents/skills/` trong thư mục chính (home) |

Ví dụ, để thêm `{{first}}` vào một dự án:

```sh
mkdir -p /path/to/your-project/.agents/skills
cp -R {{first}} /path/to/your-project/.agents/skills/
```

**Lưu ý**

- Hãy sao chép nguyên cả thư mục cùng toàn bộ nội dung bên trong. Chỉ có một phần tệp thì kỹ năng sẽ không chạy đúng.
- Nếu đã có thư mục cùng tên, hãy kiểm tra nội dung trước khi ghi đè.

## 3. Dùng thử

Sau khi cài đặt, hãy mở cuộc trò chuyện mới và gọi kỹ năng.

| Công cụ | Cách gọi |
| --- | --- |
| ChatGPT | Chọn từ `@` |
| Codex | Chọn từ `$` hoặc `/skills` |

Bạn nên bắt đầu bằng một yêu cầu không thay đổi tệp nào:

> Tôi dự định làm một báo cáo bằng tiếng Việt. Hãy cho tôi biết những điểm cần lưu ý. Đừng thay đổi bất kỳ tệp nào.

## Kiểm tra tính toàn vẹn của tệp (không bắt buộc)

Để kiểm tra tệp tải về không bị hỏng, hãy dùng [SHA256SUMS.txt]({{sums}}).

Đặt SHA256SUMS.txt vào cùng thư mục với các tệp ZIP đã tải về, rồi chạy lệnh sau trong terminal. Nếu không có `shasum`, hãy đối chiếu SHA-256 bằng công cụ tương đương như `Get-FileHash` của Windows PowerShell.

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

Nếu dòng của các tệp bạn đã tải hiển thị `OK` thì tệp không có vấn đề.

---

Công cụ khác: [Claude]({{page_claude}}) · [Gemini]({{page_gemini}})

Giao diện và điều kiện cung cấp có thể thay đổi. Vui lòng xem hướng dẫn chính thức của từng dịch vụ để biết thông tin mới nhất (trang này được kiểm tra vào ngày 14 tháng 10 năm 2026).
