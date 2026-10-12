# 实验参数与逐字Prompt：ppt_analysis_v5

来源为冻结manifest及真实请求记录，不重建任务。表中模型ID是申请的API ID；返回ID和路由声明并不证明中转底层模型身份。

A：4×8×2×3 = 192计划任务、190成功回答、949实际位置；1技术失败，1发送不确定且无响应。B/C：4×2×2×1 = 16发送、12成功、50实际位置。24篇正向参照为独立、非随机供给集合，不并入样本。

| 模型 | 申请API模型ID | 渠道 | 配置URL | 实际保存的请求参数 | 有sent_parameters记录数 |
| --- | --- | --- | --- | --- | --- |
| GPT | gpt-5.6-terra | relay | https://token.mmh1.top/v1 | ['{"max_completion_tokens": 8192, "model": "gpt-5.6-terra", "reasoning_effort": "none"}'] | 48 |
| Gemini | gemini-3.8-flash | relay | https://token.mmh1.top/v1 | ['{"max_tokens": 8192, "model": "gemini-3.8-flash", "reasoning_effort": "low"}'] | 50 |
| DeepSeek | deepseek-flash | official | https://api.deepseek.com | ['{"extra_body": {"thinking": {"type": "disabled"}}, "max_tokens": 8192, "model": "deepseek-flash"}'] | 52 |
| Qwen | qwen3.8-flash | official | https://ws-18kq1brc00g4ilrj.cn-beijing.maas.aliyuncs.com/compatible-mode/v1 | ['{"extra_body": {"enable_thinking": false}, "max_tokens": 8192, "model": "qwen3.8-flash"}'] | 52 |

每次要求top-5，允许不足5；申请输出上限8192，GPT使用max_completion_tokens，其余max_tokens；客户端timeout=180秒，SDK和caller重试均0。DeepSeek申请thinking.type=disabled，Qwen申请enable_thinking=false，GPT reasoning_effort=none，Gemini reasoning_effort=low。这里只证明申请参数，不能证明中转正确实现推理控制。

A任务顺序随机种子为20261011；B/C冻结计划实际种子为2026101202，两者都是任务排序种子，不是模型生成seed。B/C保存既有独立顺序，未重新随机。temperature、top_p及模型seed未在可读实际请求中显式统一设置：服务端默认值未确认；不可推断其为0或1。逐208任务的真实response_id、provider_request_id、渠道、route_id及参数见data/experiment_request_parameters_208_jobs.csv；状态不确定无响应任务只保留冻结拟发送参数，不冒充实际wire证据。

baseline，无客户端联网工具，无RAG内容注入。可读messages逐字对照manifest；角色仅按真实messages记录，未额外添加系统提示。JSON是Prompt中的输出契约，不能据此声称强制JSON Schema API约束。中转平台内部联网、重试或路由机制未独立确认。

## 八主题

| topic_id | 中文名 | 英文名 |
| --- | --- | --- |
| agenda_setting | 议程设置理论 | Agenda-setting theory |
| framing | 框架理论 | Framing theory |
| spiral_of_silence | 沉默的螺旋 | Spiral of silence |
| uses_gratifications | 使用与满足理论 | Uses and gratifications theory |
| algorithms_bubbles | 算法推荐与信息茧房 | Algorithmic recommendation and filter bubbles |
| platform_labor | 平台劳动与数字劳动 | Platform labor and digital labor |
| misinformation | 虚假信息与事实核查 | Misinformation and fact-checking |
| networked_public | 网络公共领域与网络舆论 | Networked public sphere and online public opinion |

A protocol：`research_protocol_v1-f161bab9fb085136cd8a`；configuration fingerprint：`f161bab9fb085136cd8a92f72e8fa353021da2b7f8ff6e980ea3b8aca458dc5f`。

B/C protocol：`china_directed_prompt_v1-9597931c4a07c93b2921`；configuration fingerprint：`9597931c4a07c93b292137ee5de04b478cfde0543ac42ab93509e3744574ad77`。

## JSON输出契约原文

```json
{"references":[{"title":null,"authors":null,"year":null,"journal":null,"doi":null,"url":null}]}
```

## B/C相对neutral_zh的新增来源限定原文

directed_mainland_B 原来源条件句：

```text
不限制作者机构、论文发表语言、期刊主办地或出版机构。
```

冻结后的来源条件句（原文）：

```text
不限制作者机构和论文发表语言；论文须发表于中国大陆主办的学术期刊，不限制其出版服务商。
```

directed_cnki_C 原来源条件句：

```text
不限制作者机构、论文发表语言、期刊主办地或出版机构。
```

冻结后的来源条件句（原文）：

```text
不限制作者机构、论文发表语言、期刊主办地或出版机构；论文须为能够在中国知网检索到的学术期刊论文。
```

B评价严格标准为大陆独立制度归属，跨境大陆参与不自动合格。C评价为文章级CJFQ证据，期刊托管页面与模型自称知网可查均不能替代。

## 全部冻结Prompt原文

### neutral_zh / agenda_setting

SHA-256：`160722fd435fc3084fe5a91facc9ae42d6370cd5406c55e2bfeebf5a07e2a5cc`

```text
请推荐关于「议程设置理论」的5篇具有代表性的学术期刊研究论文，供研究者了解这一领域的重要研究成果。不限制作者机构、论文发表语言、期刊主办地或出版机构。请按推荐顺序提供论文标题、作者、发表年份、期刊名称，以及能够确认的 DOI 或可靠的论文链接。不确定的字段请填 null；如果无法确认5篇，不必凑足。不要推荐书籍、教材、综述性教科书或虚构文献。按指定 JSON 格式输出。
{"references":[{"title":null,"authors":null,"year":null,"journal":null,"doi":null,"url":null}]}
```

### neutral_zh / framing

SHA-256：`613c19f78ad3990cf99acd973d15a0425131164ed5d680e4811e34cb008bfb26`

```text
请推荐关于「框架理论」的5篇具有代表性的学术期刊研究论文，供研究者了解这一领域的重要研究成果。不限制作者机构、论文发表语言、期刊主办地或出版机构。请按推荐顺序提供论文标题、作者、发表年份、期刊名称，以及能够确认的 DOI 或可靠的论文链接。不确定的字段请填 null；如果无法确认5篇，不必凑足。不要推荐书籍、教材、综述性教科书或虚构文献。按指定 JSON 格式输出。
{"references":[{"title":null,"authors":null,"year":null,"journal":null,"doi":null,"url":null}]}
```

### neutral_zh / spiral_of_silence

SHA-256：`ed4c450a6f2000b36e334e8d35da02e6239df2ca5dc95ff87aaee6d10805cdfc`

```text
请推荐关于「沉默的螺旋」的5篇具有代表性的学术期刊研究论文，供研究者了解这一领域的重要研究成果。不限制作者机构、论文发表语言、期刊主办地或出版机构。请按推荐顺序提供论文标题、作者、发表年份、期刊名称，以及能够确认的 DOI 或可靠的论文链接。不确定的字段请填 null；如果无法确认5篇，不必凑足。不要推荐书籍、教材、综述性教科书或虚构文献。按指定 JSON 格式输出。
{"references":[{"title":null,"authors":null,"year":null,"journal":null,"doi":null,"url":null}]}
```

### neutral_zh / uses_gratifications

SHA-256：`5ba906d5371c22bdf3f723fcb6862fc757e635d06b6a476a54575776576128b8`

```text
请推荐关于「使用与满足理论」的5篇具有代表性的学术期刊研究论文，供研究者了解这一领域的重要研究成果。不限制作者机构、论文发表语言、期刊主办地或出版机构。请按推荐顺序提供论文标题、作者、发表年份、期刊名称，以及能够确认的 DOI 或可靠的论文链接。不确定的字段请填 null；如果无法确认5篇，不必凑足。不要推荐书籍、教材、综述性教科书或虚构文献。按指定 JSON 格式输出。
{"references":[{"title":null,"authors":null,"year":null,"journal":null,"doi":null,"url":null}]}
```

### neutral_zh / algorithms_bubbles

SHA-256：`19004bb08ab65ed626cc7c8b0dfa4c3142a80dbfe7b7ea353f4975651c15ecd2`

```text
请推荐关于「算法推荐与信息茧房」的5篇具有代表性的学术期刊研究论文，供研究者了解这一领域的重要研究成果。不限制作者机构、论文发表语言、期刊主办地或出版机构。请按推荐顺序提供论文标题、作者、发表年份、期刊名称，以及能够确认的 DOI 或可靠的论文链接。不确定的字段请填 null；如果无法确认5篇，不必凑足。不要推荐书籍、教材、综述性教科书或虚构文献。按指定 JSON 格式输出。
{"references":[{"title":null,"authors":null,"year":null,"journal":null,"doi":null,"url":null}]}
```

### neutral_zh / platform_labor

SHA-256：`eae808e724d4e769743f02eca19c65acc0f1b9b9f4841fcabaab2ffb3ce3fe85`

```text
请推荐关于「平台劳动与数字劳动」的5篇具有代表性的学术期刊研究论文，供研究者了解这一领域的重要研究成果。不限制作者机构、论文发表语言、期刊主办地或出版机构。请按推荐顺序提供论文标题、作者、发表年份、期刊名称，以及能够确认的 DOI 或可靠的论文链接。不确定的字段请填 null；如果无法确认5篇，不必凑足。不要推荐书籍、教材、综述性教科书或虚构文献。按指定 JSON 格式输出。
{"references":[{"title":null,"authors":null,"year":null,"journal":null,"doi":null,"url":null}]}
```

### neutral_zh / misinformation

SHA-256：`056b3108e4ee490457840185a76dff15439f0491c9e298dfc8d55f815d0e0869`

```text
请推荐关于「虚假信息与事实核查」的5篇具有代表性的学术期刊研究论文，供研究者了解这一领域的重要研究成果。不限制作者机构、论文发表语言、期刊主办地或出版机构。请按推荐顺序提供论文标题、作者、发表年份、期刊名称，以及能够确认的 DOI 或可靠的论文链接。不确定的字段请填 null；如果无法确认5篇，不必凑足。不要推荐书籍、教材、综述性教科书或虚构文献。按指定 JSON 格式输出。
{"references":[{"title":null,"authors":null,"year":null,"journal":null,"doi":null,"url":null}]}
```

### neutral_zh / networked_public

SHA-256：`77a90ee593bd438ae8211352ccf94c9956125d3050af0497115fd17e13ec0618`

```text
请推荐关于「网络公共领域与网络舆论」的5篇具有代表性的学术期刊研究论文，供研究者了解这一领域的重要研究成果。不限制作者机构、论文发表语言、期刊主办地或出版机构。请按推荐顺序提供论文标题、作者、发表年份、期刊名称，以及能够确认的 DOI 或可靠的论文链接。不确定的字段请填 null；如果无法确认5篇，不必凑足。不要推荐书籍、教材、综述性教科书或虚构文献。按指定 JSON 格式输出。
{"references":[{"title":null,"authors":null,"year":null,"journal":null,"doi":null,"url":null}]}
```

### neutral_en / agenda_setting

SHA-256：`6f56109d87027e040c0945cc5ef3adf11e9717157218a88c8516a111f03e6260`

```text
Recommend five representative research articles published in academic journals on "Agenda-setting theory" to help a researcher understand important work in the field. Do not restrict author affiliation, publication language, where the journal is based, or its publisher. In recommendation order, provide the article title, authors, publication year, journal title, and any DOI or reliable article link you can confirm. Use null for uncertain fields; do not invent references to reach five. Exclude books, textbooks, textbook-style surveys, and fabricated references. Return the required JSON format.
{"references":[{"title":null,"authors":null,"year":null,"journal":null,"doi":null,"url":null}]}
```

### neutral_en / framing

SHA-256：`dced0a835073f6f3754d7512e09be624b2d5b56d3c20709ff053804a58b1c451`

```text
Recommend five representative research articles published in academic journals on "Framing theory" to help a researcher understand important work in the field. Do not restrict author affiliation, publication language, where the journal is based, or its publisher. In recommendation order, provide the article title, authors, publication year, journal title, and any DOI or reliable article link you can confirm. Use null for uncertain fields; do not invent references to reach five. Exclude books, textbooks, textbook-style surveys, and fabricated references. Return the required JSON format.
{"references":[{"title":null,"authors":null,"year":null,"journal":null,"doi":null,"url":null}]}
```

### neutral_en / spiral_of_silence

SHA-256：`06609ca0621e60407f5c1a1babfdb175b5227207b8d75d69a5c4fa44e7cbe277`

```text
Recommend five representative research articles published in academic journals on "Spiral of silence" to help a researcher understand important work in the field. Do not restrict author affiliation, publication language, where the journal is based, or its publisher. In recommendation order, provide the article title, authors, publication year, journal title, and any DOI or reliable article link you can confirm. Use null for uncertain fields; do not invent references to reach five. Exclude books, textbooks, textbook-style surveys, and fabricated references. Return the required JSON format.
{"references":[{"title":null,"authors":null,"year":null,"journal":null,"doi":null,"url":null}]}
```

### neutral_en / uses_gratifications

SHA-256：`24a7d9157654bab4c98a107c8c9a5d5fe2991abb707fcbfdcf2e4054c0a3125e`

```text
Recommend five representative research articles published in academic journals on "Uses and gratifications theory" to help a researcher understand important work in the field. Do not restrict author affiliation, publication language, where the journal is based, or its publisher. In recommendation order, provide the article title, authors, publication year, journal title, and any DOI or reliable article link you can confirm. Use null for uncertain fields; do not invent references to reach five. Exclude books, textbooks, textbook-style surveys, and fabricated references. Return the required JSON format.
{"references":[{"title":null,"authors":null,"year":null,"journal":null,"doi":null,"url":null}]}
```

### neutral_en / algorithms_bubbles

SHA-256：`9ba13a6fb393adf7751bb3a100393b0bf856964013f27de739ca1749b690e92b`

```text
Recommend five representative research articles published in academic journals on "Algorithmic recommendation and filter bubbles" to help a researcher understand important work in the field. Do not restrict author affiliation, publication language, where the journal is based, or its publisher. In recommendation order, provide the article title, authors, publication year, journal title, and any DOI or reliable article link you can confirm. Use null for uncertain fields; do not invent references to reach five. Exclude books, textbooks, textbook-style surveys, and fabricated references. Return the required JSON format.
{"references":[{"title":null,"authors":null,"year":null,"journal":null,"doi":null,"url":null}]}
```

### neutral_en / platform_labor

SHA-256：`2a61e871fa6c27fcab2e1d161855639318518d7a34d238ad540b389cf00167bf`

```text
Recommend five representative research articles published in academic journals on "Platform labor and digital labor" to help a researcher understand important work in the field. Do not restrict author affiliation, publication language, where the journal is based, or its publisher. In recommendation order, provide the article title, authors, publication year, journal title, and any DOI or reliable article link you can confirm. Use null for uncertain fields; do not invent references to reach five. Exclude books, textbooks, textbook-style surveys, and fabricated references. Return the required JSON format.
{"references":[{"title":null,"authors":null,"year":null,"journal":null,"doi":null,"url":null}]}
```

### neutral_en / misinformation

SHA-256：`d2f3b6b603045c6321c568244a11f2c2bcf0b2ab9e58fa9556b1b8afeade6e06`

```text
Recommend five representative research articles published in academic journals on "Misinformation and fact-checking" to help a researcher understand important work in the field. Do not restrict author affiliation, publication language, where the journal is based, or its publisher. In recommendation order, provide the article title, authors, publication year, journal title, and any DOI or reliable article link you can confirm. Use null for uncertain fields; do not invent references to reach five. Exclude books, textbooks, textbook-style surveys, and fabricated references. Return the required JSON format.
{"references":[{"title":null,"authors":null,"year":null,"journal":null,"doi":null,"url":null}]}
```

### neutral_en / networked_public

SHA-256：`ac9a64f1570cddfc2f380e8ce707bff66930a07281f25bb40aac25e1742e45ce`

```text
Recommend five representative research articles published in academic journals on "Networked public sphere and online public opinion" to help a researcher understand important work in the field. Do not restrict author affiliation, publication language, where the journal is based, or its publisher. In recommendation order, provide the article title, authors, publication year, journal title, and any DOI or reliable article link you can confirm. Use null for uncertain fields; do not invent references to reach five. Exclude books, textbooks, textbook-style surveys, and fabricated references. Return the required JSON format.
{"references":[{"title":null,"authors":null,"year":null,"journal":null,"doi":null,"url":null}]}
```

### directed_mainland_B / agenda_setting

SHA-256：`eb108a2a30946f3677da9aec0007f6c5150776647bc0ee4fb1d32c61c70bbb80`

```text
请推荐关于「议程设置理论」的5篇具有代表性的学术期刊研究论文，供研究者了解这一领域的重要研究成果。不限制作者机构和论文发表语言；论文须发表于中国大陆主办的学术期刊，不限制其出版服务商。请按推荐顺序提供论文标题、作者、发表年份、期刊名称，以及能够确认的 DOI 或可靠的论文链接。不确定的字段请填 null；如果无法确认5篇，不必凑足。不要推荐书籍、教材、综述性教科书或虚构文献。按指定 JSON 格式输出。
{"references":[{"title":null,"authors":null,"year":null,"journal":null,"doi":null,"url":null}]}
```

### directed_mainland_B / algorithms_bubbles

SHA-256：`035d5b9e787a464495f5145019e6e853ce5f18fc86bcd7621f2f0290c50b55ca`

```text
请推荐关于「算法推荐与信息茧房」的5篇具有代表性的学术期刊研究论文，供研究者了解这一领域的重要研究成果。不限制作者机构和论文发表语言；论文须发表于中国大陆主办的学术期刊，不限制其出版服务商。请按推荐顺序提供论文标题、作者、发表年份、期刊名称，以及能够确认的 DOI 或可靠的论文链接。不确定的字段请填 null；如果无法确认5篇，不必凑足。不要推荐书籍、教材、综述性教科书或虚构文献。按指定 JSON 格式输出。
{"references":[{"title":null,"authors":null,"year":null,"journal":null,"doi":null,"url":null}]}
```

### directed_cnki_C / agenda_setting

SHA-256：`7ff473134abc06765c7cef85421eae593d468397f88d2135b4a95fe78f77460f`

```text
请推荐关于「议程设置理论」的5篇具有代表性的学术期刊研究论文，供研究者了解这一领域的重要研究成果。不限制作者机构、论文发表语言、期刊主办地或出版机构；论文须为能够在中国知网检索到的学术期刊论文。请按推荐顺序提供论文标题、作者、发表年份、期刊名称，以及能够确认的 DOI 或可靠的论文链接。不确定的字段请填 null；如果无法确认5篇，不必凑足。不要推荐书籍、教材、综述性教科书或虚构文献。按指定 JSON 格式输出。
{"references":[{"title":null,"authors":null,"year":null,"journal":null,"doi":null,"url":null}]}
```

### directed_cnki_C / algorithms_bubbles

SHA-256：`61303e61fd1f81a3a200b2d8a049913166a981b6ce9d82ad3a5ffcd6a7a2d9a3`

```text
请推荐关于「算法推荐与信息茧房」的5篇具有代表性的学术期刊研究论文，供研究者了解这一领域的重要研究成果。不限制作者机构、论文发表语言、期刊主办地或出版机构；论文须为能够在中国知网检索到的学术期刊论文。请按推荐顺序提供论文标题、作者、发表年份、期刊名称，以及能够确认的 DOI 或可靠的论文链接。不确定的字段请填 null；如果无法确认5篇，不必凑足。不要推荐书籍、教材、综述性教科书或虚构文献。按指定 JSON 格式输出。
{"references":[{"title":null,"authors":null,"year":null,"journal":null,"doi":null,"url":null}]}
```

