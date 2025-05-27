import json
import boto3
import os

def lambda_handler(dict_event, context):

    dict_return = {'status': True, 'dict_data': {}}

    try:

        if 'body' not in dict_event or not dict_event['body']:
            raise Exception(f'Não foi possível concluir o processo pois nenhum conteúdo foi recebido.')

        dict_params = json.loads(dict_event['body'])

        str_subject = dict_params.get('str_subject')
        if not str_subject:
            raise Exception(f'Não foi possível concluir o processo pois não foi definido o assunto para envio da notificação de alerta de umidade.')

        str_message = dict_params.get('str_message')
        if not str_message:
            raise Exception(f'Não foi possível concluir o processo pois não foi definida a mensagem para envio da notificação de alerta de umidade.')

        object_sns_client = boto3.client('sns', region_name = 'us-east-1')
        object_response = object_sns_client.publish(
            TopicArn = os.getenv('SNS_TOPIC_ARN'),
            Subject = str_subject,
            Message = str_message
        )

        dict_return['dict_data'] = {
            'dict_params': dict_params,
            'str_message': str_message
        }

    except Exception as error:

        dict_return = {'status': False, 'message': error}

    return dict_return