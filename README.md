# PDF → MIDI / MuseScore

给合唱团和阿卡贝拉排练用的 AI agent 工作流：把 PDF 乐谱转成可编辑乐谱，逐小节对照精校，再按需导出 MIDI、总谱和分声部练习音频。

这里分享的是这次实际使用的 **[pdf-to-mscz skill](skills/pdf-to-mscz/SKILL.md)**，包含操作方法、精校要点和只读审计脚本。

```text
PDF → OMR 识别初稿 → MusicXML → MuseScore
    → 对照原谱精校 → 保存、重开、回读与排版检查
    → MSCZ / MusicXML / PDF / MIDI / 分声部音频
```

## 依赖

- **AI agent 与本地工具**：能读取文件、查看谱面，并能驱动所选工具的桌面界面或官方命令行。本次使用 Codex；需要安装识别工具时，agent 可以协助。
- **[MuseScore Studio](https://musescore.org/en)**：免费开源，负责编辑、播放及导出乐谱和音频。
- **一种能导出 MusicXML 的 OMR（光学乐谱识别）工具**：从 PDF 开始时先检查本地环境。缺少可用工具时，agent 会说明有哪些可装、各自费用和对这类谱的识别表现，等你选好再协助安装。初稿由所选引擎生成，agent 随后对照 PDF 精校。
- **PDF 查看／渲染工具**：如系统 PDF 查看器、Poppler 或 PyMuPDF，用于对照原谱和检查导出排版。
- **Python 3.9+（可选）**：附带的安装自检和结构审计脚本只用标准库。各 OMR 引擎可能有自己的额外依赖。

Audiveris、homr 和 oemer 均有免费开源方案。Halbestunde 是本项目在合唱谱上实际用过的付费选项。2026-11-08 核查时，MuseHub 美国区桌面版的一次性买断促销价为 US$24.99，划线价 US$149.99。各地售价以购买时为准。安装说明列出了各工具的配置成本、多声部和歌词等校对要点，以及实测范围。[工具选择与识别表现](skills/pdf-to-mscz/INSTALL.md#选择乐谱识别工具) · [MuseHub 官方价格](https://www.musehub.com/app/sheet-music-scanner)

## 安装与使用

下载本仓库，将完整的 `skills/pdf-to-mscz/` 文件夹放入 agent 的技能目录。Codex 的常用位置为 `~/.codex/skills/pdf-to-mscz/`。也可在新对话里请 agent 读取解压后的 `SKILL.md`。只复制主文件会遗漏操作参考和检查脚本。[安装方式与完整性自检](skills/pdf-to-mscz/INSTALL.md#安装后自检)

然后把 PDF 交给 agent，例如：

> 请用 $pdf-to-mscz 将这份 SATB 合唱 PDF 转成 MuseScore 乐谱，并做全谱精校。保留未修改的识别初稿。导出 MSCZ、MusicXML、MIDI、总谱 PDF，以及四条分声部 MP3 和一条合唱 MP3。音色用钢琴，速度四分音符 = 100；所有音频从第 1 小节开始，保留开头休止，不带节拍器。速度只用于导出，不添加到谱面。

也可指定 Audiveris 等替代引擎，或直接提供已有的 MusicXML，从校对阶段继续。默认做全谱精校；只想要初稿时明确说明。MIDI 和音频按请求导出。

附带脚本只做结构统计，不能执行 PDF 识别，也不能证明逐音准确：

```sh
python3 skills/pdf-to-mscz/scripts/inspect_score.py /path/to/score.mscz
```

完整流程要求对照原谱、实际保存后重新打开、回读内容，并检查导出 PDF 的每一页；源谱模糊或有歧义的地方会单独记录。

## 许可

© 2026 Yuxuan Jiang（[Essoz](https://github.com/Essoz)）

本仓库内容采用[知识共享 署名-非商业性使用-相同方式共享 4.0 国际许可协议（CC BY-NC-SA 4.0）](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans)，完整条款见 [LICENSE](LICENSE)。

- 可以：免费使用、复制、修改和分享
- 需要：注明出处（作者和本仓库链接）
- 不可以：用于商业目的，包括出售本 skill 或其改编版本，或把它用作收费产品、收费服务的一部分
- 改编后再分享，须采用相同的许可协议

如需商业使用，请联系作者获得授权。
