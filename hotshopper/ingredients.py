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
        self.amount_piece = piece(0)
        self.amount = gram(0)
        self.unit = unit
        if unit not in (piece, gram, kilogram):
            raise UnsupportedUnitError("This unit is not supported")
        if unit == piece:
            self.amount_piece = unit(amount)
        else:
            self.amount = unit(amount)


class AgaveSyrup(Ingredient):
    name = "Agavendicksaft"
    where = SUPERMARKET


class Ajvar(Ingredient):
    name = "Ajvar"
    where = SUPERMARKET


class ApplePuree(Ingredient):
    name = "Apfelmus"
    where = SUPERMARKET


class Asparagus(Ingredient):
    name = "Spargel"
    where = SUPERMARKET


class Avocado(Ingredient):
    name = "Avocado"
    where = MARKET


class Baguette(Ingredient):
    name = "Baguette"
    where = MARKET


class BakingPowder(Ingredient):
    name = "Backpulver"
    where = SUPERMARKET


class BarbecueMeat(Ingredient):
    name = "Grillfleisch (selbst aussuchen)"
    where = MARKET


class BasilFrozen(Ingredient):
    name = "TK-Basilikum"
    where = SUPERMARKET


class BeefCuts(Ingredient):
    name = "Rindergeschnetzeltes"
    where = MARKET


class BroccoliFrozen(Ingredient):
    name = "TK-Brokkoli"
    where = SUPERMARKET


class Buckwheat(Ingredient):
    name = "Buchweizen"
    where = SUPERMARKET


class Cabanossi(Ingredient):
    name = "Cabanossi"
    where = MARKET


class CaneSugar(Ingredient):
    name = "Rohrzucker"
    where = SUPERMARKET


class Caraway(Ingredient):
    name = "Kümmel"
    where = SUPERMARKET


class CardamomMilled(Ingredient):
    name = "gem. Kardamom"
    where = SUPERMARKET


class Carrot(Ingredient):
    name = "Karotten"
    where = MARKET


class CauliflowerFrozen(Ingredient):
    name = "TK-Blumenkohl"
    where = SUPERMARKET


class CauliflowerWithCreamFrozen(Ingredient):
    name = "TK-Rahmblumenkohl"
    where = SUPERMARKET


class Champignon(Ingredient):
    name = "Champignon(s)"
    where = MARKET


class ChickenCuts(Ingredient):
    name = "Hähnchengeschnetzeltes"
    where = MARKET


class Chicory(Ingredient):
    name = "Chicorée"
    where = MARKET


class CeleryRoot(Ingredient):
    name = "Knollensellerie"
    where = MARKET


class CheeseSlices(Ingredient):
    name = "Schablettenkäse"
    where = SUPERMARKET


class CherryTomato(Ingredient):
    name = "Kirschtomaten"
    where = MARKET


class ChiliPepper(Ingredient):
    name = "Chilischote(n)"
    where = MARKET


class Cream(Ingredient):
    name = "Sahne"
    where = SUPERMARKET


class CreamCheese(Ingredient):
    name = "Frischkäse"
    where = SUPERMARKET


class CremeFraiche(Ingredient):
    name = "Crème Fraîche"
    where = SUPERMARKET


class CroquettesFrozen(Ingredient):
    name = "TK-Kroketten"
    where = SUPERMARKET


class CoconutMilk(Ingredient):
    name = "Kokosmilch"
    where = SUPERMARKET


class Cucumber(Ingredient):
    name = "Salatgurke"
    where = MARKET


class DillFrozen(Ingredient):
    name = "TK-Dill"
    where = SUPERMARKET


class EightHerbsFrozen(Ingredient):
    name = "TK-8-Kräuter"
    where = SUPERMARKET


class Egg(Ingredient):
    name = "Ei(er)"
    where = SUPERMARKET


class FetaCheese(Ingredient):
    name = "Fetakäse"
    where = SUPERMARKET


class Fishsticks(Ingredient):
    name = "Fischstäbchen"
    where = SUPERMARKET


class FriesFrozen(Ingredient):
    name = "Pommes frittes"
    where = SUPERMARKET


class Garlic(Ingredient):
    name = "Knoblauch"
    where = MARKET


class Ginger(Ingredient):
    name = "Ingwer"
    where = MARKET


class GlassNoodles(Ingredient):
    name = "Glasnudeln"
    where = SUPERMARKET


class Gnocchi(Ingredient):
    name = "Gnocchi"
    where = SUPERMARKET


class Gorgonzola(Ingredient):
    name = "Gorgonzola"
    where = SUPERMARKET


class GoudaSlices(Ingredient):
    name = "Gouda (in Scheiben)"
    where = SUPERMARKET


class GratinCheese(Ingredient):
    name = "Gratinkäse"
    where = SUPERMARKET


class GreenCurryPaste(Ingredient):
    name = "Grüne Currypaste"
    where = SUPERMARKET


class GroundMeat(Ingredient):
    name = "Hackfleisch (gem.)"
    where = MARKET


class HamCooked(Ingredient):
    name = "Kochschinken"
    where = SUPERMARKET


class HamCubes(Ingredient):
    name = "Schinkenwürfel"
    where = SUPERMARKET


class HamSlices(Ingredient):
    name = "Schinken (Scheibe)"
    where = MARKET


class HazelnutFlakes(Ingredient):
    name = "Haselnussblättchen"
    where = SUPERMARKET


class HazelnutMilled(Ingredient):
    name = "gem. Haselnüsse"
    where = SUPERMARKET


class HokkaidoPumpkin(Ingredient):
    name = "Hokkaido-Kürbis"
    where = SUPERMARKET


class Leek(Ingredient):
    name = "Lauch"
    where = MARKET


class Lemon(Ingredient):
    name = "Zitrone"
    where = MARKET


class Lettuce(Ingredient):
    name = "Kopfsalat"
    where = MARKET


class Lime(Ingredient):
    name = "Limette(n)"
    where = SUPERMARKET


class MacadamiaNut(Ingredient):
    name = "Makademia-Nüsse"
    where = SUPERMARKET


class Macaroni(Ingredient):
    name = "Makkaroni (kurz)"
    where = SUPERMARKET


class MaggiFixLasagna(Ingredient):
    name = "MaggiFix für Lasagne"
    where = SUPERMARKET


class MaggiFixPepperCreamSchnitzel(Ingredient):
    name = "MaggiFix für Paprikarahmschnitzel"
    where = SUPERMARKET


class Mascarpone(Ingredient):
    name = "Mascarpone"
    where = SUPERMARKET


class Maultaschen(Ingredient):
    name = "Maultaschen"
    where = SUPERMARKET


class Milk(Ingredient):
    name = "Milch"
    where = SUPERMARKET


class MungbeanSproute(Ingredient):
    name = "Mungobohnensprossen"
    where = SUPERMARKET


class NoodlesSpiral(Ingredient):
    name = "Fussili-Nudeln"
    where = SUPERMARKET


class Onion(Ingredient):
    name = "Zwiebel(n)"
    where = SUPERMARKET


class OnionRed(Ingredient):
    name = "Rote Zwiebel(n)"
    where = MARKET


class Orange(Ingredient):
    name = "Orange(n)"
    where = MARKET


class ParmesanCheese(Ingredient):
    name = "Parmesankäse"
    where = SUPERMARKET


class ParsleyFrozen(Ingredient):
    name = "TK-Petersilie"
    where = SUPERMARKET


class ParsleyRoot(Ingredient):
    name = "Petersilienwurzel"
    where = MARKET


class PeasAndCarrotsFrozen(Ingredient):
    name = "TK-Erbsen+Möhren"
    where = SUPERMARKET


class PeasFrozen(Ingredient):
    name = "TK-Erbsen"
    where = SUPERMARKET


class PepperGreen(Ingredient):
    name = "Grüne Paprika(s)"
    where = MARKET


class PepperRed(Ingredient):
    name = "Rote Paprika(s)"
    where = MARKET


class PepperRoasted(Ingredient):
    name = "ger. Paprika (Glas)"
    where = SUPERMARKET


class PestoGenovese(Ingredient):
    name = "Pesto Genovese"
    where = SUPERMARKET


class PepperYellow(Ingredient):
    name = "Gelbe Paprika(s)"
    where = MARKET


class Pickles(Ingredient):
    name = "Saure Gurken"
    where = SUPERMARKET


class PineapplesSlicesPickled(Ingredient):
    name = "Ananasscheiben (in Dose)"
    where = SUPERMARKET


class Pistachios(Ingredient):
    name = "Pistazien"
    where = SUPERMARKET


class PitaBread(Ingredient):
    name = "Pitabrot (Pack)"
    where = SUPERMARKET


class PorkCuts(Ingredient):
    name = "Schweinegschnetzeltes"
    where = MARKET


class PotatoePancankesFrozen(Ingredient):
    name = "TK-Kartoffelpuffer"
    where = SUPERMARKET


class RicePudding(Ingredient):
    name = "Milchreis"
    where = SUPERMARKET


class RiceBasmati(Ingredient):
    name = "Basmatireis"
    where = SUPERMARKET


class SaladSauce(Ingredient):
    name = "Salatsauce"
    where = SUPERMARKET


class Salami(Ingredient):
    name = "Salami-Pack"
    where = SUPERMARKET


class SandwichCheese(Ingredient):
    name = "Schablettenkäse"
    where = SUPERMARKET


class SausageStripes(Ingredient):
    name = "Streifen f. Wurstsalat"
    where = SUPERMARKET


class Schupfnudeln(Ingredient):
    name = "Schupfnudeln"
    where = SUPERMARKET


class Smetana(Ingredient):
    name = "Schmand"
    where = SUPERMARKET


class SourCream(Ingredient):
    name = "Sauerrahm (pur)"
    where = SUPERMARKET


class Sourcrout(Ingredient):
    name = "Sauerkraut"
    where = SUPERMARKET


class SoySauce(Ingredient):
    name = "Sojasauce (hell)"
    where = SUPERMARKET


class SpaetzleCheese(Ingredient):
    name = "Spätzlekäse"
    where = SUPERMARKET


class SpaetzleNoodles(Ingredient):
    name = "Spätzle"
    where = SUPERMARKET


class SpaghettiNoodles(Ingredient):
    name = "Spaghetti"
    where = SUPERMARKET


class SpinachCreamed(Ingredient):
    name = "Rahmspinat"
    where = SUPERMARKET


class Sprout(Ingredient):
    name = "Rosenkohl"
    where = SUPERMARKET


class SugarSnap(Ingredient):
    name = "Zuckerschoten"
    where = MARKET


class Swede(Ingredient):
    name = "Steckrübe"
    where = MARKET


class Tagliatelle(Ingredient):
    name = "Bandnudeln"
    where = SUPERMARKET


class ToastbreadSandwich(Ingredient):
    name = "Toastbrot (Sandwich)"
    where = SUPERMARKET


class ToastbreadWheatSlice(Ingredient):
    name = "Toastbrot (Scheiben)"
    where = SUPERMARKET


class ToastbreadWholemeal(Ingredient):
    name = "Toastbrot (Vollkorn)"
    where = SUPERMARKET


class Tomato(Ingredient):
    name = "Tomate(n)"
    where = MARKET


class TomatoPaste(Ingredient):
    name = "Tomatenmark"
    where = SUPERMARKET


class TomatoPickled(Ingredient):
    name = "Dosentomaten (ganz)"
    where = SUPERMARKET


class TomatoSauce(Ingredient):
    name = "Dosentomaten (stückig/passiert)"
    where = SUPERMARKET


class TortelliniDried(Ingredient):
    name = "Tortellini (getrocknet)"
    where = SUPERMARKET


class Tortilla(Ingredient):
    name = "Tortillafladen"
    where = SUPERMARKET


class TurkeySchnitzel(Ingredient):
    name = "Putenschnitzel"
    where = MARKET


class Tzatziki(Ingredient):
    name = "Tzatziki"
    where = SUPERMARKET


class WheatFlour(Ingredient):
    name = "Weizenmehl"
    where = SUPERMARKET


class Wiener(Ingredient):
    name = "Saitenwürste"
    where = MARKET


class VanillaSugar(Ingredient):
    name = "Vanillezucker"
    where = SUPERMARKET


class VegetablesFrozen(Ingredient):
    name = "TK-Gemüse"
    where = SUPERMARKET


class Zucchini(Ingredient):
    name = "Zucchini(s)"
    where = MARKET


class _Potato(Ingredient):
    where = MARKET
    pass


class LowStarchPotatoe(_Potato):
    name = "Kartoffeln festk."


class StarchyPotato(_Potato):
    name = "Kartoffeln mehlig"


class PrimarilyWaxyPotato(_Potato):
    name = "Kartoffeln vorw. festk."
