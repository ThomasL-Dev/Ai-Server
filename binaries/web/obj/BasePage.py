import tornado.web
# ========================================== FIN DES IMPORTS ========================================================= #


class BasePage(tornado.web.RequestHandler):

    need_oauth_security = False

    local_connexion_only = False

    return_json = False

    access_permission = None

    def initialize(self, kernel):
        self.kernel = kernel
        self.get_accessing_info()
        self.check_access_permission()



    def get(self):
        try:
            if self.local_connexion_only:
                if not self.local_connexion_security():
                    self.redirect("/")
                    self.kernel.console.info(str(self.request.remote_ip) + " unauthorized to access to " + str(self.full_url), color='red')

            if self.need_oauth_security:
                if not self.oauth_security_system():
                    self.redirect('/admin/login')
                    self.kernel.console.info(str(self.request.remote_ip) + " unauthorized to access to " + str(self.full_url), color='red')

            self.on_get()
        except RuntimeError:
            pass
        except Exception as e:
            self.write(str(self.full_url) + " on get error : " + str(e))

    def on_get(self):
        pass


    def post(self):
        try:
            self.on_post()
        except Exception as e:
            self.write(str(self.full_url) + " on post error : " + str(e))

    def on_post(self):
        pass



    def set_default_headers(self):
        if self.return_json:
            self.set_header("Content-Type", "application/x-json")
        else:
            self.set_header("access-control-allow-origin", "*")
            self.set_header("Access-Control-Allow-Headers", "x-requested-with")
            self.set_header('Access-Control-Allow-Methods', 'GET, PUT, DELETE, OPTIONS')
            self.set_header("Access-Control-Allow-Headers", "access-control-allow-origin,authorization,content-type")
            self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
            self.set_header('Pragma', 'no-cache')

    def options(self):
        # no body
        self.set_status(204)
        self.finish()

    def get_arg_by_name(self, arg_name: str, default_value=None):
        return self.get_argument(arg_name, default=default_value)



    def check_access_permission(self):
        # if access permission is not None
        if self.access_permission is not None:
            # get cookie
            account_connected_cookies = self.get_secure_cookie("account-connected-cookies")
            # if cookie is not None
            if account_connected_cookies is not None:
                # decode cookie if not None
                account_connected_cookies = account_connected_cookies.decode("utf8")
                # get account in handler
                is_account_have_perm = self.kernel.AccountsHandler.have_perm(account_connected_cookies, self.access_permission)
                # if account have right perm
                if is_account_have_perm:
                    # stop function and go to page
                    return
                else:
                    # else redirect to panel
                    self.redirect("/admin/panel")

    def oauth_security_system(self):
        # get cookie
        account_connected_cookies = self.get_secure_cookie("account-connected-cookies")
        # if cookie is not None
        if account_connected_cookies is not None:
            # decode cookie if not None
            account_connected_cookies = account_connected_cookies.decode("utf8")
            # get account in handler
            account_connected = self.kernel.AccountsHandler.get_account(account_connected_cookies)
            # if account is not None
            if account_connected is not None:
                # if account is in account handler
                if account_connected_cookies == account_connected.get_name():
                    # return True
                    return True
        # else return False
        return False

    def local_connexion_security(self):
        if "192.168." in str(self.request.remote_ip) or str(self.request.remote_ip) == "127.0.0.1" or str(self.request.remote_ip) == "::1":
            return True
        return False

    def get_accessing_info(self):
        self.full_url = self.request.full_url()
        self.ip_requester = str(self.request.remote_ip)
        if "/screensaver" not in self.full_url:  # pass screensaver we dont care who access to this
            self.kernel.console.info("[WebRoute] '{}' accessing to '{}'".format(self.ip_requester, self.full_url))



