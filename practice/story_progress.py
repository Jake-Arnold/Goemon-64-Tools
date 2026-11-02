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

    @property
    def address(self):return SAVED_BASE+(self.flag_id>>3)

    @property
    def mask(self):return 1<<(self.flag_id&7)


FLAGS = (
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
)


def read_story_state(ram):
    """Small independent samples; failures remain unknown, never inferred zero.

    Samples are not an atomic frame snapshot. Advisories describe observations,
    not proof that the game's complete state is valid/invalid.
    """
    errors={};blocks={}
    for key,address,size in (('saved',SAVED_BASE,16),('bank_a',BANK_A,2),('bank_b',BANK_B,2),
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
        rows.append(dict(key=flag.key,name=flag.label,bank='Saved event data',address=flag.address,
            mask=f'0x{flag.mask:02X}',value='Unavailable' if value is None else ('Set' if value else 'Clear'),
            raw=raw,status='ERROR' if value is None else 'OBSERVED',source=flag.evidence))
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
