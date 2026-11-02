"""Scene ID catalog from klorfmorf/Goemon64Recomp src/game/scene_table.cpp.
Additional factual room labels come from pinned mn64rando room_indexes.txt.
Existing labels are retained; unresolved rooms show their native menu index.
This is a reference index, NOT an N64 scene-loading API.
"""
SCENES_TEXT = '''
0|Oedo Castle 1F Tile Room
2|Oedo Castle 1F Entrance
6|Oedo Castle 1F Congo's Feet
12|Oedo Castle 1F-2F Elevator
20|Oedo Castle 2F Congo's Hand
22|Oedo Castle 2F Congo Boss Room
26|Oedo Castle 2F-3F Elevator
40|Oedo Castle Lord's Room
47|Ghost Toys Entrance
48|Ghost Toys 1F Elevator Shogi Room
49|Ghost Toys 1F Crane Room
50|Ghost Toys 1F Spike Room
53|Ghost Toys 1F Flower Blooming Key Room
60|Ghost Toys 1F-2F Elevator
62|Ghost Toys 2F Spinning Top Key Room
69|Ghost Toys 2F Billiards Room
73|Ghost Toys 2F-3F Elevator / Darumanyo
90|Festival Temple West Main Entrance
96|Festival Temple East Tank Hallway
101|Festival Temple East Samurai Bomb Room
104|Festival Temple Central Gold Lock Room
110|Festival Temple East Ice Kunai Room
113|Festival Temple North Tsurami Boss Room
129|Gourmet Sub 2F Bazooka Room
130|Gourmet Sub 2F Jetpack Crab Room
133|Gourmet Sub 2F Lava Treadmill Room
138|Gourmet Sub 3F-4F Elevator
139|Gourmet Sub 3F Invisible Path Diamond Key Room
141|Gourmet Sub 3F Treasure Room
145|Gourmet Sub 1F-3F Entrance / Elevator
148|Gourmet Sub 3F Sushi Belt Room
153|Gourmet Sub 3F Floating Tofu Room
157|Gourmet Sub 4F Thaisamba Boss Room
168|Musical Castle 1 Entrance
169|Musical Castle 1 Flame Dango Ryo Room
170|Musical Castle 1 Tall Key & Lock Room
172|Musical Castle 1 Triple Slicer Room
173|Musical Castle 1 Gold Key Fan Room
176|Musical Castle 1 Gold Lock Fan Room
178|Musical Castle 1 Multi-Lock Fork
183|Sogen Hedge Maze
184|Musical Castle 2 Entrance
187|Musical Castle 2 Metal Box Lava Room
189|Musical Castle 2 Diamond Key Platform Elevator
191|Musical Castle 2 B1F Descent
193|Musical Castle 2 B1F Gorgeous Stage
300|Kai Highway
301|Mt. Fuji
302|Mt. Fuji Interior (Base)
303|Mt. Fuji Interior (Summit)
304|Musashi
305|Musashi-Iga Tunnel
306|Iga
307|Yamato
308|Yamato Shrine
309|Yamato - Underwater Cave
310|Yamato - Bamboo Forest
311|Yamato - Turtle Rock
312|Kii-Awaji Island
313|Kii-Awaji - Husband and Wife Rocks
314|Tosa
315|Tosa - Vine Bridge
316|Kompira Mountain 1st Block
317|Kompira Mountain 2nd Block
318|Kompira Mountain 3rd Block
319|Kompira Mountain 4th Block
320|Kompira Shrine
321|Iyo
322|Iyo - Hot Springs
323|Bizen
324|Aki - Nagato
325|Hagi
326|Akiyoshidai
327|Shuhodo Tunnel to Festival Temple
328|Izumo
329|Izumo - Big Tree
330|Inaba
331|Mutsu - Mt. Fear
332|Ugo - Stone Circle
333|Mutsu - Shoreline
334|Japan Sea - Underwater
335|Northeast Tunnel to Festival Village 1
336|Northeast Tunnel to Festival Village 2
337|Mutsu - Path to Festival Village
338|Mutsu - Uzen Tunnel
339|Kanmonkyo Gateway Viewpoint
340|Waterfall of Kegon
341|Dragon Fight
350|Oedo - Bridge to Musashi
351|Oedo Town (West)
352|Oedo Town (North)
353|Oedo Town (South)
354|Oedo - Bridge to Oedo Castle
355|Oedo Town (Northwest)
356|Path to Oedo Castle (Chain Pipe)
357|Stairway to Oedo Castle
358|Outside Oedo Castle
359|Zazen - Gate
360|Zazen - Entrance Bridge
361|Zazen Town (South)
362|Zazen - Kappa Pond
363|Zazen - Waterway
364|Zazen Town (North)
365|Zazen - Golden Temple
366|Zazen - Bridge to Bizen
367|Zazen - Path to Mt. Nyoigatake
368|Zazen - Mt. Nyoigatake
369|Zazen - Bridge to Yamato (Benkei)
370|Zazen - Waterfall
371|Zazen - Ushiwaka
373|Folkypoke Village (East)
374|Folkypoke Village (South)
375|Folkypoke Village (West)
376|Folkypoke Village (Northeast)
377|Festival Village (West)
378|Festival Village (East)
379|Festival Village - Festival Square
380|Festival Village (Northwest)
381|Festival Village - Hidden Lake Area
400|Oedo - Restaurant
401|Zazen - Restaurant
402|Folkypoke - Restaurant
403|Festival Village - Restaurant
404|Sogen - Restaurant
406|Oedo - Riceball Shop
407|Oedo - Armor Shop
408|Zazen - Riceball Shop
409|Zazen - Armor Shop
410|Folkypoke - Riceball Shop
411|Folkypoke - Armor Shop
412|Festival Village - Shop
413|Festival Village - Hidden Lake Shop
414|Sogen - Riceball Shop
415|Sogen - Armor Shop
417|Oedo - Inn
418|Zazen - Inn
419|Folkypoke - Inn
420|Festival Village - Inn
421|Sogen - Inn
423|Oedo - Plasma
424|Zazen - Plasma
425|Folkypoke - Plasma
426|Festival Village - Plasma
429|Oedo Guardhouse
430|Zazen Guardhouse
432|Oedo - Omitsu's Teahouse
433|Kai Highway Teahouse
435|Kii-Awaji Teahouse
436|Kompira Teahouse
437|Iyo Teahouse
438|Izumo Teahouse
440|Folkypoke Tourism Center
441|Kii-Awaji Tourism Center
443|West Oedo House (Drunk)
444|North Oedo House (Boy)
445|North Oedo House (Red Woman)
446|South Zazen House (Old Woman)
447|Kompira Shrine House
449|South Oedo House (Old Woman)
450|South Oedo House (Young Woman)
451|South Oedo House (Man c3)
452|South Oedo House (Empty Gym)
453|South Oedo House (Man c5)
454|Folkypoke House (Boy)
455|Folkypoke House (Old Woman)
456|Folkypoke House (Drunk)
457|Folkypoke House (Red Woman)
458|East Festival House (Dog)
459|East Festival House (Red Woman)
460|East Festival House (Drunk)
461|Northwest Festival House (Old Man)
463|South Oedo House (Occupied Gym)
464|Sasuke Jetpack Training
465|South Oedo - Goemon's House
466|Mt. Fuji - Pipe Maker's House
467|Kompira Shrine Charm Shop
468|Mt. Fear - Witch's House
480|Goemon Impact Minigame
481|Ebisumaru Sweets Minigame
482|Sasuke High Jump Minigame
'''
SCENES = dict((int(line.split('|',1)[0]), line.split('|',1)[1])
              for line in SCENES_TEXT.strip().splitlines())

# Existing labels above take precedence over external room-name annotations.
# Source: abyssonym/mn64rando 9c580d03fe89354f79c3c83ba2e1bcf192f32577
# tables/room_indexes.txt; IDs are hexadecimal warp indices, not file IDs.
ADDITIONAL_SCENES_TEXT = """
1|Oedo Castle Tile Room - Unused
3|Oedo Castle 1F Swatting Robot Silver Key Room
4|Oedo Castle 1F Gold Dango Room
5|Oedo Castle 1F Chain Pipe Fork
7|Oedo Castle 1F Chain Pipe Key Room
8|Oedo Castle 1F Swatting Robot Gold Key Room
9|Oedo Castle 1F Turtle Pad Room
10|Oedo Castle 2F Crusher Key Room
11|Oedo Castle 2F Silver Cat Room
13|Oedo Castle 2F Spike Chain Room
14|Oedo Castle 2F Dango Ninja Room
15|Oedo Castle 2F Congo's Chest
16|Oedo Castle 2F Crusher Platforms
17|Oedo Castle 2F Chain Pipe Moat
18|Oedo Castle 2F Silver Key Room
19|Oedo Castle Gold Key Room - Unused
21|Oedo Castle 2F Blocked Silver Cat Room
23|Congo Boss Room - Unused
24|Null
25|Null
27|Null
28|Oedo Castle Final Room - Unused
29|Null
30|Null
31|Null
32|Null
33|Null
34|Null
35|Null
36|Null
37|Null
38|Null
39|Null
41|Null
51|Ghost Toys 1F Cannon Room
52|Ghost Toys 1F Spike Cannon Boat Room
54|Ghost Toys 1F Shogi Cannon Gold Cat Room
57|Ghost Toys 1F Invisible Ghost Room
58|Ghost Toys 1F Spike Darumanyo Room
59|Ghost Toys 1F Invisible Ghost Key Room
61|Null
63|Ghost Toys 2F Big Spinning Spike Chain Room
64|Ghost Toys 2F Invisible Darumanyo Key Room
65|Ghost Toys 2F Jump Rope Room
66|Ghost Toys 2F Treasure Room
67|Ghost Toys 2F False Floor Gold Key Room
68|Ghost Toys 2F Darumanyo Diamond Lock Room
70|Ghost Toys 2F Spike Cannon Diamond Key Room
71|Null
72|Null
86|Oedo Castle 1st Elevator Room - Unused
91|Festival Temple West Gold Cat Dango Room
92|Festival Temple West Hot Platform Drummer Fox Room
93|Festival Temple West Hot Platform Samurai Room
94|Festival Temple West Hot Platform Gold Key Room
95|Festival Temple West Spike Chain Elly Fant Room
97|Festival Temple East Chain Pipe Room
98|Festival Temple East Meatsaw Hammer Room
99|Festival Temple East Samurai Barrel Arrow Room
100|Festival Temple East Drum Room
102|Festival Temple East Bamboo Barrel Bomb Room
103|Festival Temple East Silver Cat Lock Fork
105|Festival Temple Central Fox Tank Hallway
106|Festival Temple Central Samurai Tank Room
107|Festival Temple Central Accordion Room
108|Festival Temple Central Ring Key Hallway
109|Festival Temple Central Samurai Platform Room
111|Festival Temple North Fish Kite Waterfall Column
112|Festival Temple North Bamboo Path to Boss
114|Null
115|Null
116|Null
117|Null
118|Null
119|Null
120|Null
128|Submarine Bazooka Room - Unused
131|Gourmet Sub 2F Seahorse / Mini Ebisumaru Crosspath
132|Submarine Unknown Room - Unused
134|Gourmet Sub 2F Turret Dango Stockpile Room
135|Gourmet Sub 2F Ramen Soup Corridor
136|Submarine Red Ramen Corridor - Unused
137|Gourmet Sub 2F Underwater Spiny Key & Lock Room
140|Gourmet Sub 3F Fox Ramen Platforms & Diamond Lock Fork
142|Gourmet Sub 3F Sword Robot Key Room
143|Null
144|Gourmet Sub 3F Blaster Crab Room
146|Null
147|Null
149|Gourmet Sub 3F Chain Pipe Lava Room
150|Gourmet Sub 3F Chain Pipe Avoidance Room
151|Gourmet Sub 3F Chain Pipe Ice Kunai Combination Room
152|Gourmet Sub 2F-3F Ramen Soup Arrow Room
154|Null
155|Null
156|Null
171|Musical Castle 1 Straight Slicer Room
174|Musical Castle 1 High Jump Gold Key Waves Room
175|Musical Castle 1 Drum Jump Waves Room
177|Musical Castle 1 Waves Turret Connecting Room
179|Musical Castle 1 B1F Hammer Thrower Room
180|Musical Castle 1 B1F Rotating Cube Diamond Key Room
181|Musical Castle 1 Mini Gold Key Big Wave Generator Room
182|Musical Castle 1 Big Aquarium Room
185|Musical Castle 2 Beyond Entrance Platforms Room
186|Musical Castle 2 Left Entrance Treadmill Room
188|Musical Castle 2 Gold Cat Hallway
190|Musical Castle 2 Right Entrance Slope Room
192|Musical Castle 2 B1F Kaleidoscope Room
343|Mermaid Waterfall - Unused
346|Kompira Shrine - Unused
347|Lake Tree - Unused
372|Null
384|Zazen Waterway - Unused
405|Unknown Town Restaurant - Unused
416|Unknown Town Shop - Unused
422|Unknown Town Inn - Unused
427|Unknown Town Plasma - Unused
428|Unknown Town Plasma - Unused
431|Null
434|Awaji Island Coffee Shop - Unused
439|Null
442|Unknown Town Guardhouse - Unused
448|Unknown Town House - Unused
462|Unknown Training Gym - Unused
"""
EXTERNAL_SCENE_NAMES = dict((int(line.split('|',1)[0]), line.split('|',1)[1])
                            for line in ADDITIONAL_SCENES_TEXT.strip().splitlines())
SCENES.update((stage,name) for stage,name in EXTERNAL_SCENE_NAMES.items() if stage not in SCENES)


def unidentified_scene_name(map_id):
    if type(map_id) is not int or not 0<=map_id<=0x1E3:
        return 'Unknown / unlisted'
    from practice.scene_controls import native_debug_selection
    try:
        target=native_debug_selection(map_id,{map_id:'Unidentified'})
        return f'Unidentified room ({target["label"]})'
    except ValueError:
        return 'Unknown / unlisted'


def scene_label(map_id):
    name=SCENES[map_id] if map_id in SCENES else unidentified_scene_name(map_id)
    return f'{map_id} (0x{map_id:03X}): {name}'
