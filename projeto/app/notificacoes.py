import json
import logging
import urllib.request

from django.conf import settings

from .models import ItemPerdido

BREVO_URL = "https://api.brevo.com/v3/smtp/email"

logger = logging.getLogger(__name__)


# Manda um email pela API do Brevo
def enviar_email(para_email, para_nome, assunto, texto):

    # Sem chave, só mostra no terminal, para o site rodar em qualquer computador
    if not settings.BREVO_API_KEY:
        logger.warning("Email não enviado (falta a BREVO_API_KEY) para %s: %s", para_email, assunto)
        return False

    dados = {
        "sender": {"name": "ELO Achados e Perdidos", "email": settings.EMAIL_REMETENTE},
        "to": [{"email": para_email, "name": para_nome}],
        "subject": assunto,
        "textContent": texto,
    }

    pedido = urllib.request.Request(
        BREVO_URL,
        data=json.dumps(dados).encode("utf-8"),
        headers={
            "api-key": settings.BREVO_API_KEY,
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(pedido, timeout=10) as resposta:
            return resposta.status == 201
    except Exception as erro:
        logger.warning("Erro ao mandar email para %s: %s", para_email, erro)
        return False


# Avisa quem perdeu um item da mesma categoria do item que foi achado
def avisar_donos(item_achado):

    perdidos = ItemPerdido.objects.filter(
        categoria=item_achado.categoria
    ).exclude(
        usuario=item_achado.usuario
    ).select_related("usuario")

    enviados = 0

    for perdido in perdidos:
        assunto = f"Acharam um item parecido com o seu: {item_achado.nome_objeto}"
        texto = (
            f"Oi, {perdido.usuario.nome}!\n\n"
            f"Você reportou que perdeu \"{perdido.titulo}\", e acabaram de achar um item da mesma categoria:\n\n"
            f"{item_achado.nome_objeto}\n"
            f"Onde foi achado: {item_achado.onde_encontrou}\n"
            f"Onde está agora: {item_achado.get_onde_esta_agora_display()}\n\n"
            "Entre no ELO para ver os detalhes."
        )

        if enviar_email(perdido.usuario.email, perdido.usuario.nome, assunto, texto):
            enviados += 1

    return enviados
