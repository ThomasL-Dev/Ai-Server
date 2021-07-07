import requests
# ========================================== FIN DES IMPORTS ========================================================= #



class ComputerController:

    def __init__(self, ip: str=None):

        self.ip = ip

    def popup(self, string: str):
        self.do_request_with_param("popup", string)


    def do_simple_request(self, endpoint: str):
        if self.ip is not None:
            requests.get(f'http://{self.ip}:8080/{endpoint}')
        else:
            raise Exception('No ip where to do request')


    def do_request_with_param(self, endpoint: str, param: str):
        if self.ip is not None:
            requests.get(f'http://{self.ip}:8080/{endpoint}?param={param}')
        else:
            raise Exception('No ip where to do request')

