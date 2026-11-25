# -*- coding: utf-8 -*-
import os
import sys

BASE_DIR = r"E:\FALLOUT Ult pjt"
WV_DIR = os.path.join(BASE_DIR, "standalone_mods", "wasteland_voices")

# --- Russian text expansion (Slice 4) ---
RU_ADDITIONS = """
# ==============================================================================
# SLICE 4: EXTENDED WASTELAND QUEST STATES (5730-5778)
# ==============================================================================
{5730}{}{После того как насос заработал, в трапезной наконец-то появилась чистая вода. Хвала небесам и твоим рукам.}
{5731}{}{Водяные фильтры снова гудят. Настоятель говорит, это настоящее чудо древней инженерии.}
{5732}{}{Чистая колодезная вода без привкуса ржавчины... Мы молимся за того странника, что починил насос.}
{5733}{}{Тварь из винного погреба наконец-то издохла. Теперь послушники спускаются за бочонками без дрожи в коленях.}
{5734}{}{Говорят, в подземелье больше никто не скребется по ночам. Ты спас наши запасы вина от клыкастого чудовища.}
{5735}{}{Брат Джеймс снова разливает аббатский самогон. Без монстра в подвале работа пошла куда веселее.}
{5736}{}{Печатный станок снова заработал! Скоро мы завершим копирование медицинских трактатов древних.}
{5737}{}{С новыми шестернями книги больше не нужно переписывать от руки при тусклой лучине. Великое дело для науки.}
{5738}{}{Станок печатает четко, краска ровная. Мудрость прошлого не истлеет в пыли, пока живо наше Аббатство.}
{5740}{}{Колодец снова полон прозрачной воды! Духи земли улыбнулись нашему племени благодаря чужеземцу.}
{5741}{}{Дети больше не пьют болотную жижу. Вода из колодца холодна и сладка, как в старые времена.}
{5742}{}{Шаман окурил колодец священными травами. Теперь вода дает силы нашим воинам перед охотой.}
{5743}{}{Куранна вернулась в родную хижину! Сестра Сулика жива, и злые работорговцы не сломили ее дух.}
{5744}{}{Великий воин вернул Сулику его сестру. Все стойбище поет хвалебные песни духам Арройо.}
{5745}{}{Сулик и Куранна снова вместе у костра. Сердце племени исцелилось от тяжелого горя.}
{5746}{}{Торговец оружием покинул наше побережье. Чужие стреляющие палки больше не оскверняют обычаи предков.}
{5747}{}{Копье и лук добывали нам пищу веками. Нам не нужны железные игрушки белых людей из южных городов.}
{5748}{}{Шаман прав: жадность торговцев пулями приносит лишь кровь. Хорошо, что чужака прогнали прочь.}
{5750}{}{Хищные стебли на нижних уровнях увяли. Теперь коридоры сектора B хотя бы не пытаются тебя сожрать.}
{5751}{}{Смертоносные растения порублены в труху. Вентиляционные шахты больше не забиты ядовитой пыльцой.}
{5752}{}{Голограммы службы безопасности докладывают: биомасса сектора флоры ликвидирована. Чистый результат.}
{5753}{}{Крио-камеры наконец-то открыты! Люди, спавшие десятки лет, дышат воздухом и собираются уходить на север.}
{5754}{}{Освобожденные узники комплекса до сих пор не верят, что старый мир сгорел. Но они свободны.}
{5755}{}{Пленники покинули подземные боксы. Теперь этот бетонный склеп кажется немного менее мертвым.}
{5760}{}{Коннар раздал нам охотничьи карабины. Теперь патрульные Линетт дважды подумают, прежде чем сунуться на наши огороды.}
{5761}{}{С настоящим оружием мы больше не рабы и не мишени для развлечений сержанта Старка. Мы защитим свои дома.}
{5762}{}{Город Убежища хотел вышвырнуть нас на урановые пустоши, но с винтовками в руках с нами придется считаться.}
{5763}{}{Спасибо за ружья, путник. В этих краях уважают только тех, кто может прострелить колено на сотне ярдов.}
{5770}{}{Лагерь работорговцев разбит в пыль! Ошейники сбиты, а надсмотрщики Мецгера гниют под палящим солнцем.}
{5771}{}{Мы свободны... Свободны! Никаких больше плетей, кандалов и железных клеток. Мы уходим в горы!}
{5772}{}{Рейнджеры и бродяга с запада разнесли эту живодерню. На Пустошах стало на десяток ублюдков меньше.}
{5773}{}{Кровь работорговцев впиталась в песок. Слава тем, кто держал в руках ружья и взломал наши замки.}
{5775}{}{Наши дозорные засекли конвой работорговцев к востоку от Дена. Готовим засаду в ущелье.}
{5776}{}{Рейнджеры НКР держат слово: пока мы дышим, работорговля не перешагнет через горные перевалы.}
{5777}{}{Держи карабин чистым, а порох сухим. Пустошь не прощает тех, кто мешкает на спусковом крючке.}
{5778}{}{Мецгер думает, что он хозяин севера. Скоро мы покажем его банде, чего стоит закон Республики.}

# ==============================================================================
# SLICE 4: ENHANCED MIRIA TRAVEL & CITY FLOATS (5900-5945)
# ==============================================================================
{5900}{}{Матерь божья... Тут огни ярче, чем на ярмарке в Модоке, а от девиц за милю разит грехом. Держи руки на кошельке, дорогой.}
{5901}{}{Нью-Рино... Отец говорил, этот город сожрет любого деревенщину с потрохами. Не заглядывайся на полуголых шлюх, милый!}
{5902}{}{Казино, бандиты с автоматными стволами и запах винта... Тут убивают средь бела дня. Пойдем отсюда поскорее.}
{5903}{}{Смотри-ка, семья Мордино, семья Бишоп... Одни гангстеры кругом. Если кто полезет к нам -- стреляй первым, я прикрою.}
{5904}{}{Чистота-то какая... будто в больничной палате. Но смотрят на нас, как на тараканов в муке. Тьфу, снобы стерильные.}
{5905}{}{«Граждане» носят свои чистенькие комбинезоны, а за забором беженцы в лохмотьях подыхают с голоду. Противно смотреть.}
{5906}{}{Эта важная курица Линетт считает себя королевой мира. В Модоке за такое задирание носа ее быстро бы окунули в поилку.}
{5907}{}{У них тут все по пропускам и предписаниям. Даже чихнуть нельзя без гербовой печати. Поскорее бы обратно на воздух.}
{5908}{}{Здесь даже воздух воняет тухлятиной и гарью. Не отходи от меня ни на шаг, милый, мне не по себе от этих взглядов.}
{5909}{}{Работорговцы с татуировками на мордах... Они смотрят на меня, как на товар на ярмарке. У меня мурашки по коже.}
{5910}{}{Кругом наркоманы на ломах и беспризорники с ножиками. Держи карманы на замке, тут уведут сапоги прямо с ног.}
{5911}{}{Дыра оправдывает свое название. Худшая сточная канава на всем белом свете. Покончим с делами и уходим.}
{5912}{}{Дом... Родной Модок! Пахнет отцовской скотобойней и сеном. Не верится, что мы снова здесь, милый.}
{5913}{}{Вон дом Гришема, вон грядки Розы... Знаешь, а я скучала по этой пыльной дыре, пока мы скитались по пустошам.}
{5914}{}{Надеюсь, отец в добром здравии. Надо заглянуть к нему, только спрячь оружие, а то опять начнет ворчать про приданое.}
{5915}{}{Здесь все такое знакомое и простое. Никаких чудовищ и пуль над головой. Просто земля и работящие люди.}
{5916}{}{Пахнет перегаром, кислым мылом и сырыми шкурами. Отец говорил, в Кламате живут одни пьяницы и браконьеры. Не соврал.}
{5917}{}{Трапперы в вонючих кожаных лохмотьях... Каждый второй лыка не вяжет от самогона Бобби. Веселенькое местечко.}
{5918}{}{Смотри под ноги, тут грязи по щиколотку. И проверь затвор карабина, от такой сырости железо ржавеет на глазах.}
{5919}{}{В трактире «Золотой Гекко» ор стоит на всю улицу. Надеюсь, нам не придется выбивать кому-то зубы из-за кружки пива.}
{5920}{}{Это... океан?! Господи, он такой огромный! Воды больше, чем во всех реках севера вместе взятых!}
{5921}{}{Шииты ходят в шелках и кланяются компьютеру-Императору, а панки на ржавом танкере глушат самогон... Чудеса Пустошей.}
{5922}{}{От этих Хабологов в белых робах веет сектой за версту. Не слушай их бред про уровни духа, милый, оберут до нитки.}
{5923}{}{Соленый ветер, скрип ржавых доков и запах жареной рыбы. Совсем другой мир, не похожий на наши фермы.}
{5924}{}{Мутанты, гули и люди сидят за одним столом в кабаке? Отец бы схватился за ружье, а они тут мирно уран копают.}
{5925}{}{Шериф Маркус внушает уважение. Здоровый, как скала, но говорит рассудительнее половины мэров на Пустоши.}
{5926}{}{Из шахты тянет серным духом и рудной гарью. Город работящий, суровый, но здесь хотя бы есть порядок.}
{5927}{}{Гули тут не такие злые, как в других местах. Привыкаешь не обращать внимания на их скрипучие голоса.}
{5928}{}{Все кашляют, лица черные от золотой пыли... И все разговоры только о золоте и винте. Невеселое место.}
{5929}{}{Шахтеры спускают все заработанные крупицы золота у рулетки и на шлюх Мадам Лу. Прямо как мотыльки на костер.}
{5930}{}{Шериф Марион выглядит так, будто не спал три недели. Война рудников доведет этот город до беды.}
{5931}{}{От этой золотой лихорадки люди совсем с ума сходят. Давай закончим дела и поедем дальше, дышать нечем.}
{5932}{}{Аббатство... Тишина, как в церкви перед грозой. Монахи переписывают старые фолианты... Отец бы оценил их винные погреба.}
{5933}{}{Монахи живут скромно, молятся науке и книгам. Удивительно мирное место для нашей проклятой Пустоши.}
{5934}{}{От здешнего колокольного звона на душе становится спокойнее. Хоть где-то нет выстрелов и криков.}
{5935}{}{EPA... Голограммы? Растения, которые жрут людей?! Куда ты меня притащил?! В Модоке самое страшное было — если брамин сбежит в кукурузу!}
{5936}{}{Этот научный комплекс похож на сон безумца. Мигающие лампы, ядовитый газ и ожившие кошмары. Держи оружие наготове!}
{5937}{}{Не подходи близко к этим колбам с мутантами, милый! Мне кажется, оно шевелится внутри стекла...}
{5938}{}{Деревня дикарей на берегу... Знаешь, они очень напоминают твой народ из Арройо, о котором ты рассказывал.}
{5939}{}{Хижины из плавника, костяные наконечники... Бедные люди, но у них есть свое достоинство и гордость.}
{5940}{}{Морской прибой и запах водорослей. Если бы не работорговцы Мецгера, тут был бы настоящий рай.}
{5941}{}{Пыль скрипит на зубах... Дорогой, как думаешь, долго нам еще топать по этим пустошам? Сапоги совсем истерлись.}
{5942}{}{Фляга наполовину пуста. Надо будет наполнить водой при первой же стоянке у караванщиков.}
{5943}{}{Никогда бы не подумала, что выйду замуж за дикаря и буду кочевать по всей Калифорнии. Но с тобой не соскучишься, милый!}
{5944}{}{Ветер стих. Перед песчаной бурей всегда такая тишина... Подтяни ремни на рюкзаке, пойдем быстрее.}
{5945}{}{Когда мы наконец найдем этот твой ГЭКК, построим большой дом на ферме и заведем десяток браминов, договорились?}

# ==============================================================================
# SLICE 4: COMPANION COMBAT SHOUTS (5950-5984)
# ==============================================================================
{5950}{}{Мы и духи видим -- Избранный истекает кровью! Бей тварей сильнее, пока он на ногах!}
{5951}{}{Держись, друг! Духи предков не дадут тебе упасть на эти камни!}
{5952}{}{Кости шепчут: смерть кружит рядом! Отступай назад, Избранный, мы прикроем!}
{5953}{}{Босс, держись! Черт, черт, прими стимулятор, тебя же на куски разорвут!}
{5954}{}{Босс, отходи! Я задержу их огнем, только перевяжи раны, умоляю!}
{5955}{}{Господи, в тебя же пол-обоймы вогнали! Босс, залепи дыры, не геройствуй!}
{5956}{}{Парень, ты весь в дырах! Залепи раны стимулятором или сдохнешь прямо здесь!}
{5957}{}{Черт побери, на тебя страшно смотреть! Уходи с линии огня, живо!}
{5958}{}{Не вздумай откинуть копыта раньше меня, парень! Кольни лекарство и в укрытие!}
{5959}{}{Милый, ты ранен! Нет, только не умирай, держись, ради всего святого!}
{5960}{}{Дорогой, отступай ко мне! Я прикрою, только примени стимулятор, прошу тебя!}
{5961}{}{Твари, что вы с ним сделали?! Милый, дыши, я не дам им тебя добить!}
{5962}{}{Человек, уходи на вторую линию! Моя броня выдержит, а ты истекаешь кровью!}
{5963}{}{Держи строй, друг! Вколи стимулятор, иначе в следующий раз тебя понесут вперед ногами!}
{5964}{}{Я принимаю огонь на себя! Залечи раны, пока я перемалываю этих выродков!}
{5970}{}{Дедушка доволен этим ударом! В пыль, поганая тварь!}
{5971}{}{Кувалда нашла хребет! Духи ведут руку Сулика!}
{5972}{}{Вот так в нашем племени ломают кости врагам! Получи!}
{5973}{}{Ха! Видали?! Моя пуля нашла цель прямо в глаз!}
{5974}{}{А говорят, старик Вик не умеет стрелять! Получил, ублюдок?!}
{5975}{}{Точно в яблочко! Босс, я снял его, путь свободен!}
{5976}{}{Минус один ублюдок. Хороший выстрел, черт побери!}
{5977}{}{Прямо в репу! Вот за это я и люблю свой старый дробовик!}
{5978}{}{Ложись и не дергайся, кусок мяса! Джон Кэссиди еще не промахивался!}
{5979}{}{Получил, гад?! Не смей трогать моего мужа!}
{5980}{}{Вот тебе за Модок! Мой карабин бьет без промаха!}
{5981}{}{Отведал свинца, урод?! В следующий раз будешь думать, на кого нападать!}
{5982}{}{Вот так в старой армии Марипозы решали вопросы! Следующий!}
{5983}{}{Твой череп раскололся, как перезрелая тыква. Жалкое зрелище.}
{5984}{}{Минигану Маркуса все равно, какая на тебе броня. В фарш!}
"""

# --- English text expansion (Slice 4) ---
EN_ADDITIONS = """
# ==============================================================================
# SLICE 4: EXTENDED WASTELAND QUEST STATES (5730-5778)
# ==============================================================================
{5730}{}{Now that the pump is running, we finally have clear water in the refectory. Blessings upon your hands.}
{5731}{}{The water filters are humming again. The Abbot calls it a true miracle of ancient engineering.}
{5732}{}{Pure well water without the taste of rust... We pray for the traveler who repaired our pump.}
{5733}{}{The beast in the wine cellar is finally dead. Now the novices can fetch barrels without their knees shaking.}
{5734}{}{They say nothing scratches in the cellars at night anymore. You saved our vintages from that fanged devil.}
{5735}{}{Brother James is pouring the Abbey brew again. Work goes a whole lot faster without a monster downstairs.}
{5736}{}{The printing press is back online! Soon we will finish copying the ancient medical treatises.}
{5737}{}{With the new gears, books no longer have to be scribed by flickering candlelight. A grand day for knowledge.}
{5738}{}{The press prints clean and true. The wisdom of the past will not turn to dust while our Abbey stands.}
{5740}{}{The well is brim-full of sweet water once more! The earth spirits have smiled on our tribe thanks to you.}
{5741}{}{The little ones no longer drink brackish swamp mud. The well water is cold and sweet, just like in elder times.}
{5742}{}{The shaman smoked the well stones with holy herbs. Now the water lends strength to our hunters.}
{5743}{}{Kooranna has returned to our hearth! Sulik's sister lives, and the cruel slavers could not break her spirit.}
{5744}{}{A mighty warrior delivered Sulik's sister home. The whole camp sings songs of praise for the Arroyo spirits.}
{5745}{}{Sulik and Kooranna sit together by the fire again. The sorrow that gripped our tribe has broken.}
{5746}{}{The merchant peddling his boom-sticks has packed up and left our shores. His dirty weapons no longer poison our traditions.}
{5747}{}{Spear and bow have fed our kin for generations. We do not need the iron toys of southern town-dwellers.}
{5748}{}{The shaman spoke true: bullet-mongers bring only spilled blood. Good riddance to that greedy outsider.}
{5750}{}{The predatory tendrils on the lower decks have withered. At least Sector B corridors aren't trying to eat you alive now.}
{5751}{}{The killer flora has been hacked to mulch. The air vents are no longer choking on toxic pollen.}
{5752}{}{Security holos report: botanical biomass in the bio-sector neutralized. Clean and efficient.}
{5753}{}{The cryo-pods are finally unlocked! People who slept for decades are breathing free air and heading north.}
{5754}{}{The freed captives still can't believe the old world burned to ash. But at least they walk free now.}
{5755}{}{The prisoners have vacated the subterranean vaults. This concrete tomb feels a little less dead now.}
{5760}{}{Connar handed out hunting rifles to every able body. Lynette's patrols will think twice before trampling our crops.}
{5761}{}{With real guns in our hands, we aren't Sergeant Stark's target dummies anymore. We will defend our roofs.}
{5762}{}{Vault City wanted to dump us in the radioactive wastes, but with rifles in hand, they have to treat us like men.}
{5763}{}{Thanks for the iron, wanderer. In these hills, folks only respect someone who can punch a hole through your knee at a hundred paces.}
{5770}{}{The slaver compound is reduced to cinder! Collars are smashed and Metzger's thugs are rotting under the desert sun.}
{5771}{}{We're free... Free! No more lashes, no more iron cages. We are taking to the high ridges!}
{5772}{}{The Rangers and a drifter from the west tore that butcher's pen apart. The Wastes are down a dozen bastards.}
{5773}{}{The slavers' blood soaked into the alkali flats. Honor to the guns that kicked down our pen gates.}
{5775}{}{Our scouts spotted a slave column east of the Den. We're setting up a dead-fall in the gorge.}
{5776}{}{The NCR Rangers keep their word: as long as we draw breath, man-stealers will not cross these passes.}
{5777}{}{Keep your rifle clean and your powder dry. The Waste does not forgive hesitation on the trigger.}
{5778}{}{Metzger thinks he owns the northern trade. Soon enough we will show his cartel what Republic law feels like.}

# ==============================================================================
# SLICE 4: ENHANCED MIRIA TRAVEL & CITY FLOATS (5900-5945)
# ==============================================================================
{5900}{}{Lord have mercy... The neon here is brighter than the Modoc fair, and the girls reek of sin from a mile off. Watch your pockets, darling.}
{5901}{}{New Reno... Father used to swear this pit would eat any country boy whole. Don't you go staring at those half-naked trollops, handsome!}
{5902}{}{Casinos, hitmen packing submachine guns, and the stink of Jet... Folks get butchered in broad daylight here. Let's finish quick and go.}
{5903}{}{Look at that: the Mordinos, the Bishops... mobsters at every corner. If one of them makes a move, shoot first; I've got your back.}
{5904}{}{Look how spotless it is... like an operating room. But they stare at us like we're roaches in their flour bin. Sterile snobs.}
{5905}{}{The 'Citizens' strut around in pristine jumpsuits while refugees outside starve in muddy rags. Makes my stomach turn.}
{5906}{}{That Lynette woman acts like she owns God's green earth. Back in Modoc, sticking your nose that high gets you dunked in the trough.}
{5907}{}{They've got a stamped form for every sneeze and breath here. You can't even spit without a council permit. I want out.}
{5908}{}{The air here smells like rotting meat and grease. Don't step two feet away from me, honey; these alley stares give me the creeps.}
{5909}{}{Slavers with brand marks right across their foreheads... They look at me like a heifer at an auction. It chills my blood.}
{5910}{}{Junkies tweaking on every corner and street urchins with shivs. Button your coat tight, they'll skin your boots right off your feet.}
{5911}{}{The Den sure earned its name. The sorriest cesspool in all of California. Let's wrap up our business and hit the road.}
{5912}{}{Home... Sweet Modoc! Smells like father's slaughterhouse and fresh straw. I can hardly believe we're back, darling.}
{5913}{}{There's Grisham's roof, and Rose's bed-and-breakfast... You know, I actually missed this dusty crossroads while we were wandering.}
{5914}{}{I hope father's health is holding up. Let's go check in on him, just holstered your piece first or he'll start bickering about the dowry.}
{5915}{}{Everything here is so simple and quiet. No bullets whistling past our ears, no monsters. Just good soil and hard-working folk.}
{5916}{}{Reeks of stale booze, harsh soap, and damp gecko hides. Father always said Klamath was full of drunks and poachers. He wasn't lying.}
{5917}{}{Trappers bundled up in greasy leather rags... Half of them can barely string three words together after Bob's moonshine.}
{5918}{}{Mind your footing, the mud is ankle-deep here. And oil your rifle action; this river damp will rust steel before nightfall.}
{5919}{}{Listen to that racket coming out of the Golden Gecko. I just hope we don't have to bust teeth over a spilled mug of draft.}
{5920}{}{Is that... the ocean?! Lord Almighty, it's enormous! More water than all the northern rivers poured together!}
{5921}{}{The Shi glide around in silk robes bowing to a mainframe Emperor, while tankers punks down rotgut on a rusted hulk... Miracles of the Wastes.}
{5922}{}{Those Hubologists in their shiny white smocks smell like a cult from twenty yards away. Don't swallow their star-babble, darling, they'll fleece you dry.}
{5923}{}{Salty wind, screeching iron cranes, and the aroma of grilled fish. A whole different world from our cattle pastures.}
{5924}{}{Mutants, ghouls, and humans sharing drinks at the saloon? Father would have grabbed his shotgun, but they're just mining uranium side by side.}
{5925}{}{Sheriff Marcus commands respect. Big as a hillside boulder, but speaks more sense than half the councilmen in California.}
{5926}{}{The air from the mine shaft smells of sulfur and crushed slag. It's a tough, gritty town, but folks keep order here.}
{5927}{}{The ghouls here aren't vicious like the horror tales say. You get used to their raspy voices once you talk a spell.}
{5928}{}{Everyone's hacking up phlegm, faces black with coal and gold dust... All anyone mutters about is dust and Jet. Bleak place.}
{5929}{}{The miners blow their whole week's strike at the roulette tables and Madam Lou's girls. Like moths diving into a torch.}
{5930}{}{Sheriff Marion looks like he hasn't closed his eyes in three weeks. This claim war between the mines will end in bloodshed.}
{5931}{}{This gold fever turns decent men into wolves. Let's settle what we came for and ride on; I can hardly draw breath here.}
{5932}{}{The Abbey... Quiet as a church before the lightning cracks. The monks scribing those giant books... Father would have loved their wine cellar.}
{5933}{}{The brothers live lean, praying to science and faded ink. A surprisingly peaceful corner in our scorched world.}
{5934}{}{That chapel bell ringing across the bluffs puts my heart at ease. At least somewhere out here isn't screaming with gunsmoke.}
{5935}{}{The EPA... Holograms? Man-eating vegetation?! Where in heaven's name did you drag me?! Back home the worst scare was a brahmin loose in the corn!}
{5936}{}{This research bunker feels like a madman's fever dream. Flashing dials, poison vapor, and dead nightmares waking up. Keep that gun up!}
{5937}{}{Don't get too close to those specimen tanks, honey! I swear that thing just twitched inside the brine...}
{5938}{}{A tribe living right against the tide... You know, they remind me a lot of your Arroyo kinfolk you told me about.}
{5939}{}{Hovels lashed from driftwood, bone fish-hooks... Humble folk, but they carry themselves with quiet pride.}
{5940}{}{Ocean surf and the smell of kelp. If Metzger's man-hunters weren't prowling nearby, this would be a proper slice of paradise.}
{5941}{}{Alkali grit grinding in my teeth... Darling, how much further across these badlands? My soles are worn paper-thin.}
{5942}{}{The canteen's half-empty. We'd best fill up our waterskins at the very next trader camp.}
{5943}{}{I never dreamed I'd marry a tribal scout and trek across the whole breadth of California. But you sure keep life interesting, handsome!}
{5944}{}{The wind died right down. That dead quiet always comes before a sand-squall... Tighten your pack straps, let's make tracks.}
{5945}{}{When we finally dig up that GECK of yours, we're building a proper ranch back on the flats and raising a dozen head of cattle, deal?}

# ==============================================================================
# SLICE 4: COMPANION COMBAT SHOUTS (5950-5984)
# ==============================================================================
{5950}{}{We and the spirits see it -- the Chosen One bleeds! Strike the beasts harder while he stands!}
{5951}{}{Hold on, brother! The ancient ones will not let you fall upon these stones!}
{5952}{}{The bones whisper: death circles close! Fall back, Chosen One, we hold the line!}
{5953}{}{Boss, hang on! Dammit, dammit, shoot a stimpak, they're tearing you apart!}
{5954}{}{Boss, pull back! I'll lay down covering fire, just bandage those leaks, please!}
{5955}{}{Lord in heaven, they put half a mag into you! Boss, patch yourself up, don't play the hero!}
{5956}{}{Kid, you're ventilated like a screen door! Stimpak that puncture or you'll drop right here!}
{5957}{}{Goddammit, you look like minced meat! Get off the firing lane, double-time!}
{5958}{}{Don't you dare cash in your chips before me, kid! Jam that needle in and dive for cover!}
{5959}{}{Honey, you're hurt! No, don't you die on me, hold on, for God's sake!}
{5960}{}{Darling, fall back to me! I'll cover you, just take a stimpak, please!}
{5961}{}{You filthy bastards, what did you do to him?! Honey, breathe, I won't let them finish you!}
{5962}{}{Human, get to the rear! My plating can take the punishment; you are bleeding dry!}
{5963}{}{Hold your ground, friend! Hit a stimpak, or next time you're leaving on a stretcher!}
{5964}{}{I'm drawing their fire! Mend your flesh while I chew through these scum!}
{5970}{}{Grampy Bone is pleased with this blow! Down in the dust, foul beast!}
{5971}{}{The sledge found the spine! The spirits guide Sulik's hand!}
{5972}{}{That is how my people break a raider's back! Take that!}
{5973}{}{Ha! Did you see that?! My lead drilled him right between the eyes!}
{5974}{}{And folks say old Vic can't shoot straight! How'd that taste, bastard?!}
{5975}{}{Bullseye! Boss, I took him down, the flank is clear!}
{5976}{}{Down goes another son of a bitch. Damn fine shot, if I say so myself!}
{5977}{}{Right in the ticker! That's why I keep this old shotgun close!}
{5978}{}{Stay down and stop squirming, meat! John Cassidy hasn't missed yet!}
{5979}{}{How'd you like that, scumbag?! Don't you dare lay a finger on my husband!}
{5980}{}{That's for Modoc, you bastard! My rifle doesn't miss!}
{5981}{}{Swallow some lead, ugly! Next time think twice before jumping us!}
{5982}{}{That's how we settled arguments in the old Mariposa army! Next!}
{5983}{}{Your skull cracked like a rotten melon. Pathetic.}
{5984}{}{Marcus's minigun doesn't care what armor you're wearing. Ground chuck!}
"""

def update_text_files():
    print("[1/3] Обновление языковых файлов custom.msg и wv_dialog.msg...")
    files_to_update = [
        (os.path.join(WV_DIR, "text", "russian", "game", "custom.msg"), RU_ADDITIONS, "cp1251"),
        (os.path.join(WV_DIR, "text", "russian", "dialog", "wv_dialog.msg"), RU_ADDITIONS, "cp1251"),
        (os.path.join(WV_DIR, "text", "english", "game", "custom.msg"), EN_ADDITIONS, "latin-1"),
        (os.path.join(WV_DIR, "text", "english", "dialog", "wv_dialog.msg"), EN_ADDITIONS, "latin-1"),
    ]

    for path, addition, enc in files_to_update:
        if not os.path.exists(path):
            print(f"[ERROR] Файл не найден: {path}")
            return False
        with open(path, "r", encoding=enc, errors="replace") as f:
            content = f.read()
        
        # Check if already appended
        if "{5730}" in content:
            print(f"[*] Уже содержит строки Среза 4: {os.path.basename(path)}")
            continue

        new_content = content.strip() + "\n\n" + addition.strip() + "\n"
        with open(path, "w", encoding=enc, errors="replace") as f:
            f.write(new_content)
        print(f"[OK] Добавлены строки Среза 4 в {path} ({enc})")
    return True

if __name__ == "__main__":
    if update_text_files():
        print("Текстовые файлы успешно обновлены.")
    else:
        sys.exit(1)
