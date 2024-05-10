
class Helper:
    """
    A helper class to feature various helper functions.
    """

    @staticmethod
    def bool_string_to_int(bool_str: str) -> int:
        """
        Returns integer representation of a boolean string.

        :param bool_str: Must be 'false' or 'true'.
        :return: Integer representation of bool_str.
        """
        if bool_str.lower() == "true":
            return 1
        elif bool_str.lower() == "false":
            return 0
        else:
            var_name = f'{bool_str=}'.split('=')[0]
            raise ValueError(f"'{var_name}' has illegal value: ${bool_str}")
