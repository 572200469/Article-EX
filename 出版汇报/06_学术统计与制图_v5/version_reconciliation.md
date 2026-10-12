# 数据版本核对与分析版本选择

分析版本统一为ppt_analysis_v5：A采用v4身份审核预览；B/C采用已有逐条来源证据；24篇参照独立保留。各图只使用这一版本锁定的表，不混用发布包v3与项目v4。所有研究者终审仍pending，不能写成已完成最终人工终审。

| A推荐位置类别 | 项目/发布包v3 | v4→本次v5 | 变化 |
| --- | --- | --- | --- |
| confirmed_journal_article | 510 | 533 | 23 |
| confirmed_nonjournal_work | 41 | 79 | 38 |
| historical_carrier_pending | 0 | 6 | 6 |
| carrier_unresolved | 0 | 6 | 6 |
| unidentified_work | 398 | 325 | -73 |

v3识别551/949（58.1%），v4识别624/949（65.8%），增加73位置、7.69个百分点。其中新增普通期刊23、非期刊38、特殊历史载体6、具体载体待定6。未唯一识别325 = 324 unresolved + 1 composite；不是325条已证实虚构。原949推荐、排序及190成功回答不变。

B/C仍为16发送、12成功、50实际位置；成功包括返回空占位的技术成功，不把全null占位计为实际推荐。原已公布汇报包未被修改，GitHub未自动推送新版。来源SHA及发布包比较见data/source_version_manifest.json。

v5补充作品ID归一化：三组source ID与已有DOI ID在确认DOI、真实题名、作者、年及刊均对应时，在派生analysis_work_id中合并。普通期刊子样本的139个原来源ID对应136个去重作品；合格引文作品由未消除ID重复时的115个变为112个，Spearman全部按最终112作品复算。不修改v4 canonical_work_id，不改变624真作位置或533期刊位置，见confirmed_work_id_aliases.csv。
