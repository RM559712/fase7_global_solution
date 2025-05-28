import datetime
import os
import pprint
import sys

# > Importante: A definição abaixo referente ao diretório raiz deve ser efetuada antes das importações de arquivos do sistema.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import prompt.main as Main
from custom.helper import Helper
from models.f7_gs_location import F7GsLocation
from models.f7_gs_location_config import F7GsLocationConfig

"""
Método responsável pela exibição do cabeçalho do módulo
"""
def show_head_module():

    print('-= Localização =-')
    print('')

"""
Método responsável por verificar se existem localizações cadastradas
"""
def validate_exists_data():

    object_f7gs_location = F7GsLocation()
    bool_exists_data = object_f7gs_location.validate_exists_data()

    if bool_exists_data == False:
        raise Exception('Não existem localizações cadastradas.')


"""
Método responsável por recarregar o módulo "Localização"
"""
def require_reload():

    input(f'\nPressione <enter> para voltar ao menu do módulo "Localização"...')
    action_main()


"""
Método responsável por retornar as opções de menu do módulo "Localização"

Return: list
"""
def get_menu_options() -> list:

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
    ]


"""
Método responsável por retornar os códigos das opções de menu do módulo "Localização"

Return: list
"""
def get_menu_options_codes() -> list:

    list_return = []

    list_menu_options = get_menu_options()

    for dict_menu_option in list_menu_options:
        list_return.append(dict_menu_option['code'])

    return list_return


"""
Método responsável pela validação do parâmetro "Opção do menu" do módulo "Localização"

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
Método responsável pela formatação de visualização do ID do módulo "Localização"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_id(dict_data: dict = {}) -> str:

    str_return = 'ID: '
    str_return += f'{dict_data['LOC_ID']}' if 'LOC_ID' in dict_data and type(dict_data['LOC_ID']) != None and Helper.is_int(dict_data['LOC_ID']) == True else 'N/I'

    return str_return


"""
Método responsável pela validação do parâmetro "ID"

Return: int
"""
def validate_id() -> int:

    int_return = input(f'Informe o ID da localização: ')

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
Método responsável pela formatação de visualização do nome do módulo "Localização"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_name(dict_data: dict = {}) -> str:

    str_return = 'Nome da localização: '
    str_return += f'{dict_data['LOC_NAME'].strip()}' if 'LOC_NAME' in dict_data and type(dict_data['LOC_NAME']) != None and type(dict_data['LOC_NAME']) == str else 'N/I'

    return str_return


"""
Método responsável pela validação do parâmetro "Nome"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def validate_name(dict_data: dict = {}) -> str:

    bool_is_update = ('LOC_ID' in dict_data and type(dict_data['LOC_ID']) == int)

    str_label = f'Importante: Caso deseje manter o nome atual ( abaixo ), basta ignorar o preenchimento.\n{format_data_view_name(dict_data)}\n' if bool_is_update == True else ''
    str_label += f'Informe o nome da localização: '
    str_return = input(f'{str_label}')

    object_f7gs_location = F7GsLocation()

    while True:

        try:

            if bool_is_update == False and str_return.strip() == '':
                raise Exception('Deve ser informado um nome válido.')

            if bool_is_update == False and type(str_return) != str: 
                raise Exception('O conteúdo informado deve ser texto.')

            if str_return.strip() != '':

                list_params_validate = [

                    {'str_column': 'LOWER(LOC_NAME)', 'str_type_where': '=', 'value': str_return.lower().strip()},
                    F7GsLocation.get_params_to_active_data()

                ]

                if bool_is_update == True:

                    list_params_validate.append({'str_column': 'LOC_ID', 'str_type_where': '!=', 'value': dict_data['LOC_ID']})

                dict_location = object_f7gs_location.set_where(list_params_validate).get_one()

                if type(dict_location) == dict:
                    raise Exception(f'Já existe um registro cadastrado com o nome "{str_return.strip()}".')

            break

        except Exception as error:

            print(f'{error} Tente novamente: ', end = '')
            str_return = input()

    return str(str_return.strip())


"""
Método responsável pela formatação de visualização da latitude do módulo "Localizações"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_latitude(dict_data: dict = {}) -> str:

    str_return = 'Latitude: '
    str_return += f'{dict_data['LCO_LATITUDE']}' if 'LCO_LATITUDE' in dict_data and type(dict_data['LCO_LATITUDE']) != None and Helper.is_float(dict_data['LCO_LATITUDE']) == True else 'N/I'

    return str_return


"""
Método responsável pela validação do parâmetro "Latitude"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def validate_latitude(dict_data: dict = {}) -> float:

    bool_is_update = ('LOC_ID' in dict_data and type(dict_data['LOC_ID']) == int)

    str_label = f'Importante: Caso deseje manter a latitude atual ( abaixo ), basta ignorar o preenchimento. Caso queira apagar o valor, digite "none".\n{format_data_view_latitude(dict_data)}\n' if bool_is_update == True else ''
    str_label += f'Informe a latitude da localização em formato numérico ( ex.: 123, 123.45 ou 123,45 ): '
    float_return = input(f'{str_label}')

    while True:

        try:

            if float_return.strip() != '' and float_return.strip().lower() != 'none':

                if ',' in float_return:
                    float_return = float_return.replace(',', '.')

                if Helper.is_float(float_return) == False and Helper.is_int(float_return) == False:
                    raise Exception('O conteúdo informado deve ser numérico ( ex.: 123, 123.45 ou 123,45 ).')

            break

        except Exception as error:

            print(f'{error} Tente novamente: ', end = '')
            float_return = input()

    float_value = None
    if float_return.strip() != '':
        float_value = float(float_return) if float_return.strip().lower() != 'none' else ''

    return float_value


"""
Método responsável pela formatação de visualização da longitude do módulo "Plantações"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_longitude(dict_data: dict = {}) -> str:

    str_return = 'Longitude: '
    str_return += f'{dict_data['LCO_LONGITUDE']}' if 'LCO_LONGITUDE' in dict_data and type(dict_data['LCO_LONGITUDE']) != None and Helper.is_float(dict_data['LCO_LONGITUDE']) == True else 'N/I'

    return str_return


"""
Método responsável pela validação do parâmetro "Longitude"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def validate_longitude(dict_data: dict = {}) -> float:

    bool_is_update = ('LOC_ID' in dict_data and type(dict_data['LOC_ID']) == int)

    str_label = f'Importante: Caso deseje manter a longitude atual ( abaixo ), basta ignorar o preenchimento. Caso queira apagar o valor, digite "none".\n{format_data_view_longitude(dict_data)}\n' if bool_is_update == True else ''
    str_label += f'Informe a longitude da localização em formato numérico ( ex.: 123, 123.45 ou 123,45 ): '
    float_return = input(f'{str_label}')

    while True:

        try:

            if float_return.strip() != '' and float_return.strip().lower() != 'none':

                if ',' in float_return:
                    float_return = float_return.replace(',', '.')

                if Helper.is_float(float_return) == False and Helper.is_int(float_return) == False:
                    raise Exception('O conteúdo informado deve ser numérico ( ex.: 123, 123.45 ou 123,45 ).')

            break

        except Exception as error:

            print(f'{error} Tente novamente: ', end = '')
            float_return = input()

    float_value = None
    if float_return.strip() != '':
        float_value = float(float_return) if float_return.strip().lower() != 'none' else ''

    return float_value


"""
Método responsável pela formatação de visualização da umidade máxima para o solo do módulo "Localizações"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_humidity_max(dict_data: dict = {}) -> str:

    str_return = 'Umidade máxima para o solo: '
    str_return += f'{dict_data['LCO_HUMIDITY_MAX']}%' if 'LCO_HUMIDITY_MAX' in dict_data and type(dict_data['LCO_HUMIDITY_MAX']) != None and Helper.is_float(dict_data['LCO_HUMIDITY_MAX']) == True else 'N/I'

    return str_return


"""
Método responsável pela validação do parâmetro "Umidade máxima para o solo"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def validate_humidity_max(dict_data: dict = {}) -> float:

    bool_is_update = ('LOC_ID' in dict_data and type(dict_data['LOC_ID']) == int)

    str_label = f'Importante: Caso deseje manter a umidade máxima para o solo atual ( abaixo ), basta ignorar o preenchimento. Caso queira apagar o valor, digite "none".\n{format_data_view_humidity_max(dict_data)}\n' if bool_is_update == True else ''
    str_label += f'Informe a umidade máxima para o solo em formato numérico ( ex.: 123, 123.45 ou 123,45 ): '
    float_return = input(f'{str_label}')

    while True:

        try:

            if float_return.strip() != '' and float_return.strip().lower() != 'none':

                if ',' in float_return:
                    float_return = float_return.replace(',', '.')

                if Helper.is_float(float_return) == False and Helper.is_int(float_return) == False:
                    raise Exception('O conteúdo informado deve ser numérico ( ex.: 123, 123.45 ou 123,45 ).')

            break

        except Exception as error:

            print(f'{error} Tente novamente: ', end = '')
            float_return = input()

    float_value = None
    if float_return.strip() != '':
        float_value = float(float_return) if float_return.strip().lower() != 'none' else ''

    return float_value


"""
Método responsável pela formatação de visualização da data de cadastro do módulo "Localização"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_insert_date(dict_data: dict = {}) -> str:

    str_return = 'Data de cadastro: '
    str_return += f'{Helper.convert_date_to_pt_br(dict_data['LOC_INSERT_DATE'])}' if 'LOC_INSERT_DATE' in dict_data and type(dict_data['LOC_INSERT_DATE']) != None and type(dict_data['LOC_INSERT_DATE']) == datetime.datetime else 'N/I'

    return str_return


"""
Método responsável pela formatação de visualização da data de atualização do módulo "Localização"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_update_date(dict_data: dict = {}) -> str:

    str_return = 'Data de atualização: '
    str_return += f'{Helper.convert_date_to_pt_br(dict_data['LOC_UPDATE_DATE'])}' if 'LOC_UPDATE_DATE' in dict_data and type(dict_data['LOC_UPDATE_DATE']) != None and type(dict_data['LOC_UPDATE_DATE']) == datetime.datetime else 'N/I'

    return str_return


"""
Método responsável pela formatação de visualização de dados do módulo "Localização"

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
        str_return += f'- {format_data_view_name(dict_data)} \n'
        str_return += f'- {format_data_view_latitude(dict_data)} \n'
        str_return += f'- {format_data_view_longitude(dict_data)} \n'
        str_return += f'- {format_data_view_humidity_max(dict_data)} \n'
        str_return += f'- {format_data_view_insert_date(dict_data)} \n' if bool_show_insert_date == True else ''
        str_return += f'- {format_data_view_update_date(dict_data)} \n' if bool_show_update_date == True else ''

    return str_return


"""
Método responsável pela exibição de cadastros do módulo "Localização"
"""
def action_list():

    Main.init_step()

    validate_exists_data()

    show_head_module()

    object_f7gs_location = F7GsLocation()

    object_f7gs_location.set_select(['LOC.*', 'LCO.*'])
    object_f7gs_location.set_table('F7_GS_LOCATION LOC')
    object_f7gs_location.set_join([
        {'str_type_join': 'INNER JOIN', 'str_table': 'F7_GS_LOCATION_CONFIG LCO', 'str_where': 'LCO.LCO_LOC_ID = LOC.LOC_ID'},
    ])
    object_f7gs_location.set_where([F7GsLocation.get_params_to_active_data()])
    object_f7gs_location.set_order([{'str_column': 'LOC_ID', 'str_type_order': 'ASC'}])
    list_data = object_f7gs_location.get_data().get_list()

    for dict_data in list_data:

        print(format_data_view(dict_data))
    
    require_reload()


"""
Método responsável por executar a ação de retorno de dados de uma determinada localização
"""
def get_data_by_id(int_loc_id: int = 0) -> dict:

    object_f7gs_location = F7GsLocation()

    object_f7gs_location.set_select(['LOC.*', 'LCO.*'])
    object_f7gs_location.set_table('F7_GS_LOCATION LOC')
    object_f7gs_location.set_join([
        {'str_type_join': 'INNER JOIN', 'str_table': 'F7_GS_LOCATION_CONFIG LCO', 'str_where': 'LCO.LCO_LOC_ID = LOC.LOC_ID'},
    ])
    object_f7gs_location.set_where([

        {'str_column': 'LOC_ID', 'str_type_where': '=', 'value': int_loc_id},
        F7GsLocation.get_params_to_active_data()

    ])

    dict_data = object_f7gs_location.get_data().get_one()

    if type(dict_data) == type(None):
        raise Exception(f'Nenhum registro foi localizado com o ID {int_loc_id}.')

    return object_f7gs_location


"""
Método responsável por executar a ação de retorno de dados de configuração uma determinada localização
"""
def get_data_config_location_by_id(int_loc_id: int = 0) -> dict:

    object_f7gs_location_config = F7GsLocationConfig()

    object_f7gs_location_config.set_where([

        {'str_column': 'LCO_LOC_ID', 'str_type_where': '=', 'value': int_loc_id},
        F7GsLocationConfig.get_params_to_active_data()

    ])

    dict_data = object_f7gs_location_config.get_data().get_one()

    if type(dict_data) == type(None):
        raise Exception(f'Nenhum registro de configuração de localização foi localizado com o ID {int_loc_id}.')

    return object_f7gs_location_config


# ... Demais parâmetros...


"""
Método responsável pela exibição da funcionalidade de cadastro do módulo "Localização"
"""
def action_insert():

    Main.init_step()

    show_head_module()

    print('Os parâmetros abaixo fazem parte do cadastro principal da localização.')
    print('')

    str_loc_name = validate_name()

    # -------
    # Etapa 2
    # -------

    Main.init_step()

    show_head_module()

    print('Os próximos parâmetros fazem parte da localização geográfica. O preenchimento não é obrigatório.')
    input(f'\nPressione <enter> para continuar...')

    # -------
    # Etapa 3
    # -------

    Main.init_step()

    show_head_module()

    float_lco_latitude = validate_latitude()

    print('')

    float_lco_longitude = validate_longitude()

    print('')

    float_lco_humidity_max = validate_humidity_max()

    Main.loading('Salvando dados, por favor aguarde...')

    # -------
    # Etapa 4
    # -------

    Main.init_step()

    show_head_module()

    dict_data = {}

    dict_data['LOC_NAME'] = str_loc_name

    object_f7gs_location = F7GsLocation()
    object_f7gs_location.insert(dict_data)

    int_loc_id = object_f7gs_location.get_last_id()

    # --------------------------------------------------
    # Processo de cadastro dos parâmetros de localização
    # --------------------------------------------------

    dict_data_config_location = {}

    dict_data_config_location['LCO_LOC_ID'] = int_loc_id

    if type(float_lco_latitude) != type(None):
        dict_data_config_location['LCO_LATITUDE'] = float_lco_latitude

    if type(float_lco_longitude) != type(None):
        dict_data_config_location['LCO_LONGITUDE'] = float_lco_longitude

    if type(float_lco_humidity_max) != type(None):
        dict_data_config_location['LCO_HUMIDITY_MAX'] = float_lco_humidity_max

    object_f7gs_location_config = F7GsLocationConfig()
    object_f7gs_location_config.insert(dict_data_config_location)

    # Retorno de dados após o cadastro
    object_f7gs_location = get_data_by_id(int_loc_id)
    dict_data = object_f7gs_location.get_one()

    print(format_data_view(dict_data = dict_data, bool_show_id = False, bool_show_insert_date = False, bool_show_update_date = False))

    print('Registro cadastrado com sucesso.')

    require_reload()


"""
Método responsável pela exibição da funcionalidade de atualização do módulo "Localização"
"""
def action_update():

    Main.init_step()

    show_head_module()

    validate_exists_data()

    int_loc_id = validate_id()

    # -------
    # Etapa 2
    # -------

    Main.loading('Verificando dados, por favor aguarde...')

    Main.init_step()

    show_head_module()

    object_f7gs_location = get_data_by_id(int_loc_id)
    dict_data = object_f7gs_location.get_one()

    print('Os dados abaixo representam o cadastro atual do registro informado.')
    print('')

    print(format_data_view(dict_data))

    input(f'Pressione <enter> para continuar...')

    # -------
    # Etapa 3
    # -------

    Main.init_step()

    show_head_module()

    print('Os parâmetros abaixo fazem parte do cadastro principal da localização.')
    print('')

    str_loc_name = validate_name(dict_data)

    # -------
    # Etapa 4
    # -------

    Main.init_step()

    show_head_module()

    print('Os próximos parâmetros fazem parte da localização geográfica. O preenchimento não é obrigatório.')
    input(f'\nPressione <enter> para continuar...')

    # -------
    # Etapa 5
    # -------

    Main.init_step()

    show_head_module()

    float_lco_latitude = validate_latitude(dict_data)

    print('')

    float_lco_longitude = validate_longitude(dict_data)

    print('')

    float_lco_humidity_max = validate_humidity_max(dict_data)

    Main.loading('Salvando dados, por favor aguarde...')

    # -------
    # Etapa 6
    # -------

    Main.init_step()

    show_head_module()

    if str_loc_name.strip() != '':
        dict_data['LOC_NAME'] = str_loc_name

    object_f7gs_location.update(dict_data)

    # -----------------------------------------------------
    # Processo de atualização dos parâmetros de localização
    # -----------------------------------------------------

    object_f7gs_location_config = get_data_config_location_by_id(int_loc_id)
    dict_data_config_location = object_f7gs_location_config.get_one()

    if type(float_lco_latitude) != type(None):
        dict_data_config_location['LCO_LATITUDE'] = float_lco_latitude

    if type(float_lco_longitude) != type(None):
        dict_data_config_location['LCO_LONGITUDE'] = float_lco_longitude

    if type(float_lco_humidity_max) != type(None):
        dict_data_config_location['LCO_HUMIDITY_MAX'] = float_lco_humidity_max

    if type(dict_data_config_location) != type(None):
        object_f7gs_location_config.update(dict_data_config_location)

    # Retorno de dados após as atualizações
    object_f7gs_location = get_data_by_id(int_loc_id)
    dict_data = object_f7gs_location.get_one()

    print(format_data_view(dict_data = dict_data, bool_show_update_date = False))

    print('Registro atualizado com sucesso.')
    
    require_reload()


"""
Método responsável pela exibição da funcionalidade de exclusão do módulo "Localização"
"""
def action_delete():

    Main.init_step()

    show_head_module()

    validate_exists_data()

    int_loc_id = validate_id()

    # -------
    # Etapa 2
    # -------

    Main.loading('Verificando dados, por favor aguarde...')

    Main.init_step()

    show_head_module()

    object_f7gs_location = get_data_by_id(int_loc_id)
    dict_data = object_f7gs_location.get_one()

    dict_data['LOC_STATUS'] = F7GsLocation.STATUS_DELETED

    object_f7gs_location.update(dict_data)

    # --------------------------------------------------
    # Processo de exclusão dos parâmetros de localização
    # --------------------------------------------------

    object_f7gs_location_config = get_data_config_location_by_id(int_loc_id)
    dict_data_config_location = object_f7gs_location_config.get_one()

    dict_data_config_location['LCO_STATUS'] = F7GsLocationConfig.STATUS_DELETED

    object_f7gs_location_config.update(dict_data_config_location)

    print('Registro excluído com sucesso.')

    require_reload()


"""
Método responsável pela exibição padrão do módulo "Localização"
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