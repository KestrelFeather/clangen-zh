# ClanGen 中文试玩版

版本：v0.13.4-zh.0.1.0-alpha.2。基于官方 v0.13.4。
维护者：KestrelFeather。非官方、免费、部分界面汉化的技术试玩版。

## 开始游戏

完整解压压缩包，然后运行 `ClanGenChinese.exe`。请保留同目录下的 `_internal` 文件夹。
无需安装 Python。默认使用简体中文，可在“设置与说明 → 语言”切换英文。
设置更改后点击“保存设置”。

## 本次修订

参照猫武士维基（warriors.huijiwiki.com）的大陆简体用词，修正“泼皮猫”“新鲜猎物堆”“月”“猫物表”“九命仪式”等界面译名，并调整部分上下文误译。具体来源与保留用词见源码中的 localization/TERMINOLOGY.zh-CN.md。

## 本版范围

已翻译主菜单、常规设置的主要选项、创建族群、核心导航、猫咪资料标签、巡逻操作和月度事件界面的主要文字。
猫名、剧情事件、思想、性格技能描述及部分次要界面仍为英文；它们按原版资源回退。
自动生成猫名的规则保持原版。可以在建族时输入中文族名。
英文事件继续使用英文代词；中文代词和名字系统将在后续版本单独适配。
译文为 AI 辅助初稿与界面检查结果，尚未经过独立人工语言审核。

## 存档和更新

本版本的打包存档目录为 `%LOCALAPPDATA%\KestrelFeather\ClanGenChinese`，与原版分开。
可从游戏内“打开数据目录”访问。不要覆盖原版存档；如需试用旧存档，请先备份再复制测试。
源码运行仍在源码目录保存数据。可通过 `CLANGEN_ZH_DATA_DIR` 环境变量指定独立数据目录。
本版本使用手动下载更新，不接入官方自动更新渠道。

## 已知限制

- 大部分叙事内容、猫名和若干次要界面尚未汉化。
- 图像中的英文标题和少量图片按钮保留原样。
- 中文输入法候选窗与所有全屏分辨率尚未做真实桌面操作验证。
- 尚未验证从不同历史版本导入旧存档；请使用副本。
- 这是 alpha 试玩版，不代表完整中文正式发行。

源码、更新和问题反馈：https://github.com/KestrelFeather/clangen-zh

## 致谢与许可证

原作者 just-some-cat；原项目由 SableSteel 和众多贡献者开发。
官方源码：https://github.com/ClanGenOfficial/clangen
代码许可证 MPL-2.0；sprites/art/icon 为 CC BY-NC 4.0。保留附带的 LICENSE.md。
中文字体为 Noto Sans CJK SC，SIL OFL 1.1，许可证在 resources/fonts/NotoSansCJK-LICENSE.txt。
对应版本源码见本仓库同名 tag。不要将本版本误认为官方出品。
