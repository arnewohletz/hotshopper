
class DuplicateIndexError(Exception):
    def __init__(self, *args, **kwargs):
        pass


class DuplicateIngredientError(Exception):
    def __init__(self, *args, **kwargs):
        pass


class DuplicateRecipeError(Exception):
    def __init__(self, *args, **kwargs):
        pass


class DuplicateRecipeIngredientError(Exception):
    def __init__(self, *args, **kwargs):
        pass


class RecipeIngredientNotFoundError(Exception):
    def __init__(self, *args, **kwargs):
        pass


class UnsupportedUnitError(Exception):
    def __init__(self, *args, **kwargs):
        pass
