# 课程汇报统计与图表：ppt_analysis_v5

此目录是新派生版本，不修改PPT、原始推荐、历史报告或GitHub汇报包。研究者终审状态仍为 **pending**。

## 直接选图

- `figures/figure1_journal_brand_concentration.svg / .png`：已确认期刊子样本的Top10品牌，左为推荐位置、右为去重作品。
- `figures/figure2_citation_recommendation.svg / .png`：去重已推荐真作的引文关联；建议补充页使用，不解释为入选机制。
- `figures/figure3_ABC_title_expression.svg / .png`：两主题×A/B/C的原始题名汉字表达与各自分母。
- `figures/figure4_directed_evidence.svg / .png`：定向来源证据；B中文译载待终审，C的CJFQ未确认不是未收录。
- `figures/method_A_sample_flow.svg / .png`：949位置形成624真作位置、533期刊位置及其他类别的流程。

SVG包含字体字形路径，适合缩放；PNG为360dpi，至少4500像素宽。字体为微软雅黑与Times New Roman，蓝白学术风格。

## 支持文档

1. `version_reconciliation.md`：v3→v4变化及统一v5口径。
2. `experiment_parameters.md`：真实申请参数、渠道、指纹、八主题和20种逐字Prompt。
3. `figure_evidence.md`：来源、公式、分母、入组与缺失处理。
4. `analysis_findings.md`：可展示发现和不能成立的解释。

`data/`含逐图CSV、999位置的独立分析快照、208任务参数、20种Prompt原文、24篇非随机控制文献及来源SHA。参考集合不与实验观察合并。

## 离线复现

在项目根目录运行：

```powershell
& '.venv-desktop/Scripts/python.exe' 'outputs/ppt_evidence_v5/scripts/build_ppt_evidence_v5.py'
& '.venv-desktop/Scripts/python.exe' 'outputs/ppt_evidence_v5/scripts/validate_ppt_evidence_v5.py'
```

脚本不读取密钥、不联网、不导入模型调用器，只写本目录；依赖现有Matplotlib、NumPy、Pandas、Pillow和Windows字体。`final_validation.json`记录独立分母核对、Spearman复算、原始保护文件哈希与图形检查；`deliverable_inventory.csv`供文件追踪。

重要：主实验排序种子20261011；B/C独立冻结计划实际为2026101202。两者都不是模型生成seed，未重新随机。
