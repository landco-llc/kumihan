{{brand}}을 Claude Code와 Claude 채팅에서 사용하기 위한 절차입니다.

> **v{{version}} 안내**
> 직접 사용하는 환경에서 설치를 시험해 보실 수 있도록 제공하는 버전입니다. 각 도구에서의 동작은 아직 충분히 확인되지 않아 제대로 작동하지 않을 수 있습니다.

## 1. 설치 방법 선택

| 사용할 곳 | 권장 방법 |
| --- | --- |
{{#if marketplace}}
| Claude Code | [A. GitHub에서 설치하기](#a)(업데이트도 간편) |
{{/if}}
| Claude Code(ZIP으로 설치하려는 경우) | [{{L_zip}}. ZIP으로 설치하기](#{{l_zip}}) |
| Claude 채팅(claude.ai·앱) | [{{L_chat}}. 스킬 업로드하기](#{{l_chat}}) |

Claude Code와 Claude 채팅은 설치 방법이 다릅니다.

{{#if marketplace}}
## A. Claude Code: GitHub에서 설치하기

1. 터미널에서 KUMIHAN 배포처를 등록합니다.

   ```sh
   claude plugin marketplace add "https://github.com/landco-llc/kumihan.git#main"
   ```

2. Claude Code 대화에서 다음을 입력합니다.

   ```text
   /plugin install {{plugin}}@kumihan-marketplace
   ```

3. 내용을 확인하고 사용 범위(나만, 이 프로젝트만 등)를 선택해 설치합니다.

설치가 끝나면 다음 명령을 사용할 수 있습니다.

{{claude_commands}}

{{/if}}
## {{L_zip}}. Claude Code: ZIP으로 설치하기

1. [Claude Code용 플러그인 ZIP]({{plugin_url}})을 다운로드합니다.
{{#if plugin_folder}}
2. ZIP의 압축을 풀면 `{{plugin_folder}}` 폴더가 생깁니다.
{{else}}
2. 빈 `{{plugin}}` 폴더를 만들고 그 안에 압축을 풉니다.
{{/if}}
3. 그 폴더를 지정해 Claude Code를 실행합니다.

   ```sh
   claude --plugin-dir "/absolute/path/{{plugin_dir}}"
   ```

**주의 사항**

- 폴더 내용은 그대로 사용하세요. 파일을 지우거나 다른 파일을 섞지 마세요.
- 이 방법으로는 자동으로 업데이트되지 않습니다. 새 버전이 나오면 ZIP을 교체하세요.

## {{L_chat}}. Claude 채팅: 스킬 업로드하기

claude.ai나 Claude 앱에서 사용하는 방법입니다.

1. 사용할 스킬의 ZIP을 다운로드합니다.
{{skills_list_indented}}
2. Claude에서 **Customize → Skills**를 열고, 추가 버튼에서 **Upload a skill**을 선택합니다.
3. ZIP을 하나씩 업로드하고 스킬을 활성화합니다.

**주의 사항**

- Claude Code용 플러그인 ZIP은 여기서 사용할 수 없습니다. 스킬 ZIP을 사용하세요.
- ZIP 파일 이름은 바꾸지 말고 업로드하세요.
- 스킬을 사용하려면 설정에서 '코드 실행'이 켜져 있어야 합니다. 자세한 내용은 [Claude 공식 안내](https://support.claude.com/en/articles/12512180-use-skills-in-claude)를 참고하세요.
- 조직 계정에서는 관리자 설정에 따라 사용할 수 없을 수 있습니다.
- 업로드한 스킬은 자동으로 업데이트되지 않습니다. 새 버전이 나오면 다시 업로드하세요.

## 2. 사용해 보기

처음에는 파일을 변경하지 않는 요청으로 시험해 보시길 권장합니다.

> 한국어 웹페이지를 만들 예정입니다. 주의할 점을 알려 주세요. 파일은 변경하지 마세요.

## 파일이 올바른지 확인하기(선택)

다운로드한 파일이 손상되지 않았는지 확인하려면 [SHA256SUMS.txt]({{sums}})를 사용합니다.

다운로드한 ZIP 파일과 같은 폴더에 SHA256SUMS.txt를 두고, 터미널에서 다음 명령을 실행합니다. `shasum`이 없는 환경에서는 Windows PowerShell의 `Get-FileHash` 등으로 SHA-256을 대조하세요.

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

다운로드한 파일의 행에 `OK`가 표시되면 문제가 없습니다.

---

다른 도구: [ChatGPT·Codex]({{page_chatgpt}}) · [Gemini]({{page_gemini}})

화면과 제공 조건은 바뀔 수 있습니다. 최신 정보는 각 서비스의 공식 안내를 확인하세요(이 페이지 확인일: 2026년 10월 14일).
