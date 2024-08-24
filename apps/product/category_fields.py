from .models import *


def product_fields(product):
    if product.child_category.url == 'cpu':
        product = CpuModel.objects.get(id=product.id)

    elif product.child_category.url == 'main-board':
        product = MainBoardModel.objects.get(id=product.id)

    elif product.child_category.url == 'gpu':
        product = GpuModel.objects.get(id=product.id)

    elif product.child_category.url == 'fan-cpu':
        product = FanCpuModel.objects.get(id=product.id)

    elif product.child_category.url == 'ram':
        product = RamModel.objects.get(id=product.id)

    elif product.child_category.url == 'hard':
        product = HardModel.objects.get(id=product.id)

    elif product.child_category.url == 'ssd':
        product = SSDModel.objects.get(id=product.id)

    elif product.child_category.url == 'power':
        product = PowerModel.objects.get(id=product.id)

    elif product.child_category.url == 'case':
        product = CaseModel.objects.get(id=product.id)

    else:
        fields = [{'name': i.field.title, 'amount': i.amount} for i in ProductFieldModel.objects.filter(product=product)]
        return fields

    fields = []

    for i in product._meta.get_fields()[27:]:
        if hasattr(i, 'verbose_name'):
            if i.verbose_name != 'productmodel ptr':
                fields.append({'name': i.verbose_name , 'amount': '' if str(product.__getattribute__(i.name)).endswith('None')else product.__getattribute__(i.name)})

    return fields
