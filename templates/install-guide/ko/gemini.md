{{brand}}을 Gemini CLI와 Gemini 앱에서 사용하기 위한 절차입니다.

> **v{{version}} 안내**
> 직접 사용하는 환경에서 설치를 시험해 보실 수 있도록 제공하는 버전입니다. 각 도구에서의 동작은 아직 충분히 확인되지 않아 제대로 작동하지 않을 수 있습니다.

## 1. 설치 방법 선택

| 사용할 곳 | 권장 방법 |
| --- | --- |
| Gemini CLI(네 가지를 한 번에) | [A. 확장 프로그램으로 설치하기](#a) |
| Gemini CLI(필요한 것만) | [B. 스킬을 골라 설치하기](#b) |
| Gemini 앱(웹·Mac·스마트폰) | [C. 스킬 업로드하기](#c) |

## A. Gemini CLI: 확장 프로그램으로 설치하기

네 가지 스킬을 한 번에 설치하는 방법입니다.

1. [확장 프로그램 ZIP]({{plugin_url}})을 다운로드합니다.
{{#if plugin_folder}}
2. ZIP의 압축을 풀면 `{{plugin_folder}}` 폴더가 생깁니다.
{{else}}
2. 빈 `{{plugin}}` 폴더를 만들고 그 안에 압축을 풉니다.
{{/if}}
3. 폴더를 지정해 설치합니다.

   ```sh
   gemini extensions install "/absolute/path/{{plugin_dir}}"
   ```

확인 화면이 표시되면 내용을 확인한 뒤 진행하세요. 확장 프로그램은 설치하면 모든 프로젝트에서 활성화됩니다.

ZIP으로 설치한 경우에는 자동으로 업데이트되지 않습니다. 새 버전이 나오면 ZIP을 교체하세요.

## B. Gemini CLI: 스킬을 골라 설치하기

필요한 스킬만 프로젝트 단위로 설치하는 방법입니다. A로 설치했다면 이 절차는 필요하지 않습니다.

예를 들어 `{{first}}`를 설치하려면 대상 프로젝트에서 다음을 실행합니다.

```sh
gemini skills install https://github.com/landco-llc/kumihan --path {{skills_path}}/{{first}} --scope workspace
```

다른 스킬을 설치할 때는 `--path`를 다음과 같이 바꾸세요.

{{gemini_paths}}

`--scope workspace`는 '이 프로젝트에서만' 사용하는 설정입니다. 생략하면 모든 프로젝트에서 사용할 수 있습니다.

**업데이트할 때**

같은 명령을 다시 실행합니다. 설치된 스킬은 교체되므로, 직접 수정한 내용이 있다면 먼저 저장해 두세요.

## C. Gemini 앱: 스킬 업로드하기

1. 사용할 스킬의 ZIP을 다운로드합니다.
{{skills_list_indented}}
2. Gemini에서 **Customize**(보이지 않으면 **More**) → **Skills** → **Upload**를 엽니다.
3. ZIP을 하나씩 선택하고 내용을 확인한 뒤 **Create**를 누릅니다.

**주의 사항**

- 만 18세 이상의 개인 Google 계정에서만 사용할 수 있습니다. 직장·학교 계정에서는 현재 사용할 수 없습니다.
- 'Keep Activity(활동 저장)'를 켜 두어야 합니다.
- 기능이 순차적으로 제공되고 있어 아직 표시되지 않을 수 있습니다. 자세한 내용은 [Gemini 공식 도움말](https://support.google.com/gemini/answer/17094296?hl=ja)을 참고하세요.
- 확장 프로그램 ZIP(Gemini CLI용)은 여기서 사용할 수 없습니다.
- 업로드한 스킬은 자동으로 업데이트되지 않습니다. 새 버전이 나오면 다시 업로드하세요.

## 2. 사용해 보기

처음에는 파일을 변경하지 않는 요청으로 시험해 보시길 권장합니다.

> 한국어 프레젠테이션 자료를 만들 예정입니다. 주의할 점을 알려 주세요. 파일은 변경하지 마세요.

## 파일이 올바른지 확인하기(선택)

다운로드한 파일이 손상되지 않았는지 확인하려면 [SHA256SUMS.txt]({{sums}})를 사용합니다.

다운로드한 ZIP 파일과 같은 폴더에 SHA256SUMS.txt를 두고, 터미널에서 다음 명령을 실행합니다. `shasum`이 없는 환경에서는 Windows PowerShell의 `Get-FileHash` 등으로 SHA-256을 대조하세요.

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

다운로드한 파일의 행에 `OK`가 표시되면 문제가 없습니다.

---

다른 도구: [ChatGPT·Codex]({{page_chatgpt}}) · [Claude]({{page_claude}})

화면과 제공 조건은 바뀔 수 있습니다. 최신 정보는 각 서비스의 공식 안내를 확인하세요(이 페이지 확인일: 2026년 10월 14일).
