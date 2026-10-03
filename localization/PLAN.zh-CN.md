# ClanGen 中文版本维护计划

本项目由 KestrelFeather 独立维护，基于 ClanGenOfficial/clangen，属于非官方中文版本。
首阶段为简体中文、Windows x64、免费发布。首个界面试玩版为 `v0.13.4-zh.0.1.0-alpha.1`；覆盖范围、操作说明及已知限制见 [PREVIEW.zh-CN.md](PREVIEW.zh-CN.md)，验证证据见 [VALIDATION.zh-CN.md](VALIDATION.zh-CN.md)。

## 基线和分支

- 首版固定上游 v0.13.4，完整提交见 `upstream.json`。
- `chinese-main` 是中文版本主分支；上游 `development` 仅用于参考。
- 本地 `upstream` 指向官方，`origin` 指向中文 fork。
- 后续升级在独立分支进行，比较资源差异并运行回归检查，通过后再合入。
- 当前本地为浅克隆；需要分析完整历史或合并跨版本历史时先获取所需历史。
- 中文版本问题在本 fork 处理。保留原作者署名、许可证和原项目链接。

## 已核实的工程入口

| 内容 | 文件/位置 | 含义 |
|---|---|---|
| 语言资源 | resources/lang/en | 包含 i18n 字符串及混有逻辑数据的事件 JSON |
| 语言按钮 | resources/lang/additional_lang_list.json、scripts/screens/SettingsScreen.py | 语言列表与界面入口 |
| 资源加载 | scripts/game_structure/localization.py | 原始资源缺文件时回退，不是逐键合并 |
| 语言配置 | resources/lang/en/config.json、pronouns.en.json | 语法、代词和外貌描述组合 |
| 字体注册 | scripts/game_structure/screen_settings.py | 注册 notosans、notocjk 与 clangen 字体 |
| 字体和界面主题 | resources/fonts、resources/theme/master_screen_scale.json | 中文字体、粗体、图标及行高要一起验证 |
| 事件替换 | scripts/events_module/text_adjust.py | 猫名、族名、代词、动词等标签 |
| 数据目录 | scripts/housekeeping/datadir.py | 源码运行用当前目录；打包版用 KestrelFeather/ClanGenChinese 独立目录 |
| 更新检查 | scripts/screens/StartScreen.py | 包含 upstream 仓库身份检查；fork 的 version.ini 必须写对 |
| 构建发布 | .github/workflows/build.yml | 包含官方更新 API、itch.io 和 GitHub Release 发布步骤，需改造 |

## M0：项目初始化

- [x] 固定稳定版基线并建立中文主分支。
- [x] 提供标准库文本盘点工具，可比较原文新增、修改和删除。
- [x] 写明非官方身份、当前覆盖和验证状态。
- [ ] 建立仅服务本 fork 的 CI，再恢复 fork Actions。

## M1：中文显示和运行小样

首批字体、语言资源、中文断行和核心流程已实现，并完成 19 项专项测试、5 项上游语言/代词测试、实际游戏离屏集成流程及 Windows 打包冷启动。输入法候选窗、所有缩放/全屏组合和旧存档迁移仍待人工桌面验证；不能据此宣称完整游戏已汉化或全面测试。


1. 接入具有再分发许可的中文字体，携带许可证；检查图标字符和粗体回退。
2. 建立简体中文 locale、语言配置和设置入口。资源保留英语回退。
3. 翻译主菜单、设置、建族和猫咪资料的首批文本；界面之外保留英文并明确覆盖范围。
4. 先在 Windows 上验证中文显示、长段落换行、不同缩放、中文输入及语言切换。
5. 完成“新建族群 → 猫咪资料 → 一次巡逻 → 推进月亮 → 保存并重启读取”。
6. 确认代词、名称和历史文本在切换语言及读档后正确。

交付：`v0.13.4-zh.0.1.0-alpha.1` Windows x64 预发行试玩包。构建入口为 `tools/build_chinese.ps1`，集成验证入口为 `tools/smoke_chinese.py`。后续版本沿用先验证、再创建 tag / Release 的流程。

## M2：译文规范与批量扩充

- 建立术语表：原词、建议译名、上下文、采用的译名体系、审核状态。
- 待定事项：中文出版版本口径、猫咪代词规则、名字前后缀及晋升改名规则。
- 不直接导入已有社区译文；复用前核实其来源、版本、许可和质量。
- 先翻译可见字符串，保留 ID、JSON 键、标签、概率、条件和存档字段。
- 保护 `%{...}`、猫名代号和 HTML 标记；语法标签按解析器规则处理。
- 事件文件用事件 ID 加字段路径维护译文映射；通用盘点中的数组下标只是定位信息。
- 机器生成初稿单独标记，人工审核后才计入审核完成率。
- 完成率分界面、巡逻、月度事件、思想、条件等模块计算，排除内部标识与配置。

## M3：首个公开试玩版本

首版采用本地独立构建后上传 GitHub pre-release，提供 ZIP、SHA-256 和试玩说明。继承的 Actions 仍关闭；独立自动构建 CI 与自动更新是后续任务。


- 使用独立打包存档目录，提供明确的旧存档复制/迁移说明。
- `version.ini` 标记 KestrelFeather/clangen-zh；验证不会检查或安装官方更新。
- 替换中文版本问题反馈入口，保留原作者的署名和社区链接并标清用途。
- 将原有自动发布步骤改成自己的 GitHub Release 构建；不使用官方 API、密钥或 itch.io 目标。
- 初期手动下载更新。自动更新单列后续任务。
- Windows 构建必须在没有 Python 的环境下冷启动；检查字体/语言文件是否打包、路径含中文是否可用。
- Release 附版本/上游 commit、覆盖范围、已知问题、存档说明、源码链接、许可证和 SHA-256。
- 中文覆盖和游戏验证通过后，先以 pre-release 发布试玩版。

## 盘点工具

在源码根目录执行：

```powershell
python tools/localization_inventory.py --output .localization-work/inventory.json
python tools/localization_inventory.py --baseline .localization-work/inventory.json --output .localization-work/inventory-next.json
```

工具只使用 Python 标准库，不启动游戏，也不会修改语言资源。
报告统计 `resources/lang/en` 的全部 JSON 字符串值，包含 ID、标签、配置和重复文本，不能作为待翻译句数或完成率。
报告不覆盖代码硬编码文本、图片内文字、目录外的命名等资源，后续需要补充专项扫描。
JSON Pointer 中 `/` 和 `~` 使用标准转义；每条保留来源、原文和 SHA-256。
数组顺序变化可能产生大量差异，需要人工结合事件 ID 复核，不可自动覆盖译文。

## 许可与来源

上游 `LICENSE.md` 将代码标为 MPL-2.0，将 sprites/art/icon 标为 CC BY-NC 4.0。
发布时保留许可证、署名和对应源码获取方式；包含上游美术的版本按非商业用途维护。
新增字体也必须携带自身许可证。所有具体材料以其原许可说明为准。
原项目的贡献接收政策与本 fork 的维护流程分开；不要将本 fork 的 AI 辅助成果提交给禁止此类贡献的上游。
