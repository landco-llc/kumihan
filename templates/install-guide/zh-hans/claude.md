本指南介绍如何在 Claude Code 和 Claude 聊天中使用 {{brand}}。

> **关于 v{{version}}**
> 此版本供你在自己的环境中试用。各工具中的实际运行尚未经过充分验证，因此部分步骤可能无法按预期工作。

## 1. 选择安装方式

| 使用场景 | 推荐方式 |
| --- | --- |
{{#if marketplace}}
| Claude Code | [A. 从 GitHub 安装](#a)（更新也很方便） |
{{/if}}
| Claude Code（希望通过 ZIP 安装时） | [{{L_zip}}. 从 ZIP 安装](#{{l_zip}}) |
| Claude 聊天（claude.ai 和应用） | [{{L_chat}}. 上传技能](#{{l_chat}}) |

Claude Code 和 Claude 聊天的安装方式不同。

{{#if marketplace}}
## A. Claude Code：从 GitHub 安装

1. 在终端中注册 KUMIHAN 的发布源。

   ```sh
   claude plugin marketplace add "https://github.com/landco-llc/kumihan.git#main"
   ```

2. 在 Claude Code 的对话中输入以下内容：

   ```text
   /plugin install {{plugin}}@kumihan-marketplace
   ```

3. 确认内容，选择使用范围（仅限自己、仅限当前项目等）后进行安装。

安装完成后，即可使用以下命令：

{{claude_commands}}

{{/if}}
## {{L_zip}}. Claude Code：从 ZIP 安装

1. 下载 [Claude Code 插件 ZIP]({{plugin_url}})。
{{#if plugin_folder}}
2. 解压 ZIP 后，会得到 `{{plugin_folder}}` 文件夹。
{{else}}
2. 新建一个空的 `{{plugin}}` 文件夹，并将 ZIP 解压到其中。
{{/if}}
3. 指定该文件夹并启动 Claude Code。

   ```sh
   claude --plugin-dir "/absolute/path/{{plugin_dir}}"
   ```

**注意事项**

- 请直接使用文件夹中的内容，不要删除文件或混入其他文件。
- 此方式不会自动更新。新版本发布后，请替换 ZIP。

## {{L_chat}}. Claude 聊天：上传技能

适用于 claude.ai 和 Claude 应用。

1. 下载想要使用的技能 ZIP。
{{skills_list_indented}}
2. 在 Claude 中打开 **Customize → Skills**，通过添加按钮选择 **Upload a skill**。
3. 逐个上传 ZIP，并启用技能。

**注意事项**

- 此处不能使用 Claude Code 插件 ZIP，请使用技能 ZIP。
- 上传时请不要更改 ZIP 的文件名。
- 使用技能需要在设置中启用“代码执行”。详情请参阅 [Claude 官方说明](https://support.claude.com/en/articles/12512180-use-skills-in-claude)。
- 组织账户可能会因管理员的设置而无法使用。
- 上传的技能不会自动更新。新版本发布后，请重新上传。

## 2. 开始试用

建议先用不会修改文件的请求进行测试：

> 我准备制作一个中文网页。请告诉我需要注意哪些要点。请不要修改任何文件。

## 检查文件是否完整（可选）

如果想确认下载的文件没有损坏，请使用 [SHA256SUMS.txt]({{sums}})。

将 SHA256SUMS.txt 放在与下载的 ZIP 文件相同的文件夹中，然后在终端中运行以下命令。如果环境中没有 `shasum`，请使用 Windows PowerShell 的 `Get-FileHash` 等工具核对 SHA-256。

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

如果下载文件所在的行显示 `OK`，即表示文件没有问题。

---

其他工具：[ChatGPT / Codex]({{page_chatgpt}}) · [Gemini]({{page_gemini}})

界面和提供条件可能会发生变化。最新信息请以各服务的官方说明为准（本页确认日期：2026 年 10 月 14 日）。
