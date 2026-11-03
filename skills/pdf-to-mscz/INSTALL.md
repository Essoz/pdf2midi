# 安装与使用

这是可独立分享的 Codex 技能包。包含操作方法、精校要点和只读结构审计脚本；不包含任何用户乐谱、账号、商业软件或识别服务授权。

公开版整理：2026-11-03。默认执行“转换＋全谱精校＋实际 MSCZ 保存重开及回读＋最终 PDF 全页检查”。分享包与本地 skill 使用同一套流程，不依赖原作者的电脑路径、旧会话或某首歌的专用脚本。

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

## 所需环境

- 能导出 MusicXML 的 OMR 工具，任选一种。本次实际使用 [Halbestunde](https://www.musehub.com/app/sheet-music-scanner)（付费，通过 MuseHub 管理）；免费开源候选有 [Audiveris](https://github.com/Audiveris/audiveris)、[homr](https://github.com/liebharc/homr)、[oemer](https://github.com/BreezeWhite/oemer)。这些替代工具未在本次案例中实测；图片输入工具需先将 PDF 渲染成图片，各自安装和模型依赖以其官方说明为准。
- MuseScore Studio：用于导入 MusicXML、编辑、保存 MSCZ 与导出 PDF。
- 可操作这些应用的电脑控制接口。Codex 中可使用已连接的 computer-use 工具；技能本身不会提供该接口。
- Python 3.9+：仅运行附带审计助手时需要，无第三方 Python 包依赖。
- PDF 查看／渲染工具：用于源谱和最终排版检查。Poppler 是一种选择，不是唯一方案；矢量辅助分析可按需使用 pdfplumber 等工具。

没有电脑控制接口时，可由使用者按 `references/app-workflow.md` 完成导入导出，再让能读取本地文件的助手校对。其他支持本地指令文件的代理也可阅读 `SKILL.md`，但其安装与自动发现方式由该产品决定。

## 能力边界

附带脚本不能识别 PDF、不能自动证明音符正确，也不能替代 MuseScore。复杂记谱或低清扫描仍可能需要人工判读。技能不提供免费软件授权，不自动上传、公开或转发乐谱；使用者自行确认拥有所需的使用与分享权限。

分享时只发这个完整文件夹或其 ZIP。转换结果和私人任务材料应留在各自工作目录，不添加到技能包。
