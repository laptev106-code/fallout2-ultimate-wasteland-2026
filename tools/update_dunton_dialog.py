# -*- coding: utf-8 -*-
import os

new_ru = """{850}{}{Чего зенки вылупил? Какого черта ты забыл на пастбище?}
{851}{}{Торр попросил присмотреть за браминами от скорпионов. А вы двое что тут вынюхиваете?}
{852}{}{Не ваше собачье дело. Убирайтесь от стада, пока я не переломал вам ребра.}
{853}{}{Просто осматриваюсь. Уже ухожу.}
{860}{}{(Гнусно ухмыляется) Торр? Этот полоумный дурачок даже до трех сосчитать не может. Слушай сюда, дикарь: помоги нам отогнать пару туш, и мы отвалим тебе отборной солонины и звонких монет. По рукам?}
{861}{}{И что конкретно нужно сделать?}
{862}{}{Я не помогаю мелким скотокрадам. Пошли вон отсюда, пока целы.}
{863}{}{Мне надо прикинуть. Ждите здесь.}
{870}{}{Слышь, голодранец, ты кому хамишь? Сейчас мы с братом оторвем тебе башку и скормим собакам!}
{871}{}{Ну попробуйте, уроды. Посмотрим, чьи потроха быстрее остынут на траве.}
{872}{}{Шаг ко мне — и я выпущу вам кишки прямо под ноги скорпионам. Исчезните, куски мяса.}
{873}{}{Эй, спокойно. Я просто спросил, не надо драки.}
{880}{}{(Осаживает назад, отирая пот) Твою мать, Чак... этот дикарь совсем отбитый. Валим отсюда, ну его к черту!}
{881}{}{Ты кого пугать вздумал, дикарь?! Бак, давай разорвем этого ублюдка на куски!}"""

new_en = """{850}{}{What are you gawking at? What the hell are you doing out on these pastures?}
{851}{}{Torr asked me to watch the brahmin for radscorpions. What are you two sniffing around for?}
{852}{}{None of your damn business. Back off from the herd before I stove your ribs in.}
{853}{}{Just looking around. Leaving now.}
{860}{}{(Sneers nastily) Torr? That drooling half-wit can't even count to three. Listen here, tribal: help us cut out a couple of steers, and we'll cut you in on prime jerky and hard coin. What do you say?}
{861}{}{What's the play? What do I have to do?}
{862}{}{I don't haul water for petty rustlers. Shove off before you get hurt.}
{863}{}{I need to weigh the odds. Stay put.}
{870}{}{Listen here, ditch-born dirt-scratcher, who do you think you're mouthing off to? We'll snap your spine and feed you to the mongrels!}
{871}{}{Try it, grease-balls. Let's see whose guts turn cold on the grass first.}
{872}{}{One twitch and I'll spill your entrails for the scorpions to choke on. Vanish, meat-bags.}
{873}{}{Easy, easy. Just talking. Nobody needs a fight.}
{880}{}{(Steps back, sweating) Jesus, Chuck... this tribal's totally unhinged. Let's haul ass, he ain't worth it!}
{881}{}{Who do you think you're bluffing, savage?! Buck, let's tear this bastard to shreds!}"""

def update_file(path, new_block, encoding):
    if not os.path.exists(path):
        return
    with open(path, "r", encoding=encoding, errors="replace") as f:
        text = f.read()

    # Find where {850} starts
    pos = text.find("{850}{}")
    if pos != -1:
        base_text = text[:pos].strip() + "\n\n"
    else:
        base_text = text.strip() + "\n\n"

    full_text = base_text + new_block + "\n"
    with open(path, "wb") as f:
        f.write(full_text.encode(encoding))
    print(f"Updated {path} ({encoding})")

ru_paths = [
    r"E:\FALLOUT Ult pjt\mods\rpu_russian_uncensored.dat\text\russian\dialog\kcdunton.msg",
    r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu_russian_uncensored.dat\text\russian\dialog\kcdunton.msg",
    r"E:\Fallout2_Ultimate\Fallout2_HD\mods\rpu_russian_uncensored.dat\text\russian\dialog\kcdunton.msg",
    r"E:\FALLOUT Ult pjt\tools\kcdunton.msg"
]

en_paths = [
    r"E:\FALLOUT Ult pjt\mods\rpu_russian_uncensored.dat\text\english\dialog\kcdunton.msg",
    r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu_russian_uncensored.dat\text\english\dialog\kcdunton.msg",
    r"E:\Fallout2_Ultimate\Fallout2_HD\mods\rpu_russian_uncensored.dat\text\english\dialog\kcdunton.msg"
]

for p in ru_paths:
    update_file(p, new_ru, "cp1251")

for p in en_paths:
    update_file(p, new_en, "latin1")
