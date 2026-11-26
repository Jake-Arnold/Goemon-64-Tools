from pathlib import Path
p=Path(__file__).parent/'sources'
m={'D_8015C5C8_15D1C8':'g_system_ptr','D_801FC60C_5B851C':'D_8020151C_5BD4EC','D_801FC600_5B8510':'D_80201510_5BD4E0','func_802154FC_5D09CC':'func_8021A28C_5D581C','func_801FB270_5B7180':'func_80200180_5BC150','func_80215330_5D0800':'func_8021A0C0_5D5650','func_802154F0_5D09C0':'func_8021A280_5D5810','func_8003521C_35E1C':'func_80034E8C_35A8C','func_80215230_5D0700':'func_80219FC0_5D5550'}
for f in p.glob('usa_*.c'):
 s=f.read_text()
 for k,v in m.items():s=s.replace(k,v)
 (p/f.name.replace('usa_','japan_0_')).write_text(s)
