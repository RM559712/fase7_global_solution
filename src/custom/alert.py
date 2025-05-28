from datetime import datetime
import pprint
from models.f7_gs_sensor import F7GsSensor

class Alert:

    def __init__(self):

        pass


    def exception(self, str_message: str = '') -> str:

        if str_message.strip() != '':
            raise Exception(f'[Alert] {str_message}')


    """
    Método responsável por verificar se uma determinada localização deverá ter alerta enviado a partir de validações dos parâmetros preenchidos

    Arguments:
    - dict_filters_location: Parâmetros relacionados à localização ( dict )
    - dict_measurement: Parâmetros relacionados à medição da localização ( dict )
   
    """
    def validate_alert_by_location(self, dict_params: dict = {}) -> dict:

        dict_return = {'status': True, 'dict_data': {'dict_analysis_alert': {'status': False}}}

        try:

            dict_filters_location = dict_params.get('dict_filters_location', {})
            dict_measurement = dict_params.get('dict_measurement', {})

            """
            Validação utilizando os filtros da localização

            - Regras: A partir de parâmetros específicos, será possível verificar se um alerta deverá ou não ser enviado.
            """

            # Parâmetros relacionados à medição que deverá ser utilizada na filtragem
            int_sensor_type = dict_measurement.get('int_sensor_type', None)
            float_value = dict_measurement.get('float_value', None)
            
            if type(int_sensor_type) != type(None):

                try:

                    dict_sensor = F7GsSensor.get_type_options(int_sensor_type)

                    match int_sensor_type:

                        case F7GsSensor.TYPE_HUMIDITY:

                            float_humidity_max = dict_filters_location.get('float_humidity_max', None)

                            if type(float_humidity_max) == type(None):
                                self.exception('A localização não possui um limite de umidade para o solo configurada, portanto, a validação para envio de alerta não será executada.')
                            
                            if float_value < float_humidity_max:
                                self.exception(f'De acordo com a medição informada ( {float_value}% ), não será necessário enviar um alerta pois a umidade para o solo está abaixo do limite máximo ( {float_humidity_max}% ).')
                            
                            if float_value == float_humidity_max:
                                self.exception(f'De acordo com a medição informada ( {float_value}% ), não será necessário enviar um alerta pois a umidade para o solo está no limite máximo permitido ( {float_humidity_max}% ).')

                        case _:
                            self.exception(f'Não foi possível concluir o processo pois o tipo de sensor informado ( {dict_sensor['title']} ) não atende aos requisitos para envio de alerta.')

                    # Caso todas as validações tenham sido aprovadas, significa que o alerta deverá ser enviado
                    dict_return['dict_data']['dict_analysis_alert']['status'] = True

                except Exception as error:

                    dict_return['dict_data']['dict_analysis_alert'] = {'status': False, 'message': error}

        except Exception as error:

            dict_return = {'status': False, 'message': error}

        return dict_return


