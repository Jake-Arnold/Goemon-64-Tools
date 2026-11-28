"""Second-pass semantic purpose evidence, independent of native acceptance."""
from collections import Counter

# Explicit pairs from independently inspected source, not an address delta.
TRANSITIONS = (
    ('03380_3F80','032A4_3EA4','3ADE0','3ADE1','set'),
    ('033B0_3FB0','032D4_3ED4','3ADE0','3ADE1','increment'),
    ('033EC_3FEC','03310_3F10','3ADE0','3ADE1','decrement'),
    ('03428_4028','0334C_3F4C','3ADDE','3ADDF','set'),
    ('03478_4078','0339C_3F9C','3ADDE','3ADDF','increment'),
    ('034D0_40D0','033F4_3FF4','3ADDE','3ADDF','decrement'),
    ('03528_4128','0344C_404C','3ADD8','3ADD9','set'),
    ('03578_4178','0349C_409C','3ADD8','3ADD9','increment'),
    ('035D0_41D0','034F4_40F4','3ADD8','3ADD9','decrement'),
    ('03628_4228','0354C_414C','3ADD6','3ADD7','set'),
    ('03678_4278','0359C_419C','3ADD6','3ADD7','increment'),
    ('036D0_42D0','035F4_41F4','3ADD6','3ADD7','decrement'),
    ('03728_4328','0364C_424C','3ADD4','3ADD5','set'),
    ('0378C_438C','036B0_42B0','3ADD4','3ADD5','increment'),
    ('037E4_43E4','03708_4308','3ADD4','3ADD5','decrement'),
)

# region, original symbol, counterpart (if reviewed), subsystem, alias, operation.
PAIRS = (
    ('func_80001D68_2968','func_80001D08_2908','resource_table','read_masked_file_table_entry','Reads indexed u32 table entry with bit 31 cleared.'),
    ('func_800362DC_36EDC','func_80035F4C_36B4C','object_flags','mark_object_list_bit7','Walks linked nodes, sets flags bit 7 and returns the terminating null pointer.'),
    ('func_801DCCF0_598C00','func_801E2130_59E100','player_resources','adjust_normal_ryo','Adds signed halfword delta to Ryo word; tests signed low halfword, stores 0 or 9999 and returns 1 on bound correction, otherwise 0.'),
    ('func_801E75D4_5A34E4','func_801EC6FC_5A86CC','player_movement','player_four_way_resource_action','Dispatches actor byte +0x60 cases 0-3 to action IDs 0x82/0x8E/0x9B/0xAA; case 0 deducts ten normal-game Ryo. Exact triggering action unknown.'),
    ('func_801EA614_6159F4','func_801EFD44_61A7C4','impact_combat','impact_reward_effect_04_05_a','After null guards, calls charge adjuster with +4 and Ryo adjuster with +5 when predicate >=60; dispatches an effect with scale multiplied by three.'),
    ('func_801EA900_615CE0','func_801F0030_61AAB0','impact_combat','impact_reward_effect_04_05_b','Increments model halfword +0x16 by three; positive-height early return; eligible interaction calls charge +4 and conditional Ryo +5.'),
    ('func_80203AE4_62EEC4','func_80209214_633C94','impact_combat','impact_reward_effect_04_10','Eligible interaction calls charge +4 and conditional Ryo +10; exact actor and predicate meaning unknown.'),
    ('func_80203DFC_62F1DC','func_8020952C_633FAC','impact_combat','impact_reward_effect_04_05_c','Positive-height early return; eligible interaction calls charge +4 and conditional Ryo +5, with effect dispatch.'),
    ('func_80205C00_630FE0','func_8020B330_635DB0','impact_combat','impact_reward_effect_10_20','Two branches decrement a byte counter; one retires without reward, the other calls charge +10 and conditional Ryo +20.'),
    ('func_08000174_70D8B4','func_08000174_711DE4','event_actor','saved_flag0_dependent_actor_update','Checks saved bank C flag 0, consumes actor +0x68 bit 0x4000, conditionally sets bank A flag 0; selects action 0x43/0x44 and installs callback. Exact actor identity unknown.'),
)
SINGLE_USA = (
    ('func_80004170_4D70','system_memory','initialize_system_memory','Zeros 0xCF908 bytes, installs system pointer and initializes fill alpha and framebuffer format fields.'),
    ('func_800041E0_4DE0','system_memory','zero_bytes','Writes zero to each byte for the supplied nonnegative length.'),
    ('func_80004208_4E08','system_memory','copy_bytes_forward','Copies bytes forward from source to destination for supplied nonnegative length; no overlap handling.'),
    ('func_80016660_17260','bit_array','bit_array_set','Sets indexed bit in byte array.'),
    ('func_80016684_17284','bit_array','bit_array_clear','Clears indexed bit in byte array.'),
    ('func_800166AC_172AC','bit_array','bit_array_test','Tests indexed bit and returns normalized boolean 0/1.'),
    ('func_80021444_22044','scene_transition','request_default_entrance','Unless selector equals 0xFF, copies intended room and group, copies entrance metadata and calls follow-up helpers; always requests outer state 0x0B.'),
    ('func_800214E4_220E4','scene_transition','copy_default_entrance_record','Copies table x/y/z, heading and mode into entrance record when any coordinate nonzero; otherwise clears all five fields.'),
    ('func_800216B0_222B0','rendering','set_viewport_bounds','Rejects negative left/top, right >320, bottom >240 or inverted bounds before writing four bounds and returning 1.'),
    ('func_8001F878_20478','geometry_math','reverse_angle_triplet','Adds 512 modulo 1024 to first and third angles; replaces second with 512 minus old value modulo 1024.'),
    ('func_80036308_36F08','object_flags','dispatch_object_flag_type','Null guard then dispatches low seven flag bits 1/2/3 to distinct helper sequences; other values do nothing.'),
    ('func_800102E0_10EE0','resource_table','reset_indexed_resource_record','For index other than -1 clears selected fields in indexed 16-byte record.'),
    ('func_80212010_670FC0','resource_table','reset_39_resource_records','Calls indexed resource-record reset helper for 39 global entries.'),
)
SDK = {
    'osSpTaskYielded': ('rsp_task','Tests SP status bit 0x100 and, if bit 0x80 set, updates task flags at +4 and clears bit 1.'),
    'osSpTaskStartGo': ('rsp_task','Waits for SP device not busy, then writes SP status command 0x125.'),
    'osSpTaskYield': ('rsp_task','Writes SP status command 0x400 to request yield.'),
    'guPerspective': ('graphics_math','Builds float perspective matrix and converts it to fixed matrix.'),
    'guMtxIdent': ('graphics_math','Builds float identity matrix and converts it to fixed matrix.'),
    'guNormalize': ('graphics_math','Scales three components by reciprocal Euclidean magnitude; no zero-length guard.'),
    'osContGetQuery': ('controller_io','Delegates to controller initialization-data helper.'),
    'alUnlink': ('audio','Unlinks node by updating neighboring links if non-null.'),
    'alLink': ('audio','Inserts node after list head and repairs neighboring links.'),
    'alClose': ('audio','If audio globals nonzero, calls synthesizer deletion and clears globals.'),
    'alInit': ('audio','If audio globals null, installs global pointer and initializes synthesizer.'),
    'osVirtualToPhysical': ('address_translation','Masks direct-mapped KSEG0/KSEG1 addresses to 29 bits; otherwise probes TLB.'),
    '_timeToSamples': ('audio','Converts time using rate field +0x44 and a divisor constant, rounds then clears low four bits.'),
    '_freePVoice': ('audio','Unlinks physical voice and inserts it into list at synthesizer +0x14.'),
    '_collectPVoices': ('audio','Moves each voice from list +0x14 into list +4 until empty.'),
    '__freeParam': ('audio','Pushes parameter node onto list at audio globals +0x2C.'),
    'alSynDelete': ('audio','Clears the first word of synthesizer object; no general memory release claim.'),
    'alMainBusNew': ('audio','Initializes filter with main-bus pull/param callbacks, type 7, and three bus fields.'),
    'alAuxBusNew': ('audio','Initializes filter with auxiliary-bus pull/param callbacks, type 6, and three bus fields.'),
    'alMainBusParam': ('audio','On parameter 2 appends value to indexed array and increments index; returns zero.'),
    'alAuxBusParam': ('audio','On parameter 2 appends value to indexed array and increments index; returns zero.'),
    'alSaveParam': ('audio','For selector 1 stores word 0; for selector 6 stores word 5; returns zero.'),
    'alFxParam': ('audio','For selector 1 stores supplied value; returns zero.'),
    'alFilterNew': ('audio','Initializes link, pull/param callback pointers, two halfwords and filter type.'),
    'alSaveNew': ('audio','Initializes save filter callbacks/type 3 and fields +0x14 and +0x18.'),
    'memcpy': ('memory','Copies requested bytes forward and returns original destination.'),
    'strlen': ('memory','Scans to first zero byte and returns byte distance from start.'),
    'osCreateMesgQueue': ('os_queue','Initializes wait queues, valid count, first index, capacity and message array.'),
    'osViSwapBuffer': ('video','With interrupts disabled updates next frame pointer and sets state bit 0x10.'),
    'osAiGetLength': ('audio','Reads audio interface length register.'),
    '__osSpGetStatus': ('rsp_task','Reads SP status register.'),
    '__osSpSetStatus': ('rsp_task','Writes SP status register.'),
    'MusPtrBankGetCurrent': ('audio','Returns current pointer-bank global.'),
    '__osGetActiveQueue': ('video','Returns current VI context pointer.'),
}

GAMEPLAY = {'player_movement','character_switch','save_and_pickup_rewards','impact_combat','player_resources','event_actor'}


def refine(index, root):
    def add(region, name, subsystem, alias, operation, scope, confidence='High', extra=()):
        row = index.get((region, name))
        if row is None or row['source'] is None:
            raise ValueError('Missing pinned source for refined role: '+region+' '+name)
        refs = [row['source']['path'], *extra]
        if not all((root/p).is_file() for p in refs):
            raise ValueError('Missing refinement evidence: '+name)
        row.update(confidence='Confirmed', behavior=operation, semantic_alias=alias, subsystem=subsystem,
                   evidence=sorted(set(refs)), review_method='manual_refinement', role_confidence=confidence,
                   unresolved='Exact callers, consumers and runtime coverage beyond the stated operation remain unresolved.',
                   role_scope=scope, role_evidence=sorted(set(refs)))
        return row

    def pair(us, jp, subsystem, alias, operation, scope, confidence='High', extra=()):
        a = add('usa', us, subsystem, alias, operation, scope, confidence, extra)
        b = add('japan_0', jp, subsystem, alias, operation, scope, confidence, extra)
        for x,y in ((a,b),(b,a)):
            x['counterpart'] = {'region':y['region'],'name':y['name'],
                'evidence':sorted(set(x['evidence']+y['evidence'])),
                'regional_difference':'Shared described operation; other differences not ruled out.'}

    for row in index.values():
        # Confidence in a body is not confidence in its role in the game.
        row.update(role_confidence='Unknown', role_scope='unknown', role_evidence=[], dependency_leads=[])
        if row['review_method'] == 'manual':
            row.update(role_confidence=row['confidence'], role_scope='gameplay_subsystem' if row['subsystem'] in GAMEPLAY else 'engine_subsystem', role_evidence=list(row['evidence']))
        elif row['subsystem'] == 'resource_registration':
            row.update(role_confidence='High', role_scope='resource_family', role_evidence=list(row['evidence']))
    for u,j,state,flag,op in TRANSITIONS:
        lower = {'3ADD4':'3ADD6','3ADD6':'3ADD8','3ADD8':'3ADDE','3ADDE':'3ADE0'}.get(state)
        text = f'{op.capitalize()} transition state byte +0x{state}; clears companion byte +0x{flag}.'
        if lower:
            text += f' Resets nested state +0x{lower} through its setter.'
        if state == '3ADD4' and op == 'set':
            text += ' Sets retraces_per_game_step to 2.'
        pair('func_800'+u,'func_800'+j,'scene_transition',f'transition_{op}_{state.lower()}',text,'engine_subsystem','Confirmed',('MAP_TRANSITION_TRACE.md',))
    for u,j,sub,alias,op in PAIRS:
        extra = ('../docs/IMPACT_BATTLE_MEMORY_TRACE.md',) if sub == 'impact_combat' else ('save_resources.h',) if sub in ('player_resources','player_movement') else ()
        pair(u,j,sub,alias,op,'gameplay_subsystem' if sub in GAMEPLAY else 'engine_subsystem', 'High', extra)
        if sub in ('impact_combat','player_resources','player_movement','event_actor'):
            for k in (('usa',u),('japan_0',j)):
                index[k]['prior_research'] = 'https://github.com/Jake-Arnold/Goemon-64-Tools/pull/255'
    for k in (('usa','func_801D3A68_5FEE48'),('japan_0','func_801D9188_603C08')):
        row = index[k]
        row['semantic_alias'] = 'impact_ryo_adjust'
        row['role_evidence'].append('../docs/IMPACT_BATTLE_MEMORY_TRACE.md')
        row['prior_research'] = 'https://github.com/Jake-Arnold/Goemon-64-Tools/pull/255'
        row['unresolved'] = 'Exact caller/actor conditions and independent JP gameplay replay remain unresolved.'
    for n,sub,alias,op in SINGLE_USA:
        add('usa',n,sub,alias,op,'engine_subsystem','High')
    for row in list(index.values()):
        if row['name'] in SDK and row['source'] and row['review_method'] != 'manual':
            sub,op = SDK[row['name']]
            add(row['region'],row['name'],'sdk_'+sub,row['name'],op,'library','Confirmed')
    # Dependency leads are not classifications of their callers. No propagation of gameplay aliases.
    for row in index.values():
        row['behavior_confidence'] = row['confidence']
        for name in row['callees']:
            target = index.get((row['region'], name))
            if target and target['semantic_alias'] and target['role_confidence'] in ('Confirmed','High'):
                row['dependency_leads'].append({'name':name,'alias':target['semantic_alias'],'subsystem':target['subsystem']})


def role_summary(rows):
    levels = ('Confirmed','High','Medium','Unknown')
    counts = Counter(r['role_confidence'] for r in rows)
    return {'role_confidence':{c:counts[c] for c in levels},
            'role_scope':dict(Counter(r['role_scope'] for r in rows)),
            'refined_manual':sum(r['review_method']=='manual_refinement' for r in rows),
            'dependency_leads':sum(bool(r['dependency_leads']) for r in rows)}
