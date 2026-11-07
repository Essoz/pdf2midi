# PDF → MIDI / MuseScore

给合唱团和阿卡贝拉排练用的 AI agent 工作流：把 PDF 乐谱转成可编辑乐谱，逐小节对照精校，再按需导出 MIDI、总谱和分声部练习音频。

这里分享的是这次实际使用的 **[pdf-to-mscz skill](skills/pdf-to-mscz/SKILL.md)**，包含操作方法、精校要点和只读审计脚本。

```text
PDF → OMR 识别初稿 → MusicXML → MuseScore
    → 对照原谱精校 → 保存、重开、回读与排版检查
    → MSCZ / MusicXML / PDF / MIDI / 分声部音频
```

## 依赖

- **AI agent 与本地工具**：能读取文件、查看谱面并操作桌面应用；本次使用 Codex。所需模型、电脑控制接口和软件安装由使用者自行准备。
- **[MuseScore Studio](https://musescore.org/en)**：免费开源，负责编辑、播放及导出乐谱和音频。
- **一种能导出 MusicXML 的 OMR（光学乐谱识别）工具**：Halbestunde 只是其中一个选择，见下表。
- **PDF 查看／渲染工具**：如系统 PDF 查看器、Poppler 或 PyMuPDF，用于对照原谱和检查导出排版。
- **Python 3.9+（可选）**：仅运行附带的 `inspect_score.py` 时需要；该脚本只用标准库。各 OMR 引擎可能有自己的额外依赖。

| OMR 工具 | 费用与适用方式 |
|---|---|
| [Halbestunde / Sheet Music Scanner](https://www.musehub.com/app/sheet-music-scanner) | 本次实际使用。付费桌面应用，经 MuseHub 安装与授权，识别后导出 MusicXML。 |
| [Audiveris](https://github.com/Audiveris/audiveris) | 免费开源；可读取 PDF／扫描谱，提供桌面界面并导出 MusicXML。 |
| [homr](https://github.com/liebharc/homr) | 免费开源；将乐谱图片或 PDF 转为 MusicXML，需要配置 Python 环境及模型依赖。 |
| [oemer](https://github.com/BreezeWhite/oemer) | 免费开源；图片输入、MusicXML 输出，PDF 需先逐页渲染。原项目也推荐关注 homr。 |

这三个免费工具是候选替代，尚未在本次合唱谱案例中实测。更换 OMR 后，仍需核对声部、小节、歌词和连线；初稿能打开不代表内容正确。

**Halbestunde 买断优惠**：截至 **2026-11-03**，[MuseHub 官方页面](https://www.musehub.com/app/sheet-music-scanner)显示桌面版为一次性购买、非订阅，促销价 **US$24.99**，划线原价 **US$149.99**（约减 83%）。价格、地区税费和活动期限以购买时页面为准。

## 安装与使用

下载本仓库，将完整的 `skills/pdf-to-mscz/` 文件夹放入 Codex 的技能目录，使其结构为 `~/.codex/skills/pdf-to-mscz/SKILL.md`。已有同名技能时先保留备份；其他安装位置和说明见 [INSTALL.md](skills/pdf-to-mscz/INSTALL.md)。

然后把 PDF 交给 agent，例如：

> 请用 $pdf-to-mscz 将这份 SATB 合唱 PDF 转成 MuseScore 乐谱，并做全谱精校。用 Halbestunde 识别，保留未修改的初稿。导出 MSCZ、MusicXML、MIDI、总谱 PDF，以及四条分声部 MP3 和一条合唱 MP3。音色用钢琴，速度四分音符 = 100；所有音频从第1小节开始，保留开头休止，不带节拍器。速度只用于导出，不添加到谱面。

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
