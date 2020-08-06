from abc import ABC
from units import unit, scaled_unit
from hotshopper.errors import UnsupportedUnitError

piece = unit("St.")
gram = unit("g")
kilogram = scaled_unit("kg", "gram", 1000)


class Ingredient(ABC):
    name = ""

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


class Ajvar(Ingredient):
    name = "Ajvar"


class ApplePuree(Ingredient):
    name = "Apfelmus"


class Asparagus(Ingredient):
    name = "Spargel"


class Avocado(Ingredient):
    name = "Avocado"


class Baguette(Ingredient):
    name = "Baguette"


class BakingPowder(Ingredient):
    name = "Backpulver"


class BarbecueMeat(Ingredient):
    name = "Grillfleisch (selbst aussuchen)"


class BasilFrozen(Ingredient):
    name = "TK-Basilikum"


class BeefCuts(Ingredient):
    name = "Rindergeschnetzeltes"


class BroccoliFrozen(Ingredient):
    name = "TK-Brokkoli"


class Buckwheat(Ingredient):
    name = "Buchweizen"


class Cabanossi(Ingredient):
    name = "Cabanossi"


class CaneSugar(Ingredient):
    name = "Rohrzucker"


class Caraway(Ingredient):
    name = "Kümmel"


class CardamomMilled(Ingredient):
    name = "gem. Kardamom"


class Carrot(Ingredient):
    name = "Karotten"


class CauliflowerFrozen(Ingredient):
    name = "TK-Blumenkohl"


class CauliflowerWithCreamFrozen(Ingredient):
    name = "TK-Rahmblumenkohl"


class Champignon(Ingredient):
    name = "Champignon(s)"


class ChickenCuts(Ingredient):
    name = "Hähnchengeschnetzeltes"


class Chicory(Ingredient):
    name = "Chicorée"


class CeleryRoot(Ingredient):
    name = "Knollensellerie"


class CheeseSlices(Ingredient):
    name = "Schablettenkäse"

class CherryTomato(Ingredient):
    name = "Kirschtomaten"


class ChiliPepper(Ingredient):
    name = "Chilischote(n)"


class Cream(Ingredient):
    name = "Sahne"


class CreamCheese(Ingredient):
    name = "Frischkäse"


class CremeFraiche(Ingredient):
    name = "Crème Fraîche"


class CroquettesFrozen(Ingredient):
    name = "TK-Kroketten"


class CoconutMilk(Ingredient):
    name = "Kokosmilch"


class Cucumber(Ingredient):
    name = "Salatgurke"


class DillFrozen(Ingredient):
    name = "TK-Dill"


class EightHerbsFrozen(Ingredient):
    name = "TK-8-Kräuter"


class Egg(Ingredient):
    name = "Ei(er)"


class FetaCheese(Ingredient):
    name = "Fetakäse"


class Fishsticks(Ingredient):
    name = "Fischstäbchen"


class FriesFrozen(Ingredient):
    name = "Pommes frittes"


class Garlic(Ingredient):
    name = "Knoblauch"


class Ginger(Ingredient):
    name = "Ingwer"


class GlassNoodles(Ingredient):
    name = "Glasnudeln"


class Gnocchi(Ingredient):
    name = "Gnocchi"


class Gorgonzola(Ingredient):
    name = "Gorgonzola"


class GoudaSlices(Ingredient):
    name = "Gouda (in Scheiben)"


class GratinCheese(Ingredient):
    name = "Gratinkäse"


class GreenCurryPaste(Ingredient):
    name = "Grüne Currypaste"


class GroundMeat(Ingredient):
    name = "Hackfleisch (gem.)"


class HamCooked(Ingredient):
    name = "Kochschinken"


class HamCubes(Ingredient):
    name = "Schinkenwürfel"


class HamSlices(Ingredient):
    name = "Schinken (Scheibe)"


class HazelnutFlakes(Ingredient):
    name = "Haselnussblättchen"


class HazelnutMilled(Ingredient):
    name = "gem. Haselnüsse"


class HokkaidoPumpkin(Ingredient):
    name = "Hokkaido-Kürbis"


class Leek(Ingredient):
    name = "Lauch"


class Lemon(Ingredient):
    name = "Zitrone"


class Lettuce(Ingredient):
    name = "Kopfsalat"


class Lime(Ingredient):
    name = "Limette(n)"


class MacadamiaNut(Ingredient):
    name = "Makademia-Nüsse"


class Macaroni(Ingredient):
    name = "Makkaroni (kurz)"


class MaggiFixLasagna(Ingredient):
    name = "MaggiFix für Lasagne"


class MaggiFixPepperCreamSchnitzel(Ingredient):
    name = "MaggiFix für Paprikarahmschnitzel"


class Mascarpone(Ingredient):
    name = "Mascarpone"


class Maultaschen(Ingredient):
    name = "Maultaschen"


class Milk(Ingredient):
    name = "Milch"


class MungbeanSproute(Ingredient):
    name = "Mungobohnensprossen"


class NoodlesSpiral(Ingredient):
    name = "Fussili-Nudeln"


class Onion(Ingredient):
    name = "Zwiebel(n)"


class OnionRed(Ingredient):
    name = "Rote Zwiebel(n)"


class Orange(Ingredient):
    name = "Orange(n)"


class ParmesanCheese(Ingredient):
    name = "Parmesankäse"


class ParsleyFrozen(Ingredient):
    name = "TK-Petersilie"


class ParsleyRoot(Ingredient):
    name = "Petersilienwurzel"


class PeasAndCarrotsFrozen(Ingredient):
    name = "TK-Erbsen+Möhren"


class PeasFrozen(Ingredient):
    name = "TK-Erbsen"


class PepperGreen(Ingredient):
    name = "Grüne Paprika(s)"


class PepperRed(Ingredient):
    name = "Rote Paprika(s)"


class PepperRoasted(Ingredient):
    name = "ger. Paprika (Glas)"


class PestoGenovese(Ingredient):
    name = "Pesto Genovese"


class PepperYellow(Ingredient):
    name = "Gelbe Paprika(s)"


class Pickles(Ingredient):
    name = "Saure Gurken"


class PineapplesSlicesPickled(Ingredient):
    name = "Ananasscheiben (in Dose)"


class Pistachios(Ingredient):
    name = "Pistazien"


class PitaBread(Ingredient):
    name = "Pitabrot (Pack)"


class PorkCuts(Ingredient):
    name = "Schweinegschnetzeltes"


class PotatoePancankesFrozen(Ingredient):
    name = "TK-Kartoffelpuffer"


class RicePudding(Ingredient):
    name = "Milchreis"


class RiceBasmati(Ingredient):
    name = "Basmatireis"


class SaladSauce(Ingredient):
    name = "Salatsauce"


class Salami(Ingredient):
    name = "Salami-Pack"


class SandwichCheese(Ingredient):
    name = "Schablettenkäse"


class SausageStripes(Ingredient):
    name = "Streifen f. Wurstsalat"


class Schupfnudeln(Ingredient):
    name = "Schupfnudeln"


class Smetana(Ingredient):
    name = "Schmand"


class SourCream(Ingredient):
    name = "Sauerrahm (pur)"


class Sourcrout(Ingredient):
    name = "Sauerkraut"


class SoySauce(Ingredient):
    name = "Sojasauce (hell)"


class SpaetzleCheese(Ingredient):
    name = "Spätzlekäse"


class SpaetzleNoodles(Ingredient):
    name = "Spätzle"


class SpaghettiNoodles(Ingredient):
    name = "Spaghetti"


class SpinachCreamed(Ingredient):
    name = "Rahmspinat"


class Sprout(Ingredient):
    name = "Rosenkohl"


class SugarSnap(Ingredient):
    name = "Zuckerschoten"


class Swede(Ingredient):
    name = "Steckrübe"


class Tagliatelle(Ingredient):
    name = "Bandnudeln"


class ToastbreadSandwich(Ingredient):
    name = "Toastbrot (Sandwich)"


class ToastbreadWheatSlice(Ingredient):
    name = "Toastbrot (Scheiben)"


class ToastbreadWholemeal(Ingredient):
    name = "Toastbrot (Vollkorn)"


class Tomato(Ingredient):
    name = "Tomate(n)"


class TomatoPaste(Ingredient):
    name = "Tomatenmark"


class TomatoPickled(Ingredient):
    name = "Dosentomaten (ganz)"


class TomatoSauce(Ingredient):
    name = "Dosentomaten (stückig/passiert)"


class TortelliniDried(Ingredient):
    name = "Tortellini (getrocknet)"


class Tortilla(Ingredient):
    name = "Tortillafladen"


class TurkeySchnitzel(Ingredient):
    name = "Putenschnitzel"


class Tzatziki(Ingredient):
    name = "Tzatziki"


class WheatFlour(Ingredient):
    name = "Weizenmehl"


class Wiener(Ingredient):
    name = "Saitenwürste"


class VanillaSugar(Ingredient):
    name = "Vanillezucker"


class VegetablesFrozen(Ingredient):
    name = "TK-Gemüse"


class Zucchini(Ingredient):
    name = "Zucchini(s)"


class _Potato(Ingredient):
    pass


class LowStarchPotatoe(_Potato):
    name = "Kartoffeln festk."


class StarchyPotato(_Potato):
    name = "Kartoffeln mehlig"


class PrimarilyWaxyPotato(_Potato):
    name = "Kartoffeln vorw. festk."
