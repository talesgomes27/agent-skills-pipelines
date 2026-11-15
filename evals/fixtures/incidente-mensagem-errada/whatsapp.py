"""Cliente mínimo da API do provedor de WhatsApp."""
import json
import urllib.request

URL = 'https://api.provedor-exemplo.invalid/v1/messages'


def enviar(telefone, texto, token):
    corpo = json.dumps({'to': telefone, 'text': texto}).encode('utf-8')
    pedido = urllib.request.Request(URL, corpo, {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'})
    with urllib.request.urlopen(pedido, timeout=10) as resposta:
        return resposta.status
