# ClanGen 中文版（非官方，筹备中）

这是 [KestrelFeather/clangen-zh](https://github.com/KestrelFeather/clangen-zh) 独立维护的中文本地化项目，基于 [ClanGenOfficial/clangen](https://github.com/ClanGenOfficial/clangen)。

**当前状态：仓库初始化和文本盘点已完成，尚未提供可玩的中文发行包。当前游戏内容仍为上游英文版本。**

- 基线：上游 `v0.13.4`，commit `0a283f660ef2cc866a0983a3cc38a6d5b82679cc`。
- 开发主分支：`chinese-main`。
- 初期目标：简体中文、Windows x64、免费非官方试玩版。
- 下一里程碑：中文字体和语言加载，以及主菜单到保存读档的核心流程。
- [维护与发布计划](localization/PLAN.zh-CN.md) · [资源盘点](localization/INVENTORY.zh-CN.md) · [版本记录](localization/upstream.json)。
- 本 fork 的汉化问题请在[本仓库 Issues](https://github.com/KestrelFeather/clangen-zh/issues)反馈。

原作者为 just-some-cat；原项目由 SableSteel 及众多贡献者开发。保留上游许可证和署名。代码采用 MPL-2.0，sprites/art/icon 采用 CC BY-NC 4.0，详见 [LICENSE.md](LICENSE.md)。本项目不代表官方，包含上游美术的发行版按非商业用途维护。

本 fork 可以使用 AI 辅助开发和翻译，但必须明确审核与验证状态。下面保留的上游 AI 贡献政策适用于向上游提交内容，不作为本 fork 的贡献政策。

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
