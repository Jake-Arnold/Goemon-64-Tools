"""Curated US story observations from ROM traces and gameplay; never writes RAM."""
from dataclasses import dataclass

SAVED_BASE = 0x8015C608
BANK_A = 0x80168E90
BANK_B = 0x80168EF8


@dataclass(frozen=True)
class StoryFlag:
    key: str
    label: str
    flag_id: int
    evidence: str
    external: bool = False
    reference_count: int = 0
    reference_example: str = ''

    @property
    def address(self):return SAVED_BASE+(self.flag_id>>3)

    @property
    def mask(self):return 1<<(self.flag_id&7)


CURATED_FLAGS = (
    StoryFlag('benkei_encounter','Benkei encounter recorded',0x025,'ROM script + user tests'),
    StoryFlag('benkei_intro','Benkei first dialogue completed',0x034,'ROM script + user tests'),
    StoryFlag('benkei_defeated','Benkei defeated / crossing permitted',0x033,'ROM script + user report'),
    StoryFlag('thaisamba','Thaisamba progression / later Benkei branch',0x032,'ROM script + existing annotation'),
    StoryFlag('kihachi_referral','Kihachi referral / initialization gate',0x023,'ROM script + native guard + user report'),
    StoryFlag('food_quest','Kihachi food quest active',0x022,'ROM script + existing annotation'),
    StoryFlag('food_known','Kihachi food identity learned',0x024,'ROM script + existing annotation'),
    StoryFlag('food_hint','Kihachi food-hint stage',0x037,'ROM script + existing annotation'),
    StoryFlag('food_hint_given','Kihachi repeated hint given',0x038,'ROM script + existing annotation'),
    StoryFlag('ushi_intro','Ushiwaka introduction seen',0x02D,'ROM script + user report'),
    StoryFlag('blue_request','Three blue fish requested',0x02C,'ROM script + user report'),
    StoryFlag('yellow_request','Five yellow fish requested',0x02B,'ROM script + user report'),
    StoryFlag('red_request','Eight red fish requested',0x02A,'ROM script + user report'),
    StoryFlag('heel_recorded',"Achilles' Heel reward recorded",0x029,'ROM reward script + user report'),
    StoryFlag('temple','Ushiwaka Golden Temple stage',0x028,'ROM script + user relocation test'),
    StoryFlag('training_passed','Mini-Ebisu training passed',0x02E,'ROM success-dialogue reader + user report'),
    StoryFlag('training_failed','Mini-Ebisu training failed',0x02F,'ROM failure/retry-dialogue reader'),
    StoryFlag('training_declined','Mini-Ebisu training declined',0x030,'ROM dialogue reader/writer'),
    StoryFlag('mini_recorded','Mini-Ebisu grant recorded',0x031,'ROM reward reader/writer'),
    StoryFlag('snow_recorded','Miracle Snow progression recorded',0x035,'ROM reward reader/writer'),
    StoryFlag('baron','Met Baron in Iga',0x06F,'Existing annotation + ROM set-pattern lead'),
    StoryFlag('congo_moon_collected','Congo Miracle Moon collected',0x0A4,
              'User reports mask 0x10 sets when collecting the Miracle Moon after Congo, not at boss defeat; not independently reproduced'),
    StoryFlag('lord_event_enabled','Lord of Oedo appearance enabled',0x12D,
              'User-confirmed manual bit test: mask 0x20 enables Lord appearance; initializer func_08000000_710660 requires set'),
    StoryFlag('lord_event_completed','Lord of Oedo respawn suppressed',0x097,
              'User-confirmed manual bit test: byte 0x00 to 0x80 prevents respawning; initializer func_08000000_710660 rejects set; func_08000410_710A70 sets it'),
    StoryFlag('ghost_torch_04','Ghost Toys entrance right torch lit',0x19A,
              'Entrance update func_08006490_6F9970 tests this and ID 0x19B before unlocking; sides from user-confirmed decimal sequences; persistence user-reported'),
    StoryFlag('ghost_torch_08','Ghost Toys entrance left torch lit',0x19B,
              'Entrance update func_08006490_6F9970 tests this and ID 0x19A before unlocking; sides from user-confirmed decimal sequences; persistence user-reported'),
    StoryFlag('ghost_entrance_unlocked','Ghost Toys entrance unlocked',0x19C,
              'Native update sets after both torch bits; initializer reads separately; user reports manual opening without flames and persistence once lit'),
    StoryFlag('oedo_elly_collected','Oedo Castle Mr. Elly Fant collected (map)',0x0FF,
              'User touch capture: 0x00 to 0x80 at 0x8015C627; user reports pickup no longer respawns; not independently replayed'),
    StoryFlag('ghost_arrow_collected','Ghost Toys Mr. Arrow collected (boss location)',0x105,
              'User A/B: mask 0x20 set at 0x8015C628 on pickup, map 57 with unchanged character/pointers; one event trial'),
    StoryFlag('musical_arrow_collected','Musical Castle Mr. Arrow collected (boss location)',0x108,
              'User A/B screenshot: mask 0x01 set at 0x8015C629 on pickup; one event trial, no controls or reversion'),
    StoryFlag('kegon_plasma_hint','Plasma Waterfall of Kegon hint condition',0x044,
              'Existing mn64rando annotation + user Festival Village East NPC capture; ROM branch-pattern lead 0x7A2404; waterfall access not established'),
    StoryFlag('oedo_silver_key_1f','Oedo Castle 1F silver key collected',0x110,
              'User map 7 pickup sets mask 0x01; room file 0x33D definition 5 key_index 0x110; collection history, not current key count'),
    StoryFlag('oedo_silver_key_2f','Oedo Castle 2F silver key collected',0x114,
              'User map 18 pickup sets mask 0x10; room file 0x348 definition 6 key_index 0x114; collection history, not current key count'),
    StoryFlag('oedo_silver_lock_2f','Oedo Castle map 13 silver lock opened',0x113,
              'User map 13 to 14 sets mask 0x08, preserving pickup bits; room 0x343 definition 4 lock_index 0x113 accepts key 0x114'),
    StoryFlag('congo_state_candidate','Congo encounter state? (candidate)',0x132,
              'User A/B: mask 0x04 cleared during same event; cutscene/actor/room hypothesis, not confirmed'),
)


EXTERNAL_EVIDENCE = "External annotation: mn64rando; not locally gameplay-verified"

EXTERNAL_FLAGS = (
    StoryFlag('external_super_pass','Super Pass receipt recorded',0x000,EXTERNAL_EVIDENCE,True,24,'0x748B50'),
    StoryFlag('external_pass_gate','Super Pass gate opened',0x001,EXTERNAL_EVIDENCE,True,4,'0x756FA0'),
    StoryFlag('external_omitsu_ufo','Omitsu UFO conversation recorded',0x007,EXTERNAL_EVIDENCE,True,2,'0x758E80'),
    StoryFlag('external_japan_map','Japan map receipt recorded',0x009,EXTERNAL_EVIDENCE,True,4,'0x77B8E4'),
    StoryFlag('external_sasuke_recruited','Sasuke recruitment recorded',0x00E,EXTERNAL_EVIDENCE,True,5,'0x77C050'),
    StoryFlag('external_chain_pipe','Chain Pipe receipt recorded',0x010,EXTERNAL_EVIDENCE,True,9,'0x7579BC'),
    StoryFlag('external_mokubei_upgrades','Mokubei upgrades available',0x011,EXTERNAL_EVIDENCE,True,6,'0x76D714'),
    StoryFlag('external_silver_weapons','Silver weapon upgrade recorded',0x012,EXTERNAL_EVIDENCE,True,3,'0x77A624'),
    StoryFlag('external_fire_ryo','Fire Ryo receipt recorded',0x013,EXTERNAL_EVIDENCE,True,3,'0x77AD8C'),
    StoryFlag('external_koryuta_freed','Koryuta freed',0x014,EXTERNAL_EVIDENCE,True,3,'0x77B4A8'),
    StoryFlag('external_wise_man_ghost','Wise Man ghost meeting recorded',0x015,EXTERNAL_EVIDENCE,True,4,'0x76A13C'),
    StoryFlag('external_witch_unpaid','Witch conversation before payment',0x016,EXTERNAL_EVIDENCE,True,2,'0x77C098'),
    StoryFlag('external_kyushu_disappeared','Kyushu disappearance (Muscle Gym unlock)',0x017,EXTERNAL_EVIDENCE+'; user reports this enables Muscle Gym appearance in Oedo Town',True,37,'0x757024'),
    StoryFlag('external_dharmanyo_defeated','Dharmanyo defeat recorded',0x018,EXTERNAL_EVIDENCE,True,31,'0x74956C'),
    StoryFlag('external_gold_weapons','Gold weapon upgrade recorded',0x01A,EXTERNAL_EVIDENCE,True,3,'0x782F0C'),
    StoryFlag('external_sudden_instructions','Sudden Impact instructions viewed',0x01B,EXTERNAL_EVIDENCE,True,3,'0x769C30'),
    StoryFlag('external_sudden_granted','Sudden Impact grant recorded',0x01C,EXTERNAL_EVIDENCE,True,3,'0x769A78'),
    StoryFlag('external_mermaid_failed','Mermaid training failure recorded',0x01D,EXTERNAL_EVIDENCE,True,1,'0x76A130'),
    StoryFlag('external_mermaid_passed','Mermaid training success recorded',0x01E,EXTERNAL_EVIDENCE,True,1,'0x76A124'),
    StoryFlag('external_mermaid_granted','Mermaid magic grant recorded',0x01F,EXTERNAL_EVIDENCE,True,4,'0x76A674'),
    StoryFlag('external_super_jump_granted','Super Jump grant recorded',0x020,EXTERNAL_EVIDENCE,True,4,'0x764728'),
    StoryFlag('external_super_jump_instructions','Super Jump instructions viewed',0x021,EXTERNAL_EVIDENCE,True,3,'0x76AA14'),
    StoryFlag('external_priest_declined','Priest training offer declined',0x026,EXTERNAL_EVIDENCE,True,2,'0x764740'),
    StoryFlag('external_priest_key','Priest training-key receipt recorded',0x027,EXTERNAL_EVIDENCE,True,3,'0x764734'),
    StoryFlag('external_yae_recruited','Yae recruitment recorded',0x03A,EXTERNAL_EVIDENCE,True,2,'0x763A24'),
    StoryFlag('external_priest_son','Priest son conversation recorded',0x03B,EXTERNAL_EVIDENCE,True,2,'0x765590'),
    StoryFlag('external_tsurami_defeated','Tsurami defeat recorded',0x040,EXTERNAL_EVIDENCE,True,4,'0x749E00'),
    StoryFlag('external_sudden_passed','Sudden Impact training success recorded',0x05F,EXTERNAL_EVIDENCE,True,1,'0x769A84'),
    StoryFlag('external_sudden_failed','Sudden Impact training failure recorded',0x060,EXTERNAL_EVIDENCE,True,2,'0x769A90'),
    StoryFlag('external_super_jump_passed','Super Jump training success recorded',0x061,EXTERNAL_EVIDENCE,True,1,'0x76A8D4'),
    StoryFlag('external_super_jump_failed','Super Jump training failure recorded',0x062,EXTERNAL_EVIDENCE,True,2,'0x76A8E0'),
    StoryFlag('external_outer_space','Outer-space arrival recorded',0x06B,EXTERNAL_EVIDENCE,True,1,'0x77E140'),
    StoryFlag('external_outer_space_departure','Outer-space departure in progress',0x06C,EXTERNAL_EVIDENCE,True,4,'0x77DDB0'),
    StoryFlag('external_sudden_jump_start','Sudden Impact / Super Jump start signal',0x079,EXTERNAL_EVIDENCE,True,2,'0x769BE8'),
    StoryFlag('external_benkei_mermaid_start','Benkei / Mermaid minigame start signal',0x07A,EXTERNAL_EVIDENCE,True,4,'0x76A11C'),
    StoryFlag('external_mini_start','Mini-Ebisu minigame start signal',0x07D,EXTERNAL_EVIDENCE,True,2,'0x76680C'),
    StoryFlag('external_dragon_folkypoke','Folkypoke dragon ride recorded',0x07F,EXTERNAL_EVIDENCE,True,3,'0x794EFC'),
)

PLACEMENT_PICKUPS = (
    StoryFlag('oedo_arrow_placement','Oedo Castle Mr. Arrow collected (boss location)',0x104,
              'ROM instantiated placement: stage 13, file 0x343, definition 13, actor 0x087; not live-tested'),
    StoryFlag('ghost_elly_placement','Ghost Toys Mr. Elly Fant collected (map)',0x100,
              'ROM instantiated placement: stage 52, file 0x367, definition 22, actor 0x086; not live-tested'),
    StoryFlag('festival_elly_placement','Festival Temple Mr. Elly Fant collected (map)',0x101,
              'ROM instantiated placement: stage 95, file 0x384, definition 9, actor 0x086; not live-tested'),
    StoryFlag('festival_arrow_placement','Festival Temple Mr. Arrow collected (boss location)',0x106,
              'ROM instantiated placement: stage 99, file 0x388, definition 16, actor 0x087; not live-tested'),
    StoryFlag('gourmet_elly_placement','Gourmet Sub Mr. Elly Fant collected (map)',0x102,
              'ROM instantiated placement: stage 145, file 0x3AF, definition 23, actor 0x086; not live-tested'),
    StoryFlag('gourmet_arrow_placement','Gourmet Sub Mr. Arrow collected (boss location)',0x107,
              'ROM instantiated placement: stage 152, file 0x3B6, definition 9, actor 0x087; not live-tested'),
    StoryFlag('musical_elly_placement','Musical Castle Mr. Elly Fant collected (map)',0x103,
              'ROM instantiated placement: stage 174, file 0x3C2, definition 14, actor 0x086; not live-tested'),
)

FLAGS = CURATED_FLAGS + EXTERNAL_FLAGS + PLACEMENT_PICKUPS


def read_story_state(ram):
    """Small independent samples; failures remain unknown, never inferred zero.

    Samples are not an atomic frame snapshot. Advisories describe observations,
    not proof that the game's complete state is valid/invalid.
    """
    errors={};blocks={}
    for key,address,size in (('saved',SAVED_BASE,0x64),('bank_a',BANK_A,2),('bank_b',BANK_B,2),
                             ('mini',0x8015C6F0,4),('heel',0x8015C70C,4)):
        if ram is None:blocks[key]=None;continue
        try:
            data=ram.read_guest(address,size)
            if len(data)!=size:raise OSError('Incomplete memory read')
            blocks[key]=data
        except (OSError,ValueError) as exc:
            blocks[key]=None;errors[key]=str(exc)
    saved=blocks['saved']
    values={flag.key:(bool(saved[flag.address-SAVED_BASE]&flag.mask) if saved is not None else None)
            for flag in FLAGS}
    def word(name):return None if blocks[name] is None else int.from_bytes(blocks[name],'big')
    mini=word('mini');heel=word('heel')
    if values['temple'] is None:ushi='Unavailable'
    elif values['temple']:
        if values['training_passed']:ushi='Training passed; grant recorded' if values['mini_recorded'] else 'Training passed; grant not recorded'
        elif values['training_declined']:ushi='Temple training offer declined'
        elif values['training_failed']:ushi='Temple training failed; retry dialogue'
        else:ushi='Golden Temple stage reached'
    else:
        ushi=next((label for key,label in (
            ('heel_recorded','Fish-sequence reward recorded'),('red_request','Eight red fish requested'),
            ('yellow_request','Five yellow fish requested'),('blue_request','Three blue fish requested'),
            ('ushi_intro','Introduction seen')) if values[key]),'Introduction not recorded')
    if values['kihachi_referral'] is None:benkei='Unavailable'
    elif values['kihachi_referral']:benkei='Kihachi referral recorded'
    elif values['thaisamba']:benkei='Later Miracle Item dialogue condition set'
    elif values['benkei_defeated']:benkei='Fight completed; crossing permitted'
    elif values['benkei_intro']:benkei='First dialogue completed'
    elif values['benkei_encounter']:benkei='Encounter recorded; first-dialogue completion clear'
    else:benkei='First encounter not recorded'
    notes=[]
    if values['mini_recorded'] and mini==0:
        notes.append('Mini-Ebisu grant is recorded but ownership is zero; the reward branch may be skipped.')
    elif values['mini_recorded'] is False and mini==1:
        notes.append('Mini-Ebisu ownership is present while its grant flag is clear.')
    if values['heel_recorded'] and heel==0:
        notes.append("Achilles' Heel reward is recorded but inventory is zero.")
    elif values['heel_recorded'] is False and heel==1:
        notes.append("Achilles' Heel inventory is present while its progression flag is clear.")
    for key,value in (('mini',mini),('heel',heel)):
        if value is not None and value not in (0,1):notes.append(f'{key} ownership word has an unexpected value 0x{value:08X}.')
    return dict(blocks=blocks,values=values,errors=errors,mini=mini,heel=heel,
                ushiwaka=ushi,benkei=benkei,advisories=notes)


def story_rows(state):
    """Simple display records shared by story table and live memory watches."""
    rows=[];saved=state['blocks']['saved']
    for flag in FLAGS:
        value=state['values'][flag.key]
        raw='—' if saved is None else f'0x{saved[flag.address-SAVED_BASE]:02X}'
        evidence=f'ID 0x{flag.flag_id:03X}; '+flag.evidence
        if flag.external:evidence+=f'; {flag.reference_count} opcode-pattern leads; first decompressed ROM {flag.reference_example}'
        rows.append(dict(key=flag.key,name=flag.label,bank='Saved event data',address=flag.address,
            mask=f'0x{flag.mask:02X}',value='Unavailable' if value is None else ('Set' if value else 'Clear'),
            raw=raw,status='ERROR' if value is None else 'OBSERVED',source=evidence))
    for key,label,address in (('bank_a','Bank A: first 16 bits',BANK_A),('bank_b','Bank B: first 16 bits',BANK_B)):
        data=state['blocks'][key];raw='—' if data is None else '0x'+data.hex().upper()
        rows.append(dict(key=key,name=label,bank=label.split(':')[0],address=address,mask='—',
            value=raw,raw=raw,status='ERROR' if data is None else 'RAW',
            source='Matching bank helpers; lifecycle/scene meanings not established'))
    for key,label,address in (('mini','Mini-Ebisu ownership word',0x8015C6F0),('heel',"Achilles' Heel inventory word",0x8015C70C)):
        value=state[key];raw='—' if value is None else f'0x{value:08X}'
        rows.append(dict(key=key,name=label,bank='Inventory',address=address,mask='—',
            value='Unavailable' if value is None else ('Absent' if value==0 else 'Present' if value==1 else 'Unexpected'),
            raw=raw,status='ERROR' if value is None else 'OBSERVED' if value in (0,1) else 'CHECK',
            source='ROM reward-script word write; separate from progression flag'))
    return rows
