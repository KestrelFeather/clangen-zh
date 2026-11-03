# 地形伤病事件：第一批中文叙事

日期：2026-11-03。基于上游 v0.13.4。本批是 alpha.5 发布后的源码更新，尚未包含在 alpha.5 Windows 下载包中。

## 覆盖范围

| 文件（resources/lang/zh/events/injury/） | 事件数 |
|---|---:|
| forest.json | 12 |
| beach.json | 18 |
| mountainous.json | 3 |
| plains.json | 6 |
| wetlands.json | 4 |
| 合计 | 43 |

翻译显示字段共 95 处：43 条事件正文、15 条伤痕历史、23 条死亡历史、14 条关系日志。重复原句在不同事件中的出现分别计数；这不是全游戏完成率，也不代表所有这些历史一定在一次游戏里出现。

五个文件均完整保留上游事件条目及顺序；只改 event_text、history 中的显示文字和 relationships.log。事件 ID、频率、地形/营地、季节、年龄/职位/性格/技能条件、伤病/伤疤 ID、关系方向和数值均保留原样。沙漠、通用伤病事件、死亡事件、外交、灾难等未翻译资源继续走 alpha.5 的英文回退。

## 译文口径

- 沿用 [术语表](TERMINOLOGY.zh-CN.md) 的大陆简体用词。2026-11-03 再次联网核对灰机 Wiki 的索引文本：[地区用词转换表](https://warriors.huijiwiki.com/wiki/Module:CGroup/Basic)中的“育婴室”“巫医巢穴”，以及[时间轴/生卒](https://warriors.huijiwiki.com/wiki/时间轴/生卒)中的“绿叶季”。没有导入 Wiki 叙事段落。
- 中文句子按中文语法改写，省略英文代词和动词变位标签，保留对应猫物、族名引用。未确认的猫名仍整体回退英文，本批不增加待确认名字的映射。
- 红色浆果、天蓝色蘑菇按原文描述，不擅自认定具体有毒物种。保留原文森林火灾、营地火灾之间的历史措辞差异，不改事件规则来迁就译文。
- 译文为 AI 辅助初稿，已进行原文对照和游戏显示检查，尚未经过独立人工语言审核。

## 验证

- `tests/test_chinese_injury_events.py` 深度比较全部逻辑字段；检查 95 处文本的猫物引用、标记、实际替换结果和 Fusion Pixel 字形覆盖。五种地形的事件对象分别验证中文 → 英文 → 中文切换。
- `tests/test_event_locale_fallback.py` 将短事件文件置于只有英文资源的临时目录，主动触发缺失中文文件的回退。新增译文不会让缺文件测试失去覆盖。
- 定向检查 49 项通过。完整中英文套件结果另见 [验证记录](VALIDATION.zh-CN.md)。
- `tools/smoke_injury_events.py` 在 `smoke_chinese.py` 创建的隔离族群中，定向执行 8 个事件，覆盖五种地形、救援、双方同时受伤、敌方族名、关系日志、伤病及待生效历史的保存重读。定向执行用于检查事件后果，不冒充随机筛选覆盖。
- 已检查 800×700 真实事件页的离屏截图：像素字形、中文断行和已显示区域无截断；保存重读后中文事件列表与伤病历史保持。没有据此宣称全部分辨率或最终打包程序验证完成。

复现集成检查（数据与正式存档隔离）：

```powershell
$env:CLANGEN_ZH_TEST_INJURY_EVENTS = '1'
$env:CLANGEN_ZH_TEST_OUTPUT = '.localization-work/injury-smoke'
.venv/Scripts/python.exe tools/smoke_chinese.py
```

下一批优先处理通用伤病事件，再补沙漠地形；这两部分仍是当前伤病叙事的主要英文来源。
