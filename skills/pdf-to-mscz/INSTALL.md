# 安装与使用

这是可独立分享的 Codex 技能包。包含操作方法、精校要点和只读结构审计脚本；不包含任何用户乐谱、账号、商业软件或识别服务授权。

分享包与本地 skill 使用同一套流程。默认执行转换、全谱精校、MSCZ 保存重开及回读、最终 PDF 全页检查。

## 安装到 Codex

解压后，把完整的 `pdf-to-mscz` 文件夹放到 Codex 的用户技能目录：

- 默认是用户主目录下的 `.codex/skills/`。
- 若自行设置了 `CODEX_HOME`，使用该目录下的 `skills/`。
- 最终结构应是 `skills/pdf-to-mscz/SKILL.md`，不要多嵌套一层同名目录。

让 Codex 刷新技能；若当前会话尚未发现它，重新打开会话／应用后再尝试。可显式输入：

> 请用 $pdf-to-mscz 把这份 PDF 乐谱转换成 MSCZ。

这句话已默认包含完整精校，不需要再补一句“精校”。只有明确要求初稿或不精校，才按基础转换执行；单纯说“快点”不表示跳过校对。

仅要初步转换时：

> 请用 $pdf-to-mscz 转换这份谱，只做基础校验，标明未精校部分。

若有必须使用的工具或方式，连同请求写清，例如“通过 computer use 使用 Halbestunde 和 MuseScore”。

千问或其他 agent 使用其产品实际支持的技能目录。也可把完整包解压到可读的工作目录，在新对话中请 agent 打开其中的 `pdf-to-mscz/SKILL.md` 并执行。安装位置和自动发现方式由各产品决定。

## 安装后自检

在解压或安装后的 `pdf-to-mscz` 文件夹里运行下列命令。Windows 可将 `python3` 换成 `py -3`；也可让 agent 按清单核对。

```sh
python3 scripts/check_install.py
```

完整包的顶层有 `SKILL.md`、`INSTALL.md`、`LICENSE`，子目录中有以下文件：

```text
agents/openai.yaml
references/app-workflow.md
references/native-mscz.md
references/proofreading.md
scripts/check_install.py
scripts/inspect_score.py
```

自检列出缺失或为空的文件。若自检脚本本身也缺失，重新解压完整包，保留目录结构；也可从[仓库的技能目录](https://github.com/Essoz/pdf2midi/tree/main/skills/pdf-to-mscz)补齐。

## 选择乐谱识别工具

只有 PDF 且本机缺少可用 OMR 时，向用户展示适合其系统的选项，问“想装哪一个？我可以帮你装。”下表列出软件费用、配置成本和可能影响校对时间的识别特点。已有合适的引擎可直接使用；用户已指定工具时先处理该工具。

| 工具 | 软件费和配置成本 | 对初稿质量已知的情况 |
|---|---|---|
| Audiveris | 免费开源。Windows、macOS、Linux 有本地安装方式，可用图形界面或批处理。 | 面向印刷五线谱。官方记录了同一谱表上相向符干被合并、音符漏识的情况。多声部挤在一行时要预留核对时间。[官方手册](https://audiveris.github.io/audiveris/_pages/handbook/) · [已知限制](https://audiveris.github.io/audiveris/_pages/reference/limitations/) |
| Halbestunde / Sheet Music Scanner | Windows、macOS，通过 MuseHub 安装和授权。2026-11-08 核查美国区桌面版为一次性买断，促销 US$24.99，划线价 US$149.99。 | 本项目用它处理过 11 页 SATB《哈利路亚》。初稿把连续的 4 个声部拆成了 8 个 part，多出一个空小节，校对时还修了时值与连线。这是一份谱的经历，不能推出跨工具的准确率排名。[MuseHub 官方售价与平台](https://www.musehub.com/app/sheet-music-scanner) |
| homr | 免费开源。需配置 Python、运行环境和模型，支持 CPU。 | 支持 PDF 和乐谱图片。项目列出八度谱号识别限制，遇到男高音常用的下八度高音谱号，须核对是否整段偏八度。[安装与输入要求](https://github.com/liebharc/homr) · [符号支持表](https://github.com/liebharc/homr/blob/main/IDEAS_FOR_CONTRIBUTORS.md#support-more-symbols) |
| oemer | 免费开源。需 Python 和模型权重，输入是图片，PDF 需先逐页渲染。 | 项目针对印刷西方记谱和拍照图像，手写谱效果有限。本项目未测过它处理合唱歌词或多声部的表现。[项目说明](https://github.com/BreezeWhite/oemer) |

向用户报价时核对其地区的官方页面，写明币种、是否买断及日期。只能看到外区价格或无法联网时，将其标为有日期的参考价，并给官方入口。上述三个免费引擎均未用本项目的同一份合唱谱做横评。引用准确率时须给出谱型、指标、样本和来源；缺少这些信息时，说明已知易错处和仍需校对的工作。用户关心实际成本时，可在选定引擎后用原谱中有代表性的一页试识，分别记录错音、节奏、歌词对位以及校对耗时，供用户判断。

用户选定后，按该系统的官方说明协助安装这一款及必要依赖。需要系统或桌面权限时，在对应步骤主动请求。装好后实际启动或检查官方命令入口，用所选工具导出并读回原始 MusicXML，再接续精校。若用户希望自己导出，只需请其提供这份 MusicXML 和对应原谱。

## 所需环境

- 从 PDF 开始时，使用一种能导出 MusicXML 的 OMR。已有对应的 MusicXML 或 MSCZ 可直接进入后续步骤。
- MuseScore Studio：用于导入 MusicXML、编辑、保存 MSCZ 与导出 PDF。
- 选择桌面操作时需要可用的电脑控制接口。所选工具支持官方命令行且用户允许时，也可采用该方式。
- Python 3.9+：用于可选的安装自检和结构审计脚本，两者均只用标准库。
- PDF 查看／渲染工具：用于源谱和最终排版检查。Poppler 是一种选择，不是唯一方案；矢量辅助分析可按需使用 pdfplumber 等工具。

没有电脑控制接口时，可由使用者按 [应用流程](references/app-workflow.md) 完成桌面应用的导入导出，再让能读取文件和查看谱面的助手校对。

## 能力边界

附带脚本不能识别 PDF、不能自动证明音符正确，也不能替代 MuseScore。复杂记谱或低清扫描仍可能需要人工判读。技能不提供免费软件授权，不自动上传、公开或转发乐谱；使用者自行确认拥有所需的使用与分享权限。

分享时发送完整文件夹或其压缩包。转换结果和私人任务材料留在各自工作目录。

© 2026 Yuxuan Jiang（Essoz）。本包采用 CC BY-NC-SA 4.0，详见随附的 [LICENSE](LICENSE) 和[原项目](https://github.com/Essoz/pdf2midi)。
