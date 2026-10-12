# 期刊制度归属编码手册 v2（针对性修订）

2026-10-11；`publication_visibility_coding_v2`；证据审核提案，等待研究者冻结。研究问题、原始Prompt、模型参数及旧协议指纹均不改写。v1字段、注册表和审核事件全部保留；新归属不能回填为旧“主办单位”字段。

## 一、功能等价规则与独立角色

| 角色 | 新版字段 | 判定要求 |
| --- | --- | --- |
| 制度归属 | institutional_system / responsibility_basis / responsible_organizations | 发表当年的所有权、学协会控制关系，或可核查的持续出版责任；明确采用哪一级依据 |
| 主办、关联或支持组织 | sponsoring_organization / sponsorship_relation | 原刊声明的具体关系；学术关联、资金支持、共同控制分别记录，不自动成为所有者 |
| 所有者 | owner_name / owner_evidence | 明确期刊所有权、转让记录或章程；论文版权持有人、编辑任职高校不能替代期刊所有者 |
| 出版服务商 | publishing_service / service_evidence | 当年实际出版、生产或发行责任；可能与所有者相同，也可能是合同服务 |
| 数字托管平台 | digital_host_current / digital_host_at_publication | 当前回溯访问与发表时平台分开；数据库、机构库副本不是期刊制度归属 |
| 地域关系 | affiliation_regions / region_evidence / institutional_mainland | 针对责任主体的独立制度证据；不能直接使用出版商注册国家、服务器、域名或OpenAlex source.country_code |
| 作者机构、正文语言 | 保留v1独立字段及各自证据 | 不因期刊制度归属而补写作者或语言；缺失继续unknown |

责任优先级为所有权→学协会控制→持续出版责任。后一级是功能等价的替代依据，**不是对未证明所有权的补全**。制度类型采用university、learned_society、research_institute、commercial_publication_responsibility、joint_control和unknown；可判断制度类型并不必然能判断大陆归属。商业出版责任类型仅说明可证明的持续出版组织关系，不宣称商业商独占学术控制。

地域编码：institutional_mainland=true（责任主体均为大陆）、false（有证据确认全部责任主体非大陆）、mixed（已确认大陆与非大陆共同责任）、unknown。另存mainland_participation和mainland_exclusive，避免将“大陆参与”与“大陆单独归属”混为一谈。国际学会不能按会员国籍、作者来源或办公地址自动赋予单一国家。当前14刊没有混合控制个案被强行判定。

## 二、特殊期刊与历史变化

1. 独立商业出版期刊：允许以创刊社论、连续卷期版权/出版声明、出版合同或转让记录证明持续出版责任；owner可仍unknown。只发现一篇文章的Published by说明时仅确认服务商，须补连续责任证据后才能判制度类型。商业商注册国仍不能决定期刊归属地域。
2. 跨国联合期刊：记录全部主体、责任性质和有效年份。学术协办、订阅优惠、联合编辑、学术协会关联不等于共同控制；没有控制证据不填joint_control。mixed单列，主统计如何归入“中国大陆出版渠道”须研究者冻结；届时并行报告“大陆独立归属”和“大陆参与”口径。
3. 历史归属变化：以ISSN-L与明确闭合年份区间定位；只覆盖本轮实际观察年。出版服务转移不自动改变所有权，平台迁移不改变制度归属。同年转移无法定位到月份/期次、区间重叠、期刊更名身份链接不清，均unknown。不得用当前页面倒推数十年前关系。
4. Public Opinion Quarterly：1972/1973记录Columbia的所有权与AAPOR的学术关联两个角色；2016记录AAPOR所有权与OUP服务；不把1985转让之后的关系回写早期作品。
5. Communication Yearbook中的Rogers/Dearing作品：作品身份已确认，但历史年度载体与后来期刊化回溯存在口径问题，两个推荐位置保留historical_carrier_pending，等待研究者裁定，不能混入普通期刊识别率。

历史连续性推断须写明两端证据、跨度和局限；仅当前刊物首页、现代版权或搜索结果零命中均不构成历史所有权证据。访问受限的索引摘录标记access_limited，不声称已经阅读完整版权页。

## 三、版本、证据与复核

新增注册表`journal_registry_20261011_institutional_v2.csv/json`继承原17个观察年份条目的旧字段，增加上述角色、依据、证据范围、未解决事项和review_status。14种期刊逐一复核；全部保持source_audited_provisional，不是研究者正式批准。

每个新条目有独立JSON审核事件，指向旧entry_id、原文件SHA256和新增字段。新版slot文件只增加字段，不修改原始推荐、排序、canonical作品身份、语言、作者机构或旧主办字段。若出现新证据应追加下一版本与事件，不编辑已有文件。

本轮把MIS Quarterly的2020年大学持续出版责任加入判定：原出版物明确标注MISRC/University of Minnesota为出版者；同时确认这不是该篇作者版权等于期刊所有权的推断。[2020原刊出版声明](https://doi.org/10.25300/MISQ/2020/14583)、[2020正式卷期目录](https://www.jstor.org/stable/e26968250)。所有权仍unknown。

Digital Journalism的创刊社论与2018原文证明跨年出版责任；Information, Communication & Society的创始编辑记录与2018原文证明连续出版关系；Communication Research的1990原刊版权记录及持续刊行资料证明Sage出版责任。三者的地域仍unknown。[创刊社论](https://www.tandfonline.com/doi/full/10.1080/21670811.2012.740264)、[创始编辑记录](https://billdutton.me/editor-and-referee-roles/)、[2018原文](https://pure.uva.nl/ws/files/23265204/Do_not_blame_it_on_the_algorithm.pdf)、[1990原刊权利记录](https://scholarcommons.sc.edu/psyc_facpub/248/)。Journalism Studies的2005历史控制关系继续unknown：后来ICA关联不能倒推到ICA相关兴趣组成立之前。

## 四、研究者待确认，不代替实质性研究决策

- 是否采纳本功能等价的三级责任规则及“商业持续出版责任”类型；所有提案保持provisional。
- mixed的大陆参与/独立归属双口径如何进入主结果；本轮只提供规则与敏感性方案。
- Yearbook历史载体是否满足研究定义中的期刊论文资格，以及以何种历史载体名称展示。
- 是否接受明确标示的历史连续性推断；正式主实验中同等证据门槛须一致应用。
- 新编码和缺失数据规则冻结后，正式实验须另存分析版本指纹；不重写预实验原生成指纹。
