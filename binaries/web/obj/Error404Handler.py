import tornado.web
# ========================================== FIN DES IMPORTS ========================================================= #


class Error404Handler(tornado.web.RequestHandler):
    # Override prepare() instead of get() to cover all possible HTTP methods.

    def prepare(self):
        self.set_status(404)
        self.redirect("/")
