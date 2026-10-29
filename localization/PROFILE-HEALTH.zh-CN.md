# 猫咪资料与健康信息：源码进度

核对日期：2026-10-29。适用于 `chinese-main` 本批源码；已发布的 Windows alpha.3 下载包不包含本批更新。本文中的数量是新增 i18n 字符串叶节点，复数形式分开计数，不能当作独立句数或整个游戏的完成率。

## 本批范围

| 内容 | 新增字符串叶节点 | 资源 |
|---|---:|---|
| 性格 | 55 | `cat/personality.zh.json` |
| 技能与经验等级 | 121 | `cat/skills.zh.json` |
| 眼睛颜色 | 22 | `cat/eyes.zh.json` |
| 毛色、花纹、毛长和外貌描述 | 92 | `cat/pelts.zh.json` |
| 饰品 | 213 | `cat/accessories.zh.json` |
| 身世介绍及分类 | 86 | `cat/backstories.zh.json` |
| 疾病名称 | 21 | `conditions/illnesses.zh.json` |
| 伤势名称 | 42 | `conditions/injuries.zh.json` |
| 永久状况及提示 | 29 | `conditions/permanent_conditions.zh.json` |
| 营养状态 | 6 | `conditions/nutrition.zh.json` |
| 草药与相关消息模板 | 54 | `conditions/herbs.zh.json` |
| 怀孕提示模板 | 11 | `conditions/pregnancy.zh.json` |
| 巫医巢穴界面及治疗日志模板 | 22 | `screens/med_den.zh.json` |
| 列表连接、标点等组合模板 | 15 | `utility.zh.json` |
| **合计** | **789** | **14 个新增语言资源文件** |

饰品中的 `Prairie fire` 尚未确认植物身份，保留英文名称并标明“花”；其三个数量形式也计在资源条数内。其他普通词汇为本 fork 的中文初译，不代表已经全部由用户人工定稿。

同时修正实际显示入口：

- 中文外貌按中文语序拼接，使用中文标点和列表连接词；英文配置不变。
- 巡逻队技能、性格以及资料页、巫医页的经验等级通过译文资源显示，内部枚举仍为原值。
- 身世页正确替换 `m_c` 和 `c_n`；公共事件替换器在中文环境下使用“某某族”，英文环境继续使用“某某Clan”。因此未译英文事件中的族名也可能以中文形式出现。
- 草药治疗日志翻译疾病名，并按语言处理英文冠词；伤病字典的键和治疗数值仍由原逻辑管理。
- 缩短巫医页页签和健康提示，避免 800×700 窗口中出现多余换行。
- 更新启动页范围说明，明确剧情仍未完整汉化、部分猫名仍为英文。

## 术语依据与未定项目

本次通过灰机 Wiki 的搜索索引正文核对中英对应，不声称取得该站全部最新修订。引用只用于术语核对；身世说明依照游戏英文自行翻译，没有复制 Wiki 叙述段落。

| 项目 | 本版用词 | 依据与限制 |
|---|---|---|
| whitecough / greencough / yellowcough / redcough | 白咳症 / 绿咳症 / 黄咳症 / 红咳症 | [伤病](https://warriors.huijiwiki.com/wiki/伤病)，搜索索引从“白咳症”重定向页读取。 |
| kittencough | 幼崽感冒 | 同上；遵照条目已有译名，没有按其他咳症机械拼成“幼崽咳症”。 |
| carrionplace disease | 垃圾场瘟疫 | [族群术语](https://warriors.huijiwiki.com/wiki/族群术语)使用该疾病名称；[地区转换表](https://warriors.huijiwiki.com/wiki/Module:CGroup/Basic)将 Carrionplace 的大陆用词列为“垃圾场”。 |
| catmint / horsetail / lungwort / ragwort / poppy | 猫薄荷 / 马尾草 / 疗肺草 / 千里光 / 罂粟籽 | [药物列表](https://warriors.huijiwiki.com/wiki/药物列表)。游戏原文未指定叶、果等部位时，不擅自增加。 |
| rose mallow | 芙蓉葵 | [Flora of China: Hibiscus moscheutos](https://efloras.org/florataxon.aspx?flora_id=2&taxon_id=200013710)提供植物名称参照，非猫武士角色定译。 |
| shock / lingering shock / recurring shock | 惊吓 / 惊魂未定 / 反复受惊 | 按游戏风险与恢复叙述作上下文暂译：涉及创伤、睡眠和压力反应，未统一套用“休克”。仍需在后续事件翻译中复核。 |
| Prairie fire（花饰） | Prairie fire 花 | **待确认**：现有证据不能确定游戏所指植物，未套用相近属种的中文名。 |
| betony / mullein / pickleweed / desert willow | 水苏 / 毛蕊花 / 盐角草 / 沙漠柳 | **本项目暂译**，本次未取得足够的灰机中英对照，不标成小说定译；后续可按图像和具体物种细化。 |

角色名前后缀仍由独立流程维护，见 [NAME-AFFIXES.zh-CN.md](NAME-AFFIXES.zh-CN.md)。本批没有修改待填名字工作簿，也没有把未经确认的角色名加入运行时映射。

## 验证

- 中文资源、占位符、字体覆盖、名字显示及语言/代词回归测试合计 86 项通过。
- 新测试检查长毛/伤痕/花纹/缺尾的组合描述，中英文列表语法切换，身世猫名/族名替换，疾病、伤势及永久状况三类治疗日志，以及内部伤病键保留。
- 真实游戏使用隔离测试目录运行：新建“晨光”族 → 猫咪资料 → 巡逻 → 推进一个月 → 保存并重新读取，核对全部原始名字前后缀未改变。
- 继续创建测试伤病，打开身世、健康、巫医巢穴和治疗日志页；共输出 21 张离屏截图。人工检查资料、健康、身世、巫医页及治疗日志截图，未见这些新增标签溢出或缺字。
- 此次是源码与离屏窗口验证，没有重新构建 Windows 包，也没有覆盖所有缩放、全屏、输入法或旧存档组合。

复现命令（在源码根目录，以已有依赖环境运行）：

```powershell
$env:PYTHONIOENCODING='utf-8'
$env:SDL_VIDEODRIVER='dummy'
$env:SDL_AUDIODRIVER='dummy'
python -m pytest tests/test_chinese_localization.py tests/test_name_localization.py tests/test_chinese_profile_health.py tests/test_lang.py tests/test_pronouns.py -q
python tools/smoke_chinese.py
```

## 仍待推进

- 生平中的训练、毕业、死亡、伤疤等叙述，以及来世接受/拒绝文本；本批仅翻译身世介绍。
- 巫医页的随机草药库存评论、完整伤病事件与生产事件；这些与本批名称、短模板是不同资源。
- 关系、伴侣、导师、收养、职位、调解、族群设置等管理界面。
- 巡逻故事、月度事件、想法及其他大段叙事。
- 用户待填的名字前后缀。未知名称继续按已有规则回退英文。

下一批优先补管理界面及相邻短文本，再分模块处理剧情。下载包的覆盖说明随下一次实际构建发布更新。
