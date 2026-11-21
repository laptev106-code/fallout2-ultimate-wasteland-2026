# Tactical Combat AI: Desperation Last Stand & Cautious Retreat
**Version:** 1.0 Hardened  
**Author:** Antigravity Engine Team  
**Game:** Fallout 2 (Compatible with Vanilla, RPU, EcCo, Nevada, Sonora, Olympus 2207)  
**Requirements:** sFall 4.x or 5.x (included with RPU / modern Fallout 2 installations)

---

## [RU] ОПИСАНИЕ И ОСОБЕННОСТИ

Модификация решает одну из самых надоедливых геймдизайнерских проблем классического Fallout 2 — **«фазу нудной зачистки» (mop-up phase)**, когда раненый противник бежит через 40 гексов на край карты, заставляя игрока тратить 5-7 пустых ходов на бессмысленную погоню.

### Ключевые механики:
1. **Тактический отход стрелков (Кайт на 12 гексах):**
   - Вооруженный враг с огнестрельным оружием и патронами при отходе на 12 гексов прекращает бегство, разворачивается и начинает прицельный отстрел игрока или его напарников с дальней дистанции.
   - Если враг вооружен холодным оружием (нож, копье) или у него закончились патроны, скрипт позволяет ему продолжить отступление, не превращая его в беспомощную мишень.

2. **Бесстрашие для элитных противников:**
   - Супермутанты, боевые роботы, когти смерти и пришельцы больше **никогда не паникуют и не убегают**. Они дерутся насмерть, как и подобает машинам и тяжелым монстрам Пустоши.

3. **Ярость отчаяния (Last Stand):**
   - Тяжелораненый гуманоид (здоровье $\le 22\%$ или $\le 15$ HP) с вероятностью 8–12% срывается в отчаянную контратаку.
   - Над головой бойца красным текстом всплывает одна из 12 боевых фраз (например: *«Живым не сдамся! Я заберу тебя с собой!»*), и он идет в последний бой.

4. **Полная защита от нелепых ситуаций (Hardened Safeguards):**
   - **Динамический выбор цели:** враг атакует ближайшего угрожающего члена группы (Сулика, Кэссиди, Вика), а не бежит через полкарты к Избранному.
   - **Фильтр мирных жителей:** горожане, дети, бродяги, проститутки и трусливые крестьяне не превращаются в берсерков и спасаются бегством.
   - **Физические травмы:** если врагу сломали обе руки или выбили глаза, он продолжает спасаться бегством, а не застревает на месте.

---

## [EN] OVERVIEW & FEATURES

Eliminates the infamous **"mop-up chase slog"** in Fallout 2, where critically wounded enemies sprint 40 hexes into the black fog of war, forcing players through 5-7 agonizingly slow running turns.

1. **Cautious Retreat & Ranged Kiting:**
   - Armed enemies with functional ranged weapons stop fleeing at safe engagement distance (12 hexes), turn around, and return fire from long range.
   - Melee enemies or enemies with empty magazines continue retreating naturally.

2. **Fearless Heavy Entities:**
   - Combat Robots, Super Mutants, Deathclaws, and Aliens **never flee in panic**. They fight to the death.

3. **Desperation Last Stand:**
   - Critically injured humanoids (HP $\le 22\%$ or $\le 15$ HP) have an 8–12% chance (scaled by Strength and Endurance) to cancel panic and launch a suicidal final counter-attack.
   - Accompanied by authentic floating red combat cries above their heads.

4. **Hardened Tactical Safeguards:**
   - **Dynamic Target Selection:** Attacks the closest threatening party member instead of a hardcoded player target.
   - **Civilian / Non-Combatant Filter:** Frightened townsfolk, prostitutes, peasants, and children never enter berserk mode.
   - **Physical Disability Filter:** Blinded enemies or enemies with both arms crippled continue fleeing without locking up.

---

## НАСТРОЙКА / CONFIGURATION (`mods/gl_laststand.ini`)

Параметры легко настраиваются в файле `mods/gl_laststand.ini`:
```ini
[Settings]
; Дистанция (в гексах), на которой стрелки прекращают бег и открывают огонь (по умолчанию: 12)
KitingDistance=12

; Базовый шанс в % (от 0 до 100) на срабатывание "Последнего боя" (по умолчанию: 8)
LastStandBaseChance=8

; Бесстрашные роботы, мутанты и когти смерти (1 = включено, 0 = выключено)
FearlessBrutes=1

; Красные боевые реплики над головой (1 = включено, 0 = выключено)
FloatCombatMessages=1
```

---

## УСТАНОВКА / INSTALLATION

1. Скопируйте папку `mods` (или положите `gl_laststand.int` в `data/scripts/`, а `gl_laststand.ini` в `mods/`) в корневую папку Fallout 2.
2. Готово! Скрипт подхватывается движком sFall автоматически на старте.
