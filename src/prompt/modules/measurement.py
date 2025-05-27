import datetime
import os
import pprint
import sys

# > Importante: A definição abaixo referente ao diretório raiz deve ser efetuada antes das importações de arquivos do sistema.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import prompt.main as Main
import prompt.modules.sensor as ModuleSensor
import prompt.modules.location as ModuleLocation
from custom.aws import Aws
from custom.helper import Helper
from models.f7_gs_measurement import F7GsMeasurement

"""
Método responsável pela exibição do cabeçalho do módulo
"""
def show_head_module():

    print('-= Medições =-')
    print('')


"""
Método responsável por verificar se existem medições cadastradas
"""
def validate_exists_data():

    object_f7gs_measurement = F7GsMeasurement()
    bool_exists_data = object_f7gs_measurement.validate_exists_data()

    if bool_exists_data == False:
        raise Exception('Não existem medições cadastradas.')


"""
Método responsável por recarregar o módulo "Medições"
"""
def require_reload():

    input(f'\nPressione <enter> para voltar ao menu do módulo "Medições"...')
    action_main()


"""
Método responsável por retornar as opções de menu do módulo "Medições"

Return: list
"""
def get_menu_options() -> list:

    """return [
        {
            'code': 1,
            'title': 'Visualizar cadastros',
            'action': action_list
        },{
            'code': 2,
            'title': 'Cadastrar',
            'action': action_insert
        },{
            'code': 3,
            'title': 'Editar',
            'action': action_update
        },{
            'code': 4,
            'title': 'Excluir',
            'action': action_delete
        },{
            'code': 5,
            'title': 'Voltar ao menu principal',
            'action': Main.init_system
        }
    ]"""

    return [
        {
            'code': 1,
            'title': 'Visualizar cadastros',
            'action': action_list
        },{
            'code': 2,
            'title': 'Cadastrar',
            'action': action_insert
        },{
            'code': 3,
            'title': 'Voltar ao menu principal',
            'action': Main.init_system
        }
    ]


"""
Método responsável por retornar os códigos das opções de menu do módulo "Medições"

Return: list
"""
def get_menu_options_codes() -> list:

    list_return = []

    list_menu_options = get_menu_options()

    for dict_menu_option in list_menu_options:
        list_return.append(dict_menu_option['code'])

    return list_return


"""
Método responsável pela validação do parâmetro "Opção do menu" do módulo "Medições"

Return: str
"""
def validate_menu_option() -> str:

    str_return = input(f'Digite uma opção: ')

    while True:

        try:

            if str_return.strip() == '':
                raise Exception('Deve ser definida uma opção válida.')

            if Helper.is_int(str_return) == False: 
                raise Exception('A opção informada deve ser numérica.')

            if int(str_return) not in get_menu_options_codes(): 
                raise Exception('A opção informada deve representar um dos menus disponíveis.')

            break

        except Exception as error:

            print(f'{error} Tente novamente: ', end = '')
            str_return = input()

    return str_return


"""
Método responsável por solicitar a opção do sistema que deverá ser executada
"""
def require_menu_option():

    str_option = validate_menu_option()

    list_menu_options = get_menu_options()

    for dict_menu_option in list_menu_options:
        if dict_menu_option['code'] == int(str_option):
            dict_menu_option['action']()


"""
Método responsável pela formatação de visualização do ID do módulo "Medições"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_id(dict_data: dict = {}) -> str:

    str_return = 'ID: '
    str_return += f'{dict_data['MSM_ID']}' if 'MSM_ID' in dict_data and type(dict_data['MSM_ID']) != None and Helper.is_int(dict_data['MSM_ID']) == True else 'N/I'

    return str_return


"""
Método responsável pela validação do parâmetro "ID"

Return: int
"""
def validate_id() -> int:

    int_return = input(f'Informe o ID da medição: ')

    while True:

        try:

            if int_return.strip() == '':
                raise Exception('Deve ser informado um ID válido.')

            if Helper.is_int(int_return) == False: 
                raise Exception('O conteúdo informado deve ser numérico.')

            break

        except Exception as error:

            print(f'{error} Tente novamente: ', end = '')
            int_return = input()

    return int(int_return)


"""
Método responsável pela validação do parâmetro "Localização"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def validate_location_id(dict_data: dict = {}) -> int:

    bool_is_update = ('MSM_ID' in dict_data and type(dict_data['MSM_ID']) == int)

    str_label = f'Importante: Caso deseje manter a localização atual ( abaixo ), basta ignorar o preenchimento.\n{ModuleLocation.format_data_view_name(dict_data)}\n' if bool_is_update == True else ''
    str_label += f'Informe a localização: '
    int_return = input(f'{str_label}')

    while True:

        try:

            if bool_is_update == False and int_return.strip() == '':
                raise Exception('Deve ser informada uma localização válida.')

            if int_return.strip() != '' and Helper.is_int(int_return) == False: 
                raise Exception('O conteúdo informado deve ser numérico.')

            if Helper.is_int(int_return) == True:

                get_data_location_by_id(int_return)

            break

        except Exception as error:

            print(f'{error} Tente novamente: ', end = '')
            int_return = input()

    return str(int_return.strip())


"""
Método responsável pela validação do parâmetro "Sensor"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def validate_sensor_id(dict_data: dict = {}) -> int:

    bool_is_update = ('MSM_ID' in dict_data and type(dict_data['MSM_ID']) == int)

    str_label = f'Importante: Caso deseje manter o sensor atual ( abaixo ), basta ignorar o preenchimento.\n{ModuleSensor.format_data_view_name(dict_data)}\n' if bool_is_update == True else ''
    str_label += f'Informe o sensor: '
    int_return = input(f'{str_label}')

    while True:

        try:

            if bool_is_update == False and int_return.strip() == '':
                raise Exception('Deve ser informado um sensor válido.')

            if int_return.strip() != '' and Helper.is_int(int_return) == False: 
                raise Exception('O conteúdo informado deve ser numérico.')

            if Helper.is_int(int_return) == True:

                get_data_sensor_by_id(int_return)

            break

        except Exception as error:

            print(f'{error} Tente novamente: ', end = '')
            int_return = input()

    return str(int_return.strip())


"""
Método responsável pela formatação de visualização do valor do módulo "Medições"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_value(dict_data: dict = {}) -> str:

    str_return = 'Valor da medição: '
    str_return += f'{dict_data['MSM_VALUE']}' if 'MSM_VALUE' in dict_data and type(dict_data['MSM_VALUE']) != None and Helper.is_float(dict_data['MSM_VALUE']) == True else 'N/I'

    return str_return


"""
Método responsável pela validação do parâmetro "Valor da medição"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def validate_value(dict_data: dict = {}) -> float:

    bool_is_update = ('MSM_ID' in dict_data and type(dict_data['MSM_ID']) == int)

    str_label = f'Importante: Caso deseje manter o valor da medição atual ( abaixo ), basta ignorar o preenchimento.\n{format_data_view_value(dict_data)}\n' if bool_is_update == True else ''
    str_label += f'Informe o valor da medição em formato numérico ( ex.: 123, 123.45 ou 123,45 ): '
    float_return = input(f'{str_label}')

    while True:

        try:

            if bool_is_update == False and float_return.strip() == '':
                raise Exception('Deve ser informado um valor válido.')

            if ',' in float_return:
                float_return = float_return.replace(',', '.')

            if Helper.is_float(float_return) == False and Helper.is_int(float_return) == False:
                raise Exception('O conteúdo informado deve ser numérico ( ex.: 123, 123.45 ou 123,45 ).')

            break

        except Exception as error:

            print(f'{error} Tente novamente: ', end = '')
            float_return = input()

    return float(float_return)


"""
Método responsável pela formatação de visualização da data de cadastro do módulo "Medições"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_insert_date(dict_data: dict = {}) -> str:

    str_return = 'Data de cadastro: '
    str_return += f'{Helper.convert_date_to_pt_br(dict_data['MSM_INSERT_DATE'])}' if 'MSM_INSERT_DATE' in dict_data and type(dict_data['MSM_INSERT_DATE']) != None and type(dict_data['MSM_INSERT_DATE']) == datetime.datetime else 'N/I'

    return str_return


"""
Método responsável pela formatação de visualização da data de atualização do módulo "Medições"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_update_date(dict_data: dict = {}) -> str:

    str_return = 'Data de atualização: '
    str_return += f'{Helper.convert_date_to_pt_br(dict_data['MSM_UPDATE_DATE'])}' if 'MSM_UPDATE_DATE' in dict_data and type(dict_data['MSM_UPDATE_DATE']) != None and type(dict_data['MSM_UPDATE_DATE']) == datetime.datetime else 'N/I'

    return str_return


"""
Método responsável pela formatação de visualização de dados do módulo "Medições"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )
- bool_show_id: Status informando se o parâmetro "ID" deverá ser exibido ( bool )
- bool_show_insert_date: Status informando se o parâmetro "Data de cadastro" deverá ser exibido ( bool )
- bool_show_update_date Status informando se o parâmetro "Data de atualização" deverá ser exibido ( bool )

Return: str
"""
def format_data_view(dict_data: dict = {}, bool_show_id: bool = True, bool_show_insert_date: bool = True, bool_show_update_date: bool = True) -> str:

    str_return = None

    if len(dict_data) > 0:

        str_return = ''
        str_return += f'- {format_data_view_id(dict_data)} \n' if bool_show_id == True else ''
        str_return += f'- {ModuleLocation.format_data_view_name(dict_data)} \n'
        str_return += f'- {ModuleSensor.format_data_view_name(dict_data)} \n'
        str_return += f'- {format_data_view_value(dict_data)} \n'
        str_return += f'- {format_data_view_insert_date(dict_data)} \n' if bool_show_insert_date == True else ''
        str_return += f'- {format_data_view_update_date(dict_data)} \n' if bool_show_update_date == True else ''

    return str_return


"""
Método responsável pela exibição de cadastros do módulo "Medições"
"""
def action_list():

    Main.init_step()

    validate_exists_data()

    show_head_module()

    object_f7gs_measurement = F7GsMeasurement()

    object_f7gs_measurement.set_select(['MSM.*', 'LOC.LOC_NAME', 'SNS.SNS_NAME'])
    object_f7gs_measurement.set_table('F7_GS_MEASUREMENT MSM')
    object_f7gs_measurement.set_join([
        {'str_type_join': 'INNER JOIN', 'str_table': 'F7_GS_LOCATION LOC', 'str_where': 'LOC.LOC_ID = MSM.MSM_LOC_ID'},
        {'str_type_join': 'INNER JOIN', 'str_table': 'F7_GS_SENSOR SNS', 'str_where': 'SNS.SNS_ID = MSM.MSM_SNS_ID'}
    ])
    object_f7gs_measurement.set_where([F7GsMeasurement.get_params_to_active_data()])
    object_f7gs_measurement.set_order([{'str_column': 'MSM.MSM_ID', 'str_type_order': 'ASC'}])
    list_data = object_f7gs_measurement.get_data().get_list()

    for dict_data in list_data:

        print(format_data_view(dict_data))
    
    require_reload()


"""
Método responsável por executar a ação de retorno de dados de uma determinada medição
"""
def get_data_by_id(int_msm_id: int = 0) -> dict:

    object_f7gs_measurement = F7GsMeasurement()

    object_f7gs_measurement.set_select(['MSM.*', 'LOC.LOC_NAME', 'SNS.SNS_NAME'])
    object_f7gs_measurement.set_table('F7_GS_MEASUREMENT MSM')
    object_f7gs_measurement.set_join([
        {'str_type_join': 'INNER JOIN', 'str_table': 'F7_GS_LOCATION LOC', 'str_where': 'LOC.LOC_ID = MSM.MSM_LOC_ID'},
        {'str_type_join': 'INNER JOIN', 'str_table': 'F7_GS_SENSOR SNS', 'str_where': 'SNS.SNS_ID = MSM.MSM_SNS_ID'}
    ])
    object_f7gs_measurement.set_where([

        {'str_column': 'MSM.MSM_ID', 'str_type_where': '=', 'value': int_msm_id},
        F7GsMeasurement.get_params_to_active_data()

    ])

    dict_data = object_f7gs_measurement.get_data().get_one()

    if type(dict_data) == type(None):
        raise Exception(f'Nenhum registro foi localizado com o ID {int_msm_id}.')

    return object_f7gs_measurement


"""
Método responsável por executar a ação de retorno de dados de uma determinada localização
"""
def get_data_location_by_id(loc_id: int = 0) -> dict:

    object_f7gs_location = ModuleLocation.get_data_by_id(loc_id)
    dict_data = object_f7gs_location.get_one()

    return dict_data


"""
Método responsável por executar a ação de retorno de dados de um determinado sensor
"""
def get_data_sensor_by_id(sns_id: int = 0) -> dict:

    object_f7gs_sensor = ModuleSensor.get_data_by_id(sns_id)
    dict_data = object_f7gs_sensor.get_one()

    return dict_data


# ... Demais parâmetros...


"""
Método responsável pela exibição da funcionalidade de cadastro do módulo "Medições"
"""
def action_insert():

    Main.init_step()

    show_head_module()

    print('Os parâmetros abaixo fazem parte do cadastro principal da medição.')
    print('')

    int_msm_loc_id = validate_location_id()

    print('')

    int_msm_sns_id = validate_sensor_id()

    print('')

    float_msm_value = validate_value()

    Main.loading('Salvando dados, por favor aguarde...')

    # -------
    # Etapa 2
    # -------

    Main.init_step()

    show_head_module()

    dict_data = {}

    dict_data['MSM_LOC_ID'] = int_msm_loc_id
    dict_data['MSM_SNS_ID'] = int_msm_sns_id
    dict_data['MSM_VALUE'] = float_msm_value

    object_f7gs_measurement = F7GsMeasurement()
    object_f7gs_measurement.insert(dict_data)

    int_msm_id = object_f7gs_measurement.get_last_id()

    # Retorno de dados após o cadastro
    object_f7gs_measurement = get_data_by_id(int_msm_id)
    dict_data = object_f7gs_measurement.get_one()

    print(format_data_view(dict_data = dict_data, bool_show_id = False, bool_show_insert_date = False, bool_show_update_date = False))

    print('Registro cadastrado com sucesso.')

    # <PENDENTE>
    # Análise do valor armazenado VERSUS o valor máximo configurado na localização

    require_reload()


"""
Método responsável pela exibição da funcionalidade de atualização do módulo "Medições"
"""
def action_update():

    Main.init_step()

    show_head_module()

    validate_exists_data()

    int_msm_id = validate_id()

    # -------
    # Etapa 2
    # -------

    Main.loading('Verificando dados, por favor aguarde...')

    Main.init_step()

    show_head_module()

    object_f7gs_measurement = get_data_by_id(int_msm_id)
    dict_data = object_f7gs_measurement.get_one()

    print('Os dados abaixo representam o cadastro atual do registro informado.')
    print('')

    print(format_data_view(dict_data))

    input(f'Pressione <enter> para continuar...')

    # -------
    # Etapa 3
    # -------

    Main.init_step()

    show_head_module()

    print('Os parâmetros abaixo fazem parte do cadastro principal da medição.')
    print('')

    int_msm_loc_id = validate_location_id(dict_data)

    print('')

    int_msm_sns_id = validate_sensor_id(dict_data)

    print('')

    float_msm_value = validate_value(dict_data)

    Main.loading('Salvando dados, por favor aguarde...')

    # -------
    # Etapa 4
    # -------

    Main.init_step()

    show_head_module()

    dict_data['MSM_LOC_ID'] = int_msm_loc_id
    dict_data['MSM_SNS_ID'] = int_msm_sns_id
    dict_data['MSM_VALUE'] = float_msm_value

    object_f7gs_measurement.update(dict_data)

    # Retorno de dados após as atualizações
    object_f7gs_measurement = get_data_by_id(int_msm_id)
    dict_data = object_f7gs_measurement.get_one()

    print(format_data_view(dict_data = dict_data, bool_show_update_date = False))

    print('Registro atualizado com sucesso.')
    
    require_reload()


"""
Método responsável pela exibição da funcionalidade de exclusão do módulo "Medições"
"""
def action_delete():

    Main.init_step()

    show_head_module()

    validate_exists_data()

    int_msm_id = validate_id()

    # -------
    # Etapa 2
    # -------

    Main.loading('Verificando dados, por favor aguarde...')

    Main.init_step()

    show_head_module()

    object_f7gs_measurement = get_data_by_id(int_msm_id)
    dict_data = object_f7gs_measurement.get_one()

    dict_data['MSM_STATUS'] = F7GsMeasurement.STATUS_DELETED

    object_f7gs_measurement.update(dict_data)

    print('Registro excluído com sucesso.')

    require_reload()


"""
Método responsável pela exibição padrão do módulo "Medições"
"""
def action_main():

    try:

        Main.init_step()

        Main.test_connection_by_database()

        show_head_module()

        list_menu_options = get_menu_options()

        for dict_menu_option in list_menu_options:
            print(f'{dict_menu_option['code']}. {dict_menu_option['title']}')

        print('')

        require_menu_option()

    except Exception as error:

        print(f'> Ocorreu o seguinte erro: {error}')
        require_reload()