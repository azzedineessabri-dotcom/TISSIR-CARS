import os
import requests
import logging
from flask import current_app

logger = logging.getLogger(__name__)

def envoyer_message_whatsapp(numero, message, api_token=None, instance_id=None):
    if not api_token or not instance_id:
        logger.warning("WhatsApp API non configuré (manque token ou instance_id)")
        return False, "API non configurée"

    if not numero:
        return False, "Numéro manquant"

    numero = numero.replace('+', '').replace(' ', '').replace('-', '')
    if not numero.startswith('212'):
        numero = '212' + numero.lstrip('0')

    try:
        url = f"https://api.ultramsg.com/{instance_id}/messages/chat"
        payload = {
            "token": api_token,
            "to": numero,
            "body": message,
            "priority": 10,
            "referenceId": ""
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        verify_ssl = os.environ.get('WHATSAPP_VERIFY_SSL', 'true').lower() == 'true'
        resp = requests.post(url, data=payload, timeout=15, verify=verify_ssl)
        result = resp.json()
        if resp.status_code == 200 and result.get('sent'):
            logger.info(f"WhatsApp envoyé à {numero}")
            return True, "Envoyé"
        logger.warning(f"WhatsApp échec: {result}")
        return False, result.get('error', 'Erreur inconnue')
    except requests.exceptions.Timeout:
        return False, "Timeout API WhatsApp"
    except Exception as e:
        logger.error(f"Erreur WhatsApp: {e}")
        return False, str(e)

def formater_message_reservation(reservation, car=None, statut="Confirmée"):
    if car is None:
        car = reservation.car
    date_debut = reservation.date_debut.strftime('%d/%m/%Y à %H:%M')
    date_fin = reservation.date_fin.strftime('%d/%m/%Y à %H:%M')

    company = current_app.config.get('COMPANY_NAME', 'Sannad Tech')
    address = current_app.config.get('COMPANY_ADDRESS', '')
    phone = current_app.config.get('COMPANY_PHONE', '')

    if statut == 'Annulée':
        emoji = "❌"
        footer_msg = "Toutes nos excuses pour la gêne occasionnée. Nous restons à votre disposition."
    elif statut == 'Terminée':
        emoji = "🏁"
        footer_msg = "Merci pour votre confiance. Au plaisir de vous revoir !"
    elif statut == 'Confirmé':
        emoji = "✅"
        footer_msg = "Merci de votre confiance ! 🙏"
    else:
        emoji = "ℹ️"
        footer_msg = "Merci de votre confiance ! 🙏"

    line = f"📋{reservation.reservation_number} | 🚗{car.brand} {car.name} | {date_debut}→{date_fin} | {reservation.duree}j | 💰{reservation.prix_total:.0f}DH"

    msg = (
        f"{emoji} *{company} - Réservation {statut}*\n\n"
        f"{line}\n\n"
        f"{'📍 ' + address if address else ''}{' | 📞 ' + phone if phone else ''}\n\n"
        f"{footer_msg}"
    )
    return msg
