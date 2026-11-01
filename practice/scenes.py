"""Scene ID catalog from klorfmorf/Goemon64Recomp src/game/scene_table.cpp.
Only explicitly transcribed IDs are named. Unknown IDs remain numeric.
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

def scene_label(map_id):
    return f'{map_id} (0x{map_id:03X}): {SCENES.get(map_id, "Unknown / unlisted")}'
