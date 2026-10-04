# v0.13.4-zh.0.1.0-alpha.2 验证记录

日期：2026-10-04。上游仍为 v0.13.4 / 0a283f660ef2cc866a0983a3cc38a6d5b82679cc。

本轮联网参照灰机 Wiki 大陆简体用词，修订 41 条已有字符串，补齐 4 条猫物表字符串；当前有 479 个含中文的字符串叶节点。来源、地区口径、保留的用词与游戏专有译法见 [TERMINOLOGY.zh-CN.md](TERMINOLOGY.zh-CN.md)。

- 20 项中文专项测试通过：键、插值、字体字符覆盖、语言切换、回退、复数、中文断行、缩放主题、独立存档目录。
- 真实 main.py 离屏集成流程通过：新建“晨光”族、资料、巡逻、推进一个月、保存和重载，保留 10 只猫的 ID 集合。
- 检查更新后的模式说明、资料月龄、月度事件、猫物表和物资下拉菜单截图；修正猫物表硬编码英文 AND，物资菜单使用符合原文 freshkill 的“新鲜猎物”。
- 完整运行 tools/build_chinese.ps1，使用锁定依赖与 Python 3.11.17，Windows x64 PyInstaller 构建成功。
- 最终 ZIP 通过 CRC 和无存档/日志检查；包内全部 zh JSON 与已审阅源码逐字节一致，版本元数据为 alpha.2。
- 从中文路径解压，在 PATH 不含 Python 的条件下以全新中文数据目录冷启动通过。
- 同一解压包载入 alpha.1 的“晨光”测试存档副本通过，族名、1 个月的族龄和 10 只猫均保留。该单例不代表验证了所有历史存档。

SHA-256：`3352ef95e9805fed01eab23c4a65a29bcd0ea7919082dc69eb9a2d2f3a89f881`。ZIP 大小：215614817 字节。

全部图形验证使用 SDL 离屏渲染；未声称实际输入法、所有全屏/缩放组合、长时间游戏或干净虚拟机测试通过。本轮是术语与上下文修订，剧情、猫名、毛色描述等仍有英文，亦不等于独立人工全量校对。

复现：按下方命令运行现有检查和构建脚本；本版集成检查增加猫物表与物资菜单截图。下方保留 alpha.1 的历史验证记录，不能将其中的测试数量误记为本轮重新运行的数量。

---

# v0.13.4-zh.0.1.0-alpha.1 验证记录

日期：2026-10-03。上游基线 v0.13.4 / 0a283f660ef2cc866a0983a3cc38a6d5b82679cc。

## 资源范围

新增 zh 语言目录：13 个显示文本文件、1 个代词文件及 config.json。
显示文本中有 475 个含中文的字符串叶节点（复数分支分别计数）；不是全游戏翻译完成率。
代词文件保留英文形式，保证未翻译的英文叙事仍可正常替换。

## 已完成验证

- 19 项中文专项检查：翻译键、插值参数、常用字符字体覆盖、语言切换、单复数、文件与字符串回退、中文断行、缩放主题和独立存档目录。
- 5 项上游语言/代词测试通过。
- 真实 main.py 初始化、真实屏幕和资源的 SDL 离屏集成运行，通过创建中文族群、猫咪资料、巡逻、推进月亮、保存、重新加载检查。
- 重新加载后的族群名为“晨光”，年龄为 1，10 只猫的 ID 集合一致。
- 对真实渲染生成的主菜单、模式选择、命名、资料、巡逻、事件、营地和语言设置截图进行视觉检查。
- PyInstaller Windows one-folder 构建完成；测试环境 PATH 仅含 Windows 目录，没有 Python。
- 打包程序在全新数据目录和中文测试存档目录各冷启动一次，均正常退出测试，显示 zh 语言且无读档错误。
- 最终 ZIP 已通过 CRC、必需资源和无存档/日志检查；从中文目录解压后，在中文数据目录、PATH 不含 Python 的条件下再次冷启动通过。
- 包内版本元数据的 upstream 为 KestrelFeather/clangen-zh，默认不检查更新，原版的自动更新入口也要求官方仓库身份。

## 验证边界

SDL 离屏渲染和直接调用屏幕事件处理器不等于真实鼠标、键盘和输入法操作测试。
中文输入法候选窗、所有桌面缩放/全屏组合、历史旧存档迁移和长时间游戏平衡尚未验证。
完整剧情、猫名及所有次要界面的中文覆盖尚未完成；译文没有独立人工语言审核。

## 复现

```powershell
uv sync --frozen --python 3.11 --group dev --group build
uv run --no-sync pytest tests/test_chinese_localization.py -q
uv run --no-sync python tools/smoke_chinese.py
powershell -ExecutionPolicy Bypass -File tools/build_chinese.ps1
```

源码集成测试输出默认位于 `.localization-work/screenshots`，每次使用独立测试数据目录。
冷启动诊断需同时设置 `CLANGEN_ZH_DATA_DIR`（隔离数据）、`CLANGEN_ZH_SMOKE_OUTPUT`（报告目录）和 `SDL_VIDEODRIVER=dummy`、`SDL_AUDIODRIVER=dummy`。
打包程序在绘制主界面 10 帧后写入 frozen-smoke.json 和 frozen-start.png 并退出；正常启动不启用此诊断。

fork Actions 暂时仍关闭。当前通过本地构建发布，不运行继承的官方 API / itch.io 发布任务。
