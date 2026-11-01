# Import original Goemon 64 item sprites

Game-owned item graphics are not part of this repository. The application can display PNG exports from your own copy of *Mystical Ninja Starring Goemon (N64)*. Do not use unrelated Goemon games or concept art as substitutes.

## Import workflow

1. Export the original sprites/textures you want as `.png` files from your own game files or a source you have permission to use.
2. Rename each PNG to the corresponding filename below.
3. In the toolkit open **Sprites → Import original PNGs from folder** and select that directory.
4. The toolkit copies only recognised names to your local writable sprite directory; these are ignored by Git. It does not upload or bundle the images.

The PNGs are optional. Without them, all 26 cards display labelled placeholders and stay clickable.

## Recognised sprite filenames

| Item / flag | Expected PNG |
|---|---|
| Goemon in party | `goemon_in_party.png` |
| Ebisumaru in party | `ebisumaru_in_party.png` |
| Sasuke in party | `sasuke_in_party.png` |
| Yae in party | `yae_in_party.png` |
| Goemon pipe upgrade | `goemon_pipe_upgrade.png` |
| Ebisumaru hammer upgrade | `ebisumaru_hammer_upgrade.png` |
| Sasuke kunai upgrade | `sasuke_kunai_upgrade.png` |
| Yae katana upgrade | `yae_katana_upgrade.png` |
| Chain Pipe | `chain_pipe.png` |
| Meat Saw Hammer | `meat_saw_hammer.png` |
| Fire Cracker Bomb | `fire_cracker_bomb.png` |
| Flute | `flute.png` |
| Windup Camera | `windup_camera.png` |
| Ice Kunai | `ice_kunai.png` |
| Bazooka | `bazooka.png` |
| Medal of Flames | `medal_of_flames.png` |
| Sudden Impact | `sudden_impact.png` |
| Mini Ebisumaru | `mini_ebisumaru.png` |
| Super Jump | `super_jump.png` |
| Magic Mermaid | `magic_mermaid.png` |
| Triton Shell | `triton_shell.png` |
| Gold Key | `gold_key.png` |
| Blue Sausage | `blue_sausage.png` |
| Pink Fish | `pink_fish.png` |
| Gold Fish | `gold_fish.png` |
| Blue Fish | `blue_fish.png` |

## Notes

- The N64 game may render inventory items as textures on 3D surfaces rather than standalone 2D sprites; use faithful still-image exports where applicable.
- `0x00`/`0x01` are used for binary flags; four weapon upgrades are 0/1/2 and Chain Pipe uses 0/2.
- Sprites are optional and do not affect memory writes.
- Keep personal ROM files, copyrighted textures and user state out of this public repository.
