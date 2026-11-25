# -*- coding: utf-8 -*-
import os, shutil

ru_kcyellow = """{100}{}{Вы видите крупную грязную собаку темно-песочного цвета, явно одичавшую.}
{101}{}{Вы видите грязную собаку песочного цвета.}
{110}{}{Гррр. Гав! Гав! Гррррр...}
{111}{}{Гав-гав, гав?}
{112}{}{(Смотря собаке в глаза) Ррррр! Аррррр! Гррррррр!}
{113}{}{Хмм, наверняка ты такая злая, потому что хочешь что-нибудь.}
{114}{}{Ты просто голодная, да, собачка? Посмотрим, осталось ли у меня немного вкусной солонины для тебя.}
{115}{}{Хмм, кажется, ты злишься от голода... Но у меня нет с собой ничего съестного.}
{116}{}{[Осторожно попятиться назад, не делая резких движений]}
{120}{}{Гав! (Собака выскакивает вперед, оскалив зубы, и хватает солонину у вас из рук. После чего она с чавканьем начинает ее жевать.)}
{121}{}{Гав! (Дворняга с радостью хватает кусок солонины, уронив ключ, который она, должно быть, держала в пасти. Вы поднимаете ключ.)}
{122}{}{М-м, солонина.}
{123}{}{Ах, бедняга, ты, наверное, есть хочешь. (Погладить собаку по голове).}
{130}{}{Гррр. Гав! Гав!}
{131}{}{Гав-гав, песик. Хе-хе.}
{132}{}{Пока, песик.}
{133}{}{Извини, сегодня у меня нет для тебя угощения.}
{134}{}{Кыш! П-шла отседа, чертова шавка.}
{140}{}{Гав, гав. Гав-гав!}
{141}{}{Гав, гав? Ау?}
{142}{}{Хорошая собачка, умница.}
{143}{}{Ты голодная, наверное, да? Наверняка, тебе хочется вкусной солонины, правда? Посмотрим, осталось ли у меня что-нибудь.}
{200}{}{Гав! (громко дышит, высунув язык. Проглатывает солонину.)}
{201}{}{Гав-гав}
{202}{}{Гав}
{203}{}{Гав, гав, гав}
{204}{}{(Смотрит на вас с обожанием)}
{205}{}{Гав!}
"""

en_kcyellow = """{100}{}{You see a large, mangy, buff colored dog with a feral look to it.}
{101}{}{You see a dusty, yellowish-buff colored, dog.}
{110}{}{Grrrrrr. Woof! Woof! Grrrrrr...}
{111}{}{Woof, Arf, Arf?}
{112}{}{(Staring into dog's eyes) Grrrr! Arrrrrgh! Grrrrrrrr!}
{113}{}{Hmm, I bet you sound angry because you want something.}
{114}{}{You're just hungry, aren't you, boy? Let me see if I have some delicious drymeat to give you.}
{115}{}{Hmm, I bet you're growling because you're hungry... But I don't have any food on me.}
{116}{}{[Carefully back away without making sudden moves]}
{120}{}{Woof! (Dog leaps forward with teeth bared -- snatches jerky from your outstretched hand -- eats jerky noisily)}
{121}{}{Woof! (The mongrel happily grabs the yummy drymeat, dropping a key that he must have had in his mouth -- you pick up the key.)}
{122}{}{Mmm, jerky.}
{123}{}{Ah, poor boy, you must have been hungry. (Patting dog on head)}
{130}{}{Grrr. Woof! Woof!}
{131}{}{Arf-arf doggy. Heh, heh.}
{132}{}{Bye, doggy.}
{133}{}{Sorry, no doggy treats for you today.}
{134}{}{Shoo! Get out of here, you damn mutt.}
{140}{}{Woof, woof. Woof-woof!}
{141}{}{Woof, woof? Eru?}
{142}{}{Good doggy, good boy.}
{143}{}{You're hungry, aren't you, boy? I bet you'd like some delicious drymeat, wouldn't you? Let's see if I have some. }
{200}{}{Woof! (pant, pant, pant -- Slurp!)}
{201}{}{Woof-woof!}
{202}{}{Arf!}
{203}{}{Arf, arf, arf!}
{204}{}{(Stares at you lovingly)}
{205}{}{Woof!}
"""

bases = [
    r"E:\FALLOUT Ult pjt\mods\rpu_russian_uncensored.dat",
    r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu_russian_uncensored.dat",
    r"E:\Fallout2_Ultimate\Fallout2_HD\mods\rpu_russian_uncensored.dat"
]

compiled_int = r"E:\FALLOUT Ult pjt\tools\kcyellow.int"

for b in bases:
    script_dir = os.path.join(b, "scripts")
    ru_dir = os.path.join(b, "text", "russian", "dialog")
    en_dir = os.path.join(b, "text", "english", "dialog")

    os.makedirs(script_dir, exist_ok=True)
    os.makedirs(ru_dir, exist_ok=True)
    os.makedirs(en_dir, exist_ok=True)

    # 1. Copy kcyellow.int
    shutil.copy2(compiled_int, os.path.join(script_dir, "kcyellow.int"))

    # 2. Write ru msg
    with open(os.path.join(ru_dir, "kcyellow.msg"), "wb") as f:
        f.write(ru_kcyellow.encode("cp1251"))

    # 3. Write en msg
    with open(os.path.join(en_dir, "kcyellow.msg"), "wb") as f:
        f.write(en_kcyellow.encode("latin1"))

    print(f"Deployed kcyellow fix to {b}")

print("ALL DEPLOYMENTS COMPLETED!")
