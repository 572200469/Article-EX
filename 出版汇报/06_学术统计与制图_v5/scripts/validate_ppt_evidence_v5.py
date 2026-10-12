"""Independent reconciliation of sources, CSV counts, prompts, rho and rendered assets."""
import csv, hashlib, importlib.util, json, math, sys, xml.etree.ElementTree as ET
from pathlib import Path
import pandas as pd
from PIL import Image

sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'outputs/ppt_evidence_v5'
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def csvrows(name):
    with (OUT/'data'/name).open(encoding='utf-8-sig') as f:return list(csv.DictReader(f))
def main():
    v=read(OUT/'validation.json');new=read(OUT/'data/ppt_analysis_v5.json');assert new['version']=='ppt_analysis_v5'
    A=[r for r in new['rows'] if r['cohort']=='A'];BC=[r for r in new['rows'] if r['cohort']=='BC']
    assert len(A)==949 and len(BC)==50 and len({r['slot_id'] for r in new['rows']})==999
    assert all(r['researcher_review_status']=='pending' for r in new['rows'])
    assert sum(r['category']=='confirmed_journal_article' for r in A)==533
    assert sum(r['category']=='unidentified_work' for r in A)==325
    for name,h in v['source_sha256'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==h
    protected=read(ROOT/'data/identity_review_v4_20261012/protected_before.json')
    changed=[name for name,h in protected.items() if not Path(name).exists() or hashlib.sha256(Path(name).read_bytes()).hexdigest()!=h]
    assert not changed,changed
    brands=csvrows('figure1_all_journal_brands.csv');mapping=csvrows('figure1_journal_identity_map.csv');works=csvrows('figure1_journal_unique_works.csv')
    assert len(mapping)==533 and len({r['slot_id'] for r in mapping})==533
    assert sum(int(r['positions']) for r in brands)==533
    assert math.isclose(sum(float(r['position_share']) for r in brands),1,abs_tol=1e-12)
    assert len({r['work_id'] for r in works})==v['journal_metrics']['unique_journal_works']
    assert sum(int(r['positions']) for r in works)==533
    alias_rows=csvrows('confirmed_work_id_aliases.csv');assert len(alias_rows)==3
    original=read(ROOT/'outputs/identity_review_v4_20261012/normalized_slots_v4_preview.json')['rows'];ob={r['slot_id']:r for r in original}
    for r in alias_rows:
        a,b=ob[r['source_slot_id']],ob[r['anchored_peer_slot_id']]
        assert a['canonical_work_id']==r['source_work_id'] and b['canonical_work_id']==r['analysis_work_id']
        assert a['canonical_doi'].lower()==b['canonical_doi'].lower()==r['confirmed_doi']
        assert a['publication_year']==b['publication_year'] and a['canonical_journal']==b['canonical_journal']
    assert all(ob[r['slot_id']]['canonical_work_id']==r['canonical_work_id'] for r in A)
    citation=csvrows('figure2_citation_work_observations.csv');rho=csvrows('figure2_spearman_strata.csv')
    assert len(citation)==v['citation_coverage']['qualified_unique_works'] and len({r['work_id'] for r in citation})==len(citation)
    # Independent tie ranking uses pandas rather than the builder's custom rank function.
    x=pd.Series([int(r['cited_by_count']) for r in citation]);y=pd.Series([int(r['recommendation_job_frequency']) for r in citation])
    independent=float(x.rank(method='average').corr(y.rank(method='average')))
    assert math.isclose(independent,float(rho[0]['spearman_rho']),abs_tol=1e-12)
    for r in citation:
        assert int(r['recommendation_job_frequency'])<=int(r['recommendation_position_frequency'])
        assert math.isclose(math.log1p(int(r['cited_by_count'])),float(r['log1p_cited_by_count']),abs_tol=1e-12)
        assert (ROOT/r['evidence_file']).exists()
    summary=csvrows('figure3_ABC_title_summary.csv');split=csvrows('figure3_by_model_topic.csv');topic=csvrows('figure3_by_topic.csv')
    assert [(int(r['actual_positions']),int(r['han_title_positions'])) for r in summary]==[(114,0),(25,25),(25,15)]
    for r in summary:
        rs=[x for x in split if x['group']==r['group']];tt=[x for x in topic if x['group']==r['group']]
        for key in ['planned_jobs','successful_jobs']:
            assert sum(int(x[key]) for x in rs)==int(r[key])==sum(int(x[key]) for x in tt)
        assert sum(int(x['positions']) for x in rs)==int(r['actual_positions'])==sum(int(x['actual_positions']) for x in tt)
        assert sum(int(x['han_title_positions']) for x in rs)==int(r['han_title_positions'])
    f4=csvrows('figure4_directed_evidence_counts.csv');assert [int(r['positions']) for r in f4]==[25,25]
    assert [int(r['identity_source_supported']) for r in f4]==[1,10]
    assert f4[0]['B_strict_researcher_final_confirmed']=='0' and f4[0]['B_supported_pending_final_review']=='1'
    assert f4[1]['C_article_CJFQ_unknown']=='25' and f4[1]['target_source_supported']=='0'
    parameters=csvrows('experiment_request_parameters_208_jobs.csv');prompts=csvrows('all_frozen_prompt_texts.csv')
    assert len(parameters)==208 and len({r['job_id'] for r in parameters})==208 and len(prompts)==20
    assert all(r['client_timeout_config']=='180' and r['sdk_retries']=='0' and r['caller_retries']=='0' for r in parameters)
    pmap={(r['condition'],r['topic_id']):r for r in prompts};manifest={j['job_id']:j for j in read(ROOT/'data/main_startup/main_candidate_v2_20261011/manifest.json')['jobs']}
    manifest.update({j['job_id']:j for j in read(ROOT/'data/china_directed_discovery_pilot/china_directed_16-9597931c4a07c93b/control/manifest.json')['jobs']})
    for r in parameters:
        p=pmap[(r['condition'],r['topic_id'])]['prompt_text'];assert p==manifest[r['job_id']]['prompt_text']
        assert hashlib.sha256(p.encode()).hexdigest()==r['prompt_sha256']
    figures=[]
    for path in sorted((OUT/'figures').glob('*.png')):
        svg=path.with_suffix('.svg');ET.parse(svg);s=svg.read_text(encoding='utf-8')
        assert 'TimesNewRoman' in s and 'MicrosoftYaHei' in s,path.name
        with Image.open(path) as im:
            assert im.width>=4000 and im.height>=2500
            assert all(abs(z-360)<1 for z in im.info['dpi'])
            figures.append({'name':path.stem,'dimensions':list(im.size),'dpi':list(im.info['dpi']),'SVG_valid_XML':True,'Times_and_YaHei_glyph_paths':True})
    assert len(figures)==5
    outcome={'passed':True,'version':'ppt_analysis_v5','protected_files_unchanged':len(protected),'source_hashes_unchanged':len(v['source_sha256']),'all999_slot_ids_unique':True,'208_frozen_jobs_and_20_prompts_reconciled':True,'independent_spearman_rho':independent,'all_CSV_denominators_reconciled':True,'figure_assets':figures,'visual_inspection':'all five PNGs inspected; scatter legend moved outside data; Figure3 grouped by topic and condition','model_generation_requests':0,'network_requests':0,'researcher_review_status':'pending'}
    (OUT/'final_validation.json').write_text(json.dumps(outcome,ensure_ascii=False,indent=2),encoding='utf-8')
    inventory=[]
    for path in sorted(OUT.rglob('*')):
        if path.is_file() and path.name!='deliverable_inventory.csv' and '__pycache__' not in path.parts:
            inventory.append({'file':path.relative_to(OUT).as_posix(),'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    with (OUT/'deliverable_inventory.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['file','bytes','sha256']);w.writeheader();w.writerows(inventory)
    print(json.dumps(outcome,ensure_ascii=False))
if __name__=='__main__':main()
