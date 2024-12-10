from logic.calculations import Parabola
from utils.parabolas import CYPHER_PARABOLA, KILLJOY_VIPER_DEADLOCK_GECKO_KAYO_PARABOLA, VIPER_BRIMSTONE_STAGE_PARABOLA, \
    SOVA_PARABOLA

class Ability:
    def __init__(self, parabola: Parabola, name: str):
        """
        Class representing an ability with a parabolic trajectory.

        Args:
            parabola (Parabola): The Parabola object representing the trajectory of the ability.
            name (str): The name of the ability.
        """
        self.parabola = parabola
        self.name = name

cypher_cage = Ability(CYPHER_PARABOLA, "cypher_cage")
deadlock_net = Ability(KILLJOY_VIPER_DEADLOCK_GECKO_KAYO_PARABOLA, "deadlock_net")
killjoy_swarm_grenade = Ability(KILLJOY_VIPER_DEADLOCK_GECKO_KAYO_PARABOLA, "killjoy_swarm_grenade")
gecko_moshpit = Ability(KILLJOY_VIPER_DEADLOCK_GECKO_KAYO_PARABOLA, "gecko_moshpit")
viper_poison_orb = Ability(KILLJOY_VIPER_DEADLOCK_GECKO_KAYO_PARABOLA, "viper_poison_orb")
kayo_fragment = Ability(KILLJOY_VIPER_DEADLOCK_GECKO_KAYO_PARABOLA, "kayo_fragment")
viper_snakebite = Ability(VIPER_BRIMSTONE_STAGE_PARABOLA, "viper_snakebite")
brimstone_molotov = Ability(VIPER_BRIMSTONE_STAGE_PARABOLA, "brimstone_molotov")
sage_slow_orb = Ability(VIPER_BRIMSTONE_STAGE_PARABOLA, "sage_slow")
sova_arrow = Ability(SOVA_PARABOLA, "sova_arrow")

abilities = [cypher_cage, deadlock_net, killjoy_swarm_grenade, gecko_moshpit, viper_snakebite, viper_poison_orb, brimstone_molotov, sage_slow_orb, kayo_fragment, sova_arrow]
