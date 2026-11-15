# Cobrança por WhatsApp

Todo dia, às 8h, manda o lembrete de vencimento a cada cliente com boleto em aberto.

    python enviar_cobranca.py clientes.csv

O envio usa a API do provedor com o token de `WHATSAPP_TOKEN`. O registro de cada envio vai para `logs/envios-<data>.log`.
