from hotshopper.ingredients import (AgaveSyrup, Ajvar, ApplePuree, Asparagus,
                                    Avocado, Baguette, BakedFishFrozen,
                                    BakingPowder, Banana,
                                    BarbecueMeat, BasilFrozen, BeefCuts,
                                    BroccoliFrozen, Buckwheat, Butter,
                                    Cabanossi,
                                    CaneSugar, Caraway, CardamomMilled, Carrot,
                                    CauliflowerFrozen,
                                    CauliflowerWithCreamFrozen, CeleryRoot,
                                    Champignon, CheeseSlices, CherryTomato,
                                    ChickenCuts, Chicory, ChiliPepper,
                                    CoconutMilk, Cream, CreamCheese,
                                    CremeFraiche, CroquettesFrozen, Cucumber,
                                    DillFrozen, Egg, EightHerbsFrozen,
                                    FetaCheese, Fishsticks, FriesFrozen,
                                    Garlic, Ginger, GlassNoodles, Gnocchi,
                                    Gorgonzola, GoudaSlices, GratinCheese,
                                    GreenCurryPaste, GroundMeat, HamCooked,
                                    HamCubes, HamSlices, HazelnutFlakes,
                                    HazelnutMilled, HokkaidoPumpkin,
                                    Leek, Lemon, Lettuce, Lime,
                                    LowStarchPotatoe, MacadamiaNut,
                                    Macaroni, MaggiFixLasagna,
                                    MaggiFixPepperCreamSchnitzel,
                                    Mascarpone, Maultaschen, Milk,
                                    MungbeanSproute, NoodlesSpiral, Onion,
                                    OnionRed, Orange, ParmesanCheese,
                                    ParsleyFrozen, ParsleyRoot,
                                    PeasAndCarrotsFrozen, PeasFrozen,
                                    PepperGreen, PepperRed, PepperRoasted,
                                    PepperYellow, PestoGenovese, Pickles,
                                    PineapplesSlicesPickled, Pistachios,
                                    PitaBread, PorkCuts,
                                    PotatoePancankesFrozen,
                                    PrimarilyWaxyPotato, Remoulade,
                                    RiceBasmati,
                                    RicePudding, SaladSauce, Salami,
                                    SandwichCheese, SausageStripes,
                                    Schupfnudeln, Smetana, SourCream,
                                    Sourcrout, SoySauce, SpaetzleCheese,
                                    SpaetzleNoodles, SpaghettiNoodles,
                                    SpinachCreamed, Sprout, StarchyPotato,
                                    Swede, Tagliatelle,
                                    ToastbreadSandwich, ToastbreadWheatSlice,
                                    ToastbreadWholemeal, Tomato, TomatoPaste,
                                    TomatoPickled, TomatoSauce,
                                    TortelliniDried, Tortilla, TurkeySchnitzel,
                                    Tzatziki, VanillaSugar, VegetablesFrozen,
                                    WheatFlour, Wiener, Zucchini)
from hotshopper.ingredients import piece, gram, Ingredients


class Recipe:
    def __init__(self):
        self.name = ""
        self.weeks = []
        self.ingredients = Ingredients()
        self.selected = False

    def select(self, selected: bool, week: int):
        if selected:
            self.selected = True
            self.weeks.append(week)
            print(self.name + " is selected for week " + str(week))
        else:
            self.weeks.remove(week)
            if len(self.weeks) == 0:
                self.selected = False
            print(self.name + " is deselected from week " + str(week))

    # def __contains__(self, typ):
    #     for ingredient, index in enumerate(self.ingredients):
    #         if isinstance(ingredient, typ):
    #             return index
    #     return -1


class PotatoSoup(Recipe):
    def __init__(self):
        super().__init__()
        self.name = "Kartoffelsuppe (S.77)"
        self.ingredients = Ingredients(
            Carrot(gram, 500),
            Onion(piece, 1),
            StarchyPotato(gram, 750),
            HamCubes(gram, 125),
            Leek(piece, 1),
            CremeFraiche(gram, 100),
            CardamomMilled(piece, 1),
            Wiener(piece, 2),
        )


class ParsleyRootCurry(Recipe):
    def __init__(self):
        super().__init__()
        self.name = "Petersilienwurzelcurry (S.89, Sep - Mai)"
        self.ingredients = [
            LowStarchPotatoe(gram, 750),
            ChiliPepper(piece, 1),
            Carrot(gram, 250),
            Onion(piece, 5),
            Ginger(piece, 1),
            Garlic(piece, 2),
            ParsleyRoot(gram, 600),
            Leek(piece, 1),
            CoconutMilk(piece, 1),
            Lime(piece, 1),
        ]


class SwedeStew(Recipe):
    def __init__(self):
        super().__init__()
        self.name = "Steckrübeneintopf (S.80, Okt - Jan)"
        self.ingredients = [
            Onion(piece, 1),
            Swede(gram, 500),
            StarchyPotato(gram, 400),
            Leek(piece, 1),
            Cream(piece, 1),
            SoySauce(piece, 1),
        ]


class SalsaNoodles(Recipe):
    def __init__(self):
        super().__init__()
        self.name = "Salsanudeln mit Tomatensalat (S.90)"
        self.ingredients = [
            SpaghettiNoodles(gram, 400),
            Lemon(piece, 1),
            ParsleyFrozen(piece, 1),
            DillFrozen(piece, 1),
            AgaveSyrup(piece, 1),
            HazelnutMilled(piece, 1),
            Onion(piece, 1),
            Tomato(piece, 4),
            BasilFrozen(piece, 1),
        ]


class OrientalSproutPan(Recipe):
    def __init__(self):
        super().__init__()
        self.name = "Orientalische Rosenkohlpfanne (S.92)"
        self.ingredients = [
            PrimarilyWaxyPotato(gram, 1000),
            Sprout(gram, 750),
            Carrot(gram, 150),
            Onion(piece, 1),
            Ginger(piece, 1),
            SoySauce(piece, 1),
            FetaCheese(gram, 100),
        ]


class OvenTomatoes(Recipe):
    def __init__(self):
        super().__init__()
        self.name = "Ofentomaten (S.100)"
        self.ingredients = [
            Caraway(piece, 1),
            PrimarilyWaxyPotato(gram, 1800),
            CaneSugar(piece, 1),
            Tomato(piece, 6),
        ]


class Pichelsteiner(Recipe):
    def __init__(self):
        super().__init__()
        self.name = "Pichelsteiner (S.116)"
        self.ingredients = [
            Carrot(gram, 400),
            CeleryRoot(gram, 250),
            LowStarchPotatoe(gram, 600),
            Leek(piece, 2),
            BeefCuts(gram, 300),
        ]


class ChicoryWithHam(Recipe):
    def __init__(self):
        super(ChicoryWithHam, self).__init__()
        self.name = "Chicorée mit Schinken (S.121, Okt-Apr)"
        self.ingredients = [
            Chicory(piece, 4),
            Orange(piece, 2),
            GoudaSlices(gram, 100),
            HamSlices(piece, 8),
            CreamCheese(piece, 1),
            PrimarilyWaxyPotato(gram, 1000),
        ]


class PepperSalad(Recipe):
    def __init__(self):
        super().__init__()
        self.name = "Paprikasalat (S.63 EX)"
        self.ingredients = [
            Cabanossi(gram, 250),
            PepperRed(piece, 6),
            Zucchini(piece, 2),
            Buckwheat(gram, 50),
        ]


class CoconutSoup(Recipe):
    def __init__(self):
        super().__init__()
        self.name = "Kokossuppe (S.76 EX)"
        self.ingredients = [
            Onion(piece, 1),
            Ginger(piece, 1),
            ChickenCuts(gram, 200),
            Carrot(gram, 200),
            MungbeanSproute(gram, 150),
            GreenCurryPaste(piece, 1),
            CoconutMilk(piece, 1),
            GlassNoodles(piece, 1),
            SoySauce(piece, 1),
        ]


class NoodlePanWithPumpkinAndTomatos(Recipe):
    def __init__(self):
        super().__init__()
        self.name = "Nudelpfanne mit Kürbis und Tomaten (S.82 EX, Sep-Dez)"
        self.ingredients = [
            Macaroni(gram, 400),
            Onion(piece, 1),
            HokkaidoPumpkin(gram, 600),
            PepperYellow(piece, 2),
            CherryTomato(gram, 200),
            Pistachios(gram, 50),
        ]


class LeekNoodles(Recipe):
    def __init__(self):
        super().__init__()
        self.name = "Lauchnudeln (S.85 EX)"
        self.ingredients = [
            Leek(piece, 1),
            Tagliatelle(gram, 300),
            OnionRed(piece, 2),
            Smetana(piece, 1),
            Pistachios(gram, 40),
        ]


class RicePan(Recipe):
    def __init__(self):
        super().__init__()
        self.name = "Reispfanne (S.88 EX)"
        self.ingredients = [
            RiceBasmati(gram, 280),
            ChiliPepper(piece, 2),
            Ginger(piece, 2),
            PepperRed(piece, 4),
            MungbeanSproute(piece, 1),
            SoySauce(piece, 1),
        ]


class GnocchiWithTomatoSauce(Recipe):
    def __init__(self):
        super().__init__()
        self.name = "Gnocchi mit Tomatensauce (S.94 EX)"
        self.ingredients = [
            Onion(piece, 1),
            Garlic(piece, 2),
            TomatoSauce(piece, 2),
            Gnocchi(gram, 1000),
            CherryTomato(gram, 200),
        ]


class PaprikaCreamCauliflower(Recipe):
    def __init__(self):
        super().__init__()
        self.name = "Paprika-Sahne-Blumenkohl (S.103 EX)"
        self.ingredients = [
            CauliflowerFrozen(gram, 1000),
            Onion(piece, 2),
            ParsleyFrozen(piece, 1),
            MacadamiaNut(gram, 80),
            Ajvar(gram, 100),
            Smetana(piece, 1),
            ToastbreadWholemeal(piece, 1),
        ]


class AsparagusWithSpinachCheeseSauce(Recipe):
    def __init__(self):
        super().__init__()
        self.name = "Spargel mit Spinat-Käse-Sauce (S.106 EX, April - Mai)"
        self.ingredients = [
            Asparagus(gram, 1000),
            Onion(piece, 2),
            SpinachCreamed(gram, 400),
            Gorgonzola(gram, 150),
            HazelnutFlakes(gram, 30),
        ]


class ChickenFajitas(Recipe):
    def __init__(self):
        super().__init__()
        self.name = "Hähnchen-Fajitas (S.117 EX)"
        self.ingredients = [
            ChiliPepper(piece, 2),
            Lime(piece, 2),
            Garlic(piece, 2),
            ChickenCuts(gram, 250),
            PepperGreen(piece, 3),
            OnionRed(piece, 3),
            Avocado(piece, 1),
            Tortilla(piece, 8),
        ]


class SproutBolognese(Recipe):
    def __init__(self):
        super().__init__()
        self.name = "Rosenkohlbolognese (S.126 EX)"
        self.ingredients = [
            StarchyPotato(gram, 800),
            Onion(piece, 2),
            Carrot(gram, 200),
            Sprout(gram, 600),
            GroundMeat(gram, 400),
            TomatoPaste(gram, 50),
        ]


class HotDogs(Recipe):
    def __init__(self):
        super().__init__()
        self.name = "Hot Dogs"
        self.ingredients = [
            Baguette(piece, 2),
            Wiener(piece, 8),
            Pickles(piece, 1),
            Onion(piece, 4),
        ]


class RicePuddingRecipe(Recipe):
    def __init__(self):
        super().__init__()
        self.name = "Milchreis"
        self.ingredients = [
            RicePudding(gram, 250),
            Milk(gram, 1000),
            VanillaSugar(piece, 1),
        ]


class SausageSalad(Recipe):
    def __init__(self):
        super().__init__()
        self.name = "Wurstsalat"
        self.ingredients = [
            SausageStripes(gram, 400),
            Pickles(piece, 1),
            Onion(piece, 2),
            Baguette(piece, 1),
        ]


class VeggieRice(Recipe):
    def __init__(self):
        super().__init__()
        self.name = "Reis-Gemüse-Pfanne (klassisch)"
        self.ingredients = [
            RiceBasmati(piece, 2),
            PepperRed(piece, 1),
            CreamCheese(gram, 300),
            TomatoPaste(gram, 150),
            Onion(piece, 2),
            Zucchini(piece, 1),
            PeasAndCarrotsFrozen(gram, 200),
            BroccoliFrozen(gram, 150),
        ]


class ZucchiniTomatoPan(Recipe):
    def __init__(self):
        super().__init__()
        self.name = "Tomaten-Zucchini-Pfanne"
        self.ingredients = [
            Onion(piece, 2),
            Garlic(piece, 2),
            Zucchini(piece, 3),
            PepperRoasted(piece, 1),
            TomatoPickled(piece, 2),
            Baguette(piece, 1),
        ]


class SaladAndMaultaschen(Recipe):
    def __init__(self):
        super(SaladAndMaultaschen, self).__init__()
        self.name = "Salat mit Maultaschen"
        self.ingredients = [
            Lettuce(piece, 1),
            Tomato(piece, 2),
            PepperRed(piece, 1),
            Cucumber(piece, 1),
            Onion(piece, 5),
            Ginger(piece, 1),
            Maultaschen(piece, 2),
            SaladSauce(piece, 1),
        ]


class NoodlesWithPesto(Recipe):
    def __init__(self):
        super().__init__()
        self.name = "Pestonudeln"
        self.ingredients = [
            PestoGenovese(piece, 1),
            NoodlesSpiral(gram, 500),
            Cream(piece, 1),
            Smetana(piece, 1),
            Champignon(gram, 250),
            Leek(piece, 2),
        ]


class ChiliMascarponeNoodles(Recipe):
    def __init__(self):
        super().__init__()
        self.name = "Chili-Mascarpone-Nudeln"
        self.ingredients = [
            NoodlesSpiral(gram, 400),
            Mascarpone(gram, 250),
            HamCooked(piece, 1),
            Cream(piece, 1),
        ]


class SchupfnudelnWithVegetables(Recipe):
    def __init__(self):
        super().__init__()
        self.name = "Gemüseschupfnudeln"
        self.ingredients = [Schupfnudeln(gram, 1000),
                            VegetablesFrozen(piece, 1)]


class SchupfnudelnWithSourcrout(Recipe):
    def __init__(self):
        super().__init__()
        self.name = "Schupfnudeln mit Sauerkraut"
        self.ingredients = [
            Schupfnudeln(gram, 1000),
            HamCubes(gram, 200),
            Sourcrout(piece, 1),
        ]


class GyrosPita(Recipe):
    def __init__(self):
        super().__init__()
        self.name = "Gyros-Pita"
        self.ingredients = [
            PorkCuts(gram, 250),
            Tomato(piece, 3),
            Onion(piece, 2),
            Tzatziki(piece, 1),
            PitaBread(piece, 1),
        ]


class FishSticks(Recipe):
    def __init__(self):
        super().__init__()
        self.name = "Fischstäbchen mit Kartoffelpüree & Erbsen"
        self.ingredients = [
            Fishsticks(piece, 1),
            PeasFrozen(piece, 1),
            StarchyPotato(gram, 700),
            Milk(gram, 100),
        ]


class BakedPotato(Recipe):
    def __init__(self):
        super().__init__()
        self.name = "Ofenkartoffeln"
        self.ingredients = [
            LowStarchPotatoe(gram, 1800),
            SourCream(piece, 2),
            EightHerbsFrozen(piece, 0.5),
        ]


class PotatoePancakes(Recipe):
    def __init__(self):
        super().__init__()
        self.name = "Kartoffelpuffer"
        self.ingredients = [PotatoePancankesFrozen(piece, 1),
                            ApplePuree(piece, 1)]


class SandwichMaker(Recipe):
    def __init__(self):
        super().__init__()
        self.name = "Sandwich-Maker"
        self.ingredients = [
            ToastbreadSandwich(piece, 1),
            Tomato(piece, 3),
            Salami(piece, 2),
            GoudaSlices(gram, 250),
        ]


class Lasagne(Recipe):
    def __init__(self):
        super().__init__()
        self.name = "Lasagne"
        self.ingredients = [
            MaggiFixLasagna(piece, 2),
            CremeFraiche(piece, 1),
            GroundMeat(gram, 250),
            GratinCheese(piece, 1),
        ]


class CroquettesWithVegetables(Recipe):
    def __init__(self):
        super().__init__()
        self.name = "Kroketten mit Gemüse"
        self.ingredients = [
            CroquettesFrozen(piece, 1),
            PeasFrozen(piece, 1),
            CauliflowerWithCreamFrozen(piece, 1),
        ]


class PepperCreamSchnitzel(Recipe):
    def __init__(self):
        super().__init__()
        self.name = "Paprikarahmschnitzel"
        self.ingredients = [
            MaggiFixPepperCreamSchnitzel(piece, 2),
            PepperRed(piece, 2),
            Cream(piece, 2),
            TurkeySchnitzel(piece, 2),
            FriesFrozen(piece, 1),
        ]


class Barbecue(Recipe):
    def __init__(self):
        super().__init__()
        self.name = "Grillen"
        self.ingredients = [
            Lettuce(piece, 1),
            Tomato(piece, 2),
            PepperRed(piece, 1),
            Cucumber(piece, 1),
            Onion(piece, 2),
            SaladSauce(piece, 1),
            Champignon(piece, 6),
            Zucchini(piece, 1),
            BarbecueMeat(piece, 1),
        ]


class Tortellini(Recipe):
    def __init__(self):
        super().__init__()
        self.name = "Tortellini"
        self.ingredients = [
            TortelliniDried(piece, 2),
            TomatoSauce(piece, 2),
            Onion(piece, 2),
            ParmesanCheese(piece, 1),
        ]


class Waffles(Recipe):
    def __init__(self):
        super().__init__()
        self.name = "Waffeln"
        self.ingredients = [
            WheatFlour(gram, 300),
            BakingPowder(gram, 10),
            CaneSugar(gram, 75),
            Egg(piece, 2),
            Milk(gram, 500),
            Butter(gram, 100)
        ]


class ToastHawaii(Recipe):
    def __init__(self):
        super().__init__()
        self.name = "Toast Hawaii"
        self.ingredients = [
            ToastbreadWheatSlice(piece, 10),
            SandwichCheese(piece, 10),
            PineapplesSlicesPickled(piece, 10),
            HamCooked(piece, 1),
            CheeseSlices(piece, 1)
        ]


class CheeseNoodles(Recipe):
    def __init__(self):
        super().__init__()
        self.name = "Käsespätzle"
        self.ingredients = Ingredients(
            SpaetzleNoodles(piece, 1),
            SpaetzleCheese(piece, 1),
            Onion(piece, 4),
        )


class SpaghettiWithTomatosauce(Recipe):
    def __init__(self):
        super().__init__()
        self.name = "Spaghetti (mit Tomatensauce)"
        self.ingredients = [
            SpaghettiNoodles(gram, 500),
            TomatoSauce(piece, 2),
            Onion(piece, 2),
            ParmesanCheese(piece, 1),
        ]


class SpaghettiAglioOlio(Recipe):
    def __init__(self):
        super().__init__()
        self.name = "Spaghetti Aglio Olio"
        self.ingredients = [
            SpaghettiNoodles(gram, 400),
            Garlic(piece, 5),
            Lemon(piece, 1),
        ]


class PepperStew(Recipe):
    def __init__(self):
        super().__init__()
        self.name = "Paprikapfanne"
        self.ingredients = [
            PepperRed(piece, 3),
            PepperYellow(piece, 3),
            Tomato(piece, 4),
            Onion(gram, 500),
        ]


class BakedFishAndVegetables(Recipe):
    def __init__(self):
        super().__init__()
        self.name = "Backfisch mit Kartoffeln & Erbsen"
        self.ingredients = [
            BakedFishFrozen(piece, 1),
            LowStarchPotatoe(gram, 800),
            PeasFrozen(piece, 1),
            Remoulade(piece, 1)
        ]


class Pancakes(Recipe):
    def __init__(self):
        super().__init__()
        self.name = "Pfannkuchen (2 Pers)"
        self.ingredients = [
            WheatFlour(gram, 200),
            Egg(piece, 4),
            Milk(gram, 325),
            ApplePuree(piece, 1),
            Banana(piece, 2)
        ]


class PotatoSaladAndMaultaschen(Recipe):
    def __init__(self):
        super().__init__()
        self.name = "Kartoffelsalat mit Maultaschen"
        self.ingredients = [
            LowStarchPotatoe(gram, 1200),
            Maultaschen(piece, 2),
            Onion(piece, 2)
        ]
