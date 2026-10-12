# 方法文献依据矩阵

核查日期2026-10-11。依据根目录研究方案，逐一核对正式出版页、出版商元数据或作者存储库正式版本。表中“直接先例”指相同方法元素，绝不表示同一研究任务或可直接外推相同结果。网络取证仅访问公开资料，Crossref/OpenAlex新API查询0，收费模型调用0。

| 文献：准确题名与稳定出处 | 真实任务/材料 | 支持本研究的参数或选择 | 关系 | 不支持的外推；核查证据 |
| --- | --- | --- | --- | --- |
| Shoemaker, P. J. & Vos, T. P. (2009). *Gatekeeping Theory*. Routledge. [出版商](https://www.routledge.com/Gatekeeping-Theory/Shoemaker-Vos/p/book/9780203931653) | 传播把关理论专著 | 编辑把关、数据库筛选与模型入口的理论对话 | 间接理论借鉴 | 不测LLM内部过程；官方搜索索引可核题名作者与出版信息，直接页面有访问限制 |
| Färber, M., Coutinho, M. & Yuan, S. (2023). *Biases in scholarly recommender systems: impact, prevalence, and mitigation*. Scientometrics 128:2703–2736. DOI10.1007/s11192-023-04636-2。[正式全文](https://link.springer.com/article/10.1007/s11192-023-04636-2) | 梳理学术推荐中的人类与系统偏差、评价与缓解框架 | 区分曝光、选择、流行度与任务基准，披露背景目录覆盖 | 间接借鉴 | 不提供中国期刊比例，不证明本项目192最优；全文/摘要与出版信息可访问 |
| Algaba, A., Mazijn, C., Holst, V., Tori, F., Wenmackers, S. & Ginis, V. (2025). *Large Language Models Reflect Human Citation Patterns with a Heightened Citation Bias*. Findings NAACL:6844–6879. DOI10.18653/v1/2025.findings-naacl.381。[正式页面](https://aclanthology.org/2025.findings-naacl.381/) | 使用AAAI/NeurIPS/ICML/ICLR论文匿名化文内引文，让参数式模型推荐参考文献；比较真实引文和高被引选择，控制年份、题长、作者数、venue | 参数式文献推荐及外部身份对照有直接先例；被引量/平台可作解释变量 | 推荐方法元素直接先例，任务迁移为间接借鉴 | 不是传播学自由top-5；不证明中国出版渠道被低估；正式摘要/元数据已读 |
| Barolo, D., Valentin, C., Karimi, F., Galárraga, L., Méndez, G. G. & Espín-Noboa, L. (2025). *Whose Name Comes Up? Auditing LLM-Based Scholar Recommendations*. arXiv2506.00074，预印本。[版本v1全文](https://arxiv.org/html/2506.00074v1) | 六开放权重模型，物理学者top-k等五任务；k=5或100，温度0，31日内每日3次，外部APS/OpenAlex参照，Jaccard一致性 | top-k审计、重复抽样与重合度为直接方法元素先例 | 方法元素直接先例 | “每日3次×31日”不等于本项目总重复3次；其有重试与CoT，本项目不照搬；不是期刊推荐且非同行评审定稿 |
| Liu, Y., Elekes, A., Lu, J., Dorantes-Gilardi, R. & Barabási, A.-L. (2025). *Unequal Scientific Recognition in the Age of LLMs*. Findings EMNLP:23558–23568. DOI10.18653/v1/2025.findings-emnlp.1279。[正式页面](https://aclanthology.org/2025.findings-emnlp.1279/) | 以OpenAlex十万物理学家及Wikipedia为对照，研究科学家识别及影响力/地理差异 | 外部记录对照、参照总体边界和地域差异需要区分 | 间接借鉴 | 学者识别不能替代论文出版渠道自然推荐；不证明训练覆盖或中国期刊因果劣势 |
| Zhu, Y., Jia, Y., Zhu, Y. & Ye, J. (2026). *Does language bias GenAI academic evaluation in humanities and social sciences? A mixed-methods study based on Chinese-language HSS papers*. JASIST77(7):940–958. DOI10.1002/asi.70079。[出版商摘要](https://asistdl.onlinelibrary.wiley.com/doi/abs/10.1002/asi.70079) | 1150篇、23学科、GPT-4o/DeepSeek-V3，中英文论文评分的被试内设计 | 同材料中英文对照、模型与语言可能交互 | 间接借鉴 | 评分与自然推荐不同；翻译是否等义仍需本研究人工审查；正式作者/题名/摘要可查，根目录短题名在此补全 |
| Zhu, J. (2025). *Generative AI for content discovery in academic publishing: A content provider’s perspective*. Information Services & Use45(1–2):48–55. DOI10.1177/18758789251336075。[正式页面](https://journals.sagepub.com/doi/10.1177/18758789251336075) | 从内容提供者角色分析发现、链接、访问及追踪；讨论GAI工具与阻断bot两难 | 主办组织、出版服务、数字平台不能混为单一来源；出版生态讨论 | 间接生态借鉴 | 不提供本研究分类算法、样本规模或因果证据；正式摘要可访问 |
| Céspedes, L., et al. (2025). *Evaluating the linguistic coverage of OpenAlex: An assessment of metadata accuracy and completeness*. JASIST76(6):884–895. DOI10.1002/asi.24979。[作者机构存储库正式版](https://lurepository.lakeheadu.ca/bitstream/handle/2453/5462/Ce%CC%81spedes-et-al-2025-Evaluating-the-linguistic-coverage-of-OpenAlex.pdf?isAllowed=y&sequence=1) | 与WoS比较，并人工核验6836篇文章语种元数据 | 论文正文语种须复核，数据库覆盖与标签错误单列 | 数据质量方法直接先例；抽样规模间接借鉴 | 不说明本项目每个中文标签错误；不能把OpenAlex当完备世界总体；PDF首面/摘要可查 |

## 参数登记

| 研究选择 | 方法证据关系 | 归属与边界 |
| --- | --- | --- |
| 4模型 | 可借鉴多模型审计（Barolo、Liu） | 本研究可用性/课程规模选择；不是唯一最优，无“2国内对2国外”的因果识别 |
| 8传播主题、经典/数字各4 | 主题差异比较有一般先例 | 具体8题是研究者选择，边界待双人审查，不能按Pilot出现比例挑题 |
| top-5 | Barolo有k=5先例但对象为学者 | 本研究便利性选择；文献没有证明期刊top-5统计学最优 |
| neutral_zh / neutral_en | Zhu等支持语言条件需要控制 | 本研究任务迁移；自然推荐Prompt翻译必须自己复核 |
| 每条件3独立重复 | 重复审计有先例 | 本研究便利性选择，不能将31日密集采样改写为支持“总3次充分”；仅报告波动 |
| 192主实验/16方法预实验 | 上述因子设计的乘积 | 本研究工作量选择，不由文献独立证成样本量或统计功效 |
| 不联网、无RAG | Algaba的参数式引文推荐 | 观察输出可见性，不能反推训练包含/抓取/召回机制 |
| C/N、C/(N-U)、未知极端范围 | 新研究方案的透明分母操作化 | 本研究定义，下界和极端区间不是偏见指数或置信区间 |
| 主办单位×机构×语言三独立量 | Zhu内容发现视角、元数据规范支持区分；Céspedes提示语种误差 | 具体中国主办定义由本研究事先制定，需要发表当年证据，不是自动文献定理 |
| ISSN-L期刊身份归一化 | [OpenAlex Sources字段](https://help.openalex.org/data/sources/attributes/)明确链接印刷/电子ISSN | 官方元数据依据；source.country_code通常是来源/出版者国别，不能替代主办证据；locations仅是传播位置 |
| 90秒、8192候选、零重试 | 历史API技术Pilot和工程安全要求 | 技术便利性选择，8192待确认，不能宣传为文献确证的公平参数 |
| 参考目录的经典/近期两层 | 背景和流行度评价可借鉴Färber/Algaba | 时间界点、范围与合法中文数据可得性仍待审；非概率目录不能计算无偏世界供给比例 |

所有文献只借鉴与其真实任务相符的元素。不增加RQ、不将出版渠道差异称作期刊质量/模型国别因果效应；主图不再使用准确率排名。全文尚未逐段读完的来源只据已核查摘要/方法段作上述限定论断。
