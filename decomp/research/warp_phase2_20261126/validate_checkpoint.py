#!/usr/bin/env python3
"""ROM-free consistency of the research checkpoint only; never certifies native proof."""
import hashlib,json
from collections import Counter
from pathlib import Path
from replay import META,ROM,COMPILER
K=Path(__file__).resolve().parent

def need(v,why):
    if not v:raise ValueError(why)

def read(n):return json.loads((K/'evidence'/n).read_text())

def check():
    pool=read('pool-proof.json');probes=read('probes.json');need(len(pool)==6 and len(probes)==36,'attempt count');need(len({x['source'] for x in probes})==36,'duplicate attempt')
    for x in probes:
        need(hashlib.sha256((K/'sources'/x['source']).read_bytes()).hexdigest()==x['source_sha256'],'probe source drift')
        need(x['compiler_sha256']==COMPILER,'compiler drift')
    for r,meta in META.items():
        names={x[0] for x in meta};pp=[x for x in pool if x['region']==r];need({x['name'] for x in pp}==names,'pool target drift');byname={x['name']:x for x in pp}
        for x in pp:
            need(x['compiler_sha256']==COMPILER and not x['named_original_gate_exact'] and all(x[k] for k in ('raw_local_text_and_relocations_exact','linked_original_text_and_extent_exact','original_pool_exact','second_source_independent_replay_exact')),'pool proof')
            need(len(x['negative_controls'])==4 and all(c['rejected'] for c in x['negative_controls']),'negative controls')
            for a in x['attempts']:need(hashlib.sha256((K/'sources'/a['source']).read_bytes()).hexdigest()==a['sha256'],'pool source drift')
        p=read(r+'-full.json');need(p['status']=='LOCAL_DUAL_REFERENCE_EXACT_PENDING_CANONICAL_VALIDATOR' and p['stage']=='complete' and p['retail_exact'] and p['retail_sha1']==ROM[r][0],'full trial status')
        need({x['name'] for x in p['native']}==names and all(x['source_sha256']==byname[x['name']]['native_sha256'] for x in p['native']),'native source drift')
        links=p['links'];need(set(links)=={'named','shadow','native'},'link coverage')
        for k,v in links.items():
            need(v['expanded_sha1']==ROM[r][1] and v['function_identities']==7376 and v['semantic_relocation_count']==(82080 if r=='usa' else 80652) and v['stable_globals']==(26714 if r=='usa' else 26393),'link identities')
            need(all(v[i] for i in ('expanded_rom_exact','function_identities_exact','globals_exact','ownership_exact')) and v['first_rom_mismatch'] is None,'link equality')
            need(v['ordinary_named_comparator_exact']==(k=='named'),'named comparator must remain unequal to native/shadow')
        d=p['semantic_relocation_dual_reference'];need(d['entire_named_reference_equals_predecessor'] and d['entire_native_equals_independent_shadow'] and d['comparator_unmodified'] and not d['ordinary_named_comparator_exact'],'full dual reference')
        for k in ('shadow','native'):
            need(links[k]['relocations_removed']==d['named_removed'] and links[k]['relocations_added']==d['local_added'],'full delta drift')
        need(links['shadow']['semantic_relocation_sha256']==links['native']['semantic_relocation_sha256'],'full relocation fingerprint drift')
        removed=Counter({tuple(x):n for x,n in d['named_removed']});added=Counter({tuple(x):n for x,n in d['local_added']});need(sum(removed.values())==sum(added.values())==6,'wrong delta count')
        need({x[-1] for x in removed}=={x['pool_symbol'] for x in pp} and {x[-1] for x in added}=={'.file_12'},'wrong delta symbols')
        need(Counter(x[:3] for x in removed.elements())==Counter(x[:3] for x in added.elements()),'wrong delta positions/types')
        i=p['strict_inventory_delta'];need(i['newly_matching_c']==3 and i['extra_positive_alias_entries']==0 and i['size_annotation_differences']==[],'strict ownership delta')
    return {'status':'RESEARCH_CHECKPOINT_CONSISTENT','functions':6,'original_bytes':712,'negative_controls':24,'canonical_promotion':False}

if __name__=='__main__':print(json.dumps(check(),indent=2))
