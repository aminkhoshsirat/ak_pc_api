from celery import shared_task


@shared_task
def create_category():
    print(2)
    return 25
