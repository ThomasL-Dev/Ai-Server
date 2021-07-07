from binaries.obj.AiObject import AiObject
# ========================================== FIN DES IMPORTS ========================================================= #


class AccountObject(AiObject):

    def __init__(self, kernel, name: str, password: str, perm: str="", active: str="true"):
        AiObject.__init__(self, kernel)
        # init vars
        self._name = name
        self._password = password
        self._perm = perm
        self._active = active



    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'name={self._name!r}, '
                f'password={self._password!r}, '
                f'perm={self._perm!r}, '
                f'actif={self._active!r}'
                f')')



    def get_name(self) -> str:
        return self._name

    def get_password(self) -> str:
        return self._password

    def get_perm(self) -> str:
        return self._perm

    def is_active(self) -> bool:
        if self._active.lower() == "true":
            return True
        else:
            return False


    def set_name(self, s: str) -> None:
        self._name = s

    def set_password(self, s: str) -> None:
        self._password = s

    def set_perm(self, s: str) -> None:
        self._perm = s

    def set_active(self, s: str) -> None:
        self._active = s