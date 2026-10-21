Hướng dẫn này giải thích cách sử dụng {{brand}} với Gemini CLI và ứng dụng Gemini.

> **Về phiên bản v{{version}}**
> Đây là phiên bản để bạn thử cài đặt trong môi trường của mình. Hoạt động trên từng công cụ chưa được kiểm chứng đầy đủ, nên một số bước có thể không chạy như mong đợi.

## 1. Chọn cách cài đặt

| Nơi bạn muốn sử dụng | Cách khuyến nghị |
| --- | --- |
| Gemini CLI (cả bốn kỹ năng cùng lúc) | [A. Cài đặt dưới dạng tiện ích mở rộng](#a) |
| Gemini CLI (chỉ những kỹ năng cần thiết) | [B. Chọn và cài từng kỹ năng](#b) |
| Ứng dụng Gemini (web, Mac, điện thoại) | [C. Tải kỹ năng lên](#c) |

## A. Gemini CLI: cài đặt dưới dạng tiện ích mở rộng

Cách này cài đặt cả bốn kỹ năng cùng một lúc.

1. Tải [ZIP tiện ích mở rộng]({{plugin_url}}) xuống.
{{#if plugin_folder}}
2. Giải nén ZIP, bạn sẽ có thư mục `{{plugin_folder}}`.
{{else}}
2. Tạo một thư mục `{{plugin}}` trống và giải nén ZIP vào trong đó.
{{/if}}
3. Cài đặt từ thư mục đó.

   ```sh
   gemini extensions install "/absolute/path/{{plugin_dir}}"
   ```

Khi màn hình xác nhận xuất hiện, hãy kiểm tra nội dung rồi tiếp tục. Sau khi cài đặt, tiện ích mở rộng sẽ có hiệu lực trong mọi dự án.

Tiện ích mở rộng cài từ ZIP sẽ không tự động cập nhật. Khi có phiên bản mới, hãy thay bằng ZIP mới.

## B. Gemini CLI: chọn và cài từng kỹ năng

Cách này chỉ cài những kỹ năng bạn cần, theo từng dự án. Nếu đã cài theo cách A thì không cần bước này.

Ví dụ, để cài `{{first}}`, hãy chạy lệnh sau trong dự án của bạn:

```sh
gemini skills install https://github.com/landco-llc/kumihan --path {{skills_path}}/{{first}} --scope workspace
```

Để cài các kỹ năng khác, hãy đổi `--path` như sau:

{{gemini_paths}}

`--scope workspace` là thiết lập để chỉ dùng “trong dự án này”. Nếu bỏ qua, kỹ năng sẽ dùng được trong mọi dự án.

**Khi cập nhật**

Chạy lại cùng lệnh đó. Kỹ năng đã cài sẽ bị thay thế, vì vậy nếu bạn đã tự chỉnh sửa, hãy lưu lại trước.

## C. Ứng dụng Gemini: tải kỹ năng lên

1. Tải ZIP của các kỹ năng bạn muốn dùng.
{{skills_list_indented}}
2. Trong Gemini, mở **Customize** (nếu không thấy, hãy mở **More**) → **Skills** → **Upload**.
3. Chọn từng ZIP, kiểm tra nội dung rồi nhấn **Create**.

**Lưu ý**

- Chỉ dành cho tài khoản Google cá nhân của người từ 18 tuổi trở lên. Hiện chưa hỗ trợ tài khoản công việc hoặc trường học.
- Cần bật “Keep Activity” (Lưu hoạt động).
- Tính năng đang được triển khai dần nên có thể chưa hiển thị với bạn. Xem thêm [Trợ giúp chính thức của Gemini](https://support.google.com/gemini/answer/17094296?hl=ja).
- Không dùng được ZIP tiện ích mở rộng (dành cho Gemini CLI) ở đây.
- Kỹ năng đã tải lên không tự động cập nhật. Khi có phiên bản mới, hãy tải lên lại.

## 2. Dùng thử

Bạn nên bắt đầu bằng một yêu cầu không thay đổi tệp nào:

> Tôi dự định làm một bài thuyết trình bằng tiếng Việt. Hãy cho tôi biết những điểm cần lưu ý. Đừng thay đổi bất kỳ tệp nào.

## Kiểm tra tính toàn vẹn của tệp (không bắt buộc)

Để kiểm tra tệp tải về không bị hỏng, hãy dùng [SHA256SUMS.txt]({{sums}}).

Đặt SHA256SUMS.txt vào cùng thư mục với các tệp ZIP đã tải về, rồi chạy lệnh sau trong terminal. Nếu không có `shasum`, hãy đối chiếu SHA-256 bằng công cụ tương đương như `Get-FileHash` của Windows PowerShell.

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

Nếu dòng của các tệp bạn đã tải hiển thị `OK` thì tệp không có vấn đề.

---

Công cụ khác: [ChatGPT / Codex]({{page_chatgpt}}) · [Claude]({{page_claude}})

Giao diện và điều kiện cung cấp có thể thay đổi. Vui lòng xem hướng dẫn chính thức của từng dịch vụ để biết thông tin mới nhất (trang này được kiểm tra vào ngày 14 tháng 10 năm 2026).
