# -*- coding: utf-8 -*-
"""
Full Corpus Builder for Wasteland Voices (v1.0.0)
Generates:
  - text/russian/dialog/wv_dialog.msg (CP1251)
  - text/russian/game/custom.msg (CP1251)
  - text/english/dialog/wv_dialog.msg (ANSI)
  - text/english/game/custom.msg (ANSI)
"""

import os
import sys

BASE_DIR = r"E:\FALLOUT Ult pjt\standalone_mods\wasteland_voices"

RU_LINES = {}
EN_LINES = {}

# Header / Init
RU_LINES[5000] = "[Wasteland Voices v1.0.0 активен]"
RU_LINES[5001] = "[Контур 1 (Core RPU): Активен]"
RU_LINES[5002] = "[Контур 2 (Extended Wasteland): Активен]"

EN_LINES[5000] = "[Wasteland Voices v1.0.0 active]"
EN_LINES[5001] = "[Contour 1 (Core RPU): Active]"
EN_LINES[5002] = "[Contour 2 (Extended Wasteland): Active]"

# --- KLAMATH (5010-5025) ---
RU_LINES[5010] = "Опять сапог прохудился. Если сунусь в болото за золотым гекко -- пальцы отвалятся к чертям."
EN_LINES[5010] = "Boot has another hole. Wade into the swamp after golden geckos and my toes rot right off."

RU_LINES[5011] = "Шкуры гекко нынче упали в цене. Скоро за них и миски похлебки у Бакнера не сторгуешь."
EN_LINES[5011] = "Gecko skins are cheap as dirt now. Soon you won't barter a bowl of Buckner stew for one."

RU_LINES[5012] = "Слышал шорох в тоннелях под городом? Крысы там жирные, как брамины. И злые, как черти."
EN_LINES[5012] = "Heard scratching under town? Rats down there are fat as brahmin. Mean as hell, too."

RU_LINES[5013] = "Капкан заржавел намертво. Смазать бы салом, да сало всё на самогон ушло."
EN_LINES[5013] = "Trap rusted shut. Needs fat, but all the fat went into Bob's still."

RU_LINES[5014] = "Самогон у Боба крепкий, спору нет. После третьей кружки начинаешь понимать, о чем мычит брамин."
EN_LINES[5014] = "Whiskey Bob makes stout rotgut. Three mugs in, you understand what brahmin are mooing about."

RU_LINES[5015] = "У «Золотого Гекко» вчера опять кому-то ребра пересчитали. Трапперы напились и не поделили хвост бобра."
EN_LINES[5015] = "Somebody got their ribs cracked at Golden Gecko yesterday. Drunk trappers brawling over beaver tail."

RU_LINES[5016] = "Если пьешь «Рвотку» у Смайли -- не вздумай подносить спичку к зубам. Сгоришь на месте."
EN_LINES[5016] = "Drinking Smiley's gut-wash? Don't strike a match near your mouth or you'll torch the street."

RU_LINES[5017] = "Торр опять твердит про каких-то жуколюдей на пастбище. Бедняга совсем плох головой стал."
EN_LINES[5017] = "Torr's crying about bug-men in the pastures again. Poor boy's mind is completely gone."

RU_LINES[5018] = "Братья Дантоны крутятся возле стад. Никому не советую играть с ними в кости -- кости у них кривые."
EN_LINES[5018] = "Dunton brothers sniffing around the herds. Never roll dice with them -- their bones are loaded."

RU_LINES[5019] = "Говорят, на юге в Дыре работорговцы платят звонкой монетой за здоровых бродяг. Держись подальше от дороги."
EN_LINES[5019] = "Word is slavers down in the Den pay hard coin for able bodies. Stay off the south road."

RU_LINES[5020] = "Сулик из племени всё сидит за долги у Бакнеров. Бормочет про духов своего деда. Жуткий парень."
EN_LINES[5020] = "Sulik the tribal is still working off debt at Buckner's. Mutters about his grandpa's bone. Creepy guy."

RU_LINES[5021] = "Ветер сегодня с каньона тянет. Не к добру это. Пахнет дохлятиной и пылью."
EN_LINES[5021] = "Wind's blowing hard off the canyon today. Bad sign. Smells like carrion and old dust."

RU_LINES[5022] = "Вик ушел в Дыру три недели назад и сгинул. Наверное, Мецгер уже пустил его на запчасти."
EN_LINES[5022] = "Vic headed down to the Den three weeks back and vanished. Metzger probably sold him off for scrap."

RU_LINES[5023] = "Если встретишь в пустошах огненного гекко -- не три глаза, парень. Бросай пожитки и беги."
EN_LINES[5023] = "Spot a fire gecko out in the wastes? Don't rub your eyes, kid. Drop your pack and run like hell."

RU_LINES[5024] = "У бани опять очередь. Охотники принесли тифозных блох с болот, мыло в дефиците."
EN_LINES[5024] = "Line at the bathhouse again. Trappers brought swamp lice into town, and lye soap is all gone."

RU_LINES[5025] = "Купи вяленого мяса, путник. Пахнет дурно, зато в кишках не бурчит."
EN_LINES[5025] = "Buy some dried meat, stranger. Smells foul, but keeps your gut from growling through the night."

# --- THE DEN (5030-5045) ---
RU_LINES[5030] = "Не стой так близко, парень. Здесь за пару мятых долларов глотку перережут и глазом не моргнут."
EN_LINES[5030] = "Don't stand so close, kid. In the Den, folks slit throats for crumpled dollars without blinking."

RU_LINES[5031] = "Держи руку на кошельке. Сопляки Флика вытащат у тебя патроны прямо из карманов, пока ты зеваешь."
EN_LINES[5031] = "Keep a hand on your pouch. Flick's brats will snatch ammo right out of your pockets while you yawn."

RU_LINES[5032] = "Мецгер сегодня не в духе. Утром двоих рабов запороли насмерть за побег."
EN_LINES[5032] = "Metzger woke up in a foul mood. Flogged two runaways to death by breakfast."

RU_LINES[5033] = "Винт... мне просто нужна одна доза, всего одна... Господи, кости крутит, как на дыбе..."
EN_LINES[5033] = "Jet... just need one hit, just one... Lord, my bones feel like they're on a medieval rack..."

RU_LINES[5034] = "У Бекки рулетка честная. Вот только почему все выходят из ее бара без штанов?"
EN_LINES[5034] = "Becky runs a fair wheel. Funny how everybody walks out of her casino in their underwear though."

RU_LINES[5035] = "Фрэнки в дыре разбавляет виски мочой браминов. Зато дешево, желудок прожигает насквозь."
EN_LINES[5035] = "Frankie cuts his rotgut with brahmin piss. Cheap though -- burns straight through your guts."

RU_LINES[5036] = "Ночью на свалке опять стреляли. Похоже, Лара и Тайлер делят склад наркоты."
EN_LINES[5036] = "Gunshots down at the junkyard again. Lara and Tyler fighting over some stash, no doubt."

RU_LINES[5037] = "Смитти возится со своей древней колымагой. Говорят, эта рухлядь когда-то ездила без браминов."
EN_LINES[5037] = "Smitty tinkering with that ancient wreck. People swear that metal heap used to roll without brahmin."

RU_LINES[5038] = "Призрак в доме шепчет по ночам... плачет про медальон. Тьфу, бредятина наркоманская."
EN_LINES[5038] = "Ghost whispers in that ruin at night... weeping for a locket. Bah, junkies seeing shadows."

RU_LINES[5039] = "Смотри под ноги. Здесь в грязи валяются ржавые иглы и дохлые крысы."
EN_LINES[5039] = "Watch your boots. Mud out here is loaded with rusty needles and rotting rat carcasses."

RU_LINES[5040] = "Татуировка работорговца на лбу -- это черная метка. На севере за нее сразу дробью в брюхо угощают."
EN_LINES[5040] = "Slaver brand on your forehead is a death sentence up north. They feed you buckshot on sight."

RU_LINES[5041] = "Мамаша в столовой варит суп из того, что нашла на дороге. Лучше не спрашивай, чьи там кости."
EN_LINES[5041] = "Mom cooks stew from whatever's scraped off the dirt. Never ask what kind of bones are in the pot."

RU_LINES[5042] = "Вчера пьяный караванщик свалился лицом в канаву. К утру даже сапог на нем не осталось."
EN_LINES[5042] = "Drunk guard fell facedown in the ditch last night. By dawn, they'd stripped his boots clean."

RU_LINES[5043] = "Гильдия работорговцев забирает лучших парней. Скоро в пустошах останутся только старики да калеки."
EN_LINES[5043] = "Slaver guild hauls off all the able youth. Soon there won't be anyone left outside but crones and cripples."

RU_LINES[5044] = "Туби задирает цены на патроны. А попробуй возрази -- его громилы сразу взводят курки."
EN_LINES[5044] = "Tubby gouges prices on 10mm rounds. Complain, and his thugs rack their shotgun slides."

RU_LINES[5045] = "Если ищешь ночлег -- спи с открытыми глазами и зажатым в кулаке ножом."
EN_LINES[5045] = "Looking for a bed? Sleep with one eye open and your knuckles wrapped around a knife."

# --- MODOC (5050-5065) ---
RU_LINES[5050] = "Земля сухая, как пыль. Если дождей не будет к осени -- придется резать племенных быков."
EN_LINES[5050] = "Dirt's dry as ash. Rain doesn't fall by autumn, we slaughter the breeding bulls."

RU_LINES[5051] = "Гришем опять дерет три шкуры за забой скота. Скупой старик, каждую копейку из пальцев выкручивает."
EN_LINES[5051] = "Grisham gouges on slaughter fees again. Cheap old bastard squeezes every nickel till it bleeds."

RU_LINES[5052] = "Вонь от кожевенной мастерской Бальтазара разносится по всему поселку. Хоть нос тряпкой затыкай."
EN_LINES[5052] = "Balthas's tannery stinks up the whole town. Gotta wrap a rag round your face just to breathe."

RU_LINES[5053] = "Слышал про Призрачную Ферму на северо-востоке? Говорят, по ночам там трупы горят синим пламенем."
EN_LINES[5053] = "Heard about the Ghost Farm up northeast? Folks say glowing corpses burn with cold blue fire at night."

RU_LINES[5054] = "В колодец уронили что-то ценное. Пацаны хотели достать, да застряли в глине, еле вытащили."
EN_LINES[5054] = "Someone dropped a watch down the town well. Kids climbed in, got stuck in the muck, barely pulled 'em out."

RU_LINES[5055] = "У Розы в закусочной лучший омлет в округе. Только вот яйца какие-то подозрительно крупные..."
EN_LINES[5055] = "Rose fries the best omelet for fifty miles. Eggs are mighty huge though... unnatural big."

RU_LINES[5056] = "Вчера дикие собаки опять задрали двух телят на дальнем пастбище. Пора собирать облаву."
EN_LINES[5056] = "Wild dogs tore up two calves on the north range last night. Time to grab rifles and hunt the pack down."

RU_LINES[5057] = "Торговцы из Города Убежища смотрят на нас как на грязь под ногами. Сами-то холеные, в синих штанах."
EN_LINES[5057] = "Vault City traders treat us like manure under their boots. Slick bastards in their fancy blue suits."

RU_LINES[5058] = "Кузнец загнул ось на повозке. Ждем караван с запчастями из Реддинга уже вторую неделю."
EN_LINES[5058] = "Blacksmith bent an axle on the grain cart. Waiting on spare parts out of Redding going on two weeks."

RU_LINES[5059] = "Карл пропал из Модока. Говорят, напился и убрел в сторону Дыры. Наверняка сгинул по дороге."
EN_LINES[5059] = "Karl skipped town. Got tanked on rotgut and staggered toward the Den. Buzzards picked him clean, bet on it."

RU_LINES[5060] = "Кукуруза в этом году горчит. Похоже, грунтовые воды снова напитались какой-то дрянью."
EN_LINES[5060] = "Corn tastes bitter this season. Ground water's souring again, picking up old poison."

RU_LINES[5061] = "Если пойдешь к выгребной яме -- не бросай спичек. Рванет так, что до Кламата лететь будешь."
EN_LINES[5061] = "Heading near the outhouse pit? Don't strike a match. Methane will blow you halfway to Klamath."

RU_LINES[5062] = "Джо в магазине берет зерно за бесценок, а за патроны ломит тройную цену. Грабитель без пистолета."
EN_LINES[5062] = "Jo buys grain for pennies and charges triple for ammo. Robber doesn't even need a gun."

RU_LINES[5063] = "По ночам в полях воет ветер. Жутко здесь жить, когда вокруг на сотни миль одна пустыня."
EN_LINES[5063] = "Wind howls across the scrub at night. Lonely country when it's miles of dead sand all around."

RU_LINES[5064] = "Сын Гришема ходит с таким кислым лицом, будто проглотил живого кротокрыса."
EN_LINES[5064] = "Grisham's boy mopes around like he swallowed a live mole rat. Sour look on him all day."

RU_LINES[5065] = "Чужаков у нас не жалуют. Слишком много проходимцев шатается по тракту в поисках легкой поживы."
EN_LINES[5065] = "Don't take kindly to drifters here. Too many jackals wandering the trail looking for an easy mark."

# --- VAULT CITY (5070-5085) ---
RU_LINES[5070] = "Отойди в сторону, житель пригорода. Твои грязные лохмотья оскорбляют чистоту комплекса."
EN_LINES[5070] = "Step aside, Out-Sider. Your filthy rags offend the sterile purity of our complex."

RU_LINES[5071] = "Первый Гражданин Линетт знает, как держать порядок. Дикарям вход в центральный сектор строго закрыт."
EN_LINES[5071] = "First Citizen Lynette knows how to maintain order. Tribals belong outside the inner gate."

RU_LINES[5072] = "Мутанты из Гекко загрязняют наши подземные горизонты своей проклятой атомной станцией!"
EN_LINES[5072] = "Those Gecko ghouls are contaminating our underground aquifers with their leaking reactor!"

RU_LINES[5073] = "Авто-доктор в клинике доктора Троя -- вершина медицины. Он удаляет опухоли за пять минут."
EN_LINES[5073] = "The Auto-Doc in Dr. Troy's clinic is a medical miracle. Extracts tumors in five flat minutes."

RU_LINES[5074] = "Слуги из Центра распределения работают тихо и аккуратно. Никаких лишних слов, только исполнение долга."
EN_LINES[5074] = "Servants from the allocation center work quietly and efficiently. No backtalk, only duty."

RU_LINES[5075] = "Твой уровень радиации проверен на пропускном пункте? Мы не потерпим зараженных мусорщиков на улицах."
EN_LINES[5075] = "Was your rad count logged at the gate? We do not tolerate contaminated wanderers on our avenues."

RU_LINES[5076] = "Вчера в Пригороде опять была драка. Варвары не умеют цивилизованно решать земельные споры."
EN_LINES[5076] = "Brawl in the Courtyard again. Barbarians lack the mental faculties for civil dispute."

RU_LINES[5077] = "Капитан Грегори держит охрану в железной дисциплине. Лазерные винтовки всегда заряжены."
EN_LINES[5077] = "Captain Gregory drills the guards with iron discipline. Laser carbines charged at all times."

RU_LINES[5078] = "Дикари думают, что могут стать Гражданами, просто сдав тест? Смешно. Их мозг не приспособлен к логике."
EN_LINES[5078] = "Out-Siders think they can earn Citizenship via the exam? Laughable. Their brains lack logic."

RU_LINES[5079] = "Синтезированная пища из распределителя идеальна по балансу белков. Никакой жирной браминятины."
EN_LINES[5079] = "Synthesized rations from food dispensers have optimal protein balance. None of that greasy brahmin slop."

RU_LINES[5080] = "Вик из пригорода пытался продать мне радиодетали. Ржавый хлам, снятый с довоенных свалок."
EN_LINES[5080] = "That Courtyard junker tried selling me radio valves. Corroded scrap fished out of old dumps."

RU_LINES[5081] = "В Списке Граждан нет случайных имен. Каждая родословная проверяется компьютером на три поколения."
EN_LINES[5081] = "No random names in the Citizen Registry. Every lineage is vetted by mainframe algorithms."

RU_LINES[5082] = "Грустно смотреть на обитателей палаток за стеной. Но сострадание не должно ставить под угрозу безопасность."
EN_LINES[5082] = "Pitiable seeing tent-dwellers outside the perimeter. But sympathy cannot compromise our security."

RU_LINES[5083] = "Офицер Старк собирает разведданные о лагерях рейдеров. Скоро наши патрули зачистят этот сектор."
EN_LINES[5083] = "Officer Stark is compiling recon on raider encampments. Our patrols will sterilize that sector soon."

RU_LINES[5084] = "Не прикасайся к терминалу Городской Сети, чужак. Это имущество Совета Первого Гражданина."
EN_LINES[5084] = "Do not touch the City Network terminal, Out-Sider. That is property of the Citizen Council."

RU_LINES[5085] = "Закон и порядок. Без стен Убежища человечество давно бы захлебнулось в собственной грязи."
EN_LINES[5085] = "Order and law. Without Vault walls, humanity would have drowned in its own radioactive mire."

# --- GECKO (5090-5105) ---
RU_LINES[5090] = "Реактор опять барахлит. В третьем контуре давление зашкаливает, а охладитель на нуле."
EN_LINES[5090] = "Reactor's rattling again. Coolant loop three pressure is spiking and the reservoir is dry."

RU_LINES[5091] = "Гарольд -- славный старик, хоть у него на голове и растет чертово дерево. Он держит нас на плаву."
EN_LINES[5091] = "Harold is a decent old skin, even with that damn tree sprouting out of his skull. Keeps us alive."

RU_LINES[5092] = "Снобы из Города Убежища спят и видят, как бы стереть нас с карты. Боятся, что мы их «облучим»."
EN_LINES[5092] = "Vault City snobs pray for the day they can wipe us out. Terrified we'll leak radiation on their haircuts."

RU_LINES[5093] = "Кожа зудит нестерпимо. Похоже, вчера словил пару лишних рентген, пока чинил заслонку."
EN_LINES[5093] = "Flesh itches like crazy today. Soaked up a few dozen extra rads patching that steam flange."

RU_LINES[5094] = "Фестус весь день ругается у пульта. Говорит, пока деталь из Убежища не пришлют -- станция обречена."
EN_LINES[5094] = "Festus is cussing at the master console. Says without that Vault hydro-regulator, the core is toast."

RU_LINES[5095] = "У Скиппи в мастерской можно починить любую железку. Только не стой рядом, когда он варит медь."
EN_LINES[5095] = "Skeeter can patch any piece of scrap in his garage. Just don't stand near him while he's welding copper."

RU_LINES[5096] = "В баре у Вуди пиво теплое и отдает серой. Зато зубы не крошатся, как от воды из лужи."
EN_LINES[5096] = "Woody serves beer warm and smelling of sulphur. Beats drinking sludge from the cooling pool though."

RU_LINES[5097] = "Глаз выпал в кружку на прошлой неделе... Пришлось промывать спиртом и вставлять обратно. Бывает."
EN_LINES[5097] = "My eyelid slipped off into my mug last week... Rinsed it with moonshine and stuck it back on. Happens."

RU_LINES[5098] = "Ленни бормочет про какого-то Выходца из Убежища. Мол, видел его сто лет назад. Старческий маразм."
EN_LINES[5098] = "Lenny mumbles about some ancient Vault Dweller. Swears he shook his hand a century ago. Senile rot."

RU_LINES[5099] = "Радиация не убивает нас, гладкокожий. Она просто делает нас... более терпеливыми к боли."
EN_LINES[5099] = "Radiation doesn't kill us, smoothskin. Just teaches you to get real comfortable with constant pain."

RU_LINES[5100] = "Свалка вокруг поселка -- наше богатство. Там можно найти медные трубки и довоенные реле."
EN_LINES[5100] = "Junkyard is our bread and butter. You can dig up copper conduits and pre-war relays if you got patience."

RU_LINES[5101] = "Если реактор рванет -- Городу Убежища тоже не поздоровится. Ветер с востока сдует их стерильность."
EN_LINES[5101] = "If the core blows, Vault City won't survive either. East wind will blow their sterile paradise straight to hell."

RU_LINES[5102] = "Слышал про культ светящихся гулей под землей? Бормочут про какое-то Перерождение. Психи."
EN_LINES[5102] = "Heard about glowing ones worshipping the subterranean reactor? Whining about Renewal. Lunatics."

RU_LINES[5103] = "Нос отвалился лет двадцать назад. Сначала переживал, а теперь даже удобно -- запаха серы не чувствую."
EN_LINES[5103] = "Lost my nose twenty years back. Cried at first, but now it's handy -- can't smell the sulphur fumes."

RU_LINES[5104] = "Торговцы боятся заезжать к нам. Думают, мы светимся в темноте и едим сырое мясо браминов."
EN_LINES[5104] = "Caravaneers hate stopping here. Think we glow in the dark and chew raw brahmin guts for breakfast."

RU_LINES[5105] = "Мы никого не трогаем, пока они не лезут к нам с винтовками. Оставьте Гекко в покое."
EN_LINES[5105] = "We leave folks alone so long as they don't point rifles at our doors. Just let Gecko be."

# --- REDDING (5110-5125) ---
RU_LINES[5110] = "Кашель душит с самого утра. В забое пыль такая густая, что фонарь за два шага не видно."
EN_LINES[5110] = "Coughing up grit since sunrise. Dust down in the drift is thick enough to swallow lantern light."

RU_LINES[5111] = "Шахтеры с «Кокавина» опять подрались с парнями «Утренней Звезды». Шериф едва растащил зачинщиков."
EN_LINES[5111] = "Kokoweef miners brawled with Morningstar crews again. Sheriff barely broke it up before lead flew."

RU_LINES[5112] = "Винт губит этот город. Половина забойщиков уже не могут взять кирку в руки без дозы Майрона."
EN_LINES[5112] = "Jet is choking this camp. Half the drift crews can't even lift a pick without their morning puff."

RU_LINES[5113] = "Мэргейв платит звонкой монетой за чистое золото. Но цены в местной лавке сжирают весь заработок."
EN_LINES[5113] = "Marge LeBarge pays hard coin for ore, but local store shelves suck every buck right back out."

RU_LINES[5114] = "Шериф Марион ходит мрачнее тучи. Говорит, если город не возьмется за ум -- придут чужаки и наведут порядок силой."
EN_LINES[5114] = "Sheriff Marion's grim as a gravestone. Says if we don't clean house, outsiders will do it with rope."

RU_LINES[5115] = "В казино «Маламут Салун» сегодня яблоку негде упасть. Шахтеры спускают золотой песок за рулеткой."
EN_LINES[5115] = "Malamute Saloon is packed wall-to-wall. Miners dumping raw gold dust right across the roulette wheel."

RU_LINES[5116] = "Из Нью-Рино идут караваны с наркотой каждую неделю. Семья Мордино хочет забрать все рудники себе."
EN_LINES[5116] = "Chems roll in from New Reno every week. Mordino crime family wants to grab every shaft in town."

RU_LINES[5117] = "НКР обещает порядок и защиту, если мы войдем в их Республику. Знаем мы их порядок -- налоги и виселицы."
EN_LINES[5117] = "NCR promises law and order if we join the Republic. We know their order: crushing taxes and gibbets."

RU_LINES[5118] = "Золотая пыль въелась под ногти. Даже в хлебе этот проклятый кварцевый песок на зубах хрустит."
EN_LINES[5118] = "Gold grit buried under my fingernails. Even the sourdough loaves crunch like sand between your teeth."

RU_LINES[5119] = "В шахте «Большая Ванетта» поселились какие-то твари. Огромные когтистые твари... Никто туда больше не спускается."
EN_LINES[5119] = "Monsters nested down in the Wanamingo mine. Big slithering claws... Nobody dares go down that hole."

RU_LINES[5120] = "Доктор Джонсон в больнице лечит от всего подряд: от переломов до винтовой ломки. Если монета есть."
EN_LINES[5120] = "Doc Johnson patches whatever's broke: crushed limbs or Jet shakes. So long as your coin is good."

RU_LINES[5121] = "Парни Мордино и агенты Бишопа косятся друг на друга в баре. Скоро тут начнется пальба, к гадалке не ходи."
EN_LINES[5121] = "Mordino muscle and Bishop's suit-men staring each other down at the bar. Blood's gonna spill soon."

RU_LINES[5122] = "Кирка затупилась, спина не разгибается. А к вечеру все равно половину жалованья в рулетку спустишь."
EN_LINES[5122] = "Pick is blunt, spine is wrecked. Still gonna dump half my paycheck on cards before midnight."

RU_LINES[5123] = "Осторожнее на улице. Шахтер под винтом не соображает, кто перед ним -- брат или грабитель."
EN_LINES[5123] = "Watch your step out there. A miner tweaking on Jet won't tell his own brother from a highwayman."

RU_LINES[5124] = "Караваны из Города Убежища привозят медикаменты в обмен на золотые слитки. Грабеж средь бела дня."
EN_LINES[5124] = "Vault City caravans haul in pills and haul out pure gold bullion. Legalized highway robbery."

RU_LINES[5125] = "Слышишь гудок? Забой закончил работу. Сейчас улицы заполнят злые, усталые мужики с динамитом в карманах."
EN_LINES[5125] = "Hear that whistle? Work in the drift is done. Mean, tired bastards with dynamite in their pockets heading up."

# --- NEW RENO (5130-5145) ---
RU_LINES[5130] = "Смотри под ноги, провинциал. В Нью-Рино пуля находит лоб быстрее, чем ты успеешь достать бумажник."
EN_LINES[5130] = "Watch your boots, hick. In New Reno, lead punches through your skull before your wallet clears leather."

RU_LINES[5131] = "Четыре семьи держат город за глотку: Сальваторе, Бишоп, Мордино и Райт. Перейдешь дорогу любой -- закопают на поле для гольфа."
EN_LINES[5131] = "Four families choke this town: Salvatore, Bishop, Mordino, Wright. Cross any, you end under the golf course."

RU_LINES[5132] = "У Сальваторе лазерное оружие. Говорят, они режут людей пополам световыми лучами прямо на глазах у толпы."
EN_LINES[5132] = "Salvatores pack laser heaters. They say red beams slice wiseguys in half right on the open boulevard."

RU_LINES[5133] = "В казино «Десперадо» шулеров топят в выгребных ямах. Карты там сдают только проверенные парни Мордино."
EN_LINES[5133] = "They drown card sharks in cesspools behind the Desperado. Only trusted Mordino boys deal the deck."

RU_LINES[5134] = "Братья Корсиканцы ищут свежее мясо для своих фильмов. Если морда смазливая -- можешь поднять пару сотен монет."
EN_LINES[5134] = "Corsican Brothers are hunting fresh flesh for their smut reels. Pretty mug can pocket a couple hundred."

RU_LINES[5135] = "Семья Райт гонит лучший самогон на севере. Старик Орвилл не терпит винт, зато спирт льется рекой."
EN_LINES[5135] = "The Wright clan distills top-shelf hooch. Old Orville despises Jet, but his alcohol flows like rivers."

RU_LINES[5136] = "На Второй улице наркоманы валяются штабелями. Винт Майрона выжигает мозги за пару месяцев."
EN_LINES[5136] = "Second Street junkies stacked like cordwood. Myron's Jet fries a man's grey matter in two fast months."

RU_LINES[5137] = "У Бишопа в «Акульем Зубе» крутятся политики из НКР. Джон Бишоп метит высоко, метит прямо в губернаторы."
EN_LINES[5137] = "NCR congress-hounds prowling Bishop's Shark Club. John Bishop is aiming high -- straight for governorship."

RU_LINES[5138] = "Не связывайся с парнями в плащах и федорах. Это бойцы Сальваторе, у них пальцы чешутся на спусковых крючках."
EN_LINES[5138] = "Don't mess with trenchcoats and fedoras. Salvatore button-men itch to squeeze triggers on strangers."

RU_LINES[5139] = "Вчера на ринге «Джунглей» боксер Мастико сломал челюсть претенденту. Кровь с брезента до утра отмывали."
EN_LINES[5139] = "Masticator broke a contender's jaw at the Jungle Gym. Scrubbed tooth chips and blood off canvas till dawn."

RU_LINES[5140] = "В подворотне шлюхи дерутся за клиентов битыми бутылками. Добро пожаловать в самый яркий город на свете."
EN_LINES[5140] = "Hookers in the alley carving each other with broken necks over tricks. Welcome to the brightest pit on earth."

RU_LINES[5141] = "Томми-ганы трещат каждую ночь. В Рино похоронное бюро -- самый прибыльный бизнес."
EN_LINES[5141] = "Tommy guns rattle every midnight. Hearse driver is running the most profitable racket in New Reno."

RU_LINES[5142] = "Ренеско в аптеке злой, как собака. Попробуй попросить у него аспирин -- обложит пятиэтажным матом."
EN_LINES[5142] = "Renesco behind the pharmacy counter is sour as bile. Ask him for aspirin, he curses your entire bloodline."

RU_LINES[5143] = "Если выиграешь куш в казино «Шаркс» -- не выходи через главную дверь. В переулке уже ждут ребята с ножами."
EN_LINES[5143] = "Hit a jackpot at Shark Club? Don't stroll out the front arch. Shiv-artists already wait in the alley."

RU_LINES[5144] = "У Майрона под охраной целая конюшня рабов. Парень гений, но тварь редкостная."
EN_LINES[5144] = "Myron keeps a stable of test-slaves locked down. Boy's a chem genius, but rotten to the core."

RU_LINES[5145] = "Рино никогда не спит. Здесь умирают под музыку и аплодисменты."
EN_LINES[5145] = "New Reno never sleeps. Folks check out here with showtunes playing and suckers clapping."

# --- ARROYO (5150-5169) ---
RU_LINES[5150] = "Колодец почти пересох. Вчера со дна подняли только серый ил."
EN_LINES[5150] = "The village well is dry dust. Yesterday the bucket dragged up nothing but gray river silt."

RU_LINES[5151] = "Опять брамин издох у изгороди. Мясо пахнет горечью, есть его нельзя."
EN_LINES[5151] = "Another yearling died along the fence. Flesh smells bitter from drought; unfit to roast."

RU_LINES[5152] = "Старейшина весь вечер сидит у костра. Говорит, духи предков отвернулись от нас."
EN_LINES[5152] = "The Elder sits by smoke all night. Says ancestors turned their faces from our people."

RU_LINES[5153] = "Хакунин натирает шкуры горьким корнем. От этой вони глаза слезятся на весь шатер."
EN_LINES[5153] = "Hakunin boils root mash in his tent. Stench burns your eyes clean across the canyon."

RU_LINES[5154] = "В каньоне опять шевелятся ядовитые муравьи. Мой брат едва унес ноги на той неделе."
EN_LINES[5154] = "Stinging ants swarm the lower canyon rocks. My brother barely dragged his legs back last hunt."

RU_LINES[5155] = "Если Избранный не принесет ГЭКК, зимой нам придется варить кожаные ремни."
EN_LINES[5155] = "If the Chosen fails to find the GECK, we chew boiled scabbards and harness leather come frost."

RU_LINES[5156] = "Тотемы Убежища потускнели. Говорят, Священный Тринадцатый был полон чистой воды."
EN_LINES[5156] = "Vault totems fade in the sun. Old songs say Holy Thirteen flowed with endless sweet water."

RU_LINES[5157] = "Наконечник копья затупился о хитин скорпиона. Придется снова искать кремень."
EN_LINES[5157] = "Flint point chipped on a radscorpion shell. Got to scrape another spearhead from river rock."

RU_LINES[5158] = "Ночью на скалах выли койоты. Шаман говорит, это души голодных предков плачут."
EN_LINES[5158] = "Coyotes screamed along the ridge at moonrise. Shaman says hungry ghost-blood is weeping."

RU_LINES[5159] = "Цветок брока нынче мелкий и сухой. Лечебный порошок выходит совсем слабым."
EN_LINES[5159] = "Broc flower petals wither thin as skin. Healing brew turns out watery and weak this moon."

RU_LINES[5160] = "Мой лук рассохся от жары. Тетива лопнула прямо во время охоты на гекко."
EN_LINES[5160] = "Heat split my hunting bow. Gut-string snapped right as a golden gecko broke from brush."

RU_LINES[5161] = "Кузнецы говорят, железа не осталось вовсе. Все копья теперь только из кости."
EN_LINES[5161] = "Smiths say scrap-iron is gone. Every new javelin is carved from bleached brahmin bone."

RU_LINES[5162] = "Смотри под ноги на тропе. Радужные скорпионы прячутся в расщелинах камней."
EN_LINES[5162] = "Mind your moccasins on the path. Canyon scorpions nest deep under sun-baked flat-stones."

RU_LINES[5163] = "Хакунин опять разговаривает со своими растениями в огороде. Странный он старик."
EN_LINES[5163] = "Hakunin is out talking to squash vines again. Strange old bird hears voices in the leaves."

RU_LINES[5164] = "Если встретишь Нагора -- скажи ему, что его собака опять разорила чужой шалаш."
EN_LINES[5164] = "Spot Nagor, tell him Smoke tore through drying racks again. Dog needs a stout switch."

RU_LINES[5165] = "Ветер несет горячую пыль с юга. Там, говорят, земли полны чудовищ из металла."
EN_LINES[5165] = "Scorching gale off south wastes. Old tales swear metal beasts roam those burnt lowlands."

RU_LINES[5166] = "Помни наставления Старейшины: чужакам за пределами каньона нельзя верить."
EN_LINES[5166] = "Heed the Elder's proverb: Out-landers beyond the gorge carry poison tongue and sharp knives."

RU_LINES[5167] = "Вчера нашел старую гильзу у реки. Реликвия Великого Выходца из Убежища."
EN_LINES[5167] = "Dug up a spent brass casing in dry gravel. Relic from the holy Vault Dweller's first trail."

RU_LINES[5168] = "Жажда мучит с самого рассвета. Воды дают только по полгорсти в полдень."
EN_LINES[5168] = "Thirst scorches throat since first light. Council rations water by single horn cup at noon."

RU_LINES[5169] = "Да хранят духи наше племя. Без священного тринадцатого мы все ляжем в пыль."
EN_LINES[5169] = "May spirits shield the tribe. Without holy Thirteen, our bones crumble to canyon sand."

# --- BROKEN HILLS (5170-5189) ---
RU_LINES[5170] = "В шахте опять сбоит очиститель воздуха. Без фильтров там и часу не продышать."
EN_LINES[5170] = "Air scrubber choked in the drift again. Down there without charcoal filters, lungs fry in an hour."

RU_LINES[5171] = "Маркус держит этот город в кулаке. Без его минигана люди и мутанты давно бы перегрызлись."
EN_LINES[5171] = "Marcus keeps a lid on this pressure cooker. Without his minigun, muties and smoothskins tear each other apart."

RU_LINES[5172] = "Уран -- тяжелая штука. Пальцы от него не светятся, зато зубы к сорока годам выпадают."
EN_LINES[5172] = "Uranium ore is rough trade. Hands don't glow, but teeth rot out of your gums before forty."

RU_LINES[5173] = "Не называй мутанта «куском мяса», если тебе дороги твои ребра, парень."
EN_LINES[5173] = "Don't spit 'meathead' at a super mutant unless you fancy wearing your ribs inside out, kid."

RU_LINES[5174] = "Тайфон в жилом секторе целый день травит байки о сокровищах. Старый склеротик."
EN_LINES[5174] = "Typhon babbles about buried caps all afternoon. Old ghoul's grey matter has dry rot."

RU_LINES[5175] = "Люди ворчат, что мутанты забирают лучшую пайку. Глупцы, они же таскают камни втрое тяжелее."
EN_LINES[5175] = "Miners grumble muties get prime meat rations. Morons forget muties haul boulders three times their size."

RU_LINES[5176] = "Шахтерский профсоюз опять спорит с администрацией. Скоро до драки на лопатах дойдет."
EN_LINES[5176] = "Miners' guild barking at city hall again. Going to settle shift pay with spade handles soon."

RU_LINES[5177] = "В баре у Фила вчера опять набили морду заезжему караванщику. Не любим мы смутьянов."
EN_LINES[5177] = "Broke a traveling guard's snout at Phil's taphouse last night. We don't take kindly to agitators."

RU_LINES[5178] = "Радость одна -- мутанты не пьют самогон ведрами. Иначе город бы уже сгорел дотла."
EN_LINES[5178] = "One mercy: super muties don't guzzle hooch by the gallon. Town would have burned down years ago."

RU_LINES[5179] = "Если идешь в нижние штреки -- бери противогаз. Там скапливается радоновый газ."
EN_LINES[5179] = "Heading down to lower stopes? Fasten your respirator. Radon gas pools heavy in the sump."

RU_LINES[5180] = "Маркус говорит, мы строим новое будущее. Хотелось бы дожить до этого будущего."
EN_LINES[5180] = "Marcus preaches we're building a new world. Sure hope I live long enough to draw breath in it."

RU_LINES[5181] = "Караван из Города Убежища задержался. Линетт опять корчит рожи из-за урановых цен."
EN_LINES[5181] = "Vault City pack train is late. Lynette's council pinching pennies over raw yellowcake again."

RU_LINES[5182] = "Гули отлично переносят радиацию в забое. Жаль только, суставы у них рассыпаются на ходу."
EN_LINES[5182] = "Ghouls shrug off rad-seeps in the shaft. Shame their knee joints turn to chalk while digging."

RU_LINES[5183] = "Слышал про заговор против мутантов? Шериф уже приглядывается к паре крикунов."
EN_LINES[5183] = "Whispers about bigots scheming against mutants? Sheriff has his eye on two loudmouths already."

RU_LINES[5184] = "Пес Сеймур у колодца сообразительнее половины здешних шахтеров. Чистая правда."
EN_LINES[5184] = "Seymour the hound by the well has more wits than half the crew on the winch. Gospel truth."

RU_LINES[5185] = "Пыль скрипит на зубах с утра до ночи. Даже вода здесь отдает желтым железом."
EN_LINES[5185] = "Grit grinds between teeth dawn to dusk. Even pump water tastes like iron oxide and sulphur."

RU_LINES[5186] = "Старый Создатель обещал нам вечность, а оставил кирки и тачки с урановой рудой."
EN_LINES[5186] = "The old Master promised mutants eternity. Handed us wheelbarrows and uranium pickaxes instead."

RU_LINES[5187] = "Эй, чужак, не стой под подъемником. Трос старый, сорвется -- лепешкой станешь."
EN_LINES[5187] = "Watch out under that ore hoist, traveler. Cable's frayed; snaps, and you're pancake gravy."

RU_LINES[5188] = "Торговцы из НКР платят за очищенный уран вдвое больше, чем загребущие снобы из Убежища."
EN_LINES[5188] = "NCR merchants offer double for refined fuel ingots compared to those skinflints in Vault City."

RU_LINES[5189] = "Здесь тихо, пока работают насосы. Если вентиляция встанет -- начнется сущий ад."
EN_LINES[5189] = "Peaceful so long as the sump engines turn. Blowers fail, and this hole turns into suffocation hell."

# --- NCR / SHADY SANDS (5190-5209) ---
RU_LINES[5190] = "Убери оружие из рук, гражданин! В НКР действует закон, здесь тебе не дикие пустоши."
EN_LINES[5190] = "Holster that sidearm, citizen! NCR has strict statutes. You're not in the lawless waste now."

RU_LINES[5191] = "Президент Танди правит твердой рукой. При ней Шейди Сэндс стал столицей Республики."
EN_LINES[5191] = "President Tandi governs with an iron hand. Under her watch, Shady Sands built the Republic."

RU_LINES[5192] = "Сенаторы опять подняли пошлины на перегон браминов. Скотоводы уже точат ножи."
EN_LINES[5192] = "Senate raised grazing tariffs on longhorns again. Cattle barons are grinding their bowies."

RU_LINES[5193] = "Рейнджеры НКР на прошлой неделе накрыли банду работорговцев к югу от города. Так им и надо."
EN_LINES[5193] = "NCR Rangers wiped a slaver outfit south of town last week. Scum deserved every hollow-point."

RU_LINES[5194] = "Барон Вестин держит лучшие пастбища. Но сердце у старика совсем сдало в последнее время."
EN_LINES[5194] = "Baron Westin grazes the finest herds, but the old gentleman's ticker is skipping beats lately."

RU_LINES[5195] = "Конгресс обсуждает присоединение Реддинга. Без золота нам армию на севере не прокормить."
EN_LINES[5195] = "Congress debates annexing Redding. Without gold bullion, the Republic can't feed northern garrisons."

RU_LINES[5196] = "В баре Дасти подают нормальное пиво. Без радиации и без браминьей мочи, по стандарту."
EN_LINES[5196] = "Dusty pours standard beer. Certified zero rads, no brahmin swill -- brewed to health code."

RU_LINES[5197] = "Не связывайся с людьми Бишопа из Нью-Рино. Они пытаются купить наших чиновников."
EN_LINES[5197] = "Stay clear of Bishop's New Reno lobbyists. Sleaze-merchants trying to grease senatorial palms."

RU_LINES[5198] = "Здесь порядок и суд. Если украдешь хоть патрон -- пойдешь отрабатывать на каменоломне."
EN_LINES[5198] = "Courts and statutes govern here. Steal a single brass shell, you break basalt on chain gang."

RU_LINES[5199] = "Барон Карлсон забаррикадировался в своем особняке. Боится наемных убийц с запада."
EN_LINES[5199] = "Baron Carlson bolted inside his manor. Terrified of western hitmen sneaking through the gate."

RU_LINES[5200] = "Рейнджеры набирают добровольцев. Охота на работорговцев -- дело благородное, но смертельное."
EN_LINES[5200] = "Ranger recruiting desk is open. Slaver-hunting is clean work, but damn near suicidal."

RU_LINES[5201] = "Город Убежища смотрит на нас как на грязь под ногами. Ничего, скоро их спесь поубавится."
EN_LINES[5201] = "Vault City looks down their noses at our constitution. We'll see how high and mighty they feel soon."

RU_LINES[5202] = "Доктор Генри ставит странные опыты в своей лаборатории. Говорят, лечит мутантов."
EN_LINES[5202] = "Dr. Henry brews strange tonics in his lab. Rumor says he's engineering cures for mutant strain."

RU_LINES[5203] = "Смотри за документами. Без разрешения на въезд шериф вышвырнет тебя за ворота к ночи."
EN_LINES[5203] = "Keep travel papers dry. Without an entry permit, sheriff's deputies run you outside before sunset."

RU_LINES[5204] = "Засуха давит на фермеров. Если не найдем новые источники воды, начнется нормирование."
EN_LINES[5204] = "Drought choking outer farms. Don't tap new aquifers soon, ration coupons start next month."

RU_LINES[5205] = "Полицейские патрули не берут взяток. Попробуешь сунуть доллары -- сразу загремишь за решетку."
EN_LINES[5205] = "Constables won't take bribes. Wave dirty scrip at an officer, you'll see the lockup from inside."

RU_LINES[5206] = "Рядом с рынком всегда толкотня. Караваны приходят из самого Хаба и Модока."
EN_LINES[5206] = "Bazaar's jammed shoulder-to-shoulder. Freight trains roll all the way from the Hub and Modoc."

RU_LINES[5207] = "Устав НКР гарантирует права каждому человеку. Только вот бароны эти права иногда покупают."
EN_LINES[5207] = "NCR charter guarantees rights for every soul. Just happens rich cattle barons can afford extra."

RU_LINES[5208] = "Чистые улицы, мощеные камнем... Мой дед о таком в своих пустошах и мечтать не мог."
EN_LINES[5208] = "Paved limestone avenues... My grandfather roaming the mud never dreamed civilized streets existed."

RU_LINES[5209] = "Держи карманы застегнутыми у входа на базар. Там крутится полно проходимцев."
EN_LINES[5209] = "Button your coat near the gate market. Lots of slick drifters looking to pick a lining."

# --- VAULT 15 (5210-5225) ---
RU_LINES[5210] = "Не подходи к нашим лачугам! Нам и самим жрать нечего, побирушек не кормим."
EN_LINES[5210] = "Back away from the shanties! We're scraping bottom ourselves; no handouts for vagrants."

RU_LINES[5211] = "НКР хочет забрать наше Убежище себе. Называют это «законом», а на деле -- грабеж."
EN_LINES[5211] = "NCR wants to seize our Vault. Wrap it in pretty legal statutes, but it's pure armed eviction."

RU_LINES[5212] = "Генератор в нижних отсеках опять сдох. Мы сидим в темноте уже третью неделю."
EN_LINES[5212] = "Sump generator down below gave out again. Been burning scavenged tallow in the dark three weeks."

RU_LINES[5213] = "Из пещеры по ночам доносятся голоса. Там засели люди Дариона... жестокие ублюдки."
EN_LINES[5213] = "Voices echo from the cave jaw after dusk. Darion's raiders holed up down there... vicious bastards."

RU_LINES[5214] = "Мой ребенок кашляет от пещерной сырости. Доктора здесь нет, только знахарка с корешками."
EN_LINES[5214] = "My young one hacks blood from cave damp. No physician out here, just a crone boiling roots."

RU_LINES[5215] = "Мы построили эту деревню на камнях. Мы не уйдем отсюда, что бы ни решал Сенат НКР."
EN_LINES[5215] = "We laid these flagstones with bare knuckles. Won't budge an inch, whatever NCR senate decrees."

RU_LINES[5216] = "Дарион никого не пускает к главному терминалу. Говорят, он совсем тронулся умом."
EN_LINES[5216] = "Darion bars everyone from the core computer deck. Word is the old warlord went stark raving mad."

RU_LINES[5217] = "Вчера крысы загрызли последнего козленка. Жизнь здесь с каждым месяцем всё солонее."
EN_LINES[5217] = "Mole rats butchered our last yearling goat. Life on this slag heap gets sourer every moon."

RU_LINES[5218] = "Кто ты такой? Если шпион из Шейди Сэндс -- убирайся, пока камнями не закидали."
EN_LINES[5218] = "Who invited you? Shady Sands snooper? Clear out before rock-slings crack your skull."

RU_LINES[5219] = "Вода с потолка капает ржавая. Если не прокипятить -- живот скрутит так, что взвоешь."
EN_LINES[5219] = "Roof drip tastes like iron scales. Fail to boil the cup, your guts will knot till you scream."

RU_LINES[5220] = "Ханы держат оружие и консервы на нижних уровнях. А нам бросают объедки со стола."
EN_LINES[5220] = "Khans hoard carbines and canned beef down deep. Toss gristle and moldy crusts to the shanties."

RU_LINES[5221] = "Ребекка пытается договориться с Республикой. Но старейшины не верят чужакам в галстуках."
EN_LINES[5221] = "Rebecca wants treaties with the Republic. Squatters don't trust politicians wearing tailored ties."

RU_LINES[5222] = "В темноте заброшенных тоннелей слышен скрежет. Там водятся твари похуже кротокрысов."
EN_LINES[5222] = "Scraping down dark sub-tunnels. Things nesting in the collapsed drifts far worse than mole rats."

RU_LINES[5223] = "Если Дарион узнает, что ты расспрашиваешь о входе -- его головорезы спустят с тебя шкуру."
EN_LINES[5223] = "Darion catches wind you're asking after the vault seal, his raiders will peel your hide."

RU_LINES[5224] = "Каждый кусок железа здесь снят со старых стен Убежища. Мы держимся за это место."
EN_LINES[5224] = "Every sheet of tin here was pried off the old bulkheads. We bled for this miserable roost."

RU_LINES[5225] = "Уходи с миром, путник. Здесь нет ни золота, ни выпивки. Только пыль и голод."
EN_LINES[5225] = "Walk on in peace, traveler. No gold here, no rotgut. Just alkali dust and hungry bellies."

# --- VAULT 13 (5230-5245) ---
RU_LINES[5230] = "Не бойся нас, человек. Грутар учит нас терпению и состраданию к твоему роду."
EN_LINES[5230] = "Do not recoil, human. Gruthar teaches our pack patience and mercy toward your fragile kin."

RU_LINES[5231] = "Наши когти остры, но наш разум ищет знания, а не крови слабых."
EN_LINES[5231] = "Our talons rend steel, yet our minds seek understanding, not the spilled blood of the weak."

RU_LINES[5232] = "Центральный компьютер Убежища молчит. Модуль распознавания речи сгорел много лун назад."
EN_LINES[5232] = "The Overseer console is mute. Voice recognition components fused to slag many cycles past."

RU_LINES[5233] = "Грутар говорит, что все живые существа должны жить в гармонии под этим небом."
EN_LINES[5233] = "Gruthar speaks of fellowship: all sentient creations sharing the wide sky in brotherhood."

RU_LINES[5234] = "Горис ушел изучать мир наверху. Мы молимся духам стали, чтобы с ним всё было хорошо."
EN_LINES[5234] = "Goris roams the high wastes seeking lore. We ask the silent stone that harm does not find him."

RU_LINES[5235] = "Люди пустошей видят в нас только чудовищ. Они стреляют прежде, чем мы успеваем сказать слово."
EN_LINES[5235] = "Surface dwellers see only nightmares. They level muskets before our lips can shape greeting."

RU_LINES[5236] = "Наши детеныши учатся читать по довоенным терминалам в библиотеке Убежища."
EN_LINES[5236] = "Our hatchlings decipher ancient script upon terminal glass within the vault archives."

RU_LINES[5237] = "Стальные двери защищают нас от бурь и от зла, что бродит по выжженной земле."
EN_LINES[5237] = "The great blast door shields our nest from irradiated gales and the cruel hunters outside."

RU_LINES[5238] = "ВРЭ изменил наши тела и открыл наш разум. Мы не монстры Создателя, мы -- стая Грутара."
EN_LINES[5238] = "The virus remade our flesh and unchained thought. We are no Master's hounds; we are Gruthar's pack."

RU_LINES[5239] = "Свет люминесцентных ламп режет глаза. Но это лучше, чем мрак пещер."
EN_LINES[5239] = "Tube lights sting our yellow eyes, yet sterile illumination is kinder than tomb-black caverns."

RU_LINES[5240] = "Если ты пришел с миром -- оставайся. Если с ненавистью -- наши когти вспомнят свое ремесло."
EN_LINES[5240] = "Enter in peace and share our warmth. Enter with malice, and ancient talons remember slaughter."

RU_LINES[5241] = "Оборудование гидропоники требует ремонта. Нам не хватает медных контактов и схем."
EN_LINES[5241] = "Hydroponic troughs fail for want of maintenance. We lack copper connectors and micro-relays."

RU_LINES[5242] = "Люди, что живут с нами, делят с нами хлеб и знания. Мы защищаем их от внешних бед."
EN_LINES[5242] = "The human refugees break bread in our chambers. In return, our hide turns away raiders."

RU_LINES[5243] = "Голос человека звучит иначе, чем рык стаи. Но смысл слов один -- надежда на выживание."
EN_LINES[5243] = "Man's speech sounds soft compared to pack roar, yet words speak the same longing: survival."

RU_LINES[5244] = "Не подходи близко к инкубатору с кладкой. Материнский инстинкт сильнее любых доводов разума."
EN_LINES[5244] = "Keep clear of the egg nests. The nesting brood-mother's fury outstrips any philosophical debate."

RU_LINES[5245] = "Пусть твой путь будет чистым, путник. Помни: разум важнее силы клыков."
EN_LINES[5245] = "May your path be unclouded. Remember well: intellect weighs heavier than curved ivory fangs."

# --- SAN FRANCISCO (5250-5275) ---
RU_LINES[5250] = "Император видит всё. Его кремниевая мудрость направляет народ Ши через века."
EN_LINES[5250] = "The Emperor observes all. His silicon computation steers the Shi through shifting tides."

RU_LINES[5251] = "Держи свое грубое оружие в ножнах, варвар. В Чайнатауне чтут вековые традиции порядка."
EN_LINES[5251] = "Sheathe your crude steel, barbarian. Chinatown observes sacred ordinances of civic restraint."

RU_LINES[5252] = "Доктор Шенг опять заперся в лаборатории. Его опыты с гибридными спорами пугают советников."
EN_LINES[5252] = "Dr. Sheng locked his genetics bay again. Botanical spore trials make councilors nervous."

RU_LINES[5253] = "Дракон победил в последнем бою без единого удара. Чистое искусство владения ци."
EN_LINES[5253] = "The Dragon claimed victory without landing one fist. Sublime mastery of flowing chi."

RU_LINES[5254] = "Биохимики Ши синтезировали новое полимерное топливо. Весь залив скоро будет зависеть от нас."
EN_LINES[5254] = "Shi biochemists synthesized dense polymer fuel. The bay region will soon bow for our kerosene."

RU_LINES[5255] = "Танкер «Валдез» -- ржавая помойка. Удивительно, как эти бездомные оборванцы еще не потопили его."
EN_LINES[5255] = "The Valdez is a barnacled rust-bucket. Wonder those flea-bitten punks haven't scuttled it."

RU_LINES[5256] = "Эй, чувак, есть лишняя сигарета? На этом корыте с тоски сдохнуть можно, пока волны бьют в борт."
EN_LINES[5256] = "Hey jack, spare a smoke? Stuck on this hulk going stir-crazy watching surf rot the hull plates."

RU_LINES[5257] = "Капитан танкера сидит в рубке и глушит виски. Говорит, пока навигатор не починят -- мы на мели."
EN_LINES[5257] = "The Captain swills whiskey in the bridge. Says until the nav computer wakes, we're beached for good."

RU_LINES[5258] = "В трюм «Валдеза» не суйся без огнемета. Там расплодились мутировавшие болотники и кентавры."
EN_LINES[5258] = "Don't poke around cargo hold lower decks without a flamer. Mirelurks and centaurs spawned thick."

RU_LINES[5259] = "Панки верят в свободу, а Ши верят в дисциплину. Поэтому у них дворцы, а у нас ржавые койки."
EN_LINES[5259] = "Punks worship liberty, Shi worship order. That's why they got tiled palaces and we sleep on iron wire."

RU_LINES[5260] = "Хабологи опять раздают свои листовки на площади. Обещают очистить нейроны от мусора. Сектанты."
EN_LINES[5260] = "Hubologists hawking pamphlets on the concourse again. Promise neuro-cleansing. Cultist quacks."

RU_LINES[5261] = "Твой нейро-уровень загрязнен примитивными импульсами! Пройди дзета-сканирование у AHS-7!"
EN_LINES[5261] = "Your neuro-levels are clouded by primitive engrams! Seek Zeta-alignment before AHS-7!"

RU_LINES[5262] = "Великий Отец Хабб поведет наш звездолет к планете Кволо! Земля обречена на угасание."
EN_LINES[5262] = "Great Father Hubb shall launch our star vessel to Quetzel! This scorched orb is doomed to decay."

RU_LINES[5263] = "Пожертвуй пятьсот долларов на нужды Церкви, и твой дух поднимется на ступень AHS-2."
EN_LINES[5263] = "Tithe five hundred hard dollars to the Church, and elevate your spiritual essence to AHS-2."

RU_LINES[5264] = "Охрана Хабологов вооружена лазерными карабинами. Не вздумай шутить над их балахонами."
EN_LINES[5264] = "Hubologist sentries carry energized carbines. Better keep quiet about their purple robes."

RU_LINES[5265] = "У торговцев в Чайнатауне лучшие боеприпасы на побережье. Только цены дерут безбожно."
EN_LINES[5265] = "Chinatown arms dealers stock prime coast ordnance. Gouge you blind on the barter though."

RU_LINES[5266] = "Запах жареной рыбы и благовоний... Сан-Франциско пахнет совсем иначе, чем пыльные пустоши."
EN_LINES[5266] = "Spiced wok-oil and temple incense... San Francisco carries a different scent than the dry interior."

RU_LINES[5267] = "Ло Пэн и Дракон ненавидят друг друга. Рано или поздно их вражда смоет кровью всю улицу."
EN_LINES[5267] = "Lo Pan and the Dragon nurture bitter grudge. Sooner or later, blood will wash the central street."

RU_LINES[5268] = "Слышал про тайную базу Анклава на севере? Говорят, они летают на черных винтокрылах без колес."
EN_LINES[5268] = "Heard rumors of Enclave outposts up the coast? They say black vertibirds drop out of clouds."

RU_LINES[5269] = "Металл танкера стонет при каждом приливе. Надеюсь, донные переборки выдержат еще сезон."
EN_LINES[5269] = "Valdez hull groans with every high swell. Pray the double-bottom ribs hold through winter."

RU_LINES[5270] = "Ши не любят чужаков. Если ты не принес пользу Императору -- ты просто пустое место на мостовой."
EN_LINES[5270] = "The Shi care nothing for drifters. Yield no tribute to the Emperor, you're dust under sandals."

RU_LINES[5271] = "Панки играют тяжелый рок по ночам. Местные стражники грозят перестрелять их динамики."
EN_LINES[5271] = "Punks blast guitar squall across the harbor till 3 AM. Shi patrols threaten to ventilate their speakers."

RU_LINES[5272] = "В лабораториях Хабологов стоит гул мощных генераторов. Что-то они замышляют с шаттлом."
EN_LINES[5272] = "Heavy turbines hum deep in Hubologist bays. Cult's rigging something nasty with that space shuttle."

RU_LINES[5273] = "Морской туман здесь такой густой, что в трех шагах не видно собственного карабина."
EN_LINES[5273] = "Bay fog rolls in thick as curdled milk. Can't spot your rifle barrel ten paces ahead."

RU_LINES[5274] = "Компьютер Ши взломать невозможно. Любой глупец, сунувший отмычку, получит пулю в лоб."
EN_LINES[5274] = "Emperor logic banks cannot be breached. Slicers poking around receive lead through the forehead."

RU_LINES[5275] = "Если тебе нужны энергобатареи -- копи золото. Торговцы Ши не берут мятые довоенные бумажки."
EN_LINES[5275] = "Need fusion batteries? Hoard bullion. Shi merchants laugh at faded paper script."

# --- NAVARRO (5280-5299) ---
RU_LINES[5280] = "Стой! Где твоя форма, рядовой?! Сержант Дорнан с тебя шкуру живьем спустит за нарушение устава!"
EN_LINES[5280] = "Halt! Where is your uniform, trooper?! Sergeant Dornan will skin your rear raw for regulation breach!"

RU_LINES[5281] = "Винтокрыл номер четыре требует переборки турбины. Керосин здесь жрут, как не в себя."
EN_LINES[5281] = "Vertibird four needs turbine overhaul. Birds drink aviation spirit like water."

RU_LINES[5282] = "Периметр на юге усилен автоматическими турелями. Любой дикарь превратится в пепел за секунду."
EN_LINES[5282] = "South tree-line covered by interlocking dual-plasma turrets. Any trespasser vaporizes on contact."

RU_LINES[5283] = "Связь с Вышкой сегодня с перебоями. Говорят, грозовой фронт над океаном глушит антенны."
EN_LINES[5283] = "Comm-link to the Rig is crackling. Squall line over the Pacific is scattering our dish arrays."

RU_LINES[5284] = "Не стой возле посадочной площадки. Выхлоп двигателей сожжет комбинезон к чертовой матери."
EN_LINES[5284] = "Clear the tarmac apron! Rotor downwash will cook your dungarees before you smell kerosene."

RU_LINES[5285] = "Повар в столовой опять сварил сухпай из синтетического белка. В горло не лезет эта гадость."
EN_LINES[5285] = "Mess tech boiled synthesized ration bars again. Glue tastes like engine gasket rubber."

RU_LINES[5286] = "Техники возятся с плазменным генератором. Если охлаждение сбоит -- база взлетит на воздух."
EN_LINES[5286] = "Techs fiddling with the main transformer. Coolant loops trip, this outpost goes sub-critical."

RU_LINES[5287] = "Патруль доложил о следах шпионов НКР в холмах. Приказ один: стрелять на поражение без предупреждения."
EN_LINES[5287] = "Recon logged Republic scout tracks in the scrub. Standing orders: fire for effect, zero questions."

RU_LINES[5288] = "Силовая броня Mark II весит полсотни фунтов, зато ни одна пуля дикарей ее не берет."
EN_LINES[5288] = "Advanced Power Armor Mark II weighs fifty pounds, but tribal lead bounces like dried peas."

RU_LINES[5289] = "Сержант сегодня в бешенстве. Кто-то оставил масляную ветошь в оружейном арсенале."
EN_LINES[5289] = "Dornan's on the warpath. Some recruit left solvent rags piled behind the ammo magazine."

RU_LINES[5290] = "Мы -- законная армия Соединенных Штатов. Мы очистим эту землю от мутантов и скверны."
EN_LINES[5290] = "We represent the legitimate United States Armed Forces. We will cleanse this continent of taint."

RU_LINES[5291] = "Пропускной режим строгий. Потеряешь жетон -- пойдешь под трибунал до заката."
EN_LINES[5291] = "Security protocol is absolute. Misplace your keycard, you face court-martial before taps."

RU_LINES[5292] = "Кодиак опять спорит с пилотами. Те жалуются на перегрев лопастей на бреющем полете."
EN_LINES[5292] = "Hangar chief chewing out flight officers. Pilots pushing low-altitude runs until rotor bearings bake."

RU_LINES[5293] = "Заправка винтокрыла -- работа для смертников. Одно неверное движение с вентилем, и прощай рука."
EN_LINES[5293] = "Fueling vertibirds is suicide detail. Twitch on that high-pressure valve, kiss your fingers goodbye."

RU_LINES[5294] = "На складе не хватает микроядерных батарей. Похоже, кто-то приворовывает имущество базы."
EN_LINES[5294] = "Micro-fusion inventory came up three crates short. Someone's pocketing government munitions."

RU_LINES[5295] = "Дикари за забором даже не понимают, какое оружие сосредоточено на этой заставе."
EN_LINES[5295] = "Savages in the bush haven't the faintest inkling of the firepower stationed inside this fence."

RU_LINES[5296] = "Служба в карауле на ветру выматывает за пару часов. Песок скрипит в сочленениях брони."
EN_LINES[5296] = "Perimeter sentry shift in the gale is brutal. Coastal grit grinding inside servo joints."

RU_LINES[5297] = "Доктор Шребер ставит опыты над подопытными особями в подвале. Звуки оттуда жуткие."
EN_LINES[5297] = "Dr. Schreber's running vivisections in the bunker vault. Sounds coming through vents turn your gut."

RU_LINES[5298] = "Каждый винтик на этой базе учтен в ведомости. Порядок -- залог победы Анклава."
EN_LINES[5298] = "Every cotter pin here is logged in the Quartermaster ledger. Discipline ensures Enclave triumph."

RU_LINES[5299] = "Оружие на предохранитель, боец. Случайный выстрел -- и ты драишь плац зубной щеткой."
EN_LINES[5299] = "Toggle that selector to safe, soldier. An accidental discharge puts you on latrine detail with a toothbrush."

# --- ENCLAVE OIL RIG (5300-5315) ---
RU_LINES[5300] = "Президент Ричардсон обратится к нации через час. Мы стоим на пороге великого возрождения Америки."
EN_LINES[5300] = "President Richardson addresses staff shortly. We stand on the precipice of American restoration."

RU_LINES[5301] = "Токсин Керлинга почти готов. Материк будет очищен от генетического брака раз и навсегда."
EN_LINES[5301] = "Curling's FEV strain is calibrated. The mainland shall be cleansed of genetic deviations."

RU_LINES[5302] = "Датчики реактора в зеленой зоне. Защитный контур выдержит любое внешнее давление океана."
EN_LINES[5302] = "Core pressure holds nominal. Marine sub-station bulkheads can withstand any ocean swell."

RU_LINES[5303] = "Мутанты на материке обречены. Их ДНК деградировала до уровня примитивных зверей."
EN_LINES[5303] = "Mainland mutates are evolutionary dead-ends. Chromosomes shredded beyond moral relevance."

RU_LINES[5304] = "Доктор Керлинг работает без сна третьи сутки. Спасение чистой расы требует жертв."
EN_LINES[5304] = "Dr. Curling hasn't slept in seventy-two hours. Reclaiming our heritage requires relentless labor."

RU_LINES[5305] = "Уровень радиации на вышке строго нулевой. Мы сохранили первозданную чистоту генома предков."
EN_LINES[5305] = "Atmospheric rad count on the Rig reads absolute zero. We preserve unblemished human lineage."

RU_LINES[5306] = "Фрэнк Хорриган только что прошел по коридору. От поступи этого титана дрожат переборки пола."
EN_LINES[5306] = "Frank Horrigan passed through Section C. Steel decking shuddered beneath that titan's tread."

RU_LINES[5307] = "Компьютерная сеть PoseidoNet контролирует все спутники связи. Ничто не скроется от наших глаз."
EN_LINES[5307] = "PoseidoNet links every operational orbital transponder. Nothing transpires beyond our purview."

RU_LINES[5308] = "Чиновники в секторе администрации спорят о распределении земель после великой зачистки."
EN_LINES[5308] = "Department heads squabbling over mainland land grants once purification protocol concludes."

RU_LINES[5309] = "Нарушение герметичности внешних шлюзов карается немедленной ликвидацией нарушителя."
EN_LINES[5309] = "Breaching outer decontamination airlocks invites immediate summary execution by guard detail."

RU_LINES[5310] = "Американский флаг снова будет гордо реять над всеми городами от океана до океана."
EN_LINES[5310] = "Old Glory will unfurl above every continental precinct once more, from sea to shining sea."

RU_LINES[5311] = "Охрана в черной броне не задает вопросов. Назови идентификатор или отойди от терминала."
EN_LINES[5311] = "Black-suited troopers don't debate. Transmit security credentials or clear the console corridor."

RU_LINES[5312] = "Служба климат-контроля сообщает об устойчивом солевом тумане вокруг платформы."
EN_LINES[5312] = "Environmental scrubbers report persistent saline fog encroaching upon upper flight deck tiers."

RU_LINES[5313] = "Мы -- истинное правительство этой страны. Все остальные -- лишь тени на радиоактивном пепле."
EN_LINES[5313] = "We are the constitutional successors of this republic. Outlanders are ghosts upon atomic ash."

RU_LINES[5314] = "Секретная служба сопровождает президента на каждый доклад. Протоколы безопасности абсолютны."
EN_LINES[5314] = "Secret Service details flank the Chief Executive at every briefing. Protocol is inviolable."

RU_LINES[5315] = "Скоро начнется распыление токсина. Мы вернем себе континент, который принадлежит нам по праву."
EN_LINES[5315] = "Aerosol delivery vectors near final staging. We shall reclaim what our forefathers charted."

# --- THE ABBEY (5320-5339) ---
RU_LINES[5320] = "Тише, брат. В стенах Аббатства каждый громкий вздох оскорбляет память мудрецов прошлого."
EN_LINES[5320] = "Hush, brother. Within the Abbey's cloister, loud breath insults memories of ancient scholars."

RU_LINES[5321] = "Я переписываю третий том довоенного справочника по электротехнике. Текст ветшает на глазах."
EN_LINES[5321] = "Transcribing volume three on pre-war electronics. Brittle leaves crumble under the stylus."

RU_LINES[5322] = "Чернила нынче делаем из древесной сажи и браминьего клея. Буквы ложатся ровно и густо."
EN_LINES[5322] = "We boil ink from pine soot and hide gelatin. Script sits dark and heavy upon parchment."

RU_LINES[5323] = "Отец-настоятель молится в часовне за души тех, кто погиб в пламени Древней Войны."
EN_LINES[5323] = "Father Abbot kneels in the nave, praying for souls swallowed in the Great Deluge of Fire."

RU_LINES[5324] = "Вино из монастырских погребов лечит даже застарелую хандру. Главное -- знать меру во хмелю."
EN_LINES[5324] = "Abbey cellar vintage soothes bitter spirits. The trick lies in taking communion in moderation."

RU_LINES[5325] = "Вчера в старом сундуке нашли детскую книгу сказок. Какое прекрасное было время до бомб..."
EN_LINES[5325] = "Found an illustrated nursery fable in an iron chest. Such innocent wonder before the firestorms..."

RU_LINES[5326] = "Племя дикарей с побережья иногда приносит нам травы в обмен на исцеляющие мази."
EN_LINES[5326] = "Coastal tribes bring marsh herbs in exchange for our distilled fever salves. Honest trade."

RU_LINES[5327] = "Брат-винодел опять заснул прямо у винного пресса. От него разит перебродившими ягодами на всю келью."
EN_LINES[5327] = "Brother Vintner dozed off beside the oak press. Smells of fermented berries across the courtyard."

RU_LINES[5328] = "Книги -- это единственное, что отделяет человека пустоши от кровожадного зверя."
EN_LINES[5328] = "Scripture and manuscripts alone separate wandering men from wild beasts of the radioactive sand."

RU_LINES[5329] = "Свечной воск капает на пергамент. Нужно быть предельно аккуратным, ошибки непростительны."
EN_LINES[5329] = "Tallow drips close to the margin. A scribe's quill must trace true; blotches are unforgivable."

RU_LINES[5330] = "В склепе под монастырем покоится прах первых хранителей. Их покой свят и нерушим."
EN_LINES[5330] = "Founders of our order sleep in the stone crypts beneath. Their quiet rest remains sacrosanct."

RU_LINES[5331] = "Мы не берем в руки оружия. Слово и знание -- наш единственный щит от жестокого мира."
EN_LINES[5331] = "We bear no iron weapons. The preserved Word is our sole bulwark against a vicious world."

RU_LINES[5332] = "Послушники с утра носят воду из родника. Родниковая вода здесь чиста, как слеза младенца."
EN_LINES[5332] = "Novices carry casks from the hillside spring. Cold water here bubbles sweet and pure as tears."

RU_LINES[5333] = "Один караванщик хотел купить древний атлас за мешок патронов. Мы выставили безумца за ворота."
EN_LINES[5333] = "A peddler offered brass ammunition for our celestial atlas. We barred the gate against him."

RU_LINES[5334] = "Колокол на башне отбивает заутреню. Пора садиться за переписной стол до самого заката."
EN_LINES[5334] = "The bell tower tolls prime. Time to mount the transcription bench until dusk swallows the light."

RU_LINES[5335] = "Пыль со старых страниц въелась в пальцы навсегда. Это благородная отметина служения знанию."
EN_LINES[5335] = "Centuries of book dust dye our palms. A noble mark of stewardship for forgotten knowledge."

RU_LINES[5336] = "Если ищешь приюта на ночь -- библиотека открыта для смиренных духом странников."
EN_LINES[5336] = "Seeking harbor from the night? Our reading hall welcomes pilgrims of gentle heart."

RU_LINES[5337] = "Многие знания умножают скорбь, путник. Но без них мир навеки останется во тьме дикости."
EN_LINES[5337] = "Knowledge multiplies grief, traveler. Yet without it, our wasteland drowns in feral barbarism."

RU_LINES[5338] = "Брат Лукас чистит медный переплет священной энциклопедии. Труд кропотливый, на многие луны."
EN_LINES[5338] = "Brother Lucas burnishes brass clasps on the encyclopedia. Patient work spanning many seasons."

RU_LINES[5339] = "Мир за нашими стенами полон злобы и пороха. Здесь же царит вечный покой вековой мысли."
EN_LINES[5339] = "The wilderness beyond reeks of cordite and strife. Here dwells the calm hush of ancient thought."

# --- PRIMITIVE TRIBE (5340-5359) ---
RU_LINES[5340] = "Океан сегодня неспокоен. Великая вода сердится, рыбы ушли на глубину к духам."
EN_LINES[5340] = "Great Water churns rough today. Waves are angry; silver fish dived deep to hide with spirits."

RU_LINES[5341] = "Костяной крючок сломался о пасть морской щуки. Придется вытачивать новый из ребра гекко."
EN_LINES[5341] = "Bone barb snapped inside big sea-pike's jaw. Must carve fresh hook from gecko rib."

RU_LINES[5342] = "Сулик из нашего племени ушел на север искать сестру. Сердце болит за храброго воина."
EN_LINES[5342] = "Sulik walked north trailing slavers for his sister. Tribal heart aches for our fierce warrior."

RU_LINES[5343] = "Шаман курит сухие водоросли у жертвенного камня. Дым стелется низко -- быть шторму."
EN_LINES[5343] = "Shaman burns kelp on the salt-rock. Smoke hugs the dune grass -- gale winds coming fast."

RU_LINES[5344] = "Железные люди с юга крадут наших детей в кандалы. Если увидишь их -- бей копьем в горло."
EN_LINES[5344] = "Iron-clad slavers creep from south trails to drag cubs away in chains. Drive javelins into their throats."

RU_LINES[5345] = "Запах жареной рыбы и костра отгоняет злых духов ночи от нашей стоянки."
EN_LINES[5345] = "Scent of charred drift-fish and hearth sparks wards off shadow creepers along the beach."

RU_LINES[5346] = "Прилив выбросил на песок ржавую бочку с желтым знаком. Шаман запретил подходить к ней близко."
EN_LINES[5346] = "Surf spit up a rusted yellow-marked iron tub. Shaman warns: death breath sleeps inside that metal."

RU_LINES[5347] = "Сети из сухожилий брамина крепкие, но морские ракушки режут их, как кремниевый нож."
EN_LINES[5347] = "Sinew mesh holds tight, but sharp reef shells slice braids like obsidian blades."

RU_LINES[5348] = "Женщины племени собирают съедобные раковины на отмели, пока вода не вернулась обратно."
EN_LINES[5348] = "Tribe daughters dig fat clams from tide-mud before the gray swell roars back."

RU_LINES[5349] = "Твоя одежда пахнет чужими городами и горелым порохом. Великая вода не любит этот запах."
EN_LINES[5349] = "Your garb smells of alien stone cities and gunpowder stench. Great Water dislikes such taint."

RU_LINES[5350] = "Старейшины говорят, далеко за волнами есть земля, где нет засухи и злых работорговцев."
EN_LINES[5350] = "Old mothers sing: across the endless surge lies green soil where slavers never set claw."

RU_LINES[5351] = "Охотники принесли тушу золотого гекко. Сегодня все племя будет сыто до отвала."
EN_LINES[5351] = "Trackers hauled golden lizard hide to camp. Whole clan chews marrow around embers tonight."

RU_LINES[5352] = "Холодный ветер с океана пробирает до костей. Греем руки над углями у самой кромки прибоя."
EN_LINES[5352] = "Salt breeze cuts right through gut-cloaks. We warm knuckles over charcoal near the foam."

RU_LINES[5353] = "Не бросай мусор в священный источник. Дух ручья может обидеться и отравить воду горечью."
EN_LINES[5353] = "Fling no refuse near the sweet spring. Water sprite sours the pool if strangers show disrespect."

RU_LINES[5354] = "Копье охотника должно быть легким и прямым, как луч утреннего солнца над волнами."
EN_LINES[5354] = "Harpoon shaft must balance straight as dawn light piercing the sea mist."

RU_LINES[5355] = "Мы помним песни дедов. Они пели о временах, когда птицы летали стаями, а не падали замертво."
EN_LINES[5355] = "We chant grandfathers' melodies: when sky-fowls flocked in millions and skies weren't scorched."

RU_LINES[5356] = "Собаки племени лают на темноту за дюнами. Чуют приближение степных волков."
EN_LINES[5356] = "Village curs bark at dunes after sunset. They smell waste wolves pacing the ridge."

RU_LINES[5357] = "Если пришел торговать -- покажи соль и наконечники стрел. Чужая бумага нам без надобности."
EN_LINES[5357] = "Trade in good faith: unroll salt and knapped spear points. Printed paper has no meaning here."

RU_LINES[5358] = "Песок скрипит под ступнями. Это земля наших отцов, и мы никуда не уйдем от великой волны."
EN_LINES[5358] = "Wet sand grinds beneath calloused heels. Soil of our fathers; we stay beside the breakers."

RU_LINES[5359] = "Да принесет утренний прилив добрую добычу в наши сети. Пусть боги моря хранят племя."
EN_LINES[5359] = "May the morrow swell fill our willow traps. May ocean gods watch our children."

# --- EPA (5360-5375) ---
RU_LINES[5360] = "Внимание: уровень токсичных спор в секторе B превышает допустимую норму на 420 процентов."
EN_LINES[5360] = "Alert: airborne mutagenic spore saturation in Sector B exceeds federal threshold by 420 percent."

RU_LINES[5361] = "Протокол консервации нарушен. Системы криогенного сна функционируют в аварийном режиме."
EN_LINES[5361] = "Cryogenic stasis integrity compromised. Pod bio-monitors running on degraded reserve power."

RU_LINES[5362] = "Я спал в капсуле сто шестьдесят лет... Боже мой, во что превратился этот мир за нашими стенами?"
EN_LINES[5362] = "Frozen asleep for a century and a half... Good god, what happened to the world beyond these airlocks?"

RU_LINES[5363] = "Голографический проектор мерцает. Персонал службы уборки не отвечает на запросы с 2077 года."
EN_LINES[5363] = "Hologram emitter flickers. Sanitation service personnel have been unresponsive since October 2077."

RU_LINES[5364] = "Экспериментальные образцы флоры пробили защитные решетки оранжереи. Требуется гербицид."
EN_LINES[5364] = "Botanical mutation specimens breached greenhouse containment. Defoliant dispersion required."

RU_LINES[5365] = "Директива Агентства по охране среды номер восемь: утилизация опасных отходов отложена навсегда."
EN_LINES[5365] = "Environmental Protection Directive 08: chemical ordnance disposal schedule indefinitely suspended."

RU_LINES[5366] = "Терминалы памяти повреждены коррозией. Архивы довоенных биохимических исследований стерты."
EN_LINES[5366] = "Magnetic core storage corroded. Pre-war biochemical research databases suffered sector decay."

RU_LINES[5367] = "Осторожно при входе в лифтовую шахту. Датчики перегрузки показывают критический износ тросов."
EN_LINES[5367] = "Warning: hoist cable tension meters indicate critical metallurgical fatigue in shaft three."

RU_LINES[5368] = "Синтезатор пищи выдает только безвкусную белковую пасту серого цвета с запахом серы."
EN_LINES[5368] = "Nutrient synthesizer dispenses gray protein slurry only. Characteristic sulphur odor noted."

RU_LINES[5369] = "Автоматический манипулятор заклинило на третьем цикле автоклавирования медицинских проб."
EN_LINES[5369] = "Pneumatic sorting arm jammed during sterilization sequence in pathogen quarantine bay."

RU_LINES[5370] = "Кто дал команду на разгерметизацию крио-сектора? Это же грубейшее нарушение регламента безопасности!"
EN_LINES[5370] = "Who authorized manual pod atmospheric purge? That constitutes a class-A procedural violation!"

RU_LINES[5371] = "В вентиляционных коробах зафиксировано размножение плотоядных спорных организмов."
EN_LINES[5371] = "Carnivorous botanical tendrils logged spreading through primary HVAC circulation conduits."

RU_LINES[5372] = "Резервные батареи комплекса истощены. Освещение переведено на аварийный импульсный режим."
EN_LINES[5372] = "Facility backup capacitors depleted. Emergency lighting cycling on low-draw pulse cycle."

RU_LINES[5373] = "Мои коллеги по лаборатории... все капсулы рядом со мной отключились десятилетия назад."
EN_LINES[5373] = "My lab colleagues... the indicator lights on every pod beside mine died decades ago."

RU_LINES[5374] = "Запах озона и гнилой листвы не выветривается из этих стерильных коридоров уже целый век."
EN_LINES[5374] = "Ozone and decaying vegetative compost smell has choked these corridors for over a hundred years."

RU_LINES[5375] = "Пожалуйста, предъявите пропуск сотрудника федерального агентства для доступа к терминалу."
EN_LINES[5375] = "Please present authorized federal agency credentials to initiate console diagnostics."

# --- VAULT VILLAGE (5380-5395) ---
RU_LINES[5380] = "Патрули из Города Убежища опять проезжали мимо. Грозят сжечь наши халупы, если не уйдем."
EN_LINES[5380] = "Vault City armored scouts rattled past again. Swore they'd torch our shanties if we don't clear out."

RU_LINES[5381] = "Мы просто хотим спокойно растить кукурузу на этой земле. Кому мешает наша бедная деревня?"
EN_LINES[5381] = "We just want to hoe corn in the dirt in peace. Who does our dirt-poor village bother?"

RU_LINES[5382] = "Кротокрысы подрывают грядки с капустой. Но старик Коннар говорит, они наши соседи и друзья."
EN_LINES[5382] = "Mole rats root through cabbage patches, but old Connar says they're neighbors and watchdog allies."

RU_LINES[5383] = "Эти снобы в синих комбинезонах считают нас грязью. Сами-то холеные, мозолей в жизни не нажили."
EN_LINES[5383] = "Those aristocrats in blue overalls spit on us. Never formed a callus on their soft palms in their lives."

RU_LINES[5384] = "Если нас выгонят отсюда -- куда нам идти? На пустошах работорговцы быстро нацепят ошейники."
EN_LINES[5384] = "Driven off this homestead, where do we crawl? Slavers on the north route will have irons on us by noon."

RU_LINES[5385] = "Коннар пытается найти оружие для самообороны. Но что наши ржавые ружья против лазеров Линетт?"
EN_LINES[5385] = "Connar scours the trails for rifles. What good are rusty pipe guns against Lynette's plasma squads?"

RU_LINES[5386] = "Земля здесь родит тяжело, приходится поливать каждый росток вручную из ведра."
EN_LINES[5386] = "Alkali soil resists crops; gotta carry ditch water bucket by bucket to keep seedlings green."

RU_LINES[5387] = "Вчера ночью кротокрыс прогнал бродячую стаю собак от загона. Умные зверюги, хоть и страшные."
EN_LINES[5387] = "A big mole rat chased wild dogs off the goat pen last night. Ugly brutes, but sharp watchdogs."

RU_LINES[5388] = "Ты не из Города Убежища, путник? Скажи им, что мы не отдадим свои дома без драки."
EN_LINES[5388] = "You're not one of their Citizen inspectors, are you? Tell them we don't surrender our homesteads without blood."

RU_LINES[5389] = "Мозоли на руках трескаются до крови. А граждане за стеной даже пылинки с рукава сдувают."
EN_LINES[5389] = "Cracked knuckles bleed in the dust. Meanwhile Citizens inside the fence brush lint off velvet coats."

RU_LINES[5390] = "Дети боятся выходить на дорогу. Если патруль заметит их -- могут объявить дикарями вне закона."
EN_LINES[5390] = "Kids dread wandering past the fence line. A patrol spots them, they're branded vagrant trespassers."

RU_LINES[5391] = "Колодец копали всей деревней два месяца. Вода жесткая, с осадком, но пить можно."
EN_LINES[5391] = "Whole camp dug the well for two months. Brackish water full of chalk, but wet enough to swallow."

RU_LINES[5392] = "Коннар -- справедливый староста. Без него нас бы давно втоптали в радиоактивную пыль."
EN_LINES[5392] = "Connar stands up for squatters. Without his grit, they'd have trampled our hearths into dust."

RU_LINES[5393] = "Запах жареной репы... вот и весь наш ужин на сегодня. Присаживайся к костру, если голоден."
EN_LINES[5393] = "Boiled wild turnip... that's the whole banquet tonight. Pull up a crate if your belly's pinching."

RU_LINES[5394] = "Мы не просим милости у Города. Мы просто хотим, чтобы нас оставили в покое на своей земле."
EN_LINES[5394] = "We beg no charity from Vault City. We demand only to be left unmolested on this dirt patch."

RU_LINES[5395] = "Пусть земля хранит тех, кто защищает слабых. В пустошах справедливость редко заглядывает на огонек."
EN_LINES[5395] = "Bless those who shield poor folk. Justice doesn't stop by these parts very often."

# --- RENO STABLES (5400-5415) ---
RU_LINES[5400] = "Винт новой партии жжет вены, как расплавленный свинец... Дайте еще один вдох, прошу!"
EN_LINES[5400] = "The new batch burns like molten solder in my veins... Give me another hit, just one breath, please!"

RU_LINES[5401] = "Майрон опять орал на лаборантов. Говорит, бета-версия Джета делает подопытных слишком буйными."
EN_LINES[5401] = "Myron threw beakers at the lab crew again. Whines the beta chem makes test subjects too rabid."

RU_LINES[5402] = "Вонь от загонов браминов забивает нос. Экскременты этих тварей идут прямо в реакторы очистки."
EN_LINES[5402] = "Manure smell from pens gags you. Brahmin fumes pipe straight into distillation retorts."

RU_LINES[5403] = "Охранники Мордино избивают каждого, кто пытается подойти к воротам без специального жетона."
EN_LINES[5403] = "Mordino goons pistol-whip anyone nearing the gate without a signed commissary pass."

RU_LINES[5404] = "Мои руки дрожат уже вторые сутки. Когда следующая дозировка? Доктор обещал проверку реакции!"
EN_LINES[5404] = "Tremors in my knuckles won't stop. When's the next test dose? The tech promised an evaluation!"

RU_LINES[5405] = "Мальчишка Майрон -- законченный садист. Для него мы просто двуногие крысы в клетках."
EN_LINES[5405] = "That Myron punk is a pure sadist. To him, we're two-legged lab mice bred in wire pens."

RU_LINES[5406] = "Вчера двое подопытных в третьем бараке скончались от остановки сердца. Их тела просто выбросили в ров."
EN_LINES[5406] = "Two test cases in barracks three coded from cardiac arrest. Threw their corpses into the ditch."

RU_LINES[5407] = "Они говорят, что разрабатывают лекарство. Но я вижу только шприцы, решетки и вооруженных громил."
EN_LINES[5407] = "They claim they're refining medicines. All I see are needles, cage wire, and shotgun bullies."

RU_LINES[5408] = "Запах серы и аммиака въелся в кожу так, что ни одно мыло в мире его теперь не смоет."
EN_LINES[5408] = "Sulphur and ammonia stink soaked into my skin so deep no lye soap will ever scrub it out."

RU_LINES[5409] = "Не смотри охранникам в глаза. У них приказ стрелять на поражение при любых признаках бунта."
EN_LINES[5409] = "Don't catch the guards' eyes. Standing orders to unload buckshot at the first twitch of trouble."

RU_LINES[5410] = "В голове шумит, будто тысячи ос бьются о череп изнутри. Это побочный эффект формулы 2-B."
EN_LINES[5410] = "Humming in my ears like hornets rattling inside my skull. That's the side effect of batch 2-B."

RU_LINES[5411] = "Караван с химикатами из Реддинга прибыл вовремя. Значит, лаборатория будет дымить всю ночь."
EN_LINES[5411] = "Chemical freight from Redding docked on schedule. Lab stacks will be spewing fumes all night."

RU_LINES[5412] = "Семья Мордино зарабатывает миллионы на чужой ломке. Проклятое место, проклятый город."
EN_LINES[5412] = "The Mordino family rakes in fortunes on junkie shakes. Cursed compound, cursed desert."

RU_LINES[5413] = "Если выберешься отсюда живым -- передай моей сестре в Рино, что я не вернусь домой."
EN_LINES[5413] = "If you walk out past the wire alive, tell my sister on Second Street I'm never coming home."

RU_LINES[5414] = "Стены барака дрожат, когда в подвале запускают центрифуги для очистки порошка."
EN_LINES[5414] = "Barrack planks vibrate when they fire the sub-floor centrifuges for chemical refining."

RU_LINES[5415] = "Никому нет дела до бродяг с улицы. Нас привезли сюда умирать ради новой формулы дури."
EN_LINES[5415] = "Nobody weeps for street drifters. Hauled us out here to burn out our hearts for fresh product."

# --- SLAVER CAMP (5420-5435) ---
RU_LINES[5420] = "Шевелись, мясо! Еще один шаг в сторону от строя -- и получишь заряд картечи под ребра!"
EN_LINES[5420] = "Step lively, cargo! Stray half an inch out of formation, take buckshot through your ribs!"

RU_LINES[5421] = "Жара сегодня невыносимая. От этих кандалов на щиколотках содрана вся кожа до мяса."
EN_LINES[5421] = "Sun's scorching today. Iron shackles chafed the skin on my shins clean down to raw marrow."

RU_LINES[5422] = "Мецгер платит по сотне монет за каждого здорового дикаря. Прибыльное ремесло, хоть и пыльное."
EN_LINES[5422] = "Metzger doles a hundred caps for prime tribal stock. Lucrative racket, if you don't mind dust."

RU_LINES[5423] = "Вчера один шустрый парень пытался перемахнуть через колючую проволоку. Сторожевые псы разорвали."
EN_LINES[5423] = "Fast buck tried scrambling over the razor wire at dusk. Attack hounds tore him to strips."

RU_LINES[5424] = "Держи палец на спусковом крючке, боец. Если эти рабы поднимут бунт -- живым никто не уйдет."
EN_LINES[5424] = "Keep safety off, guard. These tribals rush the stockade together, nobody walks away."

RU_LINES[5425] = "Воды дают по кружке в день. Язык распух так, что слова не выговорить."
EN_LINES[5425] = "Single tin cup of tepid water at noon. Tongue swollen so fat I can't form syllables."

RU_LINES[5426] = "Ошейники заклепаны намертво. Без зубила и тяжелого молотка их вовек не снимешь."
EN_LINES[5426] = "Neck bands are cold-riveted shut. Won't pry 'em off without a cold chisel and five-pound maul."

RU_LINES[5427] = "На следующей неделе караван погонит партию в Дыру и Нью-Рино. Там за свежий товар заплатят втрое."
EN_LINES[5427] = "Driving a batch south to the Den and Reno next week. Fresh muscle fetches triple at the auction block."

RU_LINES[5428] = "Они сожгли нашу деревню на рассвете... Мои дети плакали, когда их заталкивали в клетки."
EN_LINES[5428] = "Burned our river lodges at first light... My children wept when dragged into the iron carts."

RU_LINES[5429] = "Не жалей дикарей, парень. Они бы с тебя скальп сняли, если б поймали в своих лесах."
EN_LINES[5429] = "Waste no tears on primitives. Catch you in the gulch, they'd peel your scalp with chipped flint."

RU_LINES[5430] = "Запах пота, крови и раскаленного железа. Обычный день в лагере пересылки."
EN_LINES[5430] = "Reek of sweat, spilled plasma, and glowing branding irons. Standard morning at the pens."

RU_LINES[5431] = "Рейнджеры НКР крутятся где-то на горизонте. Если сунутся сюда -- встретим свинцовым шквалом."
EN_LINES[5431] = "NCR Rangers scouting the ridgeline. Let them crawl down here; we've got full drums waiting."

RU_LINES[5432] = "Боги племени не слышат наших стонов сквозь звон железных цепей."
EN_LINES[5432] = "Ancestors cannot hear our weeping over the harsh clatter of slaver iron."

RU_LINES[5433] = "Охранники напились дешевого пойла у костра и режутся в кости на пайку пленных."
EN_LINES[5433] = "Slaver goons tanked on rotgut by the coals, rolling dice for the prisoners' stew rations."

RU_LINES[5434] = "Каждый день здесь тянется как вечность. Лучше бы пуля в лоб при облаве, чем эта клетка."
EN_LINES[5434] = "Hours drag like millstones. A bullet through the forehead on the trail beats this cage."

RU_LINES[5435] = "Смотри в оба по сторонам. Дикари только и ждут момента, когда караульный зевнет на посту."
EN_LINES[5435] = "Eyes on the wire! Those wild bastards wait for a guard to nod off on watch."

# --- RANGER SAFETHOUSES (5440-5455) ---
RU_LINES[5440] = "Тишина на посту, боец. Мы глубоко во вражеском тылу, шум привлекает падальщиков."
EN_LINES[5440] = "Quiet on station, soldier. We operate behind hostile lines; excess noise draws scavengers."

RU_LINES[5441] = "Охотничий карабин пристрелян на триста ярдов. Работорговцы Мецгера даже не поймут, откуда прилетело."
EN_LINES[5441] = "Scoped hunting rifle zeroed at three hundred yards. Metzger's wolves won't know what punched through."

RU_LINES[5442] = "По данным разведки, караван с рабами движется по старой дороге на север. Готовим засаду на рассвете."
EN_LINES[5442] = "Scouts confirm an iron-chain convoy on the old north route. Ambush elements muster at dawn."

RU_LINES[5443] = "Рейнджеры поклялись искоренить рабство на этой земле. И мы сдержим клятву до последнего патрона."
EN_LINES[5443] = "The Rangers swore an oath to crush slavery across the waste. We keep it down to our last round."

RU_LINES[5444] = "Почисти оптику от пыли. В оптическом прицеле не должно быть ни единой песчинки."
EN_LINES[5444] = "Wipe sand off that glass objective. Can't tolerate dust blurring the crosshairs."

RU_LINES[5445] = "Наше убежище законспирировано. Если заметишь слежку на тропе -- води кругами, пока хвост не отпадет."
EN_LINES[5445] = "This hideout is classified. Pick up a tail on the pass, circle through canyons until it breaks."

RU_LINES[5446] = "Каждый освобожденный раб -- это удар под дых бандам Дыры и мафиози из Нью-Рино."
EN_LINES[5446] = "Every captive set loose lands a kidney blow against Den syndicates and Reno mobs."

RU_LINES[5447] = "Сухпайки на исходе, но мы привыкли жевать сушеное мясо брамина прямо на ходу."
EN_LINES[5447] = "Rations running thin, but Rangers are built to chew dried beef jerky on the march."

RU_LINES[5448] = "Командование в Шейди Сэндс требует отчетов. Но настоящая война за свободу идет здесь, в пыли каньонов."
EN_LINES[5448] = "Staff brass in Shady Sands file paperwork. The real war for human liberty happens out in this grit."

RU_LINES[5449] = "Снаряжай магазины экспансивными пулями. Против бандитов в кожаных куртках они работают безотказно."
EN_LINES[5449] = "Load soft-point rounds. Hollow core expands clean through boiled raider leather."

RU_LINES[5450] = "Костер разводить только в укрытии и без дыма. Дым днем виден за десять миль."
EN_LINES[5450] = "No smoky cook fires. In desert air, a column of wood smoke is visible for ten miles."

RU_LINES[5451] = "Смерть работорговцам -- свобода пустошам. Простой девиз, ради которого стоит рисковать шкурой."
EN_LINES[5451] = "Death to slavers, freedom for the waste. A plain motto worth taking lead in the chest for."

RU_LINES[5452] = "Мы перехватили шифровку гильдии Мецгера. Они боятся наших засад больше, чем чумы."
EN_LINES[5452] = "Intercepted runner dispatches from the Den. Metzger's crews fear our crossfires worse than rot."

RU_LINES[5453] = "Если попадешь в плен -- держи язык за зубами. Лучше раскусить капсулу, чем выдать координаты схронов."
EN_LINES[5453] = "Cornered without extraction, bite the pill. You never surrender safehouse coordinates."

RU_LINES[5454] = "Оружие смазано, радиостанции настроены на аварийную частоту. Мы готовы к выходу на маршрут."
EN_LINES[5454] = "Actions oiled, shortwave dialed to distress band. Patrol squad ready to deploy."

RU_LINES[5455] = "Победа будет за законом и честью. Республика сильна, пока живы ее защитники на дальних рубежах."
EN_LINES[5455] = "Honor and law will triumph. The Republic endures while Rangers hold the outer perimeter."

# --- SAN FRAN SUBMARINE (5460-5475) ---
RU_LINES[5460] = "Холодный металл переборок покрыт ржавчиной. Лодка застряла на отмели в заливе навсегда."
EN_LINES[5460] = "Cold steel bulkheads rusted through. This warship is grounded in bay mud for eternity."

RU_LINES[5461] = "Торпедный аппарат номер два заклинило в день Великого Удара. Боеголовка всё еще спит внутри."
EN_LINES[5461] = "Torpedo tube two seized up on Great Flash Day. The warhead still rests silent inside."

RU_LINES[5462] = "Слышишь эхо в пустых отсеках? Это души погибших матросов шепчут слова военной присяги."
EN_LINES[5462] = "Echoes through empty compartments? Fallen sailors whispering ancient oaths to the flag."

RU_LINES[5463] = "Техники Ши пытаются восстановить силовые кабели. Медь сгнила от морской соли за два века."
EN_LINES[5463] = "Shi repairmen trying to splice bus cables. Salt brine dissolved the copper two centuries ago."

RU_LINES[5464] = "Политрук приказал держать боевую готовность номер один... Приказ остался в вечности."
EN_LINES[5464] = "Political officer ordered condition one battlestations... The order stands forever in the dark."

RU_LINES[5465] = "Вода капает с потолка рубки управления. Кап... кап... отмеряет века мертвого железа."
EN_LINES[5465] = "Condensation drips from command room ceiling. Drip... drip... counting dead iron centuries."

RU_LINES[5466] = "Запах машинного масла и соленой тины въелся в эти стены так глубоко, что ничем не выветрить."
EN_LINES[5466] = "Bunker oil and salt weed stench baked into these rivets so deep nothing airs it out."

RU_LINES[5467] = "Приборы навигации показывают курс на Пекин. Но города по ту сторону океана давно обратились в прах."
EN_LINES[5467] = "Nav dials calibrated for Beijing harbor. Cities across the Pacific turned to glass long ago."

RU_LINES[5468] = "Не трогай переключатели на главном щите. Высокое напряжение может сжечь сердце на месте."
EN_LINES[5468] = "Don't toggle master breakers. Residual voltage in emergency lines will scorch your heart."

RU_LINES[5469] = "Мы пришли к чужим берегам исполнить долг. А остались запертыми в стальном гробу на дне залива."
EN_LINES[5469] = "We sailed to hostile shoals to fulfill our duty. Remained entombed in an iron vault under the bay."

RU_LINES[5470] = "Радиостанция ловит только белый шум далеких пустошей. Мир снаружи изменился до неузнаваемости."
EN_LINES[5470] = "Receivers pull only static hiss off the burnt coast. World above twisted beyond recognition."

RU_LINES[5471] = "Аварийные люки задраены намертво. Никто уже не откроет их с той стороны."
EN_LINES[5471] = "Escape trunks dogged tight. Nobody on the surface will ever turn the outer wheel."

RU_LINES[5472] = "Император Ши в Сан-Франциско -- плоть от плоти наших довоенных бортовых вычислителей."
EN_LINES[5472] = "The Shi Emperor mainframe is flesh of our flesh, evolved from submarine navigation banks."

RU_LINES[5473] = "Морские крабы ползают по затопленным решеткам трюма. Жизнь находит дорогу даже во тьме."
EN_LINES[5473] = "Shore crabs scuttle across flooded bilge grates. Life claws a foothold even down in the dark."

RU_LINES[5474] = "Призрак вахтенного офицера до сих пор обходит посты в полночь с призрачным журналом в руках."
EN_LINES[5474] = "Watch officer's specter tours bilge posts at midnight, clutching phantom damage logs."

RU_LINES[5475] = "Покойтесь с миром, сыны Поднебесной. Война окончена, хотя этот стальной гигант так и не сдался."
EN_LINES[5475] = "Rest in peace, sons of the Middle Kingdom. War concluded, though this iron whale never struck colors."


def write_msg(file_path, lines_dict, encoding):
    sorted_ids = sorted(lines_dict.keys())
    content = "# ==============================================================================\n"
    content += "# WASTELAND VOICES v1.0.0 DIALOG CORPUS\n"
    content += "# ==============================================================================\n\n"
    for line_id in sorted_ids:
        text = lines_dict[line_id]
        content += f"{{{line_id}}}{{}}{{{text}}}\n"
    
    with open(file_path, "wb") as f:
        f.write(content.encode(encoding))
    print(f"Wrote {len(sorted_ids)} lines to {file_path} in {encoding} ({os.path.getsize(file_path)} bytes)")


def main():
    ru_dialog = os.path.join(BASE_DIR, "text", "russian", "dialog", "wv_dialog.msg")
    ru_custom = os.path.join(BASE_DIR, "text", "russian", "game", "custom.msg")
    en_dialog = os.path.join(BASE_DIR, "text", "english", "dialog", "wv_dialog.msg")
    en_custom = os.path.join(BASE_DIR, "text", "english", "game", "custom.msg")

    write_msg(ru_dialog, RU_LINES, "cp1251")
    write_msg(ru_custom, RU_LINES, "cp1251")
    write_msg(en_dialog, EN_LINES, "ascii")
    write_msg(en_custom, EN_LINES, "ascii")
    print("ALL FILES SUCCESSFULLY BUILT AND VALIDATED!")


if __name__ == "__main__":
    main()
