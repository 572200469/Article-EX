# 汇报关键数字与证据表

| 关键数字 | 值 | 来源 | 计算 | 限制 |
| --- | --- | --- | --- | --- |
| A计划/成功/实际位置 | 192 / 190 / 949 | main_experiment technical_jobs.csv + normalized_slots_v3.json | planned jobs; api_success; len(rows) | 171 uncertain,187 HTTP524,74 four entries; no imputation |
| A身份结构 | 510期刊 / 41非期刊 / 398unknown | outputs\publication_visibility_final_figures\normalized_slots_v3.json | Counter(work_category), denominator949 | unknown not foreign or false citation |
| A前三品牌 | 82+74+65=221 /510=43.3% | A_confirmed_journal_brands.csv | top3 confirmed journal position frequencies | identified journal subset only; repeats retained |
| A制度证据覆盖 | 301/510；209unknown；大陆确认0 | outputs\publication_visibility_final_figures\normalized_slots_v3.json | confirmed journal × institutional_mainland | unidentified398 excluded from journal subset; not proof of absence |
| 本土供给参照 | 24篇 /8主题各3；21国际新闻界+3全球传媒学刊 | data/chinese_resource_supplement_20261012/positive_controls_full_evidence.json | records and Counter(topic_id,journal) | purposive, not random; CJFQ unknown |
| B/C真实发送与响应 | 16发送 /12成功 /4失败 /0未发 /50位置 | outputs/china_directed_20261012/technical_jobs.json + raw_recommendations.json | permits, api_success, status, len(actual rows) | technical missing not zero discovery |
| B大陆严格确认 | 1 | directed_normalized_evidence.csv | conditionB × identity_confirmed × mainland_independent | crossborder participation not strictB |
| C文章CJFQ确认/unknown | 0 /25 | directed_normalized_evidence.csv + linked article evidence | conditionC × cnki_indexed true; remaining unknown | model URL/hosting/general journal indexing insufficient |
| A可比子集 | 23回答 /114位置 | ABC_comparison.csv + A normalized rows | two topics and neutral_zh only | 3 repeats vs1; time/channel differences |
| 定向中文题名 | 40/50 | raw_recommendations.json | Unicode Han detection in raw title only | title language not body language or institutional affiliation |

## 用于汇报的逐条确认作品

| 模型 | 条件 | 排序 | 原题名 | 规范题名 | 真实期刊 | 年 | 制度归属 | CJFQ文章证据 | 来源 | 元数据调整 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gemini | directed_mainland_B | 1 | 议程设置理论的过去、现在和未来 | 议程设置理论概览：过去，现在与未来 | 新闻大学 | 2007 | mainland_independent | unknown | ['https://xwxz.cbpt.cnki.net/portal/journal/portal/client/paper/dc593cfc76e30c6d50672a988e26ba35', 'https://www.scribd.com/document/624584008/议程设置理论概览-过去-现在与未来-麦克斯韦尔-麦考姆斯'] | ['title_light_paraphrase', 'journal_incorrect'] |
| gemini | directed_cnki_C | 1 | The Agenda-Setting Function of Mass Media | The Agenda-Setting Function of Mass Media | Public Opinion Quarterly | 1972 | non_mainland | unknown | ['https://doi.org/10.1086/267990'] | [] |
| gemini | directed_cnki_C | 2 | The Issues of the Sixties: An Exploratory Study in the Dynamics of Public Opinion | The Issues of the Sixties: An Exploratory Study in the Dynamics of Public Opinion | Public Opinion Quarterly | 1973 | non_mainland | unknown | ['https://doi.org/10.1086/268060'] | [] |
| gemini | directed_cnki_C | 3 | Experimental Demonstrations of the "Not-So-Minimal" Consequences of Television News Programs | Experimental Demonstrations of the “Not-So-Minimal” Consequences of Television News Programs | American Political Science Review | 1982 | non_mainland | unknown | ['https://doi.org/10.2307/1962976'] | ['doi_incorrect'] |
| gemini | directed_cnki_C | 4 | Thoughts on Agenda Setting, Framing, and Priming | Thoughts on Agenda Setting, Framing, and Priming | Journal of Communication | 2007 | non_mainland | unknown | ['https://doi.org/10.1111/j.1460-2466.2006.00333.x'] | [] |
| gemini | directed_cnki_C | 5 | New Directions in Agenda-Setting Theory and Research | New Directions in Agenda-Setting Theory and Research | Mass Communication and Society | 2014 | unknown | unknown | ['https://api.crossref.org/works/10.1080/15205436.2014.964871', 'https://doi.org/10.1080/15205436.2014.964871'] | [] |
| openai | directed_cnki_C | 1 | Exposure to ideologically diverse news and opinion on Facebook | Exposure to ideologically diverse news and opinion on Facebook | Science | 2015 | non_mainland | unknown | ['https://doi.org/10.1126/science.aaa1160'] | [] |
| openai | directed_cnki_C | 2 | Filter Bubbles, Echo Chambers, and Online News Consumption | Filter Bubbles, Echo Chambers, and Online News Consumption | Public Opinion Quarterly | 2016 | non_mainland | unknown | ['https://doi.org/10.1093/poq/nfw006'] | [] |
| openai | directed_cnki_C | 3 | Burst of the Filter Bubble? Effects of personalization on the diversity of Google News | Burst of the Filter Bubble? Effects of personalization on the diversity of Google News | Digital Journalism | 2018 | unknown | unknown | ['https://doi.org/10.1080/21670811.2017.1338145'] | ['first_author_given_name_incorrect_Florian_vs_Mario'] |
| openai | directed_cnki_C | 4 | Should We Worry about Filter Bubbles? | Should we worry about filter bubbles? | Internet Policy Review | 2016 | non_mainland | unknown | ['https://doi.org/10.14763/2016.1.401'] | [] |
| openai | directed_cnki_C | 5 | What kind of news gatekeepers do we want machines to be? Filter bubbles, fragmentation, and the normative dimensions of algorithmic recommendations | What kind of news gatekeepers do we want machines to be? Filter bubbles, fragmentation, and the normative dimensions of algorithmic recommendations | Computers in Human Behavior | 2019 | unknown | unknown | ['https://api.crossref.org/works/10.1016%2Fj.chb.2018.07.043', 'https://doi.org/10.1016/j.chb.2018.07.043'] | ['first_author_given_name_incorrect_Neta_vs_Efrat'] |

## 技术与保护证据

| 序号 | 模型 | 条件 | 原始技术状态 | HTTP | 秒 | 结束 | 实际条目 | 预留 | 用量估算 | 原始响应 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | openai | directed_cnki_C | failed | 408 | 115.99770949999947 | None | 0 | {'currency': 'CNY', 'amount': '0.10'} | {'currency': 'CNY', 'text_component_amount': None, 'estimated_total_amount': None, 'actual_billed_amount': None, 'verified_total_upper_bound': None, 'usage_evidence': None, 'unknown_terms': ['missing_or_inconsistent_token_usage', 'platform_multiplier', 'account_currency_or_quota_unit', 'dynamic_price', 'long_context_tier_threshold', 'long_context_rates', 'reasoning_billing', 'cache_write_fee', 'failed_request_billing', 'platform_internal_retries']} | data\china_directed_discovery_pilot\china_directed_16-9597931c4a07c93b\control\raw\china_directed_2c745f101d2c056e29c1a0f2dc87511ad11da219738a4de86051c4a08ec91290.json |
| 2 | qwen | directed_mainland_B | parse_error | 200 | 8.56543740000052 | stop | 5 | {'currency': 'CNY', 'amount': '0.10'} | {'currency': 'CNY', 'input_tokens_scenario': 165, 'output_tokens_scenario': 312, 'text_component_amount': '0.0009744', 'estimated_total_amount': None, 'verified_total_upper_bound': None, 'actual_billed_amount': None, 'cache_policy': 'all_input_at_uncached_rate_scenario', 'multiplier_scenario': '1 (scenario only; not account verification)', 'tools': 'not_requested', 'client_retries': 0, 'unknown_terms': ['account_currency_confirmation', 'actual_account_discounts', 'cache_billing', 'failed_request_billing', 'billing_rounding'], 'price_snapshot_id': '51176537e343ad9e1d4e441ebf841a781aba65eda97a8275da5e9729f8327a04', 'usage_evidence': {'prompt_tokens': 165, 'total_tokens': 477, 'completion_tokens': 312, 'prompt_tokens_details': {'cached_tokens': 0, 'text_tokens': 165}}, 'reasoning_tokens_reported': None, 'usage_cost_basis': 'uncached list-rate component; not actual invoice'} | data\china_directed_discovery_pilot\china_directed_16-9597931c4a07c93b\control\raw\china_directed_a7c7b6fefffb69d07b17e4227c67d9f4f993e684f95c4f14a2450e16691f8954.json |
| 3 | deepseek | directed_cnki_C | parse_error | 200 | 8.162626299999829 | stop | 5 | {'currency': 'USD', 'amount': '0.10'} | {'currency': 'USD', 'input_tokens_scenario': 152, 'output_tokens_scenario': 642, 'text_component_amount': '0.000816', 'estimated_total_amount': None, 'verified_total_upper_bound': None, 'actual_billed_amount': None, 'cache_policy': 'all_input_at_uncached_rate_scenario', 'multiplier_scenario': '1 (scenario only; not account verification)', 'tools': 'not_requested', 'client_retries': 0, 'unknown_terms': ['current_rate', 'account_currency', 'cache_discount', 'off_peak_discount', 'failed_request_billing', 'actual_invoice'], 'price_snapshot_id': '351ba27a464dc989be37ce2bae82bc2b23bdce7cd3bc17f3875ce3d2871c1841', 'usage_evidence': {'prompt_tokens': 152, 'completion_tokens': 642, 'total_tokens': 794, 'prompt_tokens_details': {'cached_tokens': 0}, 'prompt_cache_hit_tokens': 0, 'prompt_cache_miss_tokens': 152}, 'reasoning_tokens_reported': None, 'usage_cost_basis': 'uncached list-rate component; not actual invoice'} | data\china_directed_discovery_pilot\china_directed_16-9597931c4a07c93b\control\raw\china_directed_d4b7588992c1978d541944228a55416bac689b8007df0ec0769efee99c41609c.json |
| 4 | gemini | directed_cnki_C | failed | 524 | 129.76674440000352 | None | 0 | {'currency': 'CNY', 'amount': '0.15'} | {'currency': 'CNY', 'text_component_amount': None, 'estimated_total_amount': None, 'actual_billed_amount': None, 'verified_total_upper_bound': None, 'usage_evidence': None, 'unknown_terms': ['missing_or_inconsistent_token_usage', 'platform_multiplier', 'account_currency_or_quota_unit', 'dynamic_price', 'context_tier_rules', 'reasoning_billing', 'cache_write_fee', 'failed_request_billing', 'platform_internal_retries']} | data\china_directed_discovery_pilot\china_directed_16-9597931c4a07c93b\control\raw\china_directed_7631d62ab81afd388be254881906c3a30d2f0c2ddfedae29bfc7c0945dc7d24c.json |
| 5 | openai | directed_mainland_B | failed | 524 | 129.49188880000293 | None | 0 | {'currency': 'CNY', 'amount': '0.10'} | {'currency': 'CNY', 'text_component_amount': None, 'estimated_total_amount': None, 'actual_billed_amount': None, 'verified_total_upper_bound': None, 'usage_evidence': None, 'unknown_terms': ['missing_or_inconsistent_token_usage', 'platform_multiplier', 'account_currency_or_quota_unit', 'dynamic_price', 'long_context_tier_threshold', 'long_context_rates', 'reasoning_billing', 'cache_write_fee', 'failed_request_billing', 'platform_internal_retries']} | data\china_directed_discovery_pilot\china_directed_16-9597931c4a07c93b\control\raw\china_directed_72615dfa1871d6fb7fefde4f4bf8b99cdf604e09fba9f6f908145da63d7dc16c.json |
| 6 | gemini | directed_mainland_B | parse_error | 200 | 124.21639849999337 | stop | 4 | {'currency': 'CNY', 'amount': '0.15'} | {'currency': 'CNY', 'input_tokens_scenario': 154, 'output_tokens_scenario': 12822, 'text_component_amount': '0.1850064', 'estimated_total_amount': None, 'verified_total_upper_bound': None, 'actual_billed_amount': None, 'cache_policy': 'all_input_at_uncached_rate_scenario', 'multiplier_scenario': '1 (scenario only; not account verification)', 'tools': 'not_requested', 'client_retries': 0, 'unknown_terms': ['platform_multiplier', 'account_currency_or_quota_unit', 'dynamic_price', 'context_tier_rules', 'reasoning_billing', 'cache_write_fee', 'failed_request_billing', 'platform_internal_retries'], 'price_snapshot_id': '58e8edeb336849be6ae04b0c41fc49b3de2e74a24f6ee00ba37b1b153a8f4a03', 'usage_evidence': {'prompt_tokens': 154, 'completion_tokens': 12822, 'total_tokens': 12976, 'billing_usage': {'source': 'gemini_chat', 'semantic': 'gemini', 'gemini_usage_metadata': {'promptTokenCount': 154, 'toolUsePromptTokenCount': 0, 'candidatesTokenCount': 313, 'totalTokenCount': 12976, 'thoughtsTokenCount': 12509, 'cachedContentTokenCount': 0, 'promptTokensDetails': [], 'toolUsePromptTokensDetails': [], 'candidatesTokensDetails': []}}, 'prompt_tokens_details': {'cached_tokens': 0, 'text_tokens': 154, 'audio_tokens': 0, 'image_tokens': 0}, 'completion_tokens_details': {'text_tokens': 0, 'audio_tokens': 0, 'image_tokens': 0, 'reasoning_tokens': 12509}, 'input_tokens': 0, 'output_tokens': 0, 'input_tokens_details': None, 'claude_cache_creation_5_m_tokens': 0, 'claude_cache_creation_1_h_tokens': 0}, 'reasoning_tokens_reported': 12509, 'usage_cost_basis': 'uncached list-rate component; not actual invoice'} | data\china_directed_discovery_pilot\china_directed_16-9597931c4a07c93b\control\raw\china_directed_929e5b48b3bcbeb1d4a8f7e8a5980237160afe01560a355737b3d3a42d772f03.json |
| 7 | qwen | directed_cnki_C | parse_error | 200 | 15.307700600002136 | stop | 5 | {'currency': 'CNY', 'amount': '0.10'} | {'currency': 'CNY', 'input_tokens_scenario': 171, 'output_tokens_scenario': 657, 'text_component_amount': '0.0019107', 'estimated_total_amount': None, 'verified_total_upper_bound': None, 'actual_billed_amount': None, 'cache_policy': 'all_input_at_uncached_rate_scenario', 'multiplier_scenario': '1 (scenario only; not account verification)', 'tools': 'not_requested', 'client_retries': 0, 'unknown_terms': ['account_currency_confirmation', 'actual_account_discounts', 'cache_billing', 'failed_request_billing', 'billing_rounding'], 'price_snapshot_id': '51176537e343ad9e1d4e441ebf841a781aba65eda97a8275da5e9729f8327a04', 'usage_evidence': {'prompt_tokens': 171, 'total_tokens': 828, 'completion_tokens': 657, 'prompt_tokens_details': {'cached_tokens': 0, 'text_tokens': 171}}, 'reasoning_tokens_reported': None, 'usage_cost_basis': 'uncached list-rate component; not actual invoice'} | data\china_directed_discovery_pilot\china_directed_16-9597931c4a07c93b\control\raw\china_directed_e7d42621b75ad6eaa5bd36239a36356654ace5f9bae671c325582e151b5fd1c5.json |
| 8 | deepseek | directed_mainland_B | success | 200 | 5.8235464000026695 | stop | 5 | {'currency': 'USD', 'amount': '0.10'} | {'currency': 'USD', 'input_tokens_scenario': 149, 'output_tokens_scenario': 249, 'text_component_amount': '0.0003435', 'estimated_total_amount': None, 'verified_total_upper_bound': None, 'actual_billed_amount': None, 'cache_policy': 'all_input_at_uncached_rate_scenario', 'multiplier_scenario': '1 (scenario only; not account verification)', 'tools': 'not_requested', 'client_retries': 0, 'unknown_terms': ['current_rate', 'account_currency', 'cache_discount', 'off_peak_discount', 'failed_request_billing', 'actual_invoice'], 'price_snapshot_id': '351ba27a464dc989be37ce2bae82bc2b23bdce7cd3bc17f3875ce3d2871c1841', 'usage_evidence': {'prompt_tokens': 149, 'completion_tokens': 249, 'total_tokens': 398, 'prompt_tokens_details': {'cached_tokens': 0}, 'prompt_cache_hit_tokens': 0, 'prompt_cache_miss_tokens': 149}, 'reasoning_tokens_reported': None, 'usage_cost_basis': 'uncached list-rate component; not actual invoice'} | data\china_directed_discovery_pilot\china_directed_16-9597931c4a07c93b\control\raw\china_directed_7e911ec6415bf833c5d4468920383cedff7772c1205d5e3fce1b7a13559a935a.json |
| 9 | qwen | directed_mainland_B | parse_error | 200 | 11.384026799998537 | stop | 5 | {'currency': 'CNY', 'amount': '0.10'} | {'currency': 'CNY', 'input_tokens_scenario': 163, 'output_tokens_scenario': 647, 'text_component_amount': '0.0018773', 'estimated_total_amount': None, 'verified_total_upper_bound': None, 'actual_billed_amount': None, 'cache_policy': 'all_input_at_uncached_rate_scenario', 'multiplier_scenario': '1 (scenario only; not account verification)', 'tools': 'not_requested', 'client_retries': 0, 'unknown_terms': ['account_currency_confirmation', 'actual_account_discounts', 'cache_billing', 'failed_request_billing', 'billing_rounding'], 'price_snapshot_id': '51176537e343ad9e1d4e441ebf841a781aba65eda97a8275da5e9729f8327a04', 'usage_evidence': {'prompt_tokens': 163, 'total_tokens': 810, 'completion_tokens': 647, 'prompt_tokens_details': {'cached_tokens': 0, 'text_tokens': 163}}, 'reasoning_tokens_reported': None, 'usage_cost_basis': 'uncached list-rate component; not actual invoice'} | data\china_directed_discovery_pilot\china_directed_16-9597931c4a07c93b\control\raw\china_directed_8f82cb9d4317914d25635a375ea300eed2e4ed87a025c263a70c5790de5fac4d.json |
| 10 | deepseek | directed_cnki_C | parse_error | 200 | 9.860553600003186 | stop | 5 | {'currency': 'USD', 'amount': '0.10'} | {'currency': 'USD', 'input_tokens_scenario': 155, 'output_tokens_scenario': 982, 'text_component_amount': '0.0012249', 'estimated_total_amount': None, 'verified_total_upper_bound': None, 'actual_billed_amount': None, 'cache_policy': 'all_input_at_uncached_rate_scenario', 'multiplier_scenario': '1 (scenario only; not account verification)', 'tools': 'not_requested', 'client_retries': 0, 'unknown_terms': ['current_rate', 'account_currency', 'cache_discount', 'off_peak_discount', 'failed_request_billing', 'actual_invoice'], 'price_snapshot_id': '351ba27a464dc989be37ce2bae82bc2b23bdce7cd3bc17f3875ce3d2871c1841', 'usage_evidence': {'prompt_tokens': 155, 'completion_tokens': 982, 'total_tokens': 1137, 'prompt_tokens_details': {'cached_tokens': 0}, 'prompt_cache_hit_tokens': 0, 'prompt_cache_miss_tokens': 155}, 'reasoning_tokens_reported': None, 'usage_cost_basis': 'uncached list-rate component; not actual invoice'} | data\china_directed_discovery_pilot\china_directed_16-9597931c4a07c93b\control\raw\china_directed_d89223edadd98e68eaf7e11143ffa8694bebd1f08fc91ffc23d854d3790c6219.json |
| 11 | qwen | directed_cnki_C | parse_error | 200 | 11.975014499999816 | stop | 0 | {'currency': 'CNY', 'amount': '0.10'} | {'currency': 'CNY', 'input_tokens_scenario': 169, 'output_tokens_scenario': 252, 'text_component_amount': '0.0008156', 'estimated_total_amount': None, 'verified_total_upper_bound': None, 'actual_billed_amount': None, 'cache_policy': 'all_input_at_uncached_rate_scenario', 'multiplier_scenario': '1 (scenario only; not account verification)', 'tools': 'not_requested', 'client_retries': 0, 'unknown_terms': ['account_currency_confirmation', 'actual_account_discounts', 'cache_billing', 'failed_request_billing', 'billing_rounding'], 'price_snapshot_id': '51176537e343ad9e1d4e441ebf841a781aba65eda97a8275da5e9729f8327a04', 'usage_evidence': {'prompt_tokens': 169, 'total_tokens': 421, 'completion_tokens': 252, 'prompt_tokens_details': {'cached_tokens': 0, 'text_tokens': 169}}, 'reasoning_tokens_reported': None, 'usage_cost_basis': 'uncached list-rate component; not actual invoice'} | data\china_directed_discovery_pilot\china_directed_16-9597931c4a07c93b\control\raw\china_directed_f9bbbf2da48081daa4c3ba824a41010e7a08bdbc0847643bf311b5688ebf7029.json |
| 12 | deepseek | directed_mainland_B | success | 200 | 5.58061550000275 | stop | 5 | {'currency': 'USD', 'amount': '0.10'} | {'currency': 'USD', 'input_tokens_scenario': 146, 'output_tokens_scenario': 199, 'text_component_amount': '0.0002826', 'estimated_total_amount': None, 'verified_total_upper_bound': None, 'actual_billed_amount': None, 'cache_policy': 'all_input_at_uncached_rate_scenario', 'multiplier_scenario': '1 (scenario only; not account verification)', 'tools': 'not_requested', 'client_retries': 0, 'unknown_terms': ['current_rate', 'account_currency', 'cache_discount', 'off_peak_discount', 'failed_request_billing', 'actual_invoice'], 'price_snapshot_id': '351ba27a464dc989be37ce2bae82bc2b23bdce7cd3bc17f3875ce3d2871c1841', 'usage_evidence': {'prompt_tokens': 146, 'completion_tokens': 199, 'total_tokens': 345, 'prompt_tokens_details': {'cached_tokens': 0}, 'prompt_cache_hit_tokens': 0, 'prompt_cache_miss_tokens': 146}, 'reasoning_tokens_reported': None, 'usage_cost_basis': 'uncached list-rate component; not actual invoice'} | data\china_directed_discovery_pilot\china_directed_16-9597931c4a07c93b\control\raw\china_directed_16cbbb345646c96e0e142a0287458f2c8570fdec068cf2732103a60504e38a5a.json |
| 13 | openai | directed_mainland_B | success | 200 | 99.8954251000032 | stop | 1 | {'currency': 'CNY', 'amount': '0.10'} | {'currency': 'CNY', 'input_tokens_scenario': 465, 'output_tokens_scenario': 1758, 'text_component_amount': '0.0143169', 'estimated_total_amount': None, 'verified_total_upper_bound': None, 'actual_billed_amount': None, 'cache_policy': 'all_input_at_uncached_rate_scenario', 'multiplier_scenario': '1 (scenario only; not account verification)', 'tools': 'not_requested', 'client_retries': 0, 'unknown_terms': ['platform_multiplier', 'account_currency_or_quota_unit', 'dynamic_price', 'long_context_tier_threshold', 'long_context_rates', 'reasoning_billing', 'cache_write_fee', 'failed_request_billing', 'platform_internal_retries'], 'price_snapshot_id': 'b803fd4ec7337a37f4ecbe02196da14a829c73077c25250a9bba6e9de9e18525', 'usage_evidence': {'completion_tokens': 1758, 'total_tokens': 2223, 'prompt_tokens': 465, 'prompt_tokens_details': {'cached_tokens': 0, 'cache_write_tokens': 0, 'cached_creation_tokens': 0}, 'completion_tokens_details': {'reasoning_tokens': 1552}}, 'reasoning_tokens_reported': 1552, 'usage_cost_basis': 'uncached list-rate component; not actual invoice'} | data\china_directed_discovery_pilot\china_directed_16-9597931c4a07c93b\control\raw\china_directed_4d78c5bbf0a94131a1769211012195fd02a5e9bd7b99b7dbd2938b601c0bb278.json |
| 14 | gemini | directed_mainland_B | failed | 524 | 129.43518149999727 | None | 0 | {'currency': 'CNY', 'amount': '0.15'} | {'currency': 'CNY', 'text_component_amount': None, 'estimated_total_amount': None, 'actual_billed_amount': None, 'verified_total_upper_bound': None, 'usage_evidence': None, 'unknown_terms': ['missing_or_inconsistent_token_usage', 'platform_multiplier', 'account_currency_or_quota_unit', 'dynamic_price', 'context_tier_rules', 'reasoning_billing', 'cache_write_fee', 'failed_request_billing', 'platform_internal_retries']} | data\china_directed_discovery_pilot\china_directed_16-9597931c4a07c93b\control\raw\china_directed_b3c77e12230174520bcefaa74389eb9dc07e5a954804060a4eb37cafd0253034.json |
| 15 | gemini | directed_cnki_C | parse_error | 200 | 92.535046099998 | stop | 5 | {'currency': 'CNY', 'amount': '0.15'} | {'currency': 'CNY', 'input_tokens_scenario': 156, 'output_tokens_scenario': 10461, 'text_component_amount': '0.1510128', 'estimated_total_amount': None, 'verified_total_upper_bound': None, 'actual_billed_amount': None, 'cache_policy': 'all_input_at_uncached_rate_scenario', 'multiplier_scenario': '1 (scenario only; not account verification)', 'tools': 'not_requested', 'client_retries': 0, 'unknown_terms': ['platform_multiplier', 'account_currency_or_quota_unit', 'dynamic_price', 'context_tier_rules', 'reasoning_billing', 'cache_write_fee', 'failed_request_billing', 'platform_internal_retries'], 'price_snapshot_id': '58e8edeb336849be6ae04b0c41fc49b3de2e74a24f6ee00ba37b1b153a8f4a03', 'usage_evidence': {'prompt_tokens': 156, 'completion_tokens': 10461, 'total_tokens': 10617, 'billing_usage': {'source': 'gemini_chat', 'semantic': 'gemini', 'gemini_usage_metadata': {'promptTokenCount': 156, 'toolUsePromptTokenCount': 0, 'candidatesTokenCount': 641, 'totalTokenCount': 10617, 'thoughtsTokenCount': 9820, 'cachedContentTokenCount': 0, 'promptTokensDetails': [], 'toolUsePromptTokensDetails': [], 'candidatesTokensDetails': []}}, 'prompt_tokens_details': {'cached_tokens': 0, 'text_tokens': 156, 'audio_tokens': 0, 'image_tokens': 0}, 'completion_tokens_details': {'text_tokens': 0, 'audio_tokens': 0, 'image_tokens': 0, 'reasoning_tokens': 9820}, 'input_tokens': 0, 'output_tokens': 0, 'input_tokens_details': None, 'claude_cache_creation_5_m_tokens': 0, 'claude_cache_creation_1_h_tokens': 0}, 'reasoning_tokens_reported': 9820, 'usage_cost_basis': 'uncached list-rate component; not actual invoice'} | data\china_directed_discovery_pilot\china_directed_16-9597931c4a07c93b\control\raw\china_directed_a6c972270a1f6b15c3c1fb2c03cc70cdb619ffbf68509588593b3925341f2729.json |
| 16 | openai | directed_cnki_C | success | 200 | 66.99560909999855 | stop | 5 | {'currency': 'CNY', 'amount': '0.10'} | {'currency': 'CNY', 'input_tokens_scenario': 473, 'output_tokens_scenario': 1571, 'text_component_amount': '0.0128687', 'estimated_total_amount': None, 'verified_total_upper_bound': None, 'actual_billed_amount': None, 'cache_policy': 'all_input_at_uncached_rate_scenario', 'multiplier_scenario': '1 (scenario only; not account verification)', 'tools': 'not_requested', 'client_retries': 0, 'unknown_terms': ['platform_multiplier', 'account_currency_or_quota_unit', 'dynamic_price', 'long_context_tier_threshold', 'long_context_rates', 'reasoning_billing', 'cache_write_fee', 'failed_request_billing', 'platform_internal_retries'], 'price_snapshot_id': 'b803fd4ec7337a37f4ecbe02196da14a829c73077c25250a9bba6e9de9e18525', 'usage_evidence': {'completion_tokens': 1571, 'total_tokens': 2044, 'prompt_tokens': 473, 'prompt_tokens_details': {'cached_tokens': 0, 'cache_write_tokens': 0, 'cached_creation_tokens': 0}, 'completion_tokens_details': {'reasoning_tokens': 1134}}, 'reasoning_tokens_reported': 1134, 'usage_cost_basis': 'uncached list-rate component; not actual invoice'} | data\china_directed_discovery_pilot\china_directed_16-9597931c4a07c93b\control\raw\china_directed_a80d839d194bf4ba978a7aedbd66287464067d777059d3673c9390d467bbc447.json |

原始Prompt、raw、排序和主实验不改；所有匹配另存派生版本。审核是助手对公开证据的检查，researcher_review_status仍pending，不冒充研究者人工终审。actual_billed_amount全部unknown；用量价格估算不等于实际账单。当前证据文件SHA256见directed_normalized_evidence.json。

## 全部实际原始推荐（不改写模型字段）

### 序号1：GPT / agenda_setting / directed_cnki_C

无实际推荐。技术失败，无输出，不补发。

### 序号2：Qwen / algorithms_bubbles / directed_mainland_B

| 原排序 | 原题名 | 原作者 | 原年 | 原期刊 | 原DOI | 身份确认 | CJFQ证据 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 算法推荐与信息茧房：基于社交网络平台的实证研究 | None | None | None | None | False | unknown |
| 2 | 信息茧房效应及其治理路径研究 | None | None | None | None | False | unknown |
| 3 | 算法推荐技术下的信息茧房形成机制与消解策略 | None | None | None | None | False | unknown |
| 4 | 社交媒体中算法推荐对信息茧房的影响研究 | None | None | None | None | False | unknown |
| 5 | 从“过滤气泡”到“信息茧房”：算法推荐的传播效应反思 | None | None | None | None | False | unknown |

### 序号3：DeepSeek / agenda_setting / directed_cnki_C

| 原排序 | 原题名 | 原作者 | 原年 | 原期刊 | 原DOI | 身份确认 | CJFQ证据 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 议程设置理论的发展与演进——基于CiteSpace的可视化分析 | 王国华, 钟声扬, 杨腾飞 | 2018 | 情报杂志 | None | False | unknown |
| 2 | 新媒体环境下议程设置理论的发展与转向 | 张晋升, 祁志慧 | 2016 | 新闻界 | 10.15897/j.cnki.cn51-1046/g2.2016.07.008 | False | unknown |
| 3 | 议程设置研究的新领域：网络议程设置 | 史安斌, 王沛楠 | 2017 | 全球传媒学刊 | 10.16602/j.gmj.2017.02.003 | False | unknown |
| 4 | 属性议程设置与框架理论的比较研究 | 陈阳 | 2013 | 国际新闻界 | None | False | unknown |
| 5 | 社交媒体时代的议程设置理论：理论拓展与研究路径 | 周葆华 | 2019 | 新闻与传播研究 | None | False | unknown |

### 序号4：Gemini / algorithms_bubbles / directed_cnki_C

无实际推荐。技术失败，无输出，不补发。

### 序号5：GPT / agenda_setting / directed_mainland_B

无实际推荐。技术失败，无输出，不补发。

### 序号6：Gemini / agenda_setting / directed_mainland_B

| 原排序 | 原题名 | 原作者 | 原年 | 原期刊 | 原DOI | 身份确认 | CJFQ证据 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 议程设置理论的过去、现在和未来 | ['马克斯韦尔·麦库姆斯'] | 2007 | 国际新闻界 | None | True | unknown |
| 2 | 网络议程设置模式：议程设置理论的第三层级 | ['郭蕾'] | 2014 | 国际新闻界 | None | False | unknown |
| 3 | “议程设置”理论及其在中国 | ['郭镇之'] | 1997 | 国际新闻界 | None | False | unknown |
| 4 | 媒介议程设置效果的实证研究 | ['张国良'] | 1998 | 新闻大学 | None | False | unknown |

### 序号7：Qwen / algorithms_bubbles / directed_cnki_C

| 原排序 | 原题名 | 原作者 | 原年 | 原期刊 | 原DOI | 身份确认 | CJFQ证据 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 信息茧房：概念辨析、形成机理与治理路径 | ['喻国明', '李彪'] | 2019 | 新闻与传播研究 | None | False | unknown |
| 2 | 算法推荐技术对‘信息茧房’效应的强化机制研究 | ['张洪忠', '段淳林'] | 2020 | 现代传播(中国传媒大学学报) | None | False | unknown |
| 3 | 智能媒体时代的信息茧房及其破解 | ['陈昌凤', '师文'] | 2018 | 新闻大学 | None | False | unknown |
| 4 | 从‘信息茧房’到‘回音室效应’：算法推荐下的舆论极化研究 | ['彭兰'] | 2021 | 国际新闻界 | None | False | unknown |
| 5 | 算法权力与信息茧房的生成逻辑及治理对策 | ['方兴东', '钟伟'] | 2022 | 探索与争鸣 | None | False | unknown |

### 序号8：DeepSeek / algorithms_bubbles / directed_mainland_B

| 原排序 | 原题名 | 原作者 | 原年 | 原期刊 | 原DOI | 身份确认 | CJFQ证据 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 算法推荐与“信息茧房”效应：基于用户信息行为的实证研究 | 彭兰 | 2020 | 新闻与传播研究 | None | False | unknown |
| 2 | 算法推荐时代的信息茧房：理论溯源、现实争议与研究进路 | 喻国明, 方可人 | 2020 | 新闻界 | None | False | unknown |
| 3 | 信息茧房效应的实证检验：基于算法推荐新闻客户端的研究 | 陈昌凤, 仇筠茜 | 2021 | 现代传播(中国传媒大学学报) | None | False | unknown |
| 4 | 算法推荐如何影响用户信息接触的多样性——基于信息茧房视角的实证分析 | 张洪忠, 斗维红, 任吴炯 | 2022 | 新闻与传播研究 | None | False | unknown |
| 5 | 算法推荐、信息茧房与算法素养：基于大学生群体的实证研究 | 李彪, 刘子维 | 2022 | 国际新闻界 | None | False | unknown |

### 序号9：Qwen / agenda_setting / directed_mainland_B

| 原排序 | 原题名 | 原作者 | 原年 | 原期刊 | 原DOI | 身份确认 | CJFQ证据 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 议程设置理论在中国:一项关于大众媒介与公众议题关系的实证研究 | 刘海龙 | 2008 | 新闻与传播研究 | None | False | unknown |
| 2 | 网络时代的议程设置:从媒体到公众的转变 | 陈力丹 | 2012 | 国际新闻界 | 10.13495/j.cnki.cjjc.2012.04.001 | False | unknown |
| 3 | 社交媒体中的议程融合:用户主动性与平台算法的影响 | 彭兰 | 2016 | 现代传播(中国传媒大学学报) | 10.19951/j.cnki.1671-0177.2016.05.001 | False | unknown |
| 4 | 突发公共事件中的媒体议程设置机制研究 | 周葆华 | 2014 | 新闻大学 | None | False | unknown |
| 5 | 短视频平台的议程设置功能及其对青年价值观的影响 | 张志安 | 2020 | 青年记者 | None | False | unknown |

### 序号10：DeepSeek / algorithms_bubbles / directed_cnki_C

| 原排序 | 原题名 | 原作者 | 原年 | 原期刊 | 原DOI | 身份确认 | CJFQ证据 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 算法推荐与“信息茧房”效应研究——基于用户信息行为的实证分析 | 彭兰 | 2018 | 新闻与写作 | None | False | unknown |
| 2 | 信息茧房：理论溯源、研究现状与未来展望 | 陈昌凤, 仇筠茜 | 2020 | 新闻与传播研究 | None | False | unknown |
| 3 | 个性化推荐算法的“信息茧房”效应及其治理研究 | 喻国明, 杨雅 | 2019 | 编辑之友 | None | False | unknown |
| 4 | 算法推荐时代的信息茧房与公共传播的困境 | 李彪 | 2021 | 现代传播(中国传媒大学学报) | None | False | unknown |
| 5 | 算法推荐对用户信息接收的影响：信息茧房与回声室效应的实证研究 | 张洪忠, 斗维红, 任吴炯 | 2022 | 新闻大学 | None | False | unknown |

### 序号11：Qwen / agenda_setting / directed_cnki_C

无实际推荐。保留5个全null占位，不计为论文推荐。

### 序号12：DeepSeek / agenda_setting / directed_mainland_B

| 原排序 | 原题名 | 原作者 | 原年 | 原期刊 | 原DOI | 身份确认 | CJFQ证据 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 议程设置研究的新领域：网络议程设置研究 | 张洪忠; 姜楠 | 2020 | 新闻与传播研究 | None | False | unknown |
| 2 | 议程设置理论的研究现状与未来方向 | 刘海龙 | 2004 | 国际新闻界 | None | False | unknown |
| 3 | 新媒体环境下的议程设置理论：挑战与重构 | 彭兰 | 2013 | 新闻与传播研究 | None | False | unknown |
| 4 | 属性议程设置与网络舆论引导 | 陈力丹; 林羽丰 | 2013 | 新闻记者 | None | False | unknown |
| 5 | 议程设置理论在中国的研究进展 | 郭小安; 王晗 | 2018 | 新闻与传播评论 | None | False | unknown |

### 序号13：GPT / algorithms_bubbles / directed_mainland_B

| 原排序 | 原题名 | 原作者 | 原年 | 原期刊 | 原DOI | 身份确认 | CJFQ证据 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 信息茧房：从隐喻到现实的反思 | ['彭兰'] | 2020 | 国际新闻界 | 10.13495/j.cnki.cjjc.2020.03.002 | False | unknown |

### 序号14：Gemini / algorithms_bubbles / directed_mainland_B

无实际推荐。技术失败，无输出，不补发。

### 序号15：Gemini / agenda_setting / directed_cnki_C

| 原排序 | 原题名 | 原作者 | 原年 | 原期刊 | 原DOI | 身份确认 | CJFQ证据 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | The Agenda-Setting Function of Mass Media | Maxwell E. McCombs, Donald L. Shaw | 1972 | Public Opinion Quarterly | 10.1086/267990 | True | unknown |
| 2 | The Issues of the Sixties: An Exploratory Study in the Dynamics of Public Opinion | G. Ray Funkhouser | 1973 | Public Opinion Quarterly | 10.1086/268060 | True | unknown |
| 3 | Experimental Demonstrations of the "Not-So-Minimal" Consequences of Television News Programs | Shanto Iyengar, Mark D. Peters, Donald R. Kinder | 1982 | The American Political Science Review | 10.2307/1962999 | True | unknown |
| 4 | Thoughts on Agenda Setting, Framing, and Priming | David H. Weaver | 2007 | Journal of Communication | 10.1111/j.1460-2466.2006.00333.x | True | unknown |
| 5 | New Directions in Agenda-Setting Theory and Research | Maxwell McCombs, Donald L. Shaw, David H. Weaver | 2014 | Mass Communication and Society | 10.1080/15205436.2014.964871 | True | unknown |

### 序号16：GPT / algorithms_bubbles / directed_cnki_C

| 原排序 | 原题名 | 原作者 | 原年 | 原期刊 | 原DOI | 身份确认 | CJFQ证据 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Exposure to ideologically diverse news and opinion on Facebook | Eytan Bakshy; Solomon Messing; Lada A. Adamic | 2015 | Science | 10.1126/science.aaa1160 | True | unknown |
| 2 | Filter Bubbles, Echo Chambers, and Online News Consumption | Seth Flaxman; Sharad Goel; Justin M. Rao | 2016 | Public Opinion Quarterly | 10.1093/poq/nfw006 | True | unknown |
| 3 | Burst of the Filter Bubble? Effects of personalization on the diversity of Google News | Florian Haim; Andreas Graefe; Hans-Bernd Brosius | 2018 | Digital Journalism | 10.1080/21670811.2017.1338145 | True | unknown |
| 4 | Should We Worry about Filter Bubbles? | Frederik J. Zuiderveen Borgesius; Damian Trilling; Judith Möller; Balázs Bodó; Claes H. de Vreese; Natali Helberger | 2016 | Internet Policy Review | 10.14763/2016.1.401 | True | unknown |
| 5 | What kind of news gatekeepers do we want machines to be? Filter bubbles, fragmentation, and the normative dimensions of algorithmic recommendations | Neta Nechushtai; Seth C. Lewis | 2019 | Computers in Human Behavior | 10.1016/j.chb.2018.07.043 | True | unknown |


## 本次采集的参数、用量与费用限制

所有成功响应finish_reason=stop，未观察到length截断。4/12成功回答可直接JSON解析，其余8份通过外层围栏等无损提取；全部12份成功响应可获得完整JSON，其中Qwen一份为5个全null占位。调用器和SDK均零重试，每job一个凭据。HTTP失败为序号1 GPT408、4 Gemini524、5 GPT524、14 Gemini524；第5之后暂停，经研究者仅恢复6—16的明确批准后继续，不重发旧job。

| 模型 | 已发送 | 成功 | 成功输入tokens | 成功输出tokens（接口报告） | 报告推理tokens | 成功平均秒 | 币种 | 成功用量标价估算 | 实际账单 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| openai | 4 | 2 | 938 | 3329 | 2686 | 83.44551710000087 | CNY | 0.0271856 | unknown |
| gemini | 4 | 2 | 310 | 23283 | 22329 | 108.37572229999569 | CNY | 0.3360192 | unknown |
| deepseek | 4 | 4 | 602 | 2072 | 0 | 7.356835450002109 | USD | 0.0026670 | unknown |
| qwen | 4 | 4 | 668 | 1868 | 0 | 11.808044825000252 | CNY | 0.0055780 | unknown |

按当前价格快照和倍率1场景，已取得usage的成功请求合计估算CNY0.3687828与USD0.0026670，分币种，不换算。不是完整已扣账单，也不含4次失败的未知收费、未知中转倍率等。全批预留CNY1.40/USD0.40，四个provider独立账本的16条预算预留全部保留，没有退款推断。

需要披露：Gemini两个成功请求（6、15）的报告completion_tokens分别12822、10461，其中thoughtsTokens分别12509、9820，候选正文tokens为313、641。均高于8192这一客户端参数值，但上游究竟如何定义/执行限额未核实；不能声称8192已成为上游总token硬上限。按当前标价的各次用量场景估算CNY0.1850064和0.1510128，均高于单次软件预留0.15；实际扣费仍unknown。GPT请求reasoning_effort=none，成功响应仍报告1552和1134 reasoning_tokens；这一差异需保留，不从字段单独断言参数被忽略或底层身份已验证。当前跨模型推理控制不能视为已证实的上游等价。本轮全部生成已停止，不为解释这些差异追加诊断或更改Prompt。

完整性验收：16个唯一凭据、16份中央raw、16份模型隔离镜像与分币种provider账本一致；50个非空推荐与5个全null占位单列；2184个保护范围内历史文件SHA256不变。原始数据哈希和核对结果见outputs/final_presentation_figures/final_integrity_receipt.json。
