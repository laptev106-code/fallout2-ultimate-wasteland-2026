"""
Compatibility and Conflict Resolution Engine
"""

from typing import List, Dict, Tuple
from core.manifest import COMPONENTS, ModComponent

class CompatibilityEngine:
    @staticmethod
    def validate_selection(selected_ids: List[str], target_profile: str) -> Tuple[bool, List[str], List[str]]:
        """
        Проверяет выбор компонентов на конфликты и зависимости.
        Возвращает: (is_valid, errors, warnings)
        target_profile: 'gameplay', 'hd', 'custom'
        """
        errors = []
        warnings = []
        selected_set = set(selected_ids)
        
        # 1. Проверка обязательных зависимостей
        for mod_id in selected_ids:
            mod = COMPONENTS.get(mod_id)
            if not mod:
                continue
            for req in mod.requires:
                if req not in selected_set:
                    errors.append(f"Мод '{mod.name}' требует установки '{COMPONENTS[req].name}'.")
                    
        # 2. Проверка несовместимых пар
        for mod_id in selected_ids:
            mod = COMPONENTS.get(mod_id)
            if not mod:
                continue
            for conflict in mod.conflicts_with:
                if conflict in selected_set:
                    errors.append(
                        f"Конфликт: '{mod.name}' несовместим с '{COMPONENTS[conflict].name}'. "
                        f"Они требуют разные движки (sfall 4.5.1 против Fallout2-CE) и не могут работать в одной папке!"
                    )
                    
        # 3. Проверка соответствия выбранному профилю
        if target_profile == "gameplay":
            for mod_id in selected_ids:
                mod = COMPONENTS.get(mod_id)
                if mod and mod.is_ce_only:
                    errors.append(f"Компонент '{mod.name}' предназначен только для HD-профиля (Community Edition).")
        elif target_profile == "hd":
            for mod_id in selected_ids:
                mod = COMPONENTS.get(mod_id)
                if mod and mod.is_sfall_only:
                    errors.append(f"Компонент '{mod.name}' требует sfall и не может работать в HD-профиле Dustlight.")
                    
        is_valid = len(errors) == 0
        return is_valid, list(set(errors)), list(set(warnings))

    @staticmethod
    def get_preset_components(preset_name: str) -> List[str]:
        """Возвращает проверенный список компонентов под конкретный пресет."""
        if preset_name == "gameplay_ultimate":
            return [cid for cid, c in COMPONENTS.items() if c.default_enabled_gameplay]
        elif preset_name == "hd_ultimate":
            return [cid for cid, c in COMPONENTS.items() if c.default_enabled_hd]
        return []
