from abc import ABC
from units import unit, scaled_unit
from hotshopper.errors import UnsupportedUnitError

piece = unit("St.")
gram = unit("g")
kilogram = scaled_unit("kg", "g", 1000)


class Location:
    pass


class Supermarket(Location):
    pass


class Market(Location):
    pass


SUPERMARKET = Supermarket()
MARKET = Market()


class Ingredient(ABC):
    name = ""
    where = Location()

    def __init__(self, unit: unit, amount: float):
        self.id = 0
        self.amount_piece = piece(0)
        self.amount = gram(0)
        self.unit = unit
        if unit not in (piece, gram, kilogram):
            raise UnsupportedUnitError("This unit is not supported")
        if unit == piece:
            self.amount_piece = unit(amount)
        else:
            self.amount = unit(amount)

    def get_id(self):
        return self.id


class AgaveSyrup(Ingredient):
    name = "Agavendicksaft"
    where = SUPERMARKET
    id = 7500


class Ajvar(Ingredient):
    name = "Ajvar"
    where = SUPERMARKET
    id = 8030


class ApplePuree(Ingredient):
    name = "Apfelmus"
    where = SUPERMARKET
    id = 4160


class Asparagus(Ingredient):
    name = "Spargel"
    where = SUPERMARKET
    id = 14500


class Avocado(Ingredient):
    name = "Avocado"
    where = MARKET
    id = 14510


class Baguette(Ingredient):
    name = "Baguette"
    where = MARKET
    id = 15000


class BakingPowder(Ingredient):
    name = "Backpulver"
    where = SUPERMARKET
    id = 4506


class BarbecueMeat(Ingredient):
    name = "Grillfleisch (selbst aussuchen)"
    where = MARKET
    id = 12050


class BasilFrozen(Ingredient):
    name = "TK-Basilikum"
    where = SUPERMARKET


class BeefCuts(Ingredient):
    name = "Rindergeschnetzeltes"
    where = MARKET
    id = 12040


class BroccoliFrozen(Ingredient):
    name = "TK-Brokkoli"
    where = SUPERMARKET
    id = 11080


class Buckwheat(Ingredient):
    name = "Buchweizen"
    where = SUPERMARKET
    id = 4507


class Cabanossi(Ingredient):
    name = "Cabanossi"
    where = MARKET
    id = 12061


class CaneSugar(Ingredient):
    name = "Rohrzucker"
    where = SUPERMARKET
    id = 4505


class Caraway(Ingredient):
    name = "Kümmel"
    where = SUPERMARKET
    id = 8011


class CardamomMilled(Ingredient):
    name = "gem. Kardamom"
    where = SUPERMARKET
    id = 8012


class Carrot(Ingredient):
    name = "Karotten"
    where = MARKET
    id = 14070


class CauliflowerFrozen(Ingredient):
    name = "TK-Blumenkohl"
    where = SUPERMARKET
    id = 11070


class CauliflowerWithCreamFrozen(Ingredient):
    name = "TK-Rahmblumenkohl"
    where = SUPERMARKET
    id = 11071


class Champignon(Ingredient):
    name = "Champignon(s)"
    where = MARKET
    id = 14100


class ChickenCuts(Ingredient):
    name = "Hähnchengeschnetzeltes"
    where = MARKET
    id = 12030


class Chicory(Ingredient):
    name = "Chicorée"
    where = MARKET
    id = 14120


class CeleryRoot(Ingredient):
    name = "Knollensellerie"
    where = MARKET
    id = 14140


class CheeseSlices(Ingredient):
    name = "Schablettenkäse"
    where = SUPERMARKET
    id = 5210


class CherryTomato(Ingredient):
    name = "Kirschtomaten"
    where = MARKET
    id = 14501


class ChiliPepper(Ingredient):
    name = "Chilischote(n)"
    where = MARKET
    id = 14130


class Cream(Ingredient):
    name = "Sahne"
    where = SUPERMARKET
    id = 5040


class CreamCheese(Ingredient):
    name = "Frischkäse"
    where = SUPERMARKET
    id = 5130


class CremeFraiche(Ingredient):
    name = "Crème Fraîche"
    where = SUPERMARKET
    id = 5060


class CroquettesFrozen(Ingredient):
    name = "TK-Kroketten"
    where = SUPERMARKET
    id = 11020


class CoconutMilk(Ingredient):
    name = "Kokosmilch"
    where = SUPERMARKET
    id = 8160


class Cucumber(Ingredient):
    name = "Salatgurke"
    where = MARKET
    id = 14010


class DillFrozen(Ingredient):
    name = "TK-Dill"
    where = SUPERMARKET
    id = 11101


class EightHerbsFrozen(Ingredient):
    name = "TK-8-Kräuter"
    where = SUPERMARKET
    id = 11102


class Egg(Ingredient):
    name = "Ei(er)"
    where = MARKET
    id = 13040


class FetaCheese(Ingredient):
    name = "Fetakäse"
    where = SUPERMARKET
    id = 5500


class Fishsticks(Ingredient):
    name = "Fischstäbchen"
    where = SUPERMARKET
    id = 11110


class FriesFrozen(Ingredient):
    name = "Pommes frittes"
    where = SUPERMARKET
    id = 11030


class Garlic(Ingredient):
    name = "Knoblauch"
    where = MARKET
    id = 14502


class Ginger(Ingredient):
    name = "Ingwer"
    where = MARKET
    id = 14060


class GlassNoodles(Ingredient):
    name = "Glasnudeln"
    where = SUPERMARKET
    id = 8140


class Gnocchi(Ingredient):
    name = "Gnocchi"
    where = SUPERMARKET
    id = 1030


class Gorgonzola(Ingredient):
    name = "Gorgonzola"
    where = SUPERMARKET
    id = 5501


class GoudaSlices(Ingredient):
    name = "Gouda (in Scheiben)"
    where = SUPERMARKET
    id = 5170


class GratinCheese(Ingredient):
    name = "Gratinkäse"
    where = SUPERMARKET
    id = 5200


class GreenCurryPaste(Ingredient):
    name = "Grüne Currypaste"
    where = SUPERMARKET
    id = 8500


class GroundMeat(Ingredient):
    name = "Hackfleisch (gem.)"
    where = MARKET
    id = 12010


class HamCooked(Ingredient):
    name = "Kochschinken"
    where = SUPERMARKET
    id = 6500


class HamCubes(Ingredient):
    name = "Schinkenwürfel"
    where = SUPERMARKET
    id = 6010


class HamSlices(Ingredient):
    name = "Schinken (Scheibe)"
    where = MARKET
    id = 12062


class HazelnutFlakes(Ingredient):
    name = "Haselnussblättchen"
    where = SUPERMARKET
    id = 4500


class HazelnutMilled(Ingredient):
    name = "gem. Haselnüsse"
    where = SUPERMARKET
    id = 4501


class HokkaidoPumpkin(Ingredient):
    name = "Hokkaido-Kürbis"
    where = SUPERMARKET
    id = 2500


class Leek(Ingredient):
    name = "Lauch"
    where = MARKET
    id = 14020


class Lemon(Ingredient):
    name = "Zitrone"
    where = MARKET
    id = 14503


class Lettuce(Ingredient):
    name = "Kopfsalat"
    where = MARKET
    id = 14090


class Lime(Ingredient):
    name = "Limette(n)"
    where = SUPERMARKET
    id = 2010


class MacadamiaNut(Ingredient):
    name = "Makademia-Nüsse"
    where = SUPERMARKET
    id = 4021


class Macaroni(Ingredient):
    name = "Makkaroni (kurz)"
    where = SUPERMARKET
    id = 4071


class MaggiFixLasagna(Ingredient):
    name = "MaggiFix für Lasagne"
    where = SUPERMARKET
    id = 4101


class MaggiFixPepperCreamSchnitzel(Ingredient):
    name = "MaggiFix für Paprikarahmschnitzel"
    where = SUPERMARKET
    id = 4102


class Mascarpone(Ingredient):
    name = "Mascarpone"
    where = SUPERMARKET
    id = 5150


class Maultaschen(Ingredient):
    name = "Maultaschen"
    where = SUPERMARKET
    id = 1010


class Milk(Ingredient):
    name = "Milch"
    where = SUPERMARKET
    id = 5010


class MungbeanSproute(Ingredient):
    name = "Mungobohnensprossen"
    where = SUPERMARKET
    id = 8150


class NoodlesSpiral(Ingredient):
    name = "Fussili-Nudeln"
    where = SUPERMARKET
    id = 4072


class Onion(Ingredient):
    name = "Zwiebel(n)"
    where = SUPERMARKET
    id = 2020


class OnionRed(Ingredient):
    name = "Rote Zwiebel(n)"
    where = MARKET
    id = 14081


class Orange(Ingredient):
    name = "Orange(n)"
    where = MARKET
    id = 14200


class ParmesanCheese(Ingredient):
    name = "Parmesankäse"
    where = SUPERMARKET
    id = 5190


class ParsleyFrozen(Ingredient):
    name = "TK-Petersilie"
    where = SUPERMARKET
    id = 11103


class ParsleyRoot(Ingredient):
    name = "Petersilienwurzel"
    where = MARKET
    id = 14110


class PeasAndCarrotsFrozen(Ingredient):
    name = "TK-Erbsen+Möhren"
    where = SUPERMARKET
    id = 11050


class PeasFrozen(Ingredient):
    name = "TK-Erbsen"
    where = SUPERMARKET
    id = 11060


class PepperGreen(Ingredient):
    name = "Grüne Paprika(s)"
    where = MARKET
    id = 14031


class PepperRed(Ingredient):
    name = "Rote Paprika(s)"
    where = MARKET
    id = 14032


class PepperRoasted(Ingredient):
    name = "ger. Paprika (Glas)"
    where = SUPERMARKET
    id = 8060


class PestoGenovese(Ingredient):
    name = "Pesto Genovese"
    where = SUPERMARKET
    id = 4030


class PepperYellow(Ingredient):
    name = "Gelbe Paprika(s)"
    where = MARKET
    id = 14033


class Pickles(Ingredient):
    name = "Saure Gurken"
    where = SUPERMARKET
    id = 8110


class PineapplesSlicesPickled(Ingredient):
    name = "Ananasscheiben (in Dose)"
    where = SUPERMARKET
    id = 4150


class Pistachios(Ingredient):
    name = "Pistazien"
    where = SUPERMARKET
    id = 4022


class PitaBread(Ingredient):
    name = "Pitabrot (Pack)"
    where = SUPERMARKET
    id = 7050


class PorkCuts(Ingredient):
    name = "Schweinegschnetzeltes"
    where = MARKET
    id = 12020


class PotatoePancankesFrozen(Ingredient):
    name = "TK-Kartoffelpuffer"
    where = SUPERMARKET
    id = 11010


class RicePudding(Ingredient):
    name = "Milchreis"
    where = SUPERMARKET
    id = 4502


class RiceBasmati(Ingredient):
    name = "Basmatireis"
    where = SUPERMARKET
    id = 4090


class SaladSauce(Ingredient):
    name = "Salatsauce"
    where = SUPERMARKET
    id = 8120


class Salami(Ingredient):
    name = "Salami-Pack"
    where = SUPERMARKET
    id = 6501


class SandwichCheese(Ingredient):
    name = "Schablettenkäse"
    where = SUPERMARKET
    id = 5210


class SausageStripes(Ingredient):
    name = "Streifen f. Wurstsalat"
    where = SUPERMARKET
    id = 6030


class Schupfnudeln(Ingredient):
    name = "Schupfnudeln"
    where = SUPERMARKET
    id = 1020


class Smetana(Ingredient):
    name = "Schmand"
    where = SUPERMARKET
    id = 5050


class SourCream(Ingredient):
    name = "Sauerrahm (pur)"
    where = SUPERMARKET
    id = 5070


class Sourcrout(Ingredient):
    name = "Sauerkraut"
    where = SUPERMARKET
    id = 4170


class SoySauce(Ingredient):
    name = "Sojasauce (hell)"
    where = SUPERMARKET
    id = 8130


class SpaetzleCheese(Ingredient):
    name = "Spätzlekäse"
    where = SUPERMARKET
    id = 5180


class SpaetzleNoodles(Ingredient):
    name = "Spätzle"
    where = SUPERMARKET
    id = 4080


class SpaghettiNoodles(Ingredient):
    name = "Spaghetti"
    where = SUPERMARKET
    id = 4073


class SpinachCreamed(Ingredient):
    name = "Rahmspinat"
    where = SUPERMARKET
    id = 11091


class Sprout(Ingredient):
    name = "Rosenkohl"
    where = SUPERMARKET
    id = 11092


class Swede(Ingredient):
    name = "Steckrübe"
    where = MARKET
    id = 14504


class Tagliatelle(Ingredient):
    name = "Bandnudeln"
    where = SUPERMARKET
    id = 4074


class ToastbreadSandwich(Ingredient):
    name = "Toastbrot (Sandwich)"
    where = SUPERMARKET
    id = 7041


class ToastbreadWheatSlice(Ingredient):
    name = "Toastbrot (Scheiben)"
    where = SUPERMARKET
    id = 7040


class ToastbreadWholemeal(Ingredient):
    name = "Toastbrot (Vollkorn)"
    where = SUPERMARKET
    id = 7042


class Tomato(Ingredient):
    name = "Tomate(n)"
    where = MARKET
    id = 2501


class TomatoPaste(Ingredient):
    name = "Tomatenmark"
    where = SUPERMARKET
    id = 4040


class TomatoPickled(Ingredient):
    name = "Dosentomaten (ganz)"
    where = SUPERMARKET
    id = 4050


class TomatoSauce(Ingredient):
    name = "Dosentomaten (stückig/passiert)"
    where = SUPERMARKET
    id = 4503


class TortelliniDried(Ingredient):
    name = "Tortellini (getrocknet)"
    where = SUPERMARKET
    id = 4060


class Tortilla(Ingredient):
    name = "Tortillafladen"
    where = SUPERMARKET
    id = 8170


class TurkeySchnitzel(Ingredient):
    name = "Putenschnitzel"
    where = MARKET
    id = 12500


class Tzatziki(Ingredient):
    name = "Tzatziki"
    where = SUPERMARKET
    id = 5120


class WheatFlour(Ingredient):
    name = "Weizenmehl"
    where = SUPERMARKET
    id = 4504


class Wiener(Ingredient):
    name = "Saitenwürste"
    where = MARKET
    id = 6040


class VanillaSugar(Ingredient):
    name = "Vanillezucker"
    where = SUPERMARKET
    id = 4508


class VegetablesFrozen(Ingredient):
    name = "TK-Gemüse (Mix)"
    where = SUPERMARKET
    id = 11040


class Zucchini(Ingredient):
    name = "Zucchini(s)"
    where = MARKET
    id = 14050


class _Potato(Ingredient):
    where = MARKET
    pass


class LowStarchPotatoe(_Potato):
    name = "Kartoffeln festk."
    id = 13070


class StarchyPotato(_Potato):
    name = "Kartoffeln mehlig"
    id = 13050


class PrimarilyWaxyPotato(_Potato):
    name = "Kartoffeln vorw. festk."
    id = 13060
