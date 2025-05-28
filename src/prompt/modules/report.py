import datetime
import os
import pprint
import subprocess
import sys

# > Importante: A definição abaixo referente ao diretório raiz deve ser efetuada antes das importações de arquivos do sistema.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pandas as Pandas
import matplotlib.pyplot as Pyplot
import numpy as Numpy
import seaborn as Seaborn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error, r2_score

import prompt.main as Main
import prompt.modules.location as ModuleLocation
from custom.helper import Helper
from models.f7_gs_measurement import F7GsMeasurement

"""
Método responsável pela exibição do cabeçalho do módulo
"""
def show_head_module():

    print('-= Gráficos =-')
    print('')


"""
Método responsável por recarregar o módulo "Gráficos"
"""
def require_reload():

    input(f'\nPressione <enter> para voltar ao menu do módulo "Gráficos"...')
    action_main()


"""
Método responsável por retornar as opções de menu do módulo "Gráficos"

Return: list
"""
def get_menu_options() -> list:

    return [
        {
            'code': 1,
            'title': 'Visualizar gráfico de medição',
            'action': action_graphic_measurement
        },{
            'code': 2,
            'title': 'Voltar ao menu principal',
            'action': Main.init_system
        }
    ]


"""
Método responsável por retornar os códigos das opções de menu do módulo "Gráficos"

Return: list
"""
def get_menu_options_codes() -> list:

    list_return = []

    list_menu_options = get_menu_options()

    for dict_menu_option in list_menu_options:
        list_return.append(dict_menu_option['code'])

    return list_return


"""
Método responsável pela validação do parâmetro "Opção do menu" do módulo "Gráficos"

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
Método responsável pela exibição de gráfico de irrigação do módulo "Gráficos"
"""
def action_graphic_measurement():

    Main.init_step()

    show_head_module()

    int_loc_id = ModuleLocation.validate_id()

    # -------
    # Etapa 2
    # -------

    Main.loading('Verificando dados, por favor aguarde...')

    Main.init_step()

    show_head_module()

    object_f7gs_location = ModuleLocation.get_data_by_id(int_loc_id)
    dict_data_location = object_f7gs_location.get_one()

    object_f7gs_measurement = F7GsMeasurement()

    object_f7gs_measurement.set_select(['MSM.*', 'LOC.LOC_NAME', 'SNS.SNS_NAME'])
    object_f7gs_measurement.set_table('F7_GS_MEASUREMENT MSM')
    object_f7gs_measurement.set_join([
        {'str_type_join': 'INNER JOIN', 'str_table': 'F7_GS_LOCATION LOC', 'str_where': 'LOC.LOC_ID = MSM.MSM_LOC_ID'},
        {'str_type_join': 'INNER JOIN', 'str_table': 'F7_GS_SENSOR SNS', 'str_where': 'SNS.SNS_ID = MSM.MSM_SNS_ID'}
    ])
    object_f7gs_measurement.set_where([

        {'str_column': 'MSM.MSM_LOC_ID', 'str_type_where': '=', 'value': int_loc_id},
        F7GsMeasurement.get_params_to_active_data()

    ])
    object_f7gs_measurement.set_order([{'str_column': 'MSM.MSM_ID', 'str_type_order': 'ASC'}])
    list_data = object_f7gs_measurement.get_data().get_list()

    if list_data == None:
        raise Exception('Não existem medições cadastradas para essa localização.')

    object_dataframe = Pandas.DataFrame(list_data)

    del object_dataframe['MSM_ID']
    del object_dataframe['MSM_LOC_ID']

    object_dataframe['MSM_INSERT_DATE'] = Pandas.to_datetime(object_dataframe['MSM_INSERT_DATE'])

    object_dataframe['MSM_INSERT_HOUR'] = object_dataframe['MSM_INSERT_DATE'].dt.hour
    object_dataframe['MSM_INSERT_DAY'] = object_dataframe['MSM_INSERT_DATE'].dt.dayofweek

    list_x = object_dataframe[['MSM_INSERT_HOUR', 'MSM_INSERT_DAY']]
    list_y = object_dataframe['MSM_VALUE']

    X_train, X_test, y_train, y_test = train_test_split(list_x, list_y, test_size = 0.3, random_state = 42)

    object_random_forest_regressor = RandomForestRegressor()
    object_random_forest_regressor.fit(X_train, y_train)

    y_pred = object_random_forest_regressor.predict(X_test)
    float_accuracy = object_random_forest_regressor.score(X_test, y_test)

    float_mse = mean_squared_error(y_test, y_pred)
    float_rmse = Numpy.sqrt(float_mse)
    float_mae = mean_absolute_error(y_test, y_pred)
    float_mape = mean_absolute_percentage_error(y_test, y_pred)
    float_r2 = r2_score(y_test, y_pred)

    # Gráfico de dispersão
    Pyplot.figure(figsize = (8, 6))
    Seaborn.scatterplot(x = y_test, y = y_pred)
    Pyplot.plot([list_y.min(), list_y.max()], [list_y.min(), list_y.max()], '--r', label = 'Ideal')
    Pyplot.xlabel('Valores reais (em %)')
    Pyplot.ylabel('Valores previstos (em %)')
    Pyplot.title(f'Valores reais x Valores previstos - {dict_data_location['LOC_NAME']}')
    Pyplot.legend()

    Main.init_step()

    show_head_module()

    # Métricas
    print(f'Erro Quadrático Médio: {float_mse:.2f}')
    print(f'Raiz do Erro Quadrático Médio: {float_rmse:.2f}')
    print(f'Acurácia com Random Forest Regressor: {float_accuracy:.2f}')
    print(f'Média do Erro Absoluto: {float_mae:.2f}')
    print(f'Erro Percentual Médio Absoluto: {float_mape:.2f}')
    print(f'Coeficiente de Determinação: {float_r2:.2f}')

    print('')

    print('Visualizando gráfico...')

    Pyplot.show()

    Main.init_step()

    show_head_module()

    print('Gráfico gerado e visualizado com sucesso.')

    require_reload()


"""
Método responsável pela exibição padrão do módulo "Gráficos"
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