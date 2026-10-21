本指南介绍如何在 ChatGPT 和 Codex 中使用 {{brand}}。

> **关于 v{{version}}**
> 此版本供你在自己的环境中试用。各工具中的实际运行尚未经过充分验证，因此部分步骤可能无法按预期工作。

## 1. 选择安装方式

| 使用场景 | 推荐方式 |
| --- | --- |
| ChatGPT（可以上传技能时） | [A. 逐个添加技能](#a) |
| ChatGPT（希望注册为自己专用的插件时） | [B. 作为插件统一注册](#b) |
| Codex（在电脑上使用时） | [C. 复制文件夹](#c) |

**技能**是一项独立功能；**插件**则是包含四项技能的软件包。

## 2. 下载文件

文件位于[发布页面]({{release}})。点击链接即可下载 ZIP 文件。

**插件（包含四项技能）**

- {{plugin_link}}

**技能（单独下载）**

{{skills_list}}

## A. 向 ChatGPT 添加技能

适用于 ChatGPT 界面中有“Skills”和上传选项的情况。

1. 选择一个技能 ZIP 文件并上传。
2. 确认显示的内容后添加。
3. 根据需要的技能数量，重复相同步骤。

**注意事项**

- 此方式不能使用插件 ZIP，请使用技能 ZIP。
- 仅将文件附加到对话中，并不会将其添加为技能。
- 如果界面上找不到相关选项，可能是你的套餐或应用尚未提供该功能。请查看 [OpenAI 官方说明](https://learn.chatgpt.com/docs/build-skills)。

## B. 在 ChatGPT 中注册为插件

将四项技能合并，注册为自己专用的插件。

1. 在 ChatGPT 中打开新对话，选择 `@plugin-creator`。
2. 附加插件 ZIP 文件。
3. 输入类似下面的请求：

   > 请将这个软件包注册为我个人使用的私有插件，不要提交到公开目录。

4. 注册成功后，**{{display}}** 会显示在 Plugins 的“Personal”或“Created by me”中。
5. 根据需要进行安装，并在新对话中启用。

**注意事项**

- 插件可能会被注册到团队工作区。如果只想供自己使用，请在注册前确认保存位置。
- 根据套餐或工作区设置，此功能可能无法使用。详情请参阅 [Build plugins](https://learn.chatgpt.com/docs/build-plugins) 和 [Plugins](https://learn.chatgpt.com/docs/plugins)。
- 以此方式注册的插件仅限你的账户使用，不会出现在公开目录中。

## C. 将文件夹复制到 Codex

解压技能 ZIP 后，会得到 `{{first}}` 等文件夹。将该文件夹复制到 Codex 读取的位置。

| 使用范围 | 复制目标 |
| --- | --- |
| 仅在特定项目中使用 | 项目内的 `.agents/skills/` |
| 在所有项目中使用 | 主文件夹中的 `~/.agents/skills/` |

例如，要在项目中添加 `{{first}}`，请执行以下命令：

```sh
mkdir -p /path/to/your-project/.agents/skills
cp -R {{first}} /path/to/your-project/.agents/skills/
```

**注意事项**

- 请连同文件夹内的全部内容整体复制。只复制部分文件将无法正常运行。
- 如果已存在同名文件夹，请在覆盖前确认其内容。

## 3. 开始试用

安装完成后，打开新对话并调用技能。

| 工具 | 调用方式 |
| --- | --- |
| ChatGPT | 从 `@` 中选择 |
| Codex | 从 `$` 或 `/skills` 中选择 |

建议先用不会修改文件的请求进行测试：

> 我准备制作一份中文报告。请告诉我需要注意哪些要点。请不要修改任何文件。

## 检查文件是否完整（可选）

如果想确认下载的文件没有损坏，请使用 [SHA256SUMS.txt]({{sums}})。

将 SHA256SUMS.txt 放在与下载的 ZIP 文件相同的文件夹中，然后在终端中运行以下命令。如果环境中没有 `shasum`，请使用 Windows PowerShell 的 `Get-FileHash` 等工具核对 SHA-256。

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

如果下载文件所在的行显示 `OK`，即表示文件没有问题。

---

其他工具：[Claude]({{page_claude}}) · [Gemini]({{page_gemini}})

界面和提供条件可能会发生变化。最新信息请以各服务的官方说明为准（本页确认日期：2026 年 10 月 14 日）。
