Hướng dẫn này giải thích cách sử dụng {{brand}} với Claude Code và Claude chat.

> **Về phiên bản v{{version}}**
> Đây là phiên bản để bạn thử cài đặt trong môi trường của mình. Hoạt động trên từng công cụ chưa được kiểm chứng đầy đủ, nên một số bước có thể không chạy như mong đợi.

## 1. Chọn cách cài đặt

| Nơi bạn muốn sử dụng | Cách khuyến nghị |
| --- | --- |
{{#if marketplace}}
| Claude Code | [A. Cài đặt từ GitHub](#a) (cập nhật cũng dễ dàng) |
{{/if}}
| Claude Code (nếu muốn cài từ ZIP) | [{{L_zip}}. Cài đặt từ ZIP](#{{l_zip}}) |
| Claude chat (claude.ai và ứng dụng) | [{{L_chat}}. Tải kỹ năng lên](#{{l_chat}}) |

Claude Code và Claude chat có cách cài đặt khác nhau.

{{#if marketplace}}
## A. Claude Code: cài đặt từ GitHub

1. Trong terminal, đăng ký nguồn phân phối của KUMIHAN.

   ```sh
   claude plugin marketplace add "https://github.com/landco-llc/kumihan.git#main"
   ```

2. Trong cuộc trò chuyện Claude Code, nhập lệnh sau:

   ```text
   /plugin install {{plugin}}@kumihan-marketplace
   ```

3. Kiểm tra nội dung, chọn phạm vi sử dụng (chỉ mình bạn, chỉ dự án này, v.v.) rồi cài đặt.

Sau khi cài đặt, bạn có thể dùng các lệnh sau:

{{claude_commands}}

{{/if}}
## {{L_zip}}. Claude Code: cài đặt từ ZIP

1. Tải [ZIP plugin cho Claude Code]({{plugin_url}}) xuống.
{{#if plugin_folder}}
2. Giải nén ZIP, bạn sẽ có thư mục `{{plugin_folder}}`.
{{else}}
2. Tạo một thư mục `{{plugin}}` trống và giải nén ZIP vào trong đó.
{{/if}}
3. Khởi động Claude Code với thư mục đó.

   ```sh
   claude --plugin-dir "/absolute/path/{{plugin_dir}}"
   ```

**Lưu ý**

- Hãy giữ nguyên nội dung thư mục. Không xóa tệp hoặc thêm tệp khác vào.
- Cách này không tự động cập nhật. Khi có phiên bản mới, hãy thay bằng ZIP mới.

## {{L_chat}}. Claude chat: tải kỹ năng lên

Cách này dành cho claude.ai và ứng dụng Claude.

1. Tải ZIP của các kỹ năng bạn muốn dùng.
{{skills_list_indented}}
2. Trong Claude, mở **Customize → Skills**, rồi chọn **Upload a skill** từ nút thêm.
3. Tải từng ZIP lên và bật kỹ năng.

**Lưu ý**

- Không dùng được ZIP plugin cho Claude Code ở đây. Hãy dùng ZIP của từng kỹ năng.
- Tải ZIP lên mà không đổi tên tệp.
- Để dùng kỹ năng, cần bật “thực thi mã” (code execution) trong phần cài đặt. Xem thêm [hướng dẫn chính thức của Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude).
- Với tài khoản tổ chức, tính năng có thể không dùng được tùy theo cài đặt của quản trị viên.
- Kỹ năng đã tải lên không tự động cập nhật. Khi có phiên bản mới, hãy tải lên lại.

## 2. Dùng thử

Bạn nên bắt đầu bằng một yêu cầu không thay đổi tệp nào:

> Tôi dự định làm một trang web bằng tiếng Việt. Hãy cho tôi biết những điểm cần lưu ý. Đừng thay đổi bất kỳ tệp nào.

## Kiểm tra tính toàn vẹn của tệp (không bắt buộc)

Để kiểm tra tệp tải về không bị hỏng, hãy dùng [SHA256SUMS.txt]({{sums}}).

Đặt SHA256SUMS.txt vào cùng thư mục với các tệp ZIP đã tải về, rồi chạy lệnh sau trong terminal. Nếu không có `shasum`, hãy đối chiếu SHA-256 bằng công cụ tương đương như `Get-FileHash` của Windows PowerShell.

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

Nếu dòng của các tệp bạn đã tải hiển thị `OK` thì tệp không có vấn đề.

---

Công cụ khác: [ChatGPT / Codex]({{page_chatgpt}}) · [Gemini]({{page_gemini}})

Giao diện và điều kiện cung cấp có thể thay đổi. Vui lòng xem hướng dẫn chính thức của từng dịch vụ để biết thông tin mới nhất (trang này được kiểm tra vào ngày 14 tháng 10 năm 2026).
