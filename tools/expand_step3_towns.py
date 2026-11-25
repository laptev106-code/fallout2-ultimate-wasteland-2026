# -*- coding: utf-8 -*-
import os

def expand():
    target_file = "E:/FALLOUT Ult pjt/tools/build_step3_corpus.py"
    with open(target_file, "r", encoding="utf-8") as f:
        text = f.read()

    new_towns = """
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
"""

    target = "# --- PLAYER REACTIVITY: POWER ARMOR (5800-5809) ---"
    if target in text:
        new_text = text.replace(target, new_towns + "\n" + target)
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(new_text)
        print("SUCCESS: Added new towns to build_step3_corpus.py")
    else:
        print("ERROR: Target not found in build_step3_corpus.py")

if __name__ == "__main__":
    expand()
