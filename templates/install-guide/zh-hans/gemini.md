本指南介绍如何在 Gemini CLI 和 Gemini 应用中使用 {{brand}}。

> **关于 v{{version}}**
> 此版本供你在自己的环境中试用。各工具中的实际运行尚未经过充分验证，因此部分步骤可能无法按预期工作。

## 1. 选择安装方式

| 使用场景 | 推荐方式 |
| --- | --- |
| Gemini CLI（一次安装四项技能） | [A. 作为扩展程序安装](#a) |
| Gemini CLI（只安装需要的技能） | [B. 选择技能安装](#b) |
| Gemini 应用（网页版、Mac、手机） | [C. 上传技能](#c) |

## A. Gemini CLI：作为扩展程序安装

一次性安装全部四项技能的方法。

1. 下载[扩展程序 ZIP]({{plugin_url}})。
{{#if plugin_folder}}
2. 解压 ZIP 后，会得到 `{{plugin_folder}}` 文件夹。
{{else}}
2. 新建一个空的 `{{plugin}}` 文件夹，并将 ZIP 解压到其中。
{{/if}}
3. 指定该文件夹进行安装。

   ```sh
   gemini extensions install "/absolute/path/{{plugin_dir}}"
   ```

出现确认界面时，请确认内容后再继续。扩展程序安装后，会在所有项目中生效。

通过 ZIP 安装时不会自动更新。新版本发布后，请替换 ZIP。

## B. Gemini CLI：选择技能安装

只在单个项目中安装所需技能的方法。如果已通过 A 安装，则无需执行此步骤。

例如，要安装 `{{first}}`，请在目标项目中运行以下命令：

```sh
gemini skills install https://github.com/landco-llc/kumihan --path {{skills_path}}/{{first}} --scope workspace
```

安装其他技能时，请将 `--path` 改为：

{{gemini_paths}}

`--scope workspace` 表示“仅在此项目中”使用。如果省略，技能将可在所有项目中使用。

**更新时**

再次运行相同的命令。已安装的技能会被替换，如果你自行修改过内容，请先保存。

## C. Gemini 应用：上传技能

1. 下载想要使用的技能 ZIP。
{{skills_list_indented}}
2. 在 Gemini 中打开 **Customize**（如果找不到，请打开 **More**）→ **Skills** → **Upload**。
3. 逐个选择 ZIP，确认内容后点击 **Create**。

**注意事项**

- 仅限年满 18 岁用户的个人 Google 账户使用。工作或学校账户目前不支持。
- 需要开启“Keep Activity（保存活动记录）”。
- 该功能正在逐步推出，你可能暂时还看不到。详情请参阅 [Gemini 官方帮助](https://support.google.com/gemini/answer/17094296?hl=ja)。
- 此处不能使用扩展程序 ZIP（Gemini CLI 用）。
- 上传的技能不会自动更新。新版本发布后，请重新上传。

## 2. 开始试用

建议先用不会修改文件的请求进行测试：

> 我准备制作一份中文演示文稿。请告诉我需要注意哪些要点。请不要修改任何文件。

## 检查文件是否完整（可选）

如果想确认下载的文件没有损坏，请使用 [SHA256SUMS.txt]({{sums}})。

将 SHA256SUMS.txt 放在与下载的 ZIP 文件相同的文件夹中，然后在终端中运行以下命令。如果环境中没有 `shasum`，请使用 Windows PowerShell 的 `Get-FileHash` 等工具核对 SHA-256。

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

如果下载文件所在的行显示 `OK`，即表示文件没有问题。

---

其他工具：[ChatGPT / Codex]({{page_chatgpt}}) · [Claude]({{page_claude}})

界面和提供条件可能会发生变化。最新信息请以各服务的官方说明为准（本页确认日期：2026 年 10 月 14 日）。
