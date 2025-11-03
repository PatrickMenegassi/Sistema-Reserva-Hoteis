# reserves/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
import shutil
import os

@shared_task
def send_reservation_confirmation(user_email, user_name, reservation_details):
    """Envia confirmação de reserva"""
    subject = f'Confirmação de Reserva - {reservation_details["hotel_name"]}'
    
    message = f"""
    Olá {user_name},
    
    Sua reserva foi confirmada com sucesso!
    
    📋 Detalhes da Reserva:
    • Hotel: {reservation_details['hotel_name']}
    • Quarto: {reservation_details['room_type']}  
    • Check-in: {reservation_details['check_in']}
    • Check-out: {reservation_details['check_out']}
    • Total: {reservation_details['total_price']}
    
    Obrigado por escolher nossos serviços!
    
    Atenciosamente,
    🏨 Equipe de Reservas
    """
    
    try:
        send_mail(
            subject,
            message.strip(),
            settings.DEFAULT_FROM_EMAIL,
            [user_email],
            fail_silently=False,
        )
        return f' Confirmação enviada para {user_email}'
    except Exception as e:
        # Em produção, logue o erro
        raise e

@shared_task
def send_reservation_cancellation(user_email, user_name, reservation_details):
    """Envia notificação de cancelamento"""
    subject = 'Cancelamento de Reserva'
    
    message = f"""
    Olá {user_name},
    
    Sua reserva no {reservation_details['hotel_name']} foi cancelada.
    
    📋 Detalhes da Reserva Cancelada:
    • Quarto: {reservation_details['room_type']}
    • Período: {reservation_details['check_in']} a {reservation_details['check_out']}
    
    Esperamos vê-lo novamente em breve!
    
    Atenciosamente,
    🏨 Equipe de Reservas
    """
    
    send_mail(
        subject,
        message.strip(),
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False,
    )
    return f'📧 Notificação de cancelamento enviada para {user_email}'


@shared_task
def enviar_lembrete_checkin():
    """Envia lembretes de check-in para reservas do dia"""
    from .models import Reservation
    
    hoje = timezone.now().date()
    
    reservas_hoje = Reservation.objects.filter(
        check_in=hoje,
        status='confirmed'
    )

    for reserva in reservas_hoje:
        subject = f'Lembrete de Check-in - {reserva.room.hotel.name}'
        message = f"""
        Olá {reserva.customer.first_name},
        
        Este é um lembrete amigável sobre sua reserva hoje!
        
        📋 Detalhes:
        • Hotel: {reserva.room.hotel.name}
        • Quarto: {reserva.room.room_type}
        • Check-in: {reserva.check_in}
        • Check-out: {reserva.check_out}
        
        Estamos ansiosos para recebê-lo!
        
        Atenciosamente,
        Equipe {reserva.room.hotel.name}
        """
        
        try:
            send_mail(
                subject,
                message.strip(),
                settings.DEFAULT_FROM_EMAIL,
                [reserva.customer.email],
                fail_silently=False,
            )
            print(f" Lembrete enviado para {reserva.customer.email}")
        except Exception as e:
            print(f"Erro ao enviar para {reserva.customer.email}: {e}")
    
    return f"📧 Lembretes enviados: {reservas_hoje.count()}"

@shared_task
def limpar_reservas_expiradas():
    """Limpa reservas com check-out há mais de 30 dias"""
    from .models import Reservation  # Ajuste para seu model
    
    trinta_dias_atras = timezone.now().date() - timedelta(days=30)
    reservas_expiradas = Reservation.objects.filter(
        check_out__lt=trinta_dias_atras
    )
    
    count = reservas_expiradas.count()
    reservas_expiradas.delete()
    
    return f"Reservas expiradas removidas: {count}"



# Task para TESTE RÁPIDO do agendamento
@shared_task
def task_teste_agendamento():
    """Task para testar se o agendamento está funcionando"""
    print(" CELERY BEAT FUNCIONANDO! Task executada em:", timezone.now())
    return "Task de teste executada com sucesso!"

@shared_task
def debug_test():
    """Task simples para testar o Celery"""
    print(" Celery está funcionando perfeitamente!")
    return "Debug task executada com sucesso"