import requests
import os
from dotenv import load_dotenv
from typing import List, Optional

load_dotenv()


class APISPTRANS:
    def __init__(self):
        self.__CHAVE = os.environ['CHAVE_API']
        self.__URL = os.environ['URL_API_SPTRANS']

    def __realizar_login(self) -> Optional[str]:
        """realiza o login na apo

        Returns:
            Optional[str]: retorna cookie ou nada
        """
        URL_COMPLETA = f'{self.__URL}Login/Autenticar?token={self.__CHAVE}'
        req = requests.request('POST', URL_COMPLETA, )
        cookies = req.cookies
        cookie = cookies.get('apiCredentials', '')
        return cookie

    def buscar_linhas(self) -> List:
        """busca todas as linhas

        Returns:
            Dict: Retorna a Linha
        """
        cookie = self.__realizar_login()
        URL_COMPLETA = f'{self.__URL}Posicao'
        headers = {
            'Cookie': f'apiCredentials={cookie}'
        }

        req = requests.get(url=URL_COMPLETA, headers=headers)
        return req.json()['l']
