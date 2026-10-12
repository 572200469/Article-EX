# 既有作品身份匹配程序专项审计（只读）

日期：2026-10-12。审计对象为实际生效的 `outputs/publication_visibility_final_figures/normalized_slots_v3.json`、对应缓存及程序。此次未调用网络、未调用模型、未改写旧数据；仅新增本文件。以下风险不是对任何作品真实性的判定。

## 1. 实际身份标准

`src/verify.py:20–43` 使用去标点、NFKC、casefold 后的字符序列 SequenceMatcher 比例，非语义相似度。身份通过以下二者之一：

1. 原DOI与候选DOI相同、标题相似度≥0.85、作者姓集合重合度≥0.5。
2. 标题相似度≥0.93、作者姓集合重合度≥0.5、原始年份精确属于候选canonical/online/print年份。

期刊名相似度≥0.85仅决定 verified 与 metadata_error，不是身份通过门槛；出版类型不是身份门槛。DOI错误也并非终止条件：条件2可接受真实作品并记 doi_mismatch。因此既有程序没有要求全部字段完全一致，也没有将DOI404/零命中判为虚构。然而DOI错和年份错同时存在、或候选作者缺失/格式损坏，可把真实作品排除在正向身份结果之外。

程序旧标签 unverified 在分析表中成为 unidentified_work/identity_unknown，表示未达到当时证据与规则门槛，不表示不存在。

## 2. 检索和当前v3实际覆盖

`src/verify.py:110–125`：先 Crossref 单DOI查询及 OpenAlex DOI filter；没有正向匹配时才做 Crossref query.title + query.author（rows=5），及 OpenAlex search=原题名（per-page=5）。`src/incremental_matching.py:71–79` 增加 Crossref 仅题名的 top5 备用检索，避免原作者错误完全阻断召回。

当前v3由 `scripts/main_quality_resolve.py:43–83` 生成：遍历所有去重键，**重新评估已有候选**，恢复Crossref独立subtitle、移除Jr/Sr等后缀，并使用88条助手来源复核中的正向候选覆盖旧判断；已接受身份默认保留。对已经选定且缺OpenAlex补充信息的作品进行单DOI元数据补充。这不等于对全部未知重新联网检索。`scripts/main_quality_analysis.py:48–85` 将正向候选写入新派生表，旧raw_entry/rank断言保持一致。

尚未统一覆盖：DataCite、DOI resolver终点出版商记录、更多候选/分页、合理题名变体、英文译名与正式中文原题对应、原刊卷期目录、作者别名与缩写顺序。公开中文来源主要通过另行有限来源复核，非本自动客户端完整候选管道。

## 3. 系统性风险与已支持部分

|维度|已经支持|仍需有证据修复或审查|
|---|---|---|
|作者顺序|集合比较，不关心作者列表顺序；常见 given surname 与 surname, given 均取正确姓|非逗号的 surname initials 会把最后缩写当姓；中文姓名先后顺序、译名不识别；姓前缩写粘连如 Mrogers 被当不同姓；候选作者缺失可使重合不足|
|作者缩写|名字缩写不影响以正确姓作比较|仅姓比较也可能对同姓异人过宽；未核对given names、ORCID等身份，不能用放宽姓门槛自动认定|
|年份|online/print/canonical任一精确相同即可|无正确DOI时，年份错1年也阻断；预印本/书籍版次/出版年多版本需实际证据；年份字符串未转换为整数|
|题名|NFKC、大小写、空格标点差异；v3从Crossref subtitle拼完整题名，HTML显示文本恢复|语义译名、不同副标题、数据库截断/错误题名不统一匹配；0.93字符阈值可能造成漏识别；也不能仅凭同主题题名猜同一作品|
|DOI|无DOI/错DOI能走题名作者年份备用路径；实际DOI.org DOI→DOI重定向有alias审计|canonical_doi仅去doi.org前缀和小写，不完整处理尾标点/百分号/其他URL；DataCite未查；指向另一作品应另列DOI真实对象，不能把该对象替换原推荐|
|work_id冲突|多个正向不同ID保留unknown，避免强行选一篇|同作品OA无DOI ID与Crossref DOI、多个版本/合法双DOI可产生人工待核验冲突；v3只以实际DOI→DOI重定向自动建立alias|
|候选召回|DOI+题名作者+题名only，OA/Crossref双来源|每路只有top5，不分页；作者错误可压低Crossref最初检索排序；标题only备用虽改善但仍top5|
|缓存|可复用200/404，避免重复免费查询|IncrementalClient.resolve若已有match文件即返回，unknown不会自动刷新；已有精确请求缓存404保留且没有日期失效；输入去重包含作者字符串与年份，元数据变体并未去成同一真实作品|
|期刊元数据|从OA primary_location source恢复ISSN-L，Crossref ISSN|OA primary_location不是journal时可能留空，未查其他locations；Crossref只取container-title[0]；SSR N等类型跨库误标可影响期刊分类，需独立载体审核|

`src/research_cleaning.py:25–38` 将作者字符串按and/&/中英文分号拆开，某些逗号字符串仅在每段至少两个词时拆开。因此单个 `Katz, Elihu` 正确保留供姓识别，但整串 `Katz, E., Blumler, J.` 不会正确拆成作者；本问题须靠可靠来源恢复，不更改模型原始字符串。

`src/incremental_matching.py:10–19` 去重键为DOI、规范化题名、排序规范化作者、年份的hash；这只是**推荐书目检索键**，不能称真实独立作品数。

## 4. 当前398个unknown的实际缓存诊断

共383个去重检索键。模型各自（跨模型可重复，不能相加作为全局数）：

|模型|unknown位置|该模型独立检索键|
|---|---:|---:|
|GPT|44|44|
|Gemini|17|17|
|DeepSeek|122|115|
|Qwen|215|210|

以下为重叠标志，不能相加，不能直接解释为真实漏识别数量：

|缓存标志|GPT|Gemini|DeepSeek|Qwen|合计位置|
|---|---:|---:|---:|---:|---:|
|至少1候选题名≥.93但作者score<.5|9|0|30|35|74|
|至少1候选题名≥.93且作者≥.5但原年未在候选日期集合|7|1|18|9|35|
|至少1次元数据请求状态非200/404|6|4|13|16|39|
|有正向候选但多个不同work_id|1|0|2|0|3|
|完全没有候选|1|0|4|0|5|

其余unknown不必都是零命中；大量结果只是主题相近或身份冲突的候选，未达标准。API异常标志也不表示整个候选检索均失败，更不能以失败或无索引断定虚构。

实际缓存的优先复核例：

- `Agenda-Setting Research: Where Has It Been, Where Is It Going?`，原作者Everett M. Rogers / James W. Dearing、1988。候选完全同题同年、DOI `10.1080/23808985.1988.11678708`，但候选作者登记Everett Mrogers / James Wdearing，作者score=0。这是明确的**数据库姓名格式损坏风险**，应查原刊作者/卷期后裁定，不因姓阈值直接永久unknown。
- `Utilization of Mass Communication by the Individual`，原Katz/Blumler/Gurevitch、1973。OA候选同题、仅E.J.Katz、1974，作者score=1/3，兼有年份差异。应查真实载体、作者、发表年，不自动视为同一作品，也不因多作者缺失和年误判不存在。
- `The Uses of Mass Communications: Current Perspectives on Gratifications Research`，原Blumler/Katz、1974，OA完全同题同作者但1975；另外有同题书评候选。这需要书籍/版次/书评载体区分，不能误纳普通期刊。
- `Labor Platforms and Gig Work: The Failure to Regulate` 存在多个正向ID与SSRN类型差异，原作者Dubai而候选Dubal。需核实版本对应和出版载体，不能单按标题/年份合并所有ID。

## 5. 已实际运行的离线复现

使用 `.venv-desktop/Scripts/python.exe` import上述纯函数，没有网络调用。构造真实McCombs/Shaw 1972题名候选：

1. 原题名、作者完全准确，原DOI设错误且原年份1973：unverified（title=1，author=1），说明错DOI+错年拒绝。
2. 仅将原年份改1972：metadata_error + doi_mismatch，说明存在DOI错误备用正向路径。
3. 原作者列表逆序、候选名字缩写但姓正确：author_overlap=1，**作者列表顺序本身不是漏识别问题**。
4. `Zhang Wei` 对 `Wei Zhang`：author_overlap=0。
5. `McCombs M. E.` 对 `Maxwell E. McCombs`：author_overlap=0。
6. 空作者列表，即使同DOI、全同题名：unverified。

下一轮应保持多来源、唯一作品身份的证据要求，增加失败原因和备用字段审核，而非无条件降低所有阈值。新五状态须分开于制度归属编码；尚不足证据维持 unresolved_after_review，不以原程序unknown继承为 likely_fabricated。
