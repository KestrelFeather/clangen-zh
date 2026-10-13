# Fusion Pixel 中文像素字体

采用 TakWolf 的 Fusion Pixel Font 12px proportional zh-Hans，保持原始字体文件不变。

- 项目：https://github.com/TakWolf/fusion-pixel-font
- 固定发行版：https://github.com/TakWolf/fusion-pixel-font/releases/tag/2026.09.25
- 原始下载：fusion-pixel-font-12px-proportional-otf-v2026.09.25.zip
- 使用文件：fusion-pixel-12px-proportional-zh_hans.otf
- SHA-256：e84b6d1ab8f2e25084761eb61c88b373bf1fa0b0c5e9b559d5b1d90e4d658c86
- 获取日期：2026-10-13。

字体按 SIL Open Font License 1.1 分发。归档内的 OFL.txt 与全部上游字体许可证原样保存在 FusionPixel-licenses/，含 Ark Pixel、Cubic 11、Galmuri 的署名与许可。

## 游戏显示方式

从中文 alpha.3 开始，zh locale 默认使用此像素字体，替代旧的 Noto Sans CJK。中文界面中回退的英文文本使用该字体自带的拉丁字形，以保持同一页面的风格一致。切换为 en locale 后仍使用上游原有字体；图标按钮保留 clangen 图标字体。

中文字体关闭抗锯齿，仍随原有界面字号和缩放尺寸渲染。此字体只提供常规字重，因此粗体和斜体字形均映射到同一正体文件，不合成加粗或倾斜，以免糊住小字号汉字的笔画。标题的字号、位置及下划线仍保留。

它是与游戏风格接近的中文像素字体，不是上游 clangen 字体的汉字扩展。非整数缩放下，像素宽度可能不完全均匀；未保证每种桌面缩放都能严格对齐原生 12px 网格。新增翻译和自定义姓名仍应检查字形覆盖。
