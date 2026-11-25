# -*- coding: utf-8 -*-
"""
Step 3 Corpus Builder: Wasteland Voices v1.0.0
Adds:
 - Quest state gossip (5500-5639)
 - Player reactivity: Power Armor (5800-5809)
 - Player reactivity: Heavy Weapons (5830-5835)
 - Player reactivity: Freak Companions (5850-5857)
 - Player reactivity: Low IQ (5880-5886)
Preserves:
 - Base sFall Party Control lines (0..604)
 - Base Small Talk lines (5000..5475)
Strictly enforces CP1251 for Russian and ASCII for English.
"""

import os
import sys

# Import base lines
from build_full_corpus import RU_LINES, EN_LINES, BASE_DIR
from update_custom_with_base import BASE_RU_CUSTOM, BASE_EN_CUSTOM

Q_RU = {}
Q_EN = {}

# --- KLAMATH QUESTS (5500-5521) ---
Q_RU[5500] = "В подземельях Траппертауна завелась гигантская тварь. Трапперы боятся спускаться за шкурами."
Q_EN[5500] = "Giant beast nested in Trapper Town drifts. Trappers dread crawling down for pelt trapping."

Q_RU[5501] = "Слышал этот писк под полом? Крысы под городом собираются в стаи размером с брамина."
Q_EN[5501] = "Hear that squealing beneath floorboards? Under-rats are schooling up in packs the size of brahmin."

Q_RU[5502] = "Если полезешь в тоннели Траппертауна -- возьми дробовик. Там правит какой-то крысиный вожак."
Q_EN[5502] = "Crawling into Trapper Town tunnels? Pack a scattergun. Some giant rodent warlord rules down there."

Q_RU[5503] = "Вчера крыса оттяпала трапперу два пальца прямо в постели. Пора выжигать эту дрянь."
Q_EN[5503] = "A wharf rat chewed two toes off a sleeping skinner last night. Time to burn out that filth."

Q_RU[5504] = "Крысиного Бога наконец прикончили! Траппертаун снова может спокойно ставить капканы."
Q_EN[5504] = "Rat God is butchered at last! Trapper Town skinners can string their leg-irons in peace."

Q_RU[5505] = "Говорят, тварь из подземелий была ростом с человека. Слава богу, ее разорвали на куски."
Q_EN[5505] = "Word is the tunnel beast stood tall as a grown man. Praise lead and powder it was blasted to bits."

Q_RU[5506] = "После смерти крысиного вожака мелкие грызуны разбежались по болотам. Воздух стал чище."
Q_EN[5506] = "With the big rat dead, the scuttlers scattered into the marsh. Town breathes easier today."

Q_RU[5507] = "Трапперы празднуют у Бакнеров победу над чудовищем из подвала. Самогон льется рекой."
Q_EN[5507] = "Trappers drinking to the underground monster's slaughter at Buckner's. Rotgut flowing freely."

Q_RU[5508] = "Смайли ушел за шкурами в Токсичные пещеры три недели назад. Миссис Бакнер вся в слезах."
Q_EN[5508] = "Smiley hiked north to Toxic Caves three weeks back. Widow Buckner weeps into her aprons."

Q_RU[5509] = "В Токсичных пещерах кислота прожигает сапоги за минуту. Вряд ли Смайли оттуда выберется."
Q_EN[5509] = "Green acid in Toxic Caves eats boot leather in minutes. Doubt Smiley walks out alive."

Q_RU[5510] = "Майда не находит себе места. Ее жених сгинул на севере, а золотые гекко не прощают ошибок."
Q_EN[5510] = "Maida's beside herself with worry. Her man vanished north, and golden lizards don't give quarter."

Q_RU[5511] = "Если встретишь Смайли в ядовитых норах -- помоги ему. Хотя скорее всего его уже обглодали."
Q_EN[5511] = "Spot Smiley in those caustic drifts, lend a hand. Though carrion birds likely picked him clean."

Q_RU[5512] = "Смайли вернулся из кислотных пещер! Весь обожженный, но живой. Свадьбе у Бакнеров быть!"
Q_EN[5512] = "Smiley crawled out of caustic caves! Scored by acid, but breathing. Buckner wedding is on!"

Q_RU[5513] = "Говорят, какой-то чужак вытащил Смайли прямо из пасти золотых гекко. Настоящее чудо."
Q_EN[5513] = "Folks swear a wanderer snatched Smiley right out of golden gecko jaws. Downright miracle."

Q_RU[5514] = "Смайли снова у стойки. Хлещет самогон кружками и клянется больше не соваться в кислоту."
Q_EN[5514] = "Smiley is back on his barstool. Guzzling hooch and swearing off toxic holes forever."

Q_RU[5515] = "Майда сияет как новенькая гильза. Ее слезы наконец высохли благодаря спасению жениха."
Q_EN[5515] = "Maida's grinning bright as polished brass. Her weeping stopped once her man walked through the door."

Q_RU[5516] = "Бедняга Торр плачет на пастбище. Кто-то уводит браминов по ночам, а сваливают всё на жуколюдей."
Q_EN[5516] = "Poor Torr sobs in pastures. Someone rustles brahmin at moonrise and blames imaginary bug-men."

Q_RU[5517] = "Братья Дантоны продают подозрительно дешевое мясо. Все знают, чье клеймо срезано со шкур."
Q_EN[5517] = "Dunton boys sell suspicious cheap flanks. Everybody knows whose brand was scraped off."

Q_RU[5518] = "Дантонам наконец начистили рыло за кражу скота! Торр больше не боится ночных теней."
Q_EN[5518] = "Duntons caught lead and a busted nose over rustled steers! Torr fears no shadows tonight."

Q_RU[5519] = "Стада Бакнеров теперь в безопасности. Братьям-конокрадам дали крепкий укорот."
Q_EN[5519] = "Buckner herds graze without worry now. Cattle rustlers got taught a terminal lesson."

Q_RU[5520] = "Торр опять потерял всех браминов... Беднягу совсем затюкали в поселке."
Q_EN[5520] = "Torr lost the herd again... Town bullies mocked the poor boy till he ran crying."

Q_RU[5521] = "Без коров Бакнерам придется затянуть пояса. Зима в Кламате будет голодной."
Q_EN[5521] = "Short on cows, Buckners must pinch pennies. Winter in Klamath is going to be lean and cold."

# --- THE DEN QUESTS (5530-5545) ---
Q_RU[5530] = "Мецгер держит торговца Вика в задней комнате. Заставляет чинить сломанные рации под дулом."
Q_EN[5530] = "Metzger keeps trader Vic padlocked in back. Forces him to solder wireless sets at shotgun point."

Q_RU[5531] = "Старик Вик продал работорговцам бракованную рацию. Теперь он отрабатывает долг в цепях."
Q_EN[5531] = "Old Vic peddled broken tech to slaver captains. Now he pays his tab in collar iron."

Q_RU[5532] = "Вика выкупили из гильдии работорговцев! Мецгер скрежетал зубами, но золото пересчитал."
Q_EN[5532] = "Vic bought his freedom off the slaver block! Metzger ground teeth, but counted the gold clean."

Q_RU[5533] = "Слышал, старый Вик покинул Дыру с каким-то бродягой. Повезло толстяку унести ноги."
Q_EN[5533] = "Heard fat Vic skipped town with a wanderer. Lucky tub of lard to keep his hide intact."

Q_RU[5534] = "Гильдия Мецгера перебита! Работорговцы валяются в лужах крови! Господи, неужели это правда?!"
Q_EN[5534] = "Metzger's guild was wiped out! Slavers bleeding in the gutters! Merciful lord, is it real?!"

Q_RU[5535] = "Мецгера прикончили как бешеную собаку. Теперь рабы свободны, а на улицах пахнет порохом."
Q_EN[5535] = "Metzger got put down like a rabid mongrel. Auction pens are open and cordite hangs heavy."

Q_RU[5536] = "Лара собирает людей на свалке. Говорят, они пойдут резать банду Тайлера на складе у церкви."
Q_EN[5536] = "Lara's gathering cutthroats at junkyard. Word is they'll storm Tyler's church warehouse."

Q_RU[5537] = "Тайлер и его громилы стерегут ящики с наркотой. Если Лара сунется -- там будет мясорубка."
Q_EN[5537] = "Tyler's brutes guard chem crates. Lara pushes her luck, street turns into a butcher shop."

Q_RU[5538] = "Бойня у церкви закончилась. Людей Тайлера перестреляли, теперь Лара заправляет на складе."
Q_EN[5538] = "Church warehouse shootout concluded. Tyler's crew took dirt naps; Lara runs the stash now."

Q_RU[5539] = "Ночью на складе трещали автоматы. Утром могильщик вывез целую телегу свежих покойников."
Q_EN[5539] = "Grease guns rattled past midnight. Gravedigger hauled a cart piled high with stiff carcasses."

Q_RU[5540] = "Банда Лары полегла у ворот церкви. Тайлер смеется и раздает винт своим шестеркам."
Q_EN[5540] = "Lara's outfit got chewed to pieces at church gates. Tyler's handing out victory Jet to goons."

Q_RU[5541] = "Одной бандой меньше, одной больше... В Дыре вывески меняются, а кровь в грязи всё та же."
Q_EN[5541] = "One gang drops, another rises... Signs change in the Den, but red mud tastes identical."

Q_RU[5542] = "В развалинах по ночам воет призрак женщины. Ищет золотой кулон и пугает бродяг до полусмерти."
Q_EN[5542] = "Ghost woman wails inside ruins after dusk. Weeping for a gold locket, scaring vagrants pale."

Q_RU[5543] = "Не ходи к заброшенному дому в темноте. Там стонет мертвая Анна, требуя вернуть медальон."
Q_EN[5543] = "Steer clear of the burnt house at midnight. Dead Anna shrieks for her stolen heirloom."

Q_RU[5544] = "Призрак Анны наконец упокоился! Медальон вернули в могилу, вой в руинах прекратился."
Q_EN[5544] = "Anna's specter sleeps at last! Locket laid in her grave, howling in the cellar died down."

Q_RU[5545] = "Кости Анны похоронили по-человечески. Даже в таком мерзком месте нашлась минута милосердия."
Q_EN[5545] = "Anna's bones got a decent Christian burial. Strange to find a sliver of mercy in this pit."

# --- MODOC QUESTS (5550-5563) ---
Q_RU[5550] = "На Призрачной ферме мертвецы на кольях горят синим пламенем! Земля там проклята навеки!"
Q_EN[5550] = "Glowing corpses impaled on stakes at Ghost Farm! Blue fire burns their bones; soil is cursed!"

Q_RU[5551] = "Совет Модока хочет собрать ополчение и сжечь Призрачную ферму вместе со всеми чертями."
Q_EN[5551] = "Modoc town council wants to muster militia and torch the Ghost Farm to cinder."

Q_RU[5552] = "Слэги -- не демоны, а живые люди! Они подписали торговый договор с Модоком на поставку зерна!"
Q_EN[5552] = "The Slags are no ghouls, but living folk! Signed a grain barter treaty with Modoc council!"

Q_RU[5553] = "Подземный народ вышел к нам с миром. Теперь у нас будут полные амбары и крепкая охрана."
Q_EN[5553] = "Under-dwellers trade in open daylight now. Granaries will be full and crops protected."

Q_RU[5554] = "Призрачную ферму залили кровью! Всех подземных жителей перебили из дробовиков до последнего."
Q_EN[5554] = "Ghost Farm ran red with slaughter! Shotguns cleared the subterranean tunnels down to infants."

Q_RU[5555] = "Резня на ферме была ужасной. Посевы сожжены, Модок остался один на один с засухой."
Q_EN[5555] = "Butchery at the farm solved nothing. Crops torched; Modoc sits alone facing dry starvation."

Q_RU[5556] = "Бальтазар потерял сына. Маленький Джонни пропал, а его собака Лэдди лает на колодец."
Q_EN[5556] = "Balthas lost his only boy. Little Jonny vanished, and Laddie the dog barks down the dry well."

Q_RU[5557] = "Кожевенник почернел от горя. Если Джонни упал в колодец -- живым его уже не достать."
Q_EN[5557] = "Tanner is sick with grief. If Jonny tumbled down the masonry, he's crushed stone cold."

Q_RU[5558] = "Джонни нашелся! Его прятали Слэги под землей! Бальтазар плачет от счастья в мастерской!"
Q_EN[5558] = "Jonny came home! The Slags kept him safe underground! Balthas is weeping tears of joy!"

Q_RU[5559] = "Мальчишка дома и обнимает пса Лэдди. Вся улица празднует возвращение сорванца."
Q_EN[5559] = "The boy is back hugging Laddie by the hearth. Entire street celebrating the little scamp."

Q_RU[5560] = "Джонни мертв... На дне пещеры нашли только детскую куртку. Бальтазар не переживет этого."
Q_EN[5560] = "Jonny is dead... Only a ragged child's coat fetched from the pit. Balthas is a broken man."

Q_RU[5561] = "Горе в семье кожевенника. Горожане обходят дом Бальтазара стороной -- тяжело видеть его боль."
Q_EN[5561] = "Sorrow hangs heavy over the tannery. Folks step softly around Balthas; pain's too raw to watch."

# --- GECKO & VAULT CITY QUESTS (5570-5581) ---
Q_RU[5570] = "Реактор Посейдон плюется паром! Если третий контур лопнет -- радиоактивная волна смоет Гекко!"
Q_EN[5570] = "Poseidon core spitting hot steam! Third coolant conduit fails, atomic fallout cooks Gecko!"

Q_RU[5571] = "В Городе Убежища грозят сравнять нас с землей, если мы не прекратим сливать изотопы в грунтовые воды."
Q_EN[5571] = "Vault City warns they'll shell us to gravel if coolant runoff keeps poisoning regional wells."

Q_RU[5572] = "Гидромагнитный регулятор установлен! Реактор гудит плавно и тихо, радиационный фон упал!"
Q_EN[5572] = "Hydro-magnet regulator seated in core! Reactor hums smooth and cool; rad levels dropped!"

Q_RU[5573] = "Чужак починил наш реактор без единого выстрела! Гарольд сияет, наливает пиво каждому встречному!"
Q_EN[5573] = "A wanderer tuned our plant without spilling a drop! Harold's buying rounds for the whole bar!"

Q_RU[5574] = "Данные диска Волт-Сити загружены в ядро! Энергосеть оптимизирована, тока хватит на весь север!"
Q_EN[5574] = "Vault City data disk patched the logic banks! Grid optimized; power enough for the north!"

Q_RU[5575] = "Теперь Волт-Сити покупает наше электричество! Гули и люди связаны одним проводом!"
Q_EN[5575] = "Vault City purchases our megawatts now! Ghouls and smoothskins bound by the same copper line!"

Q_RU[5576] = "Реактор расплавился! Активная зона прожгла фундамент! Гекко превратился в радиоактивный ад!"
Q_EN[5576] = "Meltdown in sector four! Core burned straight to bedrock! Gecko is a glowing atomic tomb!"

Q_RU[5577] = "Смерть и пепел... Те, кто выжил после аварии, бегут на пустоши, теряя остатки плоти на бегу."
Q_EN[5577] = "Death and hot cinder... Survivors fleeing into salt wastes, shedding skin as they sprint."

Q_RU[5578] = "Граждане Волт-Сити в ярости: фон в водопроводе упал, придраться к гулям больше не за что!"
Q_EN[5578] = "Vault City councilors furious: well monitors read clean; no excuse left to wipe out ghouls!"

Q_RU[5579] = "Совет Первого Гражданина признал полезность Гекко. Энергетический кризис предотвращен."
Q_EN[5579] = "First Citizen council acknowledged Gecko's utility. Regional blackout crisis averted."

Q_RU[5580] = "Линетт скрежещет зубами: дикарь принес мир с мутантами, которого они не хотели."
Q_EN[5580] = "Lynette chews her lip raw: an out-lander brokered peace with muties she aimed to cleanse."

Q_RU[5581] = "Капитан Грегори усилил караулы у ворот: мир с Гекко шаток, граждане боятся заразу."
Q_EN[5581] = "Captain Gregory doubled gate watches: peace with Gecko is uneasy; Citizens dread plague."

# --- BROKEN HILLS QUESTS (5600-5611) ---
Q_RU[5600] = "В урановой шахте встал очиститель воздуха. Забойщики задыхаются от радона, добыча сорвана."
Q_EN[5600] = "Air scrubber choked in uranium drift. Miners suffocating on radon gas; ore quotas ruined."

Q_RU[5601] = "Без детали из Нью-Рино шахта превратится в газовую камеру. Маркус сбился с ног в поисках."
Q_EN[5601] = "Lacking parts out of New Reno, shaft turns into a gas coffin. Marcus scouring trails for parts."

Q_RU[5602] = "Очиститель починен! Вентиляторы ревут, радон выкачан, шахтеры снова гребут уран на-гора!"
Q_EN[5602] = "Scrubber purring like new! Intake blowers roaring; radon purged; picks striking yellowcake!"

Q_RU[5603] = "Урановая руда пошла караванами на юг. В Брокен Хиллс снова зазвенела полновесная монета!"
Q_EN[5603] = "Refined ore trains rolling south again. Honest bullion clinking across Broken Hills counters!"

Q_RU[5604] = "Заговор против мутантов раскрыт! Фрэнсис и Мэнсон за решеткой, взрывчатку обезвредили!"
Q_EN[5604] = "Anti-mutant plot broken open! Franc and Manson behind bars; sabotage satchels defused!"

Q_RU[5605] = "Маркус спас мир между расами. Человеческие фанатики сидят в тюрьме и ждут справедливого суда."
Q_EN[5605] = "Marcus preserved the peace. Human zealots sit locked down awaiting impartial magistrate trial."

Q_RU[5606] = "В шахте нашли тела пропавших жителей... Фанатики убивали исподтишка, сея ненависть."
Q_EN[5606] = "Missing townsfolk found butchered in tunnels... Hate-mongers worked in dark to start blood."

Q_RU[5607] = "Чеда поймали на воровстве караванных денег! Шериф Маркус вытряс из него все до последнего цента."
Q_EN[5607] = "Chad caught red-handed skimming caravan coin! Sheriff shook every stolen nickel from his coat."

Q_RU[5608] = "Чед бежал из города, бросив счета. Теперь караваны водит честный парень."
Q_EN[5608] = "Chad skipped across borders, ditching ledgers. Honest drivers cracking the whips on freight now."

Q_RU[5609] = "Очиститель взорвали! Шахта завалена намертво, город остался без работы и средств к жизни."
Q_EN[5609] = "Scrubber detonated by saboteurs! Drift collapsed; town robbed of commerce and bread."

Q_RU[5610] = "Маркус убит... Город разорван пополам, люди и мутанты режут друг друга на баррикадах!"
Q_EN[5610] = "Marcus fell in the dust... Town ripped asunder; men and mutants gutting each other on ruins!"

Q_RU[5611] = "Брокен Хиллс умирает. Без шерифа и без шахты здесь скоро останутся только пустые бутылки."
Q_EN[5611] = "Broken Hills is bleeding out. Without sheriff and ore hoist, only broken glass remains."

# --- REDDING QUESTS (5620-5631) ---
Q_RU[5620] = "В «Большой Ванетте» плодятся зубастые твари! Забойщики отказываются лезть под землю за любые деньги."
Q_EN[5620] = "Fanged horrors breeding in Wanamingo shaft! Miners drop tools, refusing shifts at any wage."

Q_RU[5621] = "Винт Майрона косит шахтеров пачками. Доктор Джонсон завален умирающими с пеной у рта."
Q_EN[5621] = "Myron's Jet dropping drift-hands in heaps. Doc Johnson's clinic packed with foaming junkies."

Q_RU[5622] = "Матка ванаминго и ее выводок уничтожены! Мэр продал права на рудник, золото снова потекло рекой!"
Q_EN[5622] = "Wanamingo brood-queen roasted to ash! Mayor auctioned shaft deeds; bullion flows again!"

Q_RU[5623] = "Шахта Ванетта зачищена до последнего штрека! Больше никакие щупальца не утащат людей во мрак."
Q_EN[5623] = "Wanamingo drifts sterilized clean! No slithering monstrosities dragging diggers into pits."

Q_RU[5624] = "Доктор Джонсон получил лекарство от Джета! Запойные торчки очистились и снова встали к забою!"
Q_EN[5624] = "Doc Johnson mixed the Jet antidote cure! Shaking addicts sobered up and grabbed their picks!"

Q_RU[5625] = "Винтовая лихорадка отступила! Нью-Рино больше не держит Реддинг за горло через ампулы дури!"
Q_EN[5625] = "Jet fever broken across town! New Reno's chemical leash snapped clean off Redding's neck!"

Q_RU[5626] = "Порезанная шлюха у Лу... Наемники Мордино беспредельничают, шериф Марион с трудом держит порядок."
Q_EN[5626] = "Girl slashed open at Lou's saloon... Mordino thugs running wild; Sheriff barely holding line."

Q_RU[5627] = "Шахтер-головорез арестован за нападение в салуне. Закон в Реддинге еще что-то значит."
Q_EN[5627] = "Blade-hound locked in cells for saloon carving. Law still carries teeth along these streets."

Q_RU[5628] = "Шахты встали. Торчки перебили охрану склада, город сползает в пучину дикого хаоса."
Q_EN[5628] = "Rubble sealed the stopes. Addicts raided the depot; settlement sliding into lawless ruin."

Q_RU[5629] = "НКР готовит аннексию Реддинга. Без золота Республика не оставит наш лагерь в покое."
Q_EN[5629] = "NCR senate gearing for annexation. Without ore bullion, Republic won't bypass our borders."

Q_RU[5630] = "Семья Мордино подмяла оба рудника. Теперь шахтеры работают за понюшку винтового порошка."
Q_EN[5630] = "Mordino cartel bought both mine gates. Miners swing sledgehammers for pinches of brown chem."

Q_RU[5631] = "Город Убежища прислал своих врачей. За каждую таблетку они требуют подписать кабальные векселя."
Q_EN[5631] = "Vault City doctors arrived with medical bags. Charge indentured servitude for every sterile pill."


# --- ARROYO QUESTS (5640-5649) ---
Q_RU[5640] = "Избранный вошел в Храм. Духи предков взвешивают его плоть и сердце."
Q_EN[5640] = "Chosen One entered the Temple. Ancestor spirits weigh his flesh and soul."

Q_RU[5641] = "Если Избранный не вернется из Храма, наше племя сотрет песок пустошей."
Q_EN[5641] = "If the Chosen fails the Temple, wasteland sands will scour our tribe away."

Q_RU[5642] = "Храм покорился! На плечах Избранного сияет священный комбинезон Тринадцать!"
Q_EN[5642] = "Temple trials conquered! Holy Suit Thirteen gleams on the Chosen back!"

Q_RU[5643] = "Старейшая вручила диск святого Убежища. Теперь наша судьба на южных тропах."
Q_EN[5643] = "The Elder handed down the holy Vault holodisk. Our fate walks south now."

Q_RU[5644] = "Колодец почти пересох. Дети жуют сухие корни, женщины плачут над очагом."
Q_EN[5644] = "The cistern is nearly dry. Children chew bitter roots; women weep by coals."

Q_RU[5645] = "Без святого ГЭКК наши шатры опустеют до первых заморозков. Время на исходе."
Q_EN[5645] = "Without the holy GECK our tents will empty before frost. Time is dying."

Q_RU[5646] = "Хакунин благодарит духов: злые сорняки вырваны с корнем из священного сада."
Q_EN[5646] = "Hakunin praises spirits: the foul weed-fiends were torn from holy soil."

Q_RU[5647] = "Шаман снова варит целебный порошок. От его котла пахнет терпким дымом и жизнью."
Q_EN[5647] = "The shaman brews healing powder again. Kettle reeks of bitter herbs and life."

Q_RU[5648] = "В лагере только кровь и гильзы... Железные птицы унесли наших родных на юг!"
Q_EN[5648] = "Only blood and brass left in camp... Iron birds carried our blood south!"

Q_RU[5649] = "Боги покинули Арройо. Повсюду пепел и следы тяжелых кованых сапог."
Q_EN[5649] = "The gods abandoned Arroyo. Only cold ash and heavy combat boot tracks."

# --- NEW RENO QUESTS (5650-5665) ---
Q_RU[5650] = "Старик Орвилл в ярости. Если найдут того, кто продал Джет Ричарду, будет бойня."
Q_EN[5650] = "Old Orville is spitting rage. They find who sold Jet to Richard, blood floods."

Q_RU[5651] = "Мальчишка Райтов захлебнулся пеной в переулке. Братья заряжают дробовики."
Q_EN[5651] = "Young Wright choked on foam in an alley. His brothers are loading shotguns."

Q_RU[5652] = "Ричарда отравили скорпионьим ядом! Торговцы в Рино совсем берега потеряли."
Q_EN[5652] = "Richard was poisoned by radscorpion venom! Chem peddlers lost all shame."

Q_RU[5653] = "Райты узнали правду о смерти сына. Теперь кому-то в городе не сносить головы."
Q_EN[5653] = "The Wrights bought the truth behind the boy death. Somebody head will roll."

Q_RU[5654] = "Люди Сальваторе ходят гоголем со своими световыми пушками. Никто не смеет пикнуть."
Q_EN[5654] = "Salvatore button-men swagger with their light-guns. Nobody dares breathe."

Q_RU[5655] = "Мистер Сальваторе задохнулся в постели! Его лазерные стрелки разбежались как крысы."
Q_EN[5655] = "Mr. Salvatore choked in his sheets! His laser triggermen scattered like rats."

Q_RU[5656] = "Бишоп скупает наемников и засматривается на юг. Казино «Шарк» гребет крышки лопатой."
Q_EN[5656] = "Bishop hiring mercs and eyeing the south. The Shark Club rakes chips in heaps."

Q_RU[5657] = "Джона Бишопа порешили в его пентхаусе! Теперь за его шлюх и столы начнется грызня."
Q_EN[5657] = "John Bishop got butchered in his penthouse! War begins over his girls and felt."

Q_RU[5658] = "Большой Хесус варит тонны Джета на конюшнях. Весь город сидит на его химической игле."
Q_EN[5658] = "Big Jesus cooks tons of Jet at the stables. Whole town hooked on his needle."

Q_RU[5659] = "Большой Хесус Мордино сдох от сердечного приступа! Конюшни наконец очистят от дерьма."
Q_EN[5659] = "Big Jesus Mordino dropped dead of a seizure! Stables might get shoveled at last."

Q_RU[5660] = "Слыхал? У какого-то приезжего лоха увели новенькую «Хризалис Корвегу» прямо с улицы!"
Q_EN[5660] = "Heard? Some greenhorn had a shiny Chrysalis Corvega boosted off the tarmac!"

Q_RU[5661] = "Тот парень на Корвеге перебил автоворов у Ти-Рэя и забрал тачку назад. Крутой черт."
Q_EN[5661] = "That Corvega drifter ventilated chop-shop goons and drove his rig away."

Q_RU[5662] = "Братья Корсиканцы ищут свежее мясо для порнофильмов. Платят мало, зато слава на всю пустошь."
Q_EN[5662] = "Corsican Brothers hiring fresh meat for peep reels. Low pay, but wasteland fame."

Q_RU[5663] = "В зале Джунглей новый чемпион! Выбил зубы Морису Мастике прямо на канаты!"
Q_EN[5663] = "New heavyweight champ at the Jungle! Knocked Masticator teeth into the ropes!"

Q_RU[5664] = "Не стой под неоном после заката. В Рино пулю схватить дешевле, чем стакан воды."
Q_EN[5664] = "Do not idle under neon after dark. Catching lead in Reno is cheaper than water."

Q_RU[5665] = "Винтовые торчки выгребают карманы прямо в сточной канаве. Жуткий городишко."
Q_EN[5665] = "Jet addicts turning their pockets inside out in the ditch. Ugly damned town."

# --- NCR QUESTS (5670-5682) ---
Q_RU[5670] = "Сквоттеры из Убежища 15 не пускают геодезистов Республики. Сенат теряет терпение."
Q_EN[5670] = "Vault 15 squatters barring Republic surveyors. Senate patience is wearing thin."

Q_RU[5671] = "Банда Дариона засела на руинах 15-го. Караванщики боятся ходить тем трактом."
Q_EN[5671] = "Darion raiders holed up in Vault 15 ruins. Caravaners dread that desert trail."

Q_RU[5672] = "Договор с Убежищем 15 подписан! Скоро поезда Республики пойдут через восточные перевалы."
Q_EN[5672] = "Vault 15 treaty ratified! Republic ore trains will roll through passes soon."

Q_RU[5673] = "Дарион и его Ханы уничтожены! Призрак старой банды наконец выжжен из тоннелей."
Q_EN[5673] = "Darion and his Khans wiped out! The old raider ghost is purged from drifts."

Q_RU[5674] = "В канцелярии президента Танди завелся крот. Секретные доклады утекают на север."
Q_EN[5674] = "A mole is nested in President Tandi staff. State dispatches leaking north."

Q_RU[5675] = "Предателя в Совете разоблачили! Канцелярию обыскали рейнджеры, шпион под стражей."
Q_EN[5675] = "The senate traitor was unmasked! Rangers tossed his chambers; spy in irons."

Q_RU[5676] = "У скотоводов Вестина крадут браминов целыми гуртами. Подозревают каких-то тварей."
Q_EN[5676] = "Westin herds are being rustled by the score. Ranch hands suspect desert beasts."

Q_RU[5677] = "Пастбища Вестина зачищены! Больше ни один двуглавый бык не пропадет в ночи."
Q_EN[5677] = "Westin grazing pastures sterilized! Not another twin-head steer vanished."

Q_RU[5678] = "Рейнджеры объявили награду за лагеря работорговцев. Скоро начнется большая охота."
Q_EN[5678] = "NCR Rangers posted bounties on slaver compounds. Big purge coming down the pike."

Q_RU[5679] = "Лагерь работорговцев к северу от города стерт в пыль! Свободные люди славят Рейнджеров."
Q_EN[5679] = "Slaver outpost north of town leveled to dust! Free citizens toast the Rangers."

Q_RU[5680] = "Спрячь оружие, гражданин. Маршалы НКР стреляют на поражение без предупреждений."
Q_EN[5680] = "Holster that hardware, citizen. NCR Marshals shoot to kill without polite words."

Q_RU[5681] = "Танди правит твердой рукой, но налоги Сената скоро разденут мелких фермеров догола."
Q_EN[5681] = "Tandi rules with iron grip, but senate taxes will strip homesteaders bare."

Q_RU[5682] = "На Базаре за стеной крутятся подозрительные типы. Без кобуры туда лучше не соваться."
Q_EN[5682] = "Shifty cutthroats pacing the outer Bazaar. Do not step past gates unarmed."

# --- SAN FRANCISCO QUESTS (5690-5701) ---
Q_RU[5690] = "Танкер «Валдез» ржавеет в доках. Без топлива и навигационного чипа он никуда не поплывет."
Q_EN[5690] = "The Valdez rusts in dock slip. Lacking fuel and a nav-chip, she will not budge."

Q_RU[5691] = "Трюм танкера кишит чудовищами. Бродяги с верхней палубы боятся спускаться вниз."
Q_EN[5691] = "Tanker hold crawls with monstrosities. Upper deck punks fear climbing below."

Q_RU[5692] = "Топливо закачано в цистерны «Валдеза»! Машинное отделение гудит, паровые клапаны дрожат!"
Q_EN[5692] = "Fuel surged into the Valdez tanks! Engine compartments humming, relief valves hot!"

Q_RU[5693] = "Танкер готов к выходу в океан! Чужак восстановил компьютеры и запустил гребной винт!"
Q_EN[5693] = "Tanker is rigged for sea! An out-lander patched navigation and turned screws!"

Q_RU[5694] = "Дракон и Ло Пэн собирают бойцов. Их вражда на кулаках скоро спалит Чайнатаун."
Q_EN[5694] = "The Dragon and Lo Pan drill fighters. Their bare-knuckle feud will burn town."

Q_RU[5695] = "Ло Пэн повержен в честном поединке! Дракон восстановил честь боевых школ Ши."
Q_EN[5695] = "Lo Pan fell in honest ring combat! Dragon restored honor to the Shi dojos."

Q_RU[5696] = "Дракон убит... Ло Пэн торжествует, теперь на улицах Чайнатауна правит грубая сила."
Q_EN[5696] = "Dragon is dead... Lo Pan gloats; naked muscle and thugs dictate the avenues now."

Q_RU[5697] = "Хабологи зазывают в свой дворец. Обещают очистить нейроны, а сами выманивают деньги."
Q_EN[5697] = "Hubologists hawking in their palace. Promise clean zeta scans, just want coin."

Q_RU[5698] = "АХС-9 прикончили прямо в алтаре! Звездная секта в панике сжигает свои лживые памфлеты."
Q_EN[5698] = "AHS-9 butchered at the altar! Star cult scurrying to burn their fraudulent tracts."

Q_RU[5699] = "Император Ши принимает решения через терминалы. Никто из смертных не видел его лица."
Q_EN[5699] = "The Shi Emperor decrees through terminal banks. No living soul saw his visage."

Q_RU[5700] = "Девчонку Бэджера вытащили из трюма целой и невредимой! Хакер счастлив и готов помочь."
Q_EN[5700] = "Badger girl hauled from the hold alive! The punk hacker is singing praises."

Q_RU[5701] = "Ученые Ши выращивают синтетическую кожу и лозы, способные очистить радиоактивную пустошь."
Q_EN[5701] = "Shi chemists synthesize polymer skins and botanicals to purge poisoned dirt."

# --- VAULT 15 / VAULT 13 QUESTS (5710-5716) ---
Q_RU[5710] = "Мы просто хотим растить маис и жить в мире. Почему НКР не оставит наш лагерь в покое?"
Q_EN[5710] = "We just want to tend maize and live in peace. Why will not NCR leave us alone?"

Q_RU[5711] = "Дарион сидит на нижних ярусах и бредит местью. Мы боимся его головорезов больше солдат."
Q_EN[5711] = "Darion festers in lower vaults dreaming vengeance. We dread his thugs worse than NCR."

Q_RU[5712] = "Дариона больше нет! Теперь мы граждане Республики, нам обещали генераторы и семена."
Q_EN[5712] = "Darion is dead! We are Republic citizens now; they promised dynamos and seed grain."

Q_RU[5713] = "Разумные когти смерти стерегут святой вход... Они говорят человеческими голосами!"
Q_EN[5713] = "Sentient deathclaws guarding the holy portal... They speak with human tongue!"

Q_RU[5714] = "Грутар говорит правду: его народ хочет мира с людьми, а не человеческого мяса."
Q_EN[5714] = "Gruthar speaks truth: his clutch seeks peace with mankind, not butchered flesh."

Q_RU[5715] = "Чужак починил главный терминал Убежища! Теперь инкубатор работает на полную мощность."
Q_EN[5715] = "An out-lander repaired main mainframe! Egg nurseries cycling at full wattage."

Q_RU[5716] = "Когти смерти перебиты... Вся пещера залита кровью мутантов и завалена стреляными гильзами."
Q_EN[5716] = "The deathclaws were slaughtered... Cave floor slick with ichor and heavy brass."

# --- PLAYER REACTIVITY: POWER ARMOR (5800-5809) ---
Q_RU[5800] = "Матерь божья... Это что за ходячая танковая башня?! Не стреляй, железный человек!"
Q_EN[5800] = "Holy mother... What kind of walking turret is that?! Don't fire, iron demon!"

Q_RU[5801] = "Святые духи предков... Сам Стальной Воин спустился с небес! Не гневайся на наше племя!"
Q_EN[5801] = "Spirits of the ancients... The Steel Warrior walked down from the sky! Spare our hearths!"

Q_RU[5802] = "Вот это броня... Мой 10-миллиметровый от такого нагрудника только искрами брызнет."
Q_EN[5802] = "Look at that plate... My 10mm slugs would just bounce like copper sparks off that chest."

Q_RU[5803] = "Предъявите разрешение на ношение силовой брони армейского образца, гражданин! Руки на виду!"
Q_EN[5803] = "Display your ordnance registration for military-grade powered suit, citizen! Keep paws clear!"

Q_RU[5804] = "Эй, здоровяк, внутри этой консервной банки не жарко? Выглядишь так, будто можешь пробить стену лбом."
Q_EN[5804] = "Hey hoss, sweat boiling inside that tin can? Look like you could walk straight through brick."

Q_RU[5805] = "Парни Сальваторе с их лазерами будут чесать затылки, если ты зайдешь к ним в казино."
Q_EN[5805] = "Salvatore button-men with their laser heaters will sweat bullets if you stroll into their pit."

Q_RU[5806] = "Шаги гудят по мостовой, как удары молота. Отойду-ка я подальше, от греха подальше."
Q_EN[5806] = "Your boots rattle paving stones like forge hammers. Stepping off the curb before I'm flat."

Q_RU[5807] = "Такую броню делали до войны для штурма бункеров. Ни один рейдерский нож ее не поцарапает."
Q_EN[5807] = "They milled that armor pre-war for clearing concrete redoubts. Raider shivs won't scratch it."

Q_RU[5808] = "Ты внутри живой или это довоенный робот с поехавшей программой? Жуткое зрелище."
Q_EN[5808] = "Breathing meat inside there, or ancient cybernetic sentry running corrupt code? Terrifying."

Q_RU[5809] = "Послушай, сэр... или мэм... мы мирные люди. Пожалуйста, не раздави наши палатки."
Q_EN[5809] = "Look here, sir... or ma'am... we're peaceful folk. Please don't trample down our shanties."

# --- PLAYER REACTIVITY: HEAVY WEAPONS (5830-5835) ---
Q_RU[5830] = "Эй! Опусти ствол в землю! С этой пушкой ты разнесешь весь квартал одной случайной очередью!"
Q_EN[5830] = "Hey! Drop that barrel toward dirt! One stray burst from that cannon shreds half the precinct!"

Q_RU[5831] = "Убери палец со спуска, псих! Огнемет на людной улице -- это верная смерть для всех вокруг!"
Q_EN[5831] = "Finger off the paddle, lunatic! Waving a flamer down a crowded avenue is suicide for everyone!"

Q_RU[5832] = "Шериф! Тут бродит маньяк с шестиствольным пулеметом наперевес! Спасайся кто может!"
Q_EN[5832] = "Sheriff! Madman prowling the boardwalk packing a six-barrel rotary! Run for cellars!"

Q_RU[5833] = "Оружие на предохранитель, путник! Направь эту базуку в другую сторону, не испытывай судьбу."
Q_EN[5833] = "Toggle that safety on, traveler! Point that bazooka at empty sky; don't gamble with fates."

Q_RU[5834] = "Ты что, на войну собрался? С таким стволом только на когтей смерти ходить, а не по базару гулять."
Q_EN[5834] = "Marching for total war? That piece is built to split deathclaws, not browse marketplace stalls."

Q_RU[5835] = "Господи, если эта штука плюнет огнем -- от меня и сапог не останется. Отойди от меня!"
Q_EN[5835] = "Lord, if that nozzle spits flame, my boots won't even survive the roast. Step the hell back!"

# --- PLAYER REACTIVITY: FREAK COMPANIONS (5850-5857) ---
Q_RU[5850] = "Господи помилуй... Это настоящий супермутант Создателя! Держи своего людоеда на привязи!"
Q_EN[5850] = "Merciful lord... A genuine Master's super mutant! Keep that flesh-eater on a stout chain!"

Q_RU[5851] = "Не подпускай этого зеленого громилу ко мне! Он же может оторвать мне руку и не заметить!"
Q_EN[5851] = "Keep that green mountain away from my porch! Brute could tear off my arm and never notice!"

Q_RU[5852] = "Маркус? Шериф из Брокен Хиллс бродит по нашим улицам? Надеюсь, его миниган заряжен холостыми."
Q_EN[5852] = "Marcus? Broken Hills sheriff touring our avenues? Sure pray that rotary is loaded blanks."

Q_RU[5853] = "Фу, какая вонь! От этого гуля пахнет разрытой могилой и формалином! Уберите его из лавки!"
Q_EN[5853] = "Phew, what rot! That ghoul reeks of unsealed crypts and embalming brine! Shove him outside!"

Q_RU[5854] = "Эй, старый мертвец, смотри под ноги, у тебя кусок уха на тротуар отвалился!"
Q_EN[5854] = "Watch your boots, dead man! Chunk of dried ear just peeled off and bounced on the wood!"

Q_RU[5855] = "Кто этот здоровяк в плаще с капюшоном? Он не человек... у него когти под рукавами размером с саблю!"
Q_EN[5855] = "Who is that hooded giant? That's no man... he's got talons under those sleeves broad as sabers!"

Q_RU[5856] = "Под этим балахоном прячется чудовище! Я видел, как у него блеснули желтые звериные глаза!"
Q_EN[5856] = "Monster lurking beneath that cowl! Caught a flash of cold slit-pupil eyes behind the cloth!"

Q_RU[5857] = "Твой отряд похож на бродячий цирк уродов. Надеюсь, твои монстры умеют вести себя прилично."
Q_EN[5857] = "Your squad resembles a traveling sideshow freak tent. Hope your beasts are housebroken."

# --- PLAYER REACTIVITY: LOW IQ (5880-5886) ---
Q_RU[5880] = "Ох, бедняга... Мозгов у тебя не больше, чем у сушеной репы. Держи леденец и иди своей дорогой."
Q_EN[5880] = "Oh, poor soul... Got no more wits than a boiled turnip. Take this rock candy and wander on."

Q_RU[5881] = "Иди отсюда, дурачок. У меня нет блестящих камушков и сладких корешков для тебя."
Q_EN[5881] = "Shoo now, simpleton. I haven't got shiny pebbles or sweet cane roots to barter for drool."

Q_RU[5882] = "Смотри-ка, двух слов связать не может, только слюни пускает. Кто выпустил его без присмотра?"
Q_EN[5882] = "Look at that: can't string two grunts together without slobbering. Who let him roam loose?"

Q_RU[5883] = "Привет, здоровяк! Хочешь погладить брамина? Только пальцы ему в рот не суй, откусит."
Q_EN[5883] = "Howdy, big guy! Fancy petting the heifer? Just keep thumbs out of her chops or she'll nip 'em."

Q_RU[5884] = "Не мычи на меня, дикарь. Кыш-кыш от витрины, распугаешь нормальных покупателей."
Q_EN[5884] = "Don't bray at me, primitive. Shoo off the boardwalk before you spook paying customers."

Q_RU[5885] = "Бедный парень, природа совсем обделила тебя умом. Не трогай железо -- пальчики прищемишь."
Q_EN[5885] = "Poor jack, nature shorted you on grey matter. Don't touch that iron gear -- pinch your digits."

Q_RU[5886] = "Говори медленнее, я не понимаю твое улюлюканье. Хотя лучше вообще помолчи, за умного сойдешь."
Q_EN[5886] = "Speak slow, can't parse your hooting. Better yet, clamp jaws shut; folks might think you're wise."


def main():
    # Merge existing base small talk + new quest/reactivity lines
    ALL_RU = dict(RU_LINES)
    ALL_RU.update(Q_RU)

    ALL_EN = dict(EN_LINES)
    ALL_EN.update(Q_EN)

    ru_dialog = os.path.join(BASE_DIR, "text", "russian", "dialog", "wv_dialog.msg")
    ru_custom = os.path.join(BASE_DIR, "text", "russian", "game", "custom.msg")
    en_dialog = os.path.join(BASE_DIR, "text", "english", "dialog", "wv_dialog.msg")
    en_custom = os.path.join(BASE_DIR, "text", "english", "game", "custom.msg")

    sorted_ids = sorted(ALL_RU.keys())

    header = "# ==============================================================================\n"
    header += f"# WASTELAND VOICES v1.0.0 CORPUS ({len(sorted_ids)} LINES)\n"
    header += "# ==============================================================================\n\n"

    ru_content = header + "".join(f"{{{i}}}{{}}{{{ALL_RU[i]}}}\n" for i in sorted_ids)
    en_content = header + "".join(f"{{{i}}}{{}}{{{ALL_EN[i]}}}\n" for i in sorted_ids)

    # 1. Dialog files (5000+)
    with open(ru_dialog, "wb") as f:
        f.write(ru_content.encode("cp1251"))
    with open(en_dialog, "wb") as f:
        f.write(en_content.encode("ascii"))

    # 2. Custom.msg files (0..604 base sFall party lines + 5000+ mod lines)
    full_ru_custom = BASE_RU_CUSTOM + "\n" + ru_content
    full_en_custom = BASE_EN_CUSTOM + "\n" + en_content

    with open(ru_custom, "wb") as f:
        f.write(full_ru_custom.encode("cp1251"))
    with open(en_custom, "wb") as f:
        f.write(full_en_custom.encode("ascii"))

    print(f"Step 3 Corpus Built Successfully!")
    print(f"Total lines: {len(sorted_ids)}")
    print(f"  RU dialog: {os.path.getsize(ru_dialog)} bytes")
    print(f"  RU custom: {os.path.getsize(ru_custom)} bytes")
    print(f"  EN dialog: {os.path.getsize(en_dialog)} bytes")
    print(f"  EN custom: {os.path.getsize(en_custom)} bytes")

if __name__ == "__main__":
    main()
