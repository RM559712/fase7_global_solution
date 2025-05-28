import json
import pprint
import requests
from custom.config import Config
from custom.helper import Helper

class Aws:

    def __init__(self):

        pass


    def exception(self, str_message: str = '') -> str:

        if str_message.strip() != '':
            raise Exception(f'[Aws] {str_message}')


    def __get_params_by_aws(self) -> dict:

        object_config = Config()
        return object_config.get_params_by_aws()


    def __get_params_by_services(self) -> dict:

        dict_params_aws = self.__get_params_by_aws()

        if 'services' not in dict_params_aws or type(dict_params_aws['services']) != dict or len(dict_params_aws['services']) == 0:
            self.exception('Não foi possível concluir o processo pois os parâmetros de serviços não foram definidos.')

        return dict_params_aws['services']


    def __get_params_by_sns(self) -> dict:

        dict_params_services = self.__get_params_by_services()

        if 'sns' not in dict_params_services or type(dict_params_services['sns']) != dict or len(dict_params_services['sns']) == 0:
            self.exception('Não foi possível concluir o processo pois os parâmetros do serviço "sns" não foram definidos.')

        return dict_params_services['sns']


    def __get_params_by_alert_humidity(self) -> dict:

        dict_params_sns = self.__get_params_by_sns()

        if 'alert-humidity' not in dict_params_sns or type(dict_params_sns['alert-humidity']) != dict or len(dict_params_sns['alert-humidity']) == 0:
            self.exception('Não foi possível concluir o processo pois os parâmetros do serviço "sns > alert-humidity" não foram definidos.')

        return dict_params_sns['alert-humidity']


    def __get_url_by_alert_humidity(self) -> str:

        dict_params_alert_humidity = self.__get_params_by_alert_humidity()

        if 'url' not in dict_params_alert_humidity or dict_params_alert_humidity['url'].strip() == '':
            self.exception('Não foi possível concluir o processo pois a url do serviço "sns > alert-humidity" não foi definida.')

        return dict_params_alert_humidity['url'].strip()

    

    def __execute_request(self, str_url = None, str_type: str = 'POST', dict_params_request: dict = {}) -> dict:

        if type(str_url) == type(None) or type(str_url) != str:
            self.exception('Não foi possível concluir o processo pois a url para execução do serviço não foi definida.')

        if type(str_type) == type(None) or type(str_type) != str or str_type not in ['GET', 'POST']:
            self.exception('Não foi possível concluir o processo pois o tipo de execução não foi definido.')

        if type(dict_params_request) != dict:
            self.exception('Não foi possível concluir o processo pois os parâmetros da requisição não foram definidos corretamente.')

        if str_type.strip() == 'GET':
            object_request = requests.get(str_url, json = dict_params_request)

        if str_type.strip() == 'POST':
            object_request = requests.post(str_url, json = dict_params_request)

        dict_return = object_request.json()

        if object_request.status_code not in [200]:

            str_exception = f'Não foi possível concluir o processo devido ao código de erro retornado: {object_request.status_code}.'

            str_error_request = dict_return.get('message')

            if type(str_error_request) != type(None):
                str_exception += f' Erro retornado: {str_error_request}'

            self.exception(str_exception)

        return dict_return


    """
    Método responsável por enviar mensagens a partir da ação de cadastro de medições

    Arguments:
    - str_sensor_name: Nome do sensor ( str )
    - str_location_name: Nome da localização ( str )
    - float_location_max_humidity: Umidade máxima suportada no solo da localização ( float )
    - float_measurement_value: Valor da medição ( float )
    - str_insert_date: Data de cadastro ( str )
   
    """
    def send_message_by_alert_humidity(self, str_sensor_name: str = None, str_location_name: str = None, float_location_max_humidity: float = 0.00, float_measurement_value: float = 0.00, str_insert_date: str = None)-> dict:

        dict_return = {'status': True, 'dict_data': {}}

        try:

            dict_params_request = {}

            if type(str_sensor_name) == type(None) or type(str_sensor_name) != str or str_sensor_name.strip() == '':
                self.exception('Não foi possível concluir o processo pois o nome do sensor não foi definido.')

            if type(str_location_name) == type(None) or type(str_location_name) != str or str_location_name.strip() == '':
                self.exception('Não foi possível concluir o processo pois o nome da localização não foi definida.')

            if type(float_location_max_humidity) == type(None) or type(float_location_max_humidity) != float:
                self.exception('Não foi possível concluir o processo pois o valor de umidade máxima suportada na localização não foi definido.')

            if type(float_measurement_value) == type(None) or type(float_measurement_value) != float:
                self.exception('Não foi possível concluir o processo pois o valor da medição não foi definido.')

            if type(str_insert_date) == type(None) or type(str_insert_date) != str or str_insert_date.strip() == '':
                self.exception('Não foi possível concluir o processo pois a data de cadastro não foi definida.')

            dict_params_request['str_subject'] = f'Alerta de possível instabilidade de solo'
            dict_params_request['str_message'] = f'''

                Uma medição de umidade de solo foi cadastrada a partir do sensor "{str_sensor_name}" na localização "{str_location_name}" com o valor de {float_measurement_value}% em {str_insert_date}.

                De acordo com a configuração de umidade máxima para o solo dessa localização, a medição é superior ao máximo permitido ( {float_location_max_humidity}% ), podendo ocasionar as possíveis situações:

                - Perda de coesão entre as partículas: A água em excesso age como lubrificante entre os grãos do solo, diminuindo a força de atrito que os mantém unidos. Isso enfraquece a estrutura do solo.
                - Aumento do peso do solo: A água acumulada no solo aumenta sua massa, o que pressiona camadas inferiores e pode provocar escorregamento - especialmente em terrenos inclinados.
                - Pressão intersticial (ou poro-pressão) elevada: Quando os poros do solo se enchem de água, a pressão interna cresce e empurra as partículas umas contra as outras, reduzindo a resistência ao cisalhamento (força que mantém o solo coeso).
                - Saturação e liquefação: Em casos extremos, o solo pode entrar em um estado de liquefação, comportando-se como um líquido em vez de um sólido — situação extremamente perigosa.

                Dadas as situações acima, existem riscos diretos associados à instabilidade do solo, podendo causar:

                - Deslizamentos de terra (escorregamentos): Partes da encosta cedem e se deslocam com lama, árvores e pedras.
                - Afundamentos e rachaduras: O solo pode ceder, criando buracos ou rachaduras em estruturas.
                - Comprometimento de fundações: Prédios e casas construídas sobre solo encharcado podem ter suas fundações deslocadas ou afundadas.

            '''

            str_url = f'{self.__get_url_by_alert_humidity()}'
            dict_return['dict_data'] = self.__execute_request(str_url, 'POST', dict_params_request)

        except Exception as error:

            dict_return = {'status': False, 'message': error}

        return dict_return