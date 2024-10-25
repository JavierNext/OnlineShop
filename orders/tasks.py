from celery import shared_task
from django.core.mail import EmailMessage
from .models import Order

@shared_task
def order_created(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = (
        f'Dear {order.first_name},\n\n'
        f'You have successfully placed an order.'
        f'Your order ID is {order.id}.'
    )
    # Crear el mensaje de correo
    email = EmailMessage(subject, message, 'testprogramacion01@gmail.com', [order.email])

    # Obtener los productos del pedido y adjuntar PDFs si están disponibles
    for item in order.items.all():  # Asumiendo que `items` es el campo de productos en el pedido
        if item.product.pdf_file:  # Asegúrate de que el producto tenga un archivo PDF
            pdf_path = item.product.pdf_file.path
            email.attach_file(pdf_path)

    # Enviar el correo electrónico
    mail_sent = email.send()
    return mail_sent