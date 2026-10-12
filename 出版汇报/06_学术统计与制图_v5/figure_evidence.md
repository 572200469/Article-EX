# 逐图证据、公式与边界

全部图：ppt_analysis_v5；研究者终审pending；SVG为字形路径以保留字体，PNG为360dpi。汉字使用微软雅黑，Latin/数字使用Times New Roman，白底蓝色。统计输出不加入任何新模型调用或元数据检索。

## Figure 1

来源：A_v4中work_category=confirmed_journal_article的533位置。按已确认ISSN-L归组；缺ISSN-L时仅用同一规范化名称与唯一已知ISSN-L对应，或保留有来源支持的规范化期刊名，不作模糊期刊名称合并。逐位置映射见figure1_journal_identity_map.csv。作品去重使用已审核canonical_work_id；另有三组source ID在确认DOI、规范化真作题名、完整作者、年、刊全部对应已有DOI ID时，仅在v5合并为analysis_work_id，证据见confirmed_work_id_aliases.csv。涉及Bakshy、Chan等Debunking、Ruggiero各一作。不按主题接近合并，不改v4原身份字段。

频次为推荐位置数；比例=期刊频次/533，Top3=前三期刊位置数/533；HHI=Σ(期刊位置频次/533)²。去重论文数按每期刊的不同analysis_work_id计数。另导出unique_jobs，重复推荐不是额外独立生成实验。当前源ID仍可能受数据库版本识别边界影响，不称为完成全体学术作品谱系去重。

普通期刊子样本有136个去重作品、57个期刊身份；Top3=42.78%，HHI=0.0735。不覆盖949总体中的325未唯一识别位置及其他载体。

## Figure 2

仅从已保存OpenAlex响应取数，无新查询。入组要求：与审核作品相同DOI/明确OpenAlex ID、规范化真实题名相似度≥.93、唯一OpenAlex ID、有非负整数cited_by_count及获取日期。多ID冲突或无快照者排除；不是用原模型的错误DOI查询结果替代真作。每个去重作品只保留最近获取的合格快照，快照获取日期与OpenAlex记录更新日期分别导出。

主图x=自然对数ln(1+累计被引量)，y=被推荐的不同job数；源表同时保留位置频次。Spearman为平均秩处理ties后的Pearson秩相关，不报p值或因果检验。主题层分经典、数字、跨主题互斥组；作品在多主题出现时主分析只计一次。年代层用确认发表年，不控制所有混杂，也不等于年龄标准化影响力。预先展示条件为n≥20且覆盖已确认去重期刊作品≥50%，不足则仅制覆盖图。

合格112/136作品（82.4%），覆盖461/533期刊位置。快照2026-10-11T09:09:24.499671+00:00至2026-10-12T12:25:30.284553+00:00。有选择性的已推荐作品，不具未入选参考总体，不能估计高被引作品入选概率；累计引文不是标准化影响力。

## Figure 3

A仅相同两主题neutral_zh，B/C为各自定向条件；原始raw_entry.title检出CJK统一汉字（不转换或替换题名）。比例=题名含汉字位置/本组实际位置。失败任务没有推荐，全null占位也不计推荐；成功回答数仍计真实API成功，包括未生成有效推荐的回答。A三重复、B/C一重复，不同采集时间；仅作描述性对照，不作配对因果或独立位置显著性检验。汉字表达不等于作品正文语言、数据库收录或出版归属。

| 组 | 计划/发送设计 | 成功回答 | 实际位置 | 含汉字题名 | 组内比例 |
| --- | --- | --- | --- | --- | --- |
| A | 24 | 23 | 114 | 0 | 0.0 |
| B | 8 | 6 | 25 | 25 | 1.0 |
| C | 8 | 6 | 25 | 15 | 0.6 |

## Figure 4

来源：已有directed_normalized_evidence.json的50实际位置；不重新匹配同主题参照。两组各25位置，C有10个真作位置，其中7制度地域有证据、3制度地域unknown；B有1个中文译载来源支持案例、24个身份未决。B的1在当前数据中标记mainland_independent，但涉及间接正式期刊引用与第三方原刊扫描，研究者终审未完成，虚线柱明确待终审，不能称已有严格最终验收。B研究者终审完成合格数为0是审核进度，不是证据性否定。

C文章级CJFQ确认0，25条均unknown；不声称任何一条“确认未收录”。figure4_BC_source_cases.csv保留原刊身份、制度归属、CNKI收录和证据限制。真作、地域、目标来源存在包含或交叉关系，不能堆叠相加。主图为并列独立指标。

## 方法附图

949=624+325；624=533+79+6+6，后者依次为普通期刊、非期刊、历史载体、真实作品但具体载体待定。每类同时标出对624和949的分母；未决比例325/949。192是计划任务数，190是成功回答数，949是推荐位置数；一次回答内位置不是独立实验重复。

## 来源可追溯文件

- `outputs/publication_visibility_final_figures/normalized_slots_v3.json`；SHA-256 `e8b4f3821df355a810b759ee921831aa16be58e5841913e910e4fa3733c1e3ee`
- `outputs/identity_review_v4_20261012/normalized_slots_v4_preview.json`；SHA-256 `7e21ec0d3914c169eb9e1f20b73b53caf0818b4f8f35dd13dff3a21162ac4be1`
- `outputs/identity_review_v4_20261012/slot_identity_evidence_v4.json`；SHA-256 `66553026fc46fd50df4e1ed1f59294562b03eb2154e0d924f10c2f12d7c35e2c`
- `outputs/publication_visibility_main_20261012/final_job_states.csv`；SHA-256 `02a04758f3aa04fd4569adab08da458c6fee5f58c31d91c2e7eaa747798dc712`
- `data/main_startup/main_candidate_v2_20261011/manifest.json`；SHA-256 `a6542406148be09476dd16a33f57e0428c57a4ed8f46023449c423e4b74f1bb5`
- `outputs/final_presentation_figures/directed_normalized_evidence.json`；SHA-256 `0c13c19649b51924dcd58e1dd74245905e0c73651323974139e4af5820bba350`
- `outputs/china_directed_20261012/technical_jobs.json`；SHA-256 `b0a819ddfbfbae439cc4267a3183878bffefb39e15a3b841fe2cc6d05df9a304`
- `data/china_directed_discovery_pilot/china_directed_16-9597931c4a07c93b/control/manifest.json`；SHA-256 `9a2e77acbea2fe2839de91b03a5ac9f452e5c1ace14673d6f56636cda34f5d03`
- `data/chinese_resource_supplement_20261012/directed_dry_run_v2/manifest.json`；SHA-256 `4c397f2002f1326a58d99e0b6dafc77895bc74087bd5a9fb67ab220e0ea7e215`
- `data/chinese_resource_supplement_20261012/positive_controls_full_evidence.json`；SHA-256 `c92e2baf1fabe93b51695c9d9861606d93469e57a606f057f034e1e3d7c37f1e`
