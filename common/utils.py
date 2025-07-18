from django.db.models import Model


def delete_object(model_object: Model) -> None:
    model_object.delete()
