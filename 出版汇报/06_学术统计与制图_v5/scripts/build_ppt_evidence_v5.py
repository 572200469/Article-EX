"""Offline, source-bound statistics and figures. No network, SDK or credential imports.

Run from any directory with the project's plotting environment:
  .venv-desktop/Scripts/python.exe outputs/ppt_evidence_v5/scripts/build_ppt_evidence_v5.py
All writes are confined to outputs/ppt_evidence_v5. Source records remain immutable.
"""
import collections, copy, csv, hashlib, html, json, math, re, unicodedata
from pathlib import Path
from difflib import SequenceMatcher
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'outputs/ppt_evidence_v5'
VERSION = 'ppt_analysis_v5'
PROVIDERS = ['openai', 'gemini', 'deepseek', 'qwen']
LABEL = dict(openai='GPT', gemini='Gemini', deepseek='DeepSeek', qwen='Qwen')
CONDITION = dict(neutral_zh='A', directed_mainland_B='B', directed_cnki_C='C')
TOPICS = ['agenda_setting', 'algorithms_bubbles']
BLUE, LIGHT, GREY = '#003B70', '#648FB5', '#9BA7B1'
SOURCES = {
    'A_v3': 'outputs/publication_visibility_final_figures/normalized_slots_v3.json',
    'A_v4': 'outputs/identity_review_v4_20261012/normalized_slots_v4_preview.json',
    'v4_evidence': 'outputs/identity_review_v4_20261012/slot_identity_evidence_v4.json',
    'A_jobs': 'outputs/publication_visibility_main_20261012/final_job_states.csv',
    'A_manifest': 'data/main_startup/main_candidate_v2_20261011/manifest.json',
    'BC_rows': 'outputs/final_presentation_figures/directed_normalized_evidence.json',
    'BC_jobs': 'outputs/china_directed_20261012/technical_jobs.json',
    'BC_manifest': 'data/china_directed_discovery_pilot/china_directed_16-9597931c4a07c93b/control/manifest.json',
    'BC_frozen_plan': 'data/chinese_resource_supplement_20261012/directed_dry_run_v2/manifest.json',
    'controls': 'data/chinese_resource_supplement_20261012/positive_controls_full_evidence.json',
}
WORK_ALIASES = {}

def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def dump(name, value):
    (OUT/name).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')

def csvout(name, rows, fields=None):
    fields = fields or list(dict.fromkeys(k for r in rows for k in r))
    with (OUT/'data'/name).open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore'); w.writeheader()
        for r in rows:
            w.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (dict,list)) else v for k,v in r.items()})

def norm(x):
    return re.sub(r'[^\w]+', '', unicodedata.normalize('NFKC', html.unescape(str(x or '')).casefold()), flags=re.U)

def journal_norm(x):
    return norm(html.unescape(str(x or '')).replace('&', ' and '))

def doi(x):
    return re.sub(r'^(https?://(dx\.)?doi\.org/|doi:)', '', str(x or '').strip(), flags=re.I).lower()

def workkey(r):
    key = r.get('canonical_work_id')
    if not key: raise ValueError('Confirmed work has no evidence-bound identifier: '+r['slot_id'])
    return WORK_ALIASES.get(key,key)

def derive_work_aliases(rows):
    # A source-generated ID is not a distinct work when exact, confirmed DOI and
    # all identity anchors correspond to a DOI-identified record already in v4.
    def anchor_text(x):
        x=unicodedata.normalize('NFKD',html.unescape(str(x or '')).casefold())
        return re.sub(r'[^\w]+','', ''.join(c for c in x if not unicodedata.combining(c)))
    def authors(r):return sorted(anchor_text(a) for a in r.get('canonical_authors',[]))
    targets=collections.defaultdict(list)
    for r in rows:
        if str(r.get('canonical_work_id','')).startswith('doi:'):targets[r['canonical_work_id']].append(r)
    aliases={};proof=[]
    for r in rows:
        wid=r['canonical_work_id'];d=doi(r.get('canonical_doi'));target='doi:'+d
        if wid.startswith('doi:') or not d or target not in targets:continue
        peers=[p for p in targets[target] if anchor_text(p['canonical_title'])==anchor_text(r['canonical_title']) and authors(p)==authors(r) and p['publication_year']==r['publication_year'] and journal_norm(p['canonical_journal'])==journal_norm(r['canonical_journal'])]
        if peers:
            aliases[wid]=target
            if not any(p['source_work_id']==wid for p in proof):
                proof.append({'source_work_id':wid,'analysis_work_id':target,'confirmed_doi':d,'canonical_title':r['canonical_title'],'canonical_authors':r['canonical_authors'],'year':r['publication_year'],'journal':r['canonical_journal'],'source_slot_id':r['slot_id'],'anchored_peer_slot_id':peers[0]['slot_id'],'rule':'same confirmed DOI + exact normalized canonical title/authors/year/journal; accent normalization only','original_v4_unchanged':True,'version':VERSION})
    return aliases,proof

def has_han(x):
    return bool(re.search('[\u3400-\u9fff\U00020000-\U0002ffff]', str(x or '')))

def mdtable(rows, cols):
    text = '| '+' | '.join(v for k,v in cols)+' |\n| '+' | '.join('---' for _ in cols)+' |\n'
    return text+'\n'.join('| '+' | '.join(str(r.get(k,'unknown')).replace('|','/').replace('\n',' ') for k,v in cols)+' |' for r in rows)

def spearman(x,y):
    # Average ranks for ties; Pearson correlation of ranks. No p-values: these are selected works.
    def ranks(values):
        a=np.asarray(values,float); order=np.argsort(a,kind='stable'); out=np.empty(len(a)); i=0
        while i<len(a):
            j=i+1
            while j<len(a) and a[order[j]]==a[order[i]]:j+=1
            out[order[i:j]]=(i+j-1)/2+1; i=j
        return out
    if len(x)<3 or len(set(x))<2 or len(set(y))<2:return None
    return float(np.corrcoef(ranks(x),ranks(y))[0,1])

def journal_groups(rows):
    # Link exact normalized canonical names to ISSN-L only where the observed mapping is unique.
    known=collections.defaultdict(set)
    for r in rows:
        if r.get('journal_issn_l'):known[journal_norm(r['canonical_journal'])].add(r['journal_issn_l'])
    groups=collections.defaultdict(list); mapping=[]
    for r in rows:
        name=html.unescape(r['canonical_journal']); linked=known[journal_norm(name)]
        ident=r.get('journal_issn_l') or (next(iter(linked)) if len(linked)==1 else None)
        key='issn-l:'+ident if ident else 'canonical-label:'+journal_norm(name)
        groups[key].append(r)
        mapping.append({'slot_id':r['slot_id'],'journal_key':key,'canonical_label':name,'issn_l':ident,
                        'basis':'row confirmed ISSN-L' if r.get('journal_issn_l') else 'unique exact canonical-name to confirmed ISSN-L' if ident else 'source-supported canonical label; ISSN-L unavailable', 'version':VERSION})
    return groups,mapping

def citation_index(A, evidence):
    """Only read saved OpenAlex responses; never retrieve new metadata."""
    files=set()
    for r in A:
        files.update(r.get('evidence_files',[]))
        if r.get('match_event_file'):files.add(str(ROOT/r['match_event_file']))
    for r in evidence:
        for q in r.get('source_queries',[]):
            if q.get('evidence_file'):files.add(q['evidence_file'])
    files.update(str(p) for p in (ROOT/'data/identity_review_v4_20261012/public_cache').glob('*.json'))
    bydoi=collections.defaultdict(list); byid=collections.defaultdict(list); examined=[]
    def collect(ev, file):
        if ev.get('source')!='openalex' or ev.get('status')!=200:return
        b=ev.get('body') or {}
        if not isinstance(b,dict):return
        date=ev.get('retrieved_at') or ev.get('timestamp')
        if not date:return
        for w in b.get('results',[b]):
            if not isinstance(w,dict) or not w.get('id') or type(w.get('cited_by_count')) is not int:continue
            rec={ 'openalex_id':w['id'], 'doi':doi(w.get('doi')), 'title':w.get('title') or w.get('display_name'),
                  'year':w.get('publication_year'), 'cited_by_count':w['cited_by_count'], 'snapshot_date':date,
                  'metadata_updated_date':w.get('updated_date'), 'evidence_file':str(file.relative_to(ROOT)),
                  'endpoint':ev.get('url'), 'source':'saved OpenAlex metadata response'}
            if rec['doi']:bydoi[rec['doi']].append(rec)
            byid[w['id']].append(rec)
    for name in sorted(files):
        path=Path(name)
        if not path.is_absolute():path=ROOT/path
        if not path.exists() or path.suffix!='.json':continue
        d=read(path);examined.append(str(path.relative_to(ROOT)))
        if isinstance(d,dict):
            collect(d,path)
            for ev in d.get('evidence',[]):collect(ev,path)
    return bydoi,byid,examined

def format_rho(v):return 'NA' if v is None else f'{v:.3f}'

def setup_fonts():
    for p in ['C:/Windows/Fonts/times.ttf','C:/Windows/Fonts/msyh.ttc']:
        if not Path(p).exists():raise FileNotFoundError('Required font not found: '+p)
        font_manager.fontManager.addfont(p)
    plt.rcParams.update({'font.family':['Times New Roman','Microsoft YaHei'], 'font.size':12,
                        'axes.unicode_minus':False, 'svg.fonttype':'path', 'figure.facecolor':'white',
                        'axes.spines.top':False,'axes.spines.right':False,'axes.edgecolor':'#CAD3DB',
                        'axes.labelcolor':BLUE,'text.color':'#203243','xtick.color':'#203243','ytick.color':'#203243'})

def export(fig,name,foot):
    fig.text(.025,.024,foot,fontsize=10,va='bottom',linespacing=1.5)
    for ax in fig.axes:
        if ax.axison:ax.grid(axis='x',color='#E7ECF1',linewidth=.6);ax.set_axisbelow(True)
    fig.savefig(OUT/'figures'/(name+'.png'),dpi=360,facecolor='white')
    fig.savefig(OUT/'figures'/(name+'.svg'),facecolor='white')
    plt.close(fig)

def figures(brands, citation_rows, corr, citation_coverage, ABC, topic_counts, funnel, flow, metrics):
    setup_fonts()
    top=brands[:10]; fig,axes=plt.subplots(1,2,figsize=(15.5,9),gridspec_kw={'width_ratios':[2.4,1]})
    names=[r['journal'] for r in top]; y=np.arange(len(top))
    axes[0].barh(y,[r['positions'] for r in top],color=BLUE,height=.65)
    axes[0].set_yticks(y,names,fontsize=11);axes[0].invert_yaxis();axes[0].set_xlabel('推荐位置频次（含重复）')
    axes[0].set_xlim(0,max(r['positions'] for r in top)*1.37)
    for i,r in enumerate(top):axes[0].text(r['positions']+.7,i,f"{r['positions']}  ({r['position_share']*100:.1f}%)",va='center',fontsize=11)
    axes[1].barh(y,[r['unique_works'] for r in top],color=LIGHT,height=.65);axes[1].set_yticks(y,[]);axes[1].invert_yaxis();axes[1].set_xlabel('去重作品数')
    axes[1].set_xlim(0,max(r['unique_works'] for r in top)*1.3)
    for i,r in enumerate(top):axes[1].text(r['unique_works']+.2,i,str(r['unique_works']),va='center')
    fig.suptitle('Figure 1  自然推荐中已确认期刊的品牌集中',fontsize=19,x=.53,y=.96)
    fig.subplots_adjust(left=.31,right=.96,top=.88,bottom=.18,wspace=.2)
    export(fig,'figure1_journal_brand_concentration',f"n = 533 个普通期刊推荐位置 / {metrics['unique_journal_works']} 个去重作品；每个百分比分母均为 533，非 949。\nTop 3 = {metrics['top3_share']*100:.1f}%；HHI = {metrics['hhi']:.3f}。{VERSION} / v4 身份审核，研究者终审 pending；未识别位置不进入此子样本。")

    sufficient=citation_coverage['qualified_unique_works']>=20 and citation_coverage['unique_work_coverage']>=.5
    if sufficient:
        fig,ax=plt.subplots(figsize=(13,8)); marks={'classical':('o',BLUE,'经典主题'), 'digital':('s',LIGHT,'数字主题'),'mixed':('^',GREY,'跨主题')}
        for group,(marker,col,label) in marks.items():
            rs=[r for r in citation_rows if r['topic_stratum']==group]
            if rs:ax.scatter([r['log1p_cited_by_count'] for r in rs],[r['recommendation_job_frequency'] for r in rs],s=43,alpha=.68,c=col,marker=marker,label=f'{label} (n = {len(rs)})',edgecolors='white',linewidth=.4)
        ax.set_xlabel('ln(1 + OpenAlex 累计被引量)');ax.set_ylabel('被推荐的不同回答数（去重 job）')
        ax.set_title('Figure 2  已推荐真作子集：累计引文与重复推荐频次',fontsize=18,pad=17)
        allcorr=next(r for r in corr if r['stratum']=='all')
        ax.text(.025,.97,f"n = {len(citation_rows)}；Spearman ρ = {format_rho(allcorr['spearman_rho'])}\n仅描述已推荐、已识别且有引文快照的作品",transform=ax.transAxes,va='top',bbox={'facecolor':'white','edgecolor':'#DCE5ED','pad':8})
        ax.legend(loc='upper center',bbox_to_anchor=(.5,-.16),ncol=3,frameon=False,fontsize=11);fig.subplots_adjust(bottom=.28,left=.11,right=.97,top=.87)
        classic=next(r for r in corr if r['stratum']=='classical');digital=next(r for r in corr if r['stratum']=='digital');d2000=next((r for r in corr if r['stratum']=='2000s'),None)
        strat=f"经典主题 ρ = {format_rho(classic['spearman_rho'])} (n = {classic['n_unique_works']})；数字主题 ρ = {format_rho(digital['spearman_rho'])} (n = {digital['n_unique_works']})。"
        if d2000:strat+=f" 2000s：ρ = {format_rho(d2000['spearman_rho'])} (n = {d2000['n_unique_works']})。"
        export(fig,'figure2_citation_recommendation',f"统计单位：每个去重作品 1 点；覆盖 {len(citation_rows)}/{citation_coverage['eligible_unique_journal_works']} 个已识别期刊作品（{100*citation_coverage['unique_work_coverage']:.1f}%），{citation_coverage['covered_positions']}/533 个期刊位置。\n{strat}\n快照 {citation_coverage['snapshot_date_min'][:10]}—{citation_coverage['snapshot_date_max'][:10]}；年代关系不完全一致，累计引文并非标准化影响力。\n无未入选参考总体，无显著性或入选概率推断。{VERSION}，终审 pending。")
    else:
        fig,ax=plt.subplots(figsize=(12,6));ax.barh(['合格引文作品','无合格引文证据'],[len(citation_rows),citation_coverage['eligible_unique_journal_works']-len(citation_rows)],color=[BLUE,GREY]);ax.set_title('Figure 2  引文证据覆盖不足：不展示关系推断');ax.set_xlabel('去重期刊作品数');fig.subplots_adjust(bottom=.23,left=.22)
        export(fig,'figure2_citation_recommendation',f"覆盖 {len(citation_rows)}/{citation_coverage['eligible_unique_journal_works']}；低于事先设定 n ≥ 20 且覆盖 ≥ 50% 的展示条件。{VERSION}，终审 pending。")

    fig,ax=plt.subplots(figsize=(13,8));x=np.arange(2)
    for i,summary in enumerate(ABC):
        rs=[next(r for r in topic_counts if r['group']==summary['group'] and r['topic_id']==topic) for topic in TOPICS]
        bars=ax.bar(x+(i-1)*.24,[r['han_title_proportion']*100 for r in rs],color=[BLUE,LIGHT,GREY][i],width=.21,label=summary['group']+'：'+summary['label'])
        for b,r in zip(bars,rs):ax.text(b.get_x()+b.get_width()/2,b.get_height()+3,f"{r['han_title_positions']}/{r['actual_positions']}\n({100*r['han_title_proportion']:.1f}%)",ha='center',fontsize=12)
    ax.set_xticks(x,['议程设置理论','算法推荐与信息茧房'],fontsize=14)
    ax.legend(loc='upper center',bbox_to_anchor=(.5,-.11),ncol=3,frameon=False,fontsize=11)
    ax.set_ylabel('原始题名含汉字的推荐位置比例（%）');ax.set_ylim(0,116);ax.set_title('Figure 3  同两主题中文提问下的原始题名表达',fontsize=18,pad=18);fig.subplots_adjust(left=.11,right=.96,bottom=.25,top=.87)
    export(fig,'figure3_ABC_title_expression',f"两主题合计：A 23/24 成功、114 位置；B 6/8 成功、25 位置；C 6/8 成功、25 位置。柱上分母为各组×主题的实际位置。\nA 每组合 3 次重复，B/C 各 1 次，采集时间不同；失败、无响应及全 null 占位不计推荐，分模型与主题计数见源表。\n汉字题名 ≠ 中文正文 ≠ 大陆出版归属。{VERSION}，探索性描述，不作因果检验。")

    fig,axes=plt.subplots(1,2,figsize=(15,8.7));labels=['实际推荐位置','真作身份有来源证据','期刊制度地域有证据','目标来源已取得证据','目标来源尚未确认','作品身份尚未确认']
    for ax,r in zip(axes,funnel):
        vals=[r['positions'],r['identity_source_supported'],r['journal_affiliation_source_supported'],r['target_source_supported'],r['target_source_not_confirmed'],r['identity_unresolved']]
        bars=ax.barh(np.arange(6),vals,color=[BLUE,LIGHT,LIGHT,BLUE,GREY,GREY],height=.62)
        if r['group']=='B':bars[3].set_facecolor('white');bars[3].set_edgecolor(BLUE);bars[3].set_linewidth(1.8);bars[3].set_linestyle('--')
        ax.set_yticks(np.arange(6),labels if r['group']=='B' else []);ax.invert_yaxis();ax.set_xlim(0,29);ax.set_xlabel('推荐位置数（交叉指标，不堆叠）')
        for i,v in enumerate(vals):ax.text(v+.5,i,str(v)+('（待终审）' if r['group']=='B' and i in [1,2,3] else ''),va='center',fontsize=11)
        ax.set_title('B：中国大陆独立归属' if r['group']=='B' else 'C：文章级 CJFQ 可检索性',fontsize=15,pad=18)
    fig.suptitle('Figure 4  定向发现：推荐声明与来源确认证据',fontsize=19,y=.96)
    fig.subplots_adjust(left=.21,right=.97,top=.85,bottom=.23,wspace=.17)
    export(fig,'figure4_directed_evidence',f"B/C 各 n = 25 位置；真作身份：B 1、C 10；制度地域有证据：B 1、C 7。B 虚线 1 为中文译载待终审，已完成研究者终审的严格合格数为 0。\nC 的文章级 CJFQ 确认证据为 0，25 位置收录状态均待核实；未确认 ≠ 确认未收录。各行交叉，不可相加。\n{VERSION}；B 来源含正式期刊的间接引用与第三方扫描，不能称已取得该作品的完整原刊直接证据。")

    fig,ax=plt.subplots(figsize=(14,9));ax.axis('off');ax.set_xlim(0,14);ax.set_ylim(0,9)
    def box(x,y,w,h,title,sub,color=BLUE):
        ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=.12,rounding_size=.04',facecolor='white',edgecolor=color,linewidth=1.5))
        ax.text(x+w/2,y+h*.68,title,ha='center',va='center',fontsize=15,color=color)
        ax.text(x+w/2,y+h*.28,sub,ha='center',va='center',fontsize=11,color='#203243')
    def arrow(a,b):ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-|>',mutation_scale=15,color=LIGHT,linewidth=1.5))
    box(4.1,7.1,5.8,1.0,'192 计划任务 → 190 成功回答','1 技术失败；1 发送状态不确定、无响应')
    box(4.1,5.65,5.8,1.0,'949 个实际推荐位置','统计起点；不把每份回答中的推荐当独立实验')
    box(.8,3.85,6,1.0,'624 个可对应真实作品的位置','624 / 949 = 65.8%')
    box(8,3.85,5.1,1.0,'325 个无法唯一对应的位置','324 未决 + 1 拼接；325 / 949 = 34.2%',GREY)
    arrow((7,7.1),(7,6.65));arrow((6,5.65),(3.8,4.85));arrow((8,5.65),(10.5,4.85))
    cats=[('普通期刊',533),('非期刊',79),('特殊历史载体',6),('具体载体待定',6)]
    for i,(name,n) in enumerate(cats):
        x=.4+i*3.4;box(x,1.35,3.05,1.5,f'{name}：{n}',f'{n}/624 = {100*n/624:.1f}% 真作\n{n}/949 = {100*n/949:.1f}% 全体')
        arrow((3.8,3.85),(x+1.525,2.85))
    fig.suptitle('方法附图  A组身份识别与期刊样本形成',fontsize=20,y=.97)
    export(fig,'method_A_sample_flow',f"筛选单位为推荐位置，主要重复观测单位为 job；原始推荐与排序均未改变。unknown 是证据状态，不是虚构类别。\n{VERSION}，采用 v4 身份审核 / publication_visibility_coding_v2；研究者终审 pending。")
    return sufficient

def main():
    for sub in ['figures','data','scripts']:(OUT/sub).mkdir(parents=True,exist_ok=True)
    paths={k:ROOT/v for k,v in SOURCES.items()};before={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in paths.values()}
    A3=read(paths['A_v3'])['rows'];A=read(paths['A_v4'])['rows'];BC=read(paths['BC_rows'])['rows']; E=read(paths['v4_evidence'])['rows']
    M=read(paths['A_manifest']);N=read(paths['BC_manifest']);BJ=read(paths['BC_jobs'])['rows'];controls=read(paths['controls'])['records']
    with paths['A_jobs'].open(encoding='utf-8-sig') as f:AJ=list(csv.DictReader(f))
    assert len(A)==949 and len(M['jobs'])==192 and len(AJ)==192
    assert len(BC)==50 and len(N['jobs'])==16 and len(BJ)==16 and len(controls)==24
    assert sum(x['work_category']!='unidentified_work' for x in A)==624
    assert sum(x['work_category']=='confirmed_journal_article' for x in A)==533
    assert sum(x['work_category']=='unidentified_work' for x in A)==325
    assert sum(x['api_success']=='True' for x in AJ)==190 and sum(x['api_success'] for x in BJ)==12
    assert all(x['raw_entry']==y['raw_entry'] for x,y in zip(A,A3))
    manifest_jobs=M['jobs'];directed_jobs=N['jobs'];topics=M['spec']['topics'];topic_names={t['id']:t['cn'] for t in topics}
    global WORK_ALIASES
    WORK_ALIASES,alias_proof=derive_work_aliases([r for r in A if r['work_category']=='confirmed_journal_article'])
    csvout('confirmed_work_id_aliases.csv',alias_proof)
    Astate={j['job_id']:j for j in AJ};BCstate={j['job_id']:j for j in BJ}
    # Create one new analytical snapshot: shared version label, independently scoped cohorts.
    slots=[]
    for cohort,rows in [('A',A),('BC',BC)]:
        for r in rows:
            slots.append({'version':VERSION,'cohort':cohort,'slot_id':r['slot_id'],'job_id':r['job_id'],'provider':r['provider'],'topic_id':r['topic_id'],'condition':r['condition'],'rank':r['rank'],'raw_entry':r['raw_entry'],
                          'canonical_work_id':r.get('canonical_work_id',r.get('reused_main_work_id')),'analysis_work_id':WORK_ALIASES.get(r.get('canonical_work_id'),r.get('canonical_work_id')) if cohort=='A' else r.get('reused_main_work_id'),'canonical_title':r.get('canonical_title'),'canonical_journal':r.get('canonical_journal'),'canonical_year':r.get('publication_year',r.get('canonical_year')),
                          'identity_state':r.get('identity_review_status_v4','source_supported' if r.get('identity_confirmed') else 'unresolved'), 'category':r.get('work_category','confirmed_journal_article' if r.get('identity_confirmed') else 'unidentified_work'),
                          'institutional_mainland':r.get('institutional_mainland',r.get('mainland_journal_institutional_affiliation','unknown')),'journal_issn_l':r.get('journal_issn_l'),'cnki_indexed':r.get('cnki_indexed','unknown'),'researcher_review_status':'pending',
                          'identity_review_scope':r.get('identity_review_scope','prior_BC_source_review_retained'), 'identity_source_record':SOURCES['A_v4'] if cohort=='A' else SOURCES['BC_rows']})
    dump('data/ppt_analysis_v5.json',{'version':VERSION,'A_positions':949,'BC_positions':50,'status':'researcher_review_pending','rows':slots,'source_sha256':before})
    csvout('ppt_analysis_v5_slots.csv',slots);csvout('positive_controls_v5.csv',[dict(r,analysis_version=VERSION,sample_design='nonrandom_positive_control_not_experimental_observation') for r in controls])
    changes=[]
    for cat in ['confirmed_journal_article','confirmed_nonjournal_work','historical_carrier_pending','carrier_unresolved','unidentified_work']:
        n3=sum(r['work_category']==cat for r in A3);n4=sum(r['work_category']==cat for r in A)
        changes.append({'category':cat,'v3':n3,'v4':n4,'change':n4-n3,'denominator':949,'version':VERSION})
    csvout('version_change_counts.csv',changes)

    journals=[r for r in A if r['work_category']=='confirmed_journal_article'];groups,mapping=journal_groups(journals);csvout('figure1_journal_identity_map.csv',mapping)
    brands=[];journal_work_rows=[]
    for key,rs in groups.items():
        label=collections.Counter(html.unescape(r['canonical_journal']) for r in rs).most_common(1)[0][0];ws=collections.defaultdict(list)
        for r in rs:ws[workkey(r)].append(r)
        brands.append({'journal_key':key,'journal':label,'positions':len(rs),'position_share':len(rs)/533,'unique_works':len(ws),'unique_jobs':len({r['job_id'] for r in rs}),'denominator_confirmed_journal_positions':533,'version':VERSION})
        for wid,rr in ws.items():journal_work_rows.append({'journal_key':key,'journal':label,'work_id':wid,'canonical_title':rr[0]['canonical_title'],'publication_year':rr[0]['publication_year'],'positions':len(rr),'unique_jobs':len({r['job_id'] for r in rr}),'slot_ids':[r['slot_id'] for r in rr],'version':VERSION})
    brands.sort(key=lambda r:(-r['positions'],r['journal_key']));csvout('figure1_all_journal_brands.csv',brands);csvout('figure1_top10_journals.csv',brands[:10]);csvout('figure1_journal_unique_works.csv',journal_work_rows)
    metrics={'unique_journal_works':len({workkey(r) for r in journals}),'journals':len(brands),'top3_share':sum(r['positions'] for r in brands[:3])/533,'hhi':sum(r['position_share']**2 for r in brands)}
    assert sum(r['positions'] for r in brands)==533

    bydoi,byid,examined=citation_index(A,E);works=collections.defaultdict(list)
    for r in journals:works[workkey(r)].append(r)
    cit=[];excluded=[]
    for wid,rs in works.items():
        canonical=rs[0];target_doi=doi(wid) if wid.startswith('doi:') else doi(canonical.get('canonical_doi'));pool=bydoi.get(target_doi,[]) if target_doi else byid.get(wid,[])
        valid=[w for w in pool if SequenceMatcher(None,norm(w['title']),norm(canonical['canonical_title'])).ratio()>=.93 and w['cited_by_count']>=0]
        ids={w['openalex_id'] for w in valid}
        if len(ids)!=1:
            excluded.append({'work_id':wid,'canonical_title':canonical['canonical_title'],'positions':len(rs),'reason':'multiple_OpenAlex_identity_candidates' if len(ids)>1 else 'no_cached_anchored_OpenAlex_citation_record','version':VERSION});continue
        chosen=sorted(valid,key=lambda w:(w['snapshot_date'],w['evidence_file']))[-1];gr={j['topic_group'] for j in manifest_jobs if j['job_id'] in {r['job_id'] for r in rs}}
        year=canonical['publication_year'];stratum=next(iter(gr)) if len(gr)==1 else 'mixed'
        cit.append({'work_id':wid,**chosen,'canonical_title':canonical['canonical_title'],'publication_year':year,'decade':f'{year//10*10}s' if type(year) is int else 'unknown','topic_stratum':stratum,'topics':sorted({r['topic_id'] for r in rs}),'models':sorted({r['provider'] for r in rs}),
                    'recommendation_position_frequency':len(rs),'recommendation_job_frequency':len({r['job_id'] for r in rs}),'log1p_cited_by_count':math.log1p(chosen['cited_by_count']),'slot_ids':[r['slot_id'] for r in rs],'version':VERSION,'researcher_review_status':'pending'})
    csvout('figure2_citation_work_observations.csv',cit);csvout('figure2_excluded_works.csv',excluded)
    corr=[]
    for kind,subsets in [('overall',{'all':cit}),('topic',{g:[r for r in cit if r['topic_stratum']==g] for g in ['classical','digital','mixed']}),('decade',{g:[r for r in cit if r['decade']==g] for g in sorted({r['decade'] for r in cit})})]:
        for group,rr in subsets.items():
            corr.append({'stratum_type':kind,'stratum':group,'n_unique_works':len(rr),'spearman_rho':spearman([r['cited_by_count'] for r in rr],[r['recommendation_job_frequency'] for r in rr]),'median_publication_year':float(np.median([r['publication_year'] for r in rr if type(r['publication_year']) is int])) if rr else None,'unit':'unique selected work','p_value':'not_computed_nonindependent_selected_sample','version':VERSION})
    csvout('figure2_spearman_strata.csv',corr)
    coverage={'qualified_unique_works':len(cit),'eligible_unique_journal_works':len(works),'unique_work_coverage':len(cit)/len(works),'covered_positions':sum(r['recommendation_position_frequency'] for r in cit),'snapshot_date_min':min((r['snapshot_date'] for r in cit),default='unknown'),'snapshot_date_max':max((r['snapshot_date'] for r in cit),default='unknown'),'display_threshold_prespecified':'n>=20 and unique_work_coverage>=0.50; descriptive only','new_metadata_queries':0,'cache_files_examined':len(examined)}
    dump('data/figure2_coverage.json',coverage)
    coverage_splits=[];included={r['work_id'] for r in cit}
    for dimension in ['provider','topic_id','condition']:
        for value in sorted({r[dimension] for r in journals}):
            rr=[r for r in journals if r[dimension]==value];keys={workkey(r) for r in rr}
            coverage_splits.append({'dimension':dimension,'value':value,'eligible_unique_works':len(keys),'citation_supported_unique_works':len(keys&included),'coverage':len(keys&included)/len(keys),'eligible_positions':len(rr),'citation_supported_positions':sum(workkey(r) in included for r in rr),'strata_overlap_not_additive':True,'version':VERSION})
    csvout('figure2_citation_coverage_by_stratum.csv',coverage_splits)

    subgroup=[r for r in A if r['condition']=='neutral_zh' and r['topic_id'] in TOPICS]
    conditions=[('A','neutral_zh',subgroup,manifest_jobs,Astate,'自然推荐'),('B','directed_mainland_B',[r for r in BC if r['condition']=='directed_mainland_B'],directed_jobs,BCstate,'大陆主办限定'),('C','directed_cnki_C',[r for r in BC if r['condition']=='directed_cnki_C'],directed_jobs,BCstate,'知网可检索限定')]
    ABC=[];split=[]
    def successful(group,state):return state.get('api_success')=='True' if group=='A' else state.get('api_success') is True
    for group,condition,rows,plan,states,label in conditions:
        js=[j for j in plan if j['condition']==condition and j['topic_id'] in TOPICS];h=sum(has_han(r['raw_entry'].get('title')) for r in rows)
        ABC.append({'group':group,'condition':condition,'label':label,'planned_jobs':len(js),'successful_jobs':sum(successful(group,states[j['job_id']]) for j in js),'actual_positions':len(rows),'han_title_positions':h,'han_title_proportion':h/len(rows),'repeat_design':3 if group=='A' else 1,'version':VERSION})
        for provider in PROVIDERS:
            for topic in TOPICS:
                rr=[r for r in rows if r['provider']==provider and r['topic_id']==topic];jj=[j for j in js if j['provider']==provider and j['topic_id']==topic]
                split.append({'group':group,'provider':provider,'topic_id':topic,'planned_jobs':len(jj),'successful_jobs':sum(successful(group,states[j['job_id']]) for j in jj),'positions':len(rr),'han_title_positions':sum(has_han(r['raw_entry'].get('title')) for r in rr),'han_title_proportion':sum(has_han(r['raw_entry'].get('title')) for r in rr)/len(rr) if rr else None,'version':VERSION})
    topic_counts=[]
    for summary in ABC:
        for topic in TOPICS:
            rr=[r for r in split if r['group']==summary['group'] and r['topic_id']==topic]
            n=sum(r['positions'] for r in rr);h=sum(r['han_title_positions'] for r in rr)
            topic_counts.append({'group':summary['group'],'topic_id':topic,'planned_jobs':sum(r['planned_jobs'] for r in rr),'successful_jobs':sum(r['successful_jobs'] for r in rr),'actual_positions':n,'han_title_positions':h,'han_title_proportion':h/n if n else None,'version':VERSION})
    csvout('figure3_ABC_title_summary.csv',ABC);csvout('figure3_by_model_topic.csv',split);csvout('figure3_by_topic.csv',topic_counts)
    csvout('figure3_raw_title_positions.csv',[{'slot_id':r['slot_id'],'job_id':r['job_id'],'group':CONDITION[r['condition']],'provider':r['provider'],'topic_id':r['topic_id'],'rank':r['rank'],'raw_title':r['raw_entry'].get('title'),'contains_han':has_han(r['raw_entry'].get('title')),'version':VERSION} for r in subgroup+BC])

    funnel=[]
    for group,condition in [('B','directed_mainland_B'),('C','directed_cnki_C')]:
        rr=[r for r in BC if r['condition']==condition];true=[r for r in rr if r['identity_confirmed']]
        affiliated=[r for r in true if r['mainland_journal_institutional_affiliation'] in ['mainland_independent','crossborder_mainland_participation','non_mainland']]
        target=sum(r['mainland_journal_institutional_affiliation']=='mainland_independent' for r in true) if group=='B' else sum(r.get('C_article_CJFQ_confirmed') is True for r in rr)
        funnel.append({'group':group,'positions':len(rr),'identity_source_supported':len(true),'journal_affiliation_source_supported':len(affiliated),'target_source_supported':target,'target_source_not_confirmed':len(rr)-target,'identity_unresolved':len(rr)-len(true),'B_strict_researcher_final_confirmed':0 if group=='B' else None,'B_supported_pending_final_review':target if group=='B' else None,'C_article_CJFQ_unknown':len(rr)-target if group=='C' else None,'C_confirmed_not_indexed':0 if group=='C' else None,'unknown_is_not_false':True,'version':VERSION})
    assert funnel[0]['target_source_supported']==1 and funnel[1]['target_source_supported']==0
    csvout('figure4_directed_evidence_counts.csv',funnel);csvout('figure4_BC_source_cases.csv',[dict(r,analysis_version=VERSION,B_strict_final_status='pending_researcher_review' if r.get('B_strict_confirmed') else 'unknown_or_not_applicable',CNKI_article_status='confirmed' if r.get('C_article_CJFQ_confirmed') else 'unknown_not_negative') for r in BC])
    flow=[{'category':c,'positions':sum(r['work_category']==c for r in A),'denominator_all_positions':949,'denominator_real_work_positions':624,'fraction_all':sum(r['work_category']==c for r in A)/949,'fraction_real_work':sum(r['work_category']==c for r in A)/624 if c!='unidentified_work' else None,'version':VERSION} for c in ['confirmed_journal_article','confirmed_nonjournal_work','historical_carrier_pending','carrier_unresolved','unidentified_work']]
    assert sum(r['positions'] for r in flow)==949;csvout('method_A_sample_flow.csv',flow)
    sufficient=figures(brands,cit,corr,coverage,ABC,topic_counts,funnel,flow,metrics)
    # Parameter and prompt documents read actual records, never generate replacement tasks.
    make_parameters(M,N,AJ,BJ,topics)
    write_documents(changes,metrics,brands,corr,coverage,ABC,funnel,sufficient,before)
    after={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in paths.values()};assert before==after
    dump('validation.json',{'version':VERSION,'source_sha256':before,'all_source_hashes_unchanged':True,'A_plan':192,'A_success':190,'A_positions':949,'A_real_positions':624,'A_journal_positions':533,'A_identity_not_unique':325,'BC_sent':16,'BC_success':12,'BC_positions':50,'controls':24,'figure_count':5,'PNG_dpi':360,'source_mixed_version_inside_figure':False,'researcher_review_status':'pending','model_generation_requests':0,'network_requests':0,'citation_coverage':coverage,'journal_metrics':metrics,'figures_are_descriptive':True})
    print(json.dumps({'version':VERSION,'journal_metrics':metrics,'citation_coverage':coverage,'spearman':corr[0]['spearman_rho'],'ABC':ABC,'funnel':funnel},ensure_ascii=False))

def make_parameters(M,N,AJ,BJ,topics):
    Astate={j['job_id']:j for j in AJ};Bstate={j['job_id']:j for j in BJ}
    records=[];prompts={};errors=[]
    rawroot=ROOT/'data/publication_visibility'/M['batch_id']
    amap={p.stem:p for p in rawroot.glob('batch_*/raw/*.json')}
    for cohort,plan,state in [('A',M['jobs'],Astate),('BC',N['jobs'],Bstate)]:
        for j in plan:
            if cohort=='A':path=amap.get(j['job_id'])
            else:path=ROOT/state[j['job_id']]['source_raw'] if state[j['job_id']].get('source_raw') else None
            raw=read(path) if path and path.exists() else {};sent=raw.get('sent_parameters');proposed=j['proposed_wire_parameters']
            if sent:
                assert sent['model']==j['requested_model']
                assert sent.get('messages')==proposed.get('messages'),j['job_id']
                assert sent.get('max_completion_tokens',sent.get('max_tokens'))==8192
            assert j['request_parameters']['timeout']==180 and j['sdk_retries']==0 and j['caller_retries']==0
            if raw:
                assert raw['prompt_text']==j['prompt_text'];assert raw['search_enabled'] is False
                assert raw['request_parameters']['timeout']==180 and raw['sdk_retries']==0 and raw['caller_retries']==0
                assert raw['protocol']==j['protocol'] and raw['request_config_id']==j['request_config_id']
            pkey=(j['condition'],j['topic_id']);prompts.setdefault(pkey,j['prompt_text']);assert prompts[pkey]==j['prompt_text']
            cfg=sent or proposed
            records.append({'version':VERSION,'cohort':cohort,'sequence':j['sequence'],'job_id':j['job_id'],'protocol':j['protocol'],'configuration_fingerprint':j['request_config_id'],'provider':j['provider'],'requested_model':j['requested_model'],'returned_model':raw.get('returned_model','unknown'),'access_channel':j['access_channel'],'route_id':j['route_id'],'base_url':raw.get('base_url',j['base_url']),'api_surface':raw.get('api_surface','unknown'),'provider_request_id':raw.get('provider_request_id'),'response_id':raw.get('response_id'),'topic_id':j['topic_id'],'condition':j['condition'],'repeat_index':j['repeat_index'],'prompt_sha256':hashlib.sha256(j['prompt_text'].encode()).hexdigest(),'messages':cfg['messages'],'model_request_parameters_without_messages':{k:v for k,v in cfg.items() if k!='messages'},'wire_parameters_basis':'saved sent_parameters' if sent else 'frozen proposed parameters; actual sent payload unavailable','client_timeout_config':j['request_parameters']['timeout'],'sdk_retries':0,'caller_retries':0,'temperature':sent.get('temperature','not_explicitly_set_server_default_unconfirmed') if sent else 'actual_payload_unavailable','top_p':sent.get('top_p','not_explicitly_set_server_default_unconfirmed') if sent else 'actual_payload_unavailable','model_generation_seed':sent.get('seed','not_explicitly_set') if sent else 'actual_payload_unavailable','client_search':raw.get('search_executed','actual_record_unavailable'),'client_tools':raw.get('tool_records','actual_record_unavailable'),'timestamp':raw.get('timestamp'),'api_success':raw.get('api_success',False),'collection_state':state[j['job_id']].get('state',state[j['job_id']].get('status')),'source_raw':str(path.relative_to(ROOT)) if path else None,'upstream_identity_independently_verified':raw.get('upstream_identity_verified','unknown')})
    csvout('experiment_request_parameters_208_jobs.csv',records)
    promptrows=[{'condition':k[0],'topic_id':k[1],'prompt_text':v,'sha256':hashlib.sha256(v.encode()).hexdigest(),'version':VERSION} for k,v in prompts.items()];csvout('all_frozen_prompt_texts.csv',promptrows)
    route=[]
    for provider in PROVIDERS:
        rr=[r for r in records if r['provider']==provider and r['wire_parameters_basis']=='saved sent_parameters'];j=next(j for j in M['jobs'] if j['provider']==provider)
        configs={json.dumps(r['model_request_parameters_without_messages'],sort_keys=True,ensure_ascii=False) for r in rr}
        route.append({'model':LABEL[provider],'requested_model':j['requested_model'],'channel':j['access_channel'],'base_url':j['base_url'],'route_id':j['route_id'],'actual_saved_wire_variants':sorted(configs),'actual_sent_payload_records':len(rr),'upstream_identity':'not independently verified for relay; configured official URL is recorded for other providers'})
    text='# 实验参数与逐字Prompt：ppt_analysis_v5\n\n来源为冻结manifest及真实请求记录，不重建任务。表中模型ID是申请的API ID；返回ID和路由声明并不证明中转底层模型身份。\n\n'
    text+='A：4×8×2×3 = 192计划任务、190成功回答、949实际位置；1技术失败，1发送不确定且无响应。B/C：4×2×2×1 = 16发送、12成功、50实际位置。24篇正向参照为独立、非随机供给集合，不并入样本。\n\n'
    text+=mdtable(route,[('model','模型'),('requested_model','申请API模型ID'),('channel','渠道'),('base_url','配置URL'),('actual_saved_wire_variants','实际保存的请求参数'),('actual_sent_payload_records','有sent_parameters记录数')])
    text+='\n\n每次要求top-5，允许不足5；申请输出上限8192，GPT使用max_completion_tokens，其余max_tokens；客户端timeout=180秒，SDK和caller重试均0。DeepSeek申请thinking.type=disabled，Qwen申请enable_thinking=false，GPT reasoning_effort=none，Gemini reasoning_effort=low。这里只证明申请参数，不能证明中转正确实现推理控制。\n\n'
    bc_seed=read(ROOT/SOURCES['BC_frozen_plan'])['random_seed']
    text+=f'A任务顺序随机种子为20261011；B/C冻结计划实际种子为{bc_seed}，两者都是任务排序种子，不是模型生成seed。B/C保存既有独立顺序，未重新随机。temperature、top_p及模型seed未在可读实际请求中显式统一设置：服务端默认值未确认；不可推断其为0或1。逐208任务的真实response_id、provider_request_id、渠道、route_id及参数见data/experiment_request_parameters_208_jobs.csv；状态不确定无响应任务只保留冻结拟发送参数，不冒充实际wire证据。\n\n'
    text+='baseline，无客户端联网工具，无RAG内容注入。可读messages逐字对照manifest；角色仅按真实messages记录，未额外添加系统提示。JSON是Prompt中的输出契约，不能据此声称强制JSON Schema API约束。中转平台内部联网、重试或路由机制未独立确认。\n\n'
    text+='## 八主题\n\n'+mdtable(topics,[('id','topic_id'),('cn','中文名'),('en','英文名')])+'\n\n'
    text+=f"A protocol：`{M['protocol']}`；configuration fingerprint：`{M['configuration_fingerprint']}`。\n\nB/C protocol：`{N['jobs'][0]['protocol']}`；configuration fingerprint：`{N['configuration_fingerprint']}`。\n\n"
    text+='## JSON输出契约原文\n\n```json\n'+M['spec']['json_contract']+'\n```\n\n'
    text+='## B/C相对neutral_zh的新增来源限定原文\n\n'
    for cond in ['directed_mainland_B','directed_cnki_C']:
        j=next(j for j in N['jobs'] if j['condition']==cond);parent=j['parent_prompt_text'];current=j['prompt_text']
        # Show whole changed source-condition sentence, not misleading diff fragments.
        old_sentence=parent.split('。')[1]+'。';new_sentence=current.split('。')[1]+'。'
        text+=f"{cond} 原来源条件句：\n\n```text\n{old_sentence}\n```\n\n冻结后的来源条件句（原文）：\n\n```text\n{new_sentence}\n```\n\n"
    text+='B评价严格标准为大陆独立制度归属，跨境大陆参与不自动合格。C评价为文章级CJFQ证据，期刊托管页面与模型自称知网可查均不能替代。\n\n## 全部冻结Prompt原文\n\n'
    for condition in ['neutral_zh','neutral_en','directed_mainland_B','directed_cnki_C']:
        for t in topics:
            if (condition,t['id']) not in prompts:continue
            prompt=prompts[(condition,t['id'])]
            text+=f"### {condition} / {t['id']}\n\nSHA-256：`{hashlib.sha256(prompt.encode()).hexdigest()}`\n\n```text\n{prompt}\n```\n\n"
    (OUT/'experiment_parameters.md').write_text(text,encoding='utf-8')

def write_documents(changes,metrics,brands,corr,coverage,ABC,funnel,sufficient,hashes):
    published=ROOT.parent/'出版汇报/04_研究数据/A_192次自然推荐'
    published_paths=list((ROOT.parent/'出版汇报').rglob('normalized_slots_v3.json'))
    published_state=[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'same_as_project_v3':hashlib.sha256(p.read_bytes()).hexdigest()==hashes[SOURCES['A_v3']]} for p in published_paths]
    dump('data/source_version_manifest.json',{'version':VERSION,'source_sha256':hashes,'published_v3_copies':published_state,'new_review_state':'pending','cohorts_kept_separate':True})
    text='# 数据版本核对与分析版本选择\n\n分析版本统一为ppt_analysis_v5：A采用v4身份审核预览；B/C采用已有逐条来源证据；24篇参照独立保留。各图只使用这一版本锁定的表，不混用发布包v3与项目v4。所有研究者终审仍pending，不能写成已完成最终人工终审。\n\n'
    text+=mdtable(changes,[('category','A推荐位置类别'),('v3','项目/发布包v3'),('v4','v4→本次v5'),('change','变化')])
    text+='\n\nv3识别551/949（58.1%），v4识别624/949（65.8%），增加73位置、7.69个百分点。其中新增普通期刊23、非期刊38、特殊历史载体6、具体载体待定6。未唯一识别325 = 324 unresolved + 1 composite；不是325条已证实虚构。原949推荐、排序及190成功回答不变。\n\nB/C仍为16发送、12成功、50实际位置；成功包括返回空占位的技术成功，不把全null占位计为实际推荐。原已公布汇报包未被修改，GitHub未自动推送新版。来源SHA及发布包比较见data/source_version_manifest.json。\n'
    text+='\nv5补充作品ID归一化：三组source ID与已有DOI ID在确认DOI、真实题名、作者、年及刊均对应时，在派生analysis_work_id中合并。普通期刊子样本的139个原来源ID对应136个去重作品；合格引文作品由未消除ID重复时的115个变为112个，Spearman全部按最终112作品复算。不修改v4 canonical_work_id，不改变624真作位置或533期刊位置，见confirmed_work_id_aliases.csv。\n'
    (OUT/'version_reconciliation.md').write_text(text,encoding='utf-8')
    evid='# 逐图证据、公式与边界\n\n全部图：ppt_analysis_v5；研究者终审pending；SVG为字形路径以保留字体，PNG为360dpi。汉字使用微软雅黑，Latin/数字使用Times New Roman，白底蓝色。统计输出不加入任何新模型调用或元数据检索。\n\n'
    evid+='## Figure 1\n\n来源：A_v4中work_category=confirmed_journal_article的533位置。按已确认ISSN-L归组；缺ISSN-L时仅用同一规范化名称与唯一已知ISSN-L对应，或保留有来源支持的规范化期刊名，不作模糊期刊名称合并。逐位置映射见figure1_journal_identity_map.csv。作品去重使用已审核canonical_work_id；另有三组source ID在确认DOI、规范化真作题名、完整作者、年、刊全部对应已有DOI ID时，仅在v5合并为analysis_work_id，证据见confirmed_work_id_aliases.csv。涉及Bakshy、Chan等Debunking、Ruggiero各一作。不按主题接近合并，不改v4原身份字段。\n\n频次为推荐位置数；比例=期刊频次/533，Top3=前三期刊位置数/533；HHI=Σ(期刊位置频次/533)²。去重论文数按每期刊的不同analysis_work_id计数。另导出unique_jobs，重复推荐不是额外独立生成实验。当前源ID仍可能受数据库版本识别边界影响，不称为完成全体学术作品谱系去重。\n\n'
    evid+=f"普通期刊子样本有{metrics['unique_journal_works']}个去重作品、{metrics['journals']}个期刊身份；Top3={metrics['top3_share']*100:.2f}%，HHI={metrics['hhi']:.4f}。不覆盖949总体中的325未唯一识别位置及其他载体。\n\n"
    evid+='## Figure 2\n\n仅从已保存OpenAlex响应取数，无新查询。入组要求：与审核作品相同DOI/明确OpenAlex ID、规范化真实题名相似度≥.93、唯一OpenAlex ID、有非负整数cited_by_count及获取日期。多ID冲突或无快照者排除；不是用原模型的错误DOI查询结果替代真作。每个去重作品只保留最近获取的合格快照，快照获取日期与OpenAlex记录更新日期分别导出。\n\n主图x=自然对数ln(1+累计被引量)，y=被推荐的不同job数；源表同时保留位置频次。Spearman为平均秩处理ties后的Pearson秩相关，不报p值或因果检验。主题层分经典、数字、跨主题互斥组；作品在多主题出现时主分析只计一次。年代层用确认发表年，不控制所有混杂，也不等于年龄标准化影响力。预先展示条件为n≥20且覆盖已确认去重期刊作品≥50%，不足则仅制覆盖图。\n\n'
    evid+=f"合格{coverage['qualified_unique_works']}/{coverage['eligible_unique_journal_works']}作品（{coverage['unique_work_coverage']*100:.1f}%），覆盖{coverage['covered_positions']}/533期刊位置。快照{coverage['snapshot_date_min']}至{coverage['snapshot_date_max']}。有选择性的已推荐作品，不具未入选参考总体，不能估计高被引作品入选概率；累计引文不是标准化影响力。\n\n"
    evid+='## Figure 3\n\nA仅相同两主题neutral_zh，B/C为各自定向条件；原始raw_entry.title检出CJK统一汉字（不转换或替换题名）。比例=题名含汉字位置/本组实际位置。失败任务没有推荐，全null占位也不计推荐；成功回答数仍计真实API成功，包括未生成有效推荐的回答。A三重复、B/C一重复，不同采集时间；仅作描述性对照，不作配对因果或独立位置显著性检验。汉字表达不等于作品正文语言、数据库收录或出版归属。\n\n'+mdtable(ABC,[('group','组'),('planned_jobs','计划/发送设计'),('successful_jobs','成功回答'),('actual_positions','实际位置'),('han_title_positions','含汉字题名'),('han_title_proportion','组内比例')])+'\n\n'
    evid+='## Figure 4\n\n来源：已有directed_normalized_evidence.json的50实际位置；不重新匹配同主题参照。两组各25位置，C有10个真作位置，其中7制度地域有证据、3制度地域unknown；B有1个中文译载来源支持案例、24个身份未决。B的1在当前数据中标记mainland_independent，但涉及间接正式期刊引用与第三方原刊扫描，研究者终审未完成，虚线柱明确待终审，不能称已有严格最终验收。B研究者终审完成合格数为0是审核进度，不是证据性否定。\n\nC文章级CJFQ确认0，25条均unknown；不声称任何一条“确认未收录”。figure4_BC_source_cases.csv保留原刊身份、制度归属、CNKI收录和证据限制。真作、地域、目标来源存在包含或交叉关系，不能堆叠相加。主图为并列独立指标。\n\n'
    evid+='## 方法附图\n\n949=624+325；624=533+79+6+6，后者依次为普通期刊、非期刊、历史载体、真实作品但具体载体待定。每类同时标出对624和949的分母；未决比例325/949。192是计划任务数，190是成功回答数，949是推荐位置数；一次回答内位置不是独立实验重复。\n\n## 来源可追溯文件\n\n'+ '\n'.join(f'- `{v}`；SHA-256 `{hashes[v]}`' for v in SOURCES.values())+'\n'
    (OUT/'figure_evidence.md').write_text(evid,encoding='utf-8')
    findings='# 可用于汇报的发现与解释边界\n\n'
    findings+=f"1. 期刊品牌呈现集中在已确认子样本：Top3占533个期刊位置的{metrics['top3_share']*100:.1f}%，HHI={metrics['hhi']:.3f}。同刊不同作品与同作重复推荐已分别计数；不能据此断言全部949推荐的出版渠道结构。\n\n"
    classic=next(r for r in corr if r['stratum']=='classical');digital=next(r for r in corr if r['stratum']=='digital');d2000=next((r for r in corr if r['stratum']=='2000s'),None)
    findings+=f"2. 引文关系{'可展示为有限子样本描述' if sufficient else '覆盖不足，不宜展示关系推断'}：{coverage['qualified_unique_works']}个作品，Spearman ρ={format_rho(corr[0]['spearman_rho'])}；经典主题ρ={format_rho(classic['spearman_rho'])}（n={classic['n_unique_works']}），数字主题ρ={format_rho(digital['spearman_rho'])}（n={digital['n_unique_works']}）。"
    if d2000:findings+=f"2000年代子组ρ={format_rho(d2000['spearman_rho'])}（n={d2000['n_unique_works']}），关联较弱，提示总体相关不代表各年代具有同样关系。"
    findings+='年代分层仍有小样本和选择问题，不能称累计引文为标准化影响力，也不能推出高被引更容易入选。\n\n'
    findings+='3. 来源限定条件与原始题名表达呈现明显的描述性差异：同主题中文A为0/114含汉字题名，B为25/25、C为15/25。这里“明显变化”指观察计数，未进行显著性检验；不同重复和时间设计不支持来源限定的因果效应。\n\n'
    findings+='4. 题名中文化与中国出版成果的真实确认是两件事。B目前仅1个大陆独立归属来源支持的译载案例且待终审；C有10个可对应真作位置，但文章级CJFQ均未确认。不能把25个中文题名或“知网可查”声明当作已发现25篇本土真实成果。\n\n'
    findings+='5. 24篇真实中国期刊正向参照证明所选主题存在公开可核实的本土供给，但集合非随机、期刊较集中，不估计全国供给比例。192自然样本与16定向试点独立保留，来源证据unknown不计为境外或未收录。\n\n'
    findings+='Figure1、Figure3和方法附图可用于正式课堂汇报，需保留分母与pending标注；Figure4可作为证据覆盖与限制图，不能展示为B/C来源命中率已完成终审。Figure2仅在合格覆盖满足门槛时作为探索性子样本关联图展示，建议放补充页，并同列年代/主题分层结果。\n\n“编辑把关—数据库把关—模型把关”可作为组织研究问题的框架；数据库覆盖、语言表达、平台路由、训练资源与经典文献累积引用等机制只能作为待检验的理论解释。现有数据不能拆分这些机制的作用，更不能认定因果歧视或给模型作总体优劣排名。未识别程度和官方/中转渠道差异均限制跨模型推断。\n'
    (OUT/'analysis_findings.md').write_text(findings,encoding='utf-8')

if __name__=='__main__':main()
