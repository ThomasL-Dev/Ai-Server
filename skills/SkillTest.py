from binaries.obj.SkillObject import SkillObject
# ========================================== FIN DES IMPORTS ========================================================= #






class SkillTest(SkillObject):

    cmd = "test"

    utterance = ["fait un test"]

    reponse = "test skill executé"


    def on_execute(self):
        self.test()

    def test(self):
        pass
