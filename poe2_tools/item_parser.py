from dataclasses import dataclass
from typing import Optional, List, Tuple

import re

@dataclass
class DamageRange:
    min_damage: float
    max_damage: float
    damage_type: str

    @property
    def average(self) -> float:
        return (self.min_damage + self.max_damage) / 2

@dataclass
class ItemStats:
    name: str
    item_class: str
    rarity: str
    quality: float
    physical_damage: DamageRange
    elemental_damages: List[DamageRange]  # List of fire, cold, lightning damages
    chaos_damage: Optional[DamageRange]
    crit_chance: float
    attacks_per_second: float
    dps: float
    physical_dps: float
    elemental_dps: float
    chaos_dps: float
    quality_adjusted_dps: float
    total_added_flat_phys: float
    increased_phys_percent: float
    accuracy_rating: int
    projectile_levels: int
    life_on_hit: int
    additional_arrows: int
    item_level: int


def parse_damage_range(text: str, damage_type: str) -> Optional[DamageRange]:
    """Parse a damage range from text for a specific damage type."""
    pattern = f"{damage_type} Damage: (\\d+)-(\\d+)"
    match = re.search(pattern, text)
    if match:
        min_dmg, max_dmg = map(float, match.groups())
        return DamageRange(min_dmg, max_dmg, damage_type.lower())
    return None

def parse_added_damage(text: str, damage_type: str) -> Optional[DamageRange]:
    """Parse added damage from mods."""
    pattern = f"Adds (\\d+) to (\\d+) {damage_type} Damage"
    match = re.search(pattern, text)
    if match:
        min_dmg, max_dmg = map(float, match.groups())
        return DamageRange(min_dmg, max_dmg, damage_type.lower())
    return None

def parse_item_stats(clipboard_text: str) -> ItemStats:
    """
    Parse Path of Exile item text and calculate various combat statistics.
    
    Args:
        clipboard_text (str): Raw item text from the game clipboard
        
    Returns:
        ItemStats: Calculated item statistics
        
    Raises:
        ValueError: If the item is not a weapon or cannot be parsed
    """
    lines = clipboard_text.split('\n')
    
    # Basic item info
    item_class = re.search(r'Item Class: (.+)', clipboard_text)
    if not item_class or 'bow' not in item_class.group(1).lower():
        raise ValueError("This parser currently only supports bows")
        
    name = next(line for line in lines if line and not line.startswith('--------'))
    rarity = re.search(r'Rarity: (.+)', clipboard_text).group(1)
    
    # Extract core stats
    quality = re.search(r'Quality: \+(\d+)%', clipboard_text)
    quality = float(quality.group(1)) if quality else 0.0
    
    # Parse all damage types
    phys_damage = parse_damage_range(clipboard_text, "Physical")
    if not phys_damage:
        phys_damage = DamageRange(0, 0, "physical")

    # Parse elemental damages (base + added)
    damage_types = ["Fire", "Cold", "Lightning"]
    elemental_damages = []
    
    for dmg_type in damage_types:
        # Check base damage
        base_dmg = parse_damage_range(clipboard_text, dmg_type)
        added_dmg = parse_added_damage(clipboard_text, dmg_type)
        
        if base_dmg or added_dmg:
            min_dmg = (base_dmg.min_damage if base_dmg else 0) + (added_dmg.min_damage if added_dmg else 0)
            max_dmg = (base_dmg.max_damage if base_dmg else 0) + (added_dmg.max_damage if added_dmg else 0)
            if min_dmg > 0 or max_dmg > 0:
                elemental_damages.append(DamageRange(min_dmg, max_dmg, dmg_type.lower()))

    # Parse chaos damage
    chaos_damage = parse_damage_range(clipboard_text, "Chaos")
    added_chaos = parse_added_damage(clipboard_text, "Chaos")
    if chaos_damage or added_chaos:
        min_chaos = (chaos_damage.min_damage if chaos_damage else 0) + (added_chaos.min_damage if added_chaos else 0)
        max_chaos = (chaos_damage.max_damage if chaos_damage else 0) + (added_chaos.max_damage if added_chaos else 0)
        chaos_damage = DamageRange(min_chaos, max_chaos, "chaos") if min_chaos > 0 or max_chaos > 0 else None
        
    # Parse attack speed and crit
    base_crit = float(re.search(r'Critical Hit Chance: ([\d.]+)%', clipboard_text).group(1))
    attacks_per_second = float(re.search(r'Attacks per Second: ([\d.]+)', clipboard_text).group(1))
    
    # Parse item level
    item_level = int(re.search(r'Item Level: (\d+)', clipboard_text).group(1))
    
    # Calculate damage modifiers
    increased_phys = sum(float(x) for x in re.findall(r'(\d+)% increased Physical Damage', clipboard_text))
    
    added_phys = parse_added_damage(clipboard_text, "Physical")
    added_phys_value = (added_phys.average if added_phys else 0)
    
    # Parse additional modifiers
    accuracy = re.search(r'\+(\d+) to Accuracy Rating', clipboard_text)
    accuracy_rating = int(accuracy.group(1)) if accuracy else 0
    
    proj_level = re.search(r'\+(\d+) to Level of all Projectile Skills', clipboard_text)
    projectile_levels = int(proj_level.group(1)) if proj_level else 0
    
    life_hit = re.search(r'Grants (\d+) Life per Enemy Hit', clipboard_text)
    life_on_hit = int(life_hit.group(1)) if life_hit else 0
    
    additional_arrow = len(re.findall(r'fire[s]? an additional Arrow', clipboard_text))
    add_arrows = re.search(r'fire[s]? (\d+) additional Arrow', clipboard_text)
    additional_arrows = int(add_arrows.group(1)) if add_arrows else 0
    additional_arrows += additional_arrow

    # Calculate DPS
    physical_dps = phys_damage.average * attacks_per_second
    elemental_dps = sum(dmg.average * attacks_per_second for dmg in elemental_damages)
    chaos_dps = chaos_damage.average * attacks_per_second if chaos_damage else 0
    
    # Total DPS
    total_dps = physical_dps + elemental_dps + chaos_dps
    
    # Calculate quality-adjusted DPS
    if quality < 20:
        quality_multiplier = (20 - quality) / 100 + 1
        adjusted_physical_dps = physical_dps * quality_multiplier
        quality_adjusted_dps = adjusted_physical_dps + elemental_dps + chaos_dps
    else:
        quality_adjusted_dps = total_dps

    return ItemStats(
        name=name,
        item_class=item_class.group(1),
        rarity=rarity,
        quality=quality,
        physical_damage=phys_damage,
        elemental_damages=elemental_damages,
        chaos_damage=chaos_damage,
        crit_chance=base_crit,
        attacks_per_second=attacks_per_second,
        dps=total_dps,
        physical_dps=physical_dps,
        elemental_dps=elemental_dps,
        chaos_dps=chaos_dps,
        quality_adjusted_dps=quality_adjusted_dps,
        total_added_flat_phys=added_phys_value,
        increased_phys_percent=increased_phys,
        accuracy_rating=accuracy_rating,
        projectile_levels=projectile_levels,
        life_on_hit=life_on_hit,
        additional_arrows=additional_arrows,
        item_level=item_level
    )

def format_item_summary(stats: ItemStats) -> str:
    """Format item statistics into a readable summary."""
    summary = [
        f"=== {stats.name} ===",
        f"Base Properties:",
        f"• Quality: +{stats.quality}%",
        f"• Phys Damage: {stats.physical_damage.min_damage}-{stats.physical_damage.max_damage}",
    ]
    
    # Add elemental damages
    for elem_dmg in stats.elemental_damages:
        summary.append(f"• {elem_dmg.damage_type.title()} Damage: {elem_dmg.min_damage}-{elem_dmg.max_damage}")
    
    # Add chaos damage if present
    if stats.chaos_damage:
        summary.append(f"• Chaos Damage: {stats.chaos_damage.min_damage}-{stats.chaos_damage.max_damage}")
    
    summary.extend([
        f"• APS: {stats.attacks_per_second:.2f}",
        f"• Crit: {stats.crit_chance}%",
        f"\nDamage Statistics:",
        f"• Physical DPS: {stats.physical_dps:.1f}",
    ])
    
    # Add elemental DPS breakdown
    if stats.elemental_dps > 0:
        summary.append(f"• Elemental DPS: {stats.elemental_dps:.1f}")
    
    # Add chaos DPS if present
    if stats.chaos_dps > 0:
        summary.append(f"• Chaos DPS: {stats.chaos_dps:.1f}")
    
    summary.append(f"• Total DPS: {stats.dps:.1f}")
    
    # Add quality-adjusted DPS if quality is less than 20%
    if stats.quality < 20:
        summary.append(f"• Total DPS(adjusted): {stats.quality_adjusted_dps:.1f}")
    
    summary.extend([
        f"\nModifiers:",
        f"• Inc. Phys: {stats.increased_phys_percent}%",
        f"• Added Phys: {stats.total_added_flat_phys:.1f}",
        f"• +Arrows: {stats.additional_arrows}",
        f"\nUtility:",
        f"• Accuracy: +{stats.accuracy_rating}",
        f"• Proj Level: +{stats.projectile_levels}",
        f"• Life on Hit: {stats.life_on_hit}",
        f"\nItem Level: {stats.item_level}"
    ])
    return "\n".join(summary)