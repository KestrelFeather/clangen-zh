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
