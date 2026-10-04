# ClanGen 中文版（非官方）

这是 [KestrelFeather/clangen-zh](https://github.com/KestrelFeather/clangen-zh) 独立维护的简体中文本地化项目，基于 [ClanGenOfficial/clangen](https://github.com/ClanGenOfficial/clangen)。

**当前 Windows x64 界面试玩版：`v0.13.4-zh.0.1.0-alpha.2`。这是部分汉化的 alpha，剧情事件、自动猫名和部分次要界面仍为英文。**

[下载中文试玩版](https://github.com/KestrelFeather/clangen-zh/releases/tag/v0.13.4-zh.0.1.0-alpha.2) · [试玩说明](localization/PREVIEW.zh-CN.md) · [术语依据](localization/TERMINOLOGY.zh-CN.md) · [验证记录](localization/VALIDATION.zh-CN.md)

完整解压 Windows ZIP 后运行 `ClanGenChinese.exe`，无需安装 Python。请保留 `_internal` 文件夹。默认简体中文，可在设置中切换英文。存档与原版分开，初期通过手动下载更新。

- 已接入中文常规/粗体字体和中文换行；翻译了主菜单、主要设置、创建族群、核心导航、资料标签、巡逻操作与月度事件界面的首批文字。
- 新增 479 个含中文的字符串值（复数分支分别计数），不是全游戏汉化完成率。译文为 AI 辅助初稿，尚无独立人工语言审核。
- 基线：上游 `v0.13.4`，commit `0a283f660ef2cc866a0983a3cc38a6d5b82679cc`；主分支 `chinese-main`。
- 通过中文专项测试、上游语言/代词测试、真实游戏离屏新建/巡逻/存读档流程和打包程序冷启动检查；真实输入法和全部全屏组合尚未验证。
- [维护与发布计划](localization/PLAN.zh-CN.md) · [初始资源盘点](localization/INVENTORY.zh-CN.md) · [版本记录](localization/upstream.json)。
- 汉化问题请在[本仓库 Issues](https://github.com/KestrelFeather/clangen-zh/issues)反馈。

源码运行：`uv sync --frozen --python 3.11 --group dev --group build`，然后 `uv run --no-sync python main.py`。Windows 构建：`powershell -ExecutionPolicy Bypass -File tools/build_chinese.ps1`。验证步骤和边界见上方验证记录。fork Actions 暂时关闭，当前本地构建发布，后续再接入独立 CI。

原作者为 just-some-cat；原项目由 SableSteel 及众多贡献者开发。保留上游许可证和署名。代码采用 MPL-2.0，sprites/art/icon 采用 CC BY-NC 4.0，详见 [LICENSE.md](LICENSE.md)。本项目不代表官方，包含上游美术的发行版按非商业用途维护。中文字体 Noto Sans CJK SC 按 SIL OFL 1.1 分发，见 [字体来源与许可](resources/fonts/NotoSansCJK-SOURCE.md)。

本 fork 使用 AI 辅助开发和翻译，并明确审核与验证状态。下面保留的上游 AI 贡献政策适用于向上游提交内容，不作为本 fork 的贡献政策。下方上游下载链接提供的是原版；中文试玩版请使用本页顶部链接。

---

# 上游 README（保留来源信息）

## On AI & LLMs

> [!WARNING]
> Issues and Pull Requests created with AI based tools are going to be closed without further comment.
> Repeat offenders will be blocked from this project until further notice.

### [Discord Server](https://discord.gg/clangen) || [Official website](https://clangen.io) || [Itch.io Page](https://sablesteel.itch.io/clan-gen-fan-edit) 

## Description
Fan-edit of the warrior cat clangen game built using Python and Pygame.

## Credits
Original creator: just-some-cat.tumblr.com

Fan-edit creator: SableSteel, and many others

## Downloads
### Stable
Stable versions can be downloaded directly from the [official ClanGen website](https://clangen.io/download)

### Development
**Note**: Development versions are automatic snapshots of current development efforts. They are _not_ stable, can crash and even corrupt your save files.
Additionally, we do not provide tech support for development versions.

Download at your own risk here: [ClanGen development download](https://clangen.io/download-development)

## Running from source
> [!WARNING]
> Running the game via poetry is no longer supported. Please use uv instead.

ClanGen uses uv to manage virtual environments. Therefore it is required to install the dependencies and run the game from source without manual tweaking.

### Installing python
> [!NOTE] 
> You no longer need to install Python on your system. uv will automatically install the correct version for you.

### Installing uv
Follow the instructions for installing uv from the official website: https://docs.astral.sh/uv/getting-started/installation/

#### Linux, macOS, WSL
Open a terminal and paste this:
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```
Then restart your terminal and check if uv is installed by running `uv --version`

#### Windows (Powershell)
Open a PowerShell window (Windows key and then enter `PowerShell`) and paste this:
```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
Then restart your terminal and check if uv is installed by running `uv --version`

### Running the game via the helper scripts
#### Linux, macOS
Double click the `run.sh` script or open it in the terminal via `./run.sh` with the current working directory set to the game's root directory.

#### Windows
Double click the `run.bat` script.

### Running the game via Visual Studio Code
> [!NOTE] 
> uv automatically creates the .venv folder in the root directory of the game, unlike poetry.

First, you need to let uv install the dependencies. To do so, run the following command in the terminal:
```
uv sync
```

After that, ensure that you have the Python extension installed in Visual Studio Code. You can install it from the Extensions tab on the left sidebar. [(or click here)
](https://marketplace.visualstudio.com/items?itemName=ms-python.python)

Then, open the Command Palette (Ctrl+Shift+P) and search for `Python: Select Interpreter`. Select the virtual environment created by uv (it should mention a `.venv` somewhere).

Finally, open the `main.py` file and click the play button in the top right corner to run the game.


## Bug Reporting
We have migrated to GitHub Issues for bug reporting and tracking. We no longer review bug reports from the retired Google Form.

## Contributing
If you'd like to contribute to Clangen, please read our [Contributing guide](https://github.com/ClanGenOfficial/clangen/blob/development/CONTRIBUTING.md).
