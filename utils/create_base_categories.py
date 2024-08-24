from apps.product.models import *


def create_categories():
    main_category, status = MainCategoryModel.objects.get_or_create(title='کامپیوتر', url='computer', active=True)

    category, status = ChildCategoryModel.objects.get_or_create(title='قطعات کامپیوتری', url='computer-parts', base_category=main_category, active=True)

    ChildCategoryModel.objects.get_or_create(title='پردازنده', url='cpu',base_category=main_category, parent_category=category, active=True)

    ChildCategoryModel.objects.get_or_create(title='مادربرد', url='main-board', base_category=main_category, parent_category=category, active=True)

    ChildCategoryModel.objects.get_or_create(title='کارت گرافیک', url='gpu', base_category=main_category, parent_category=category, active=True)

    ChildCategoryModel.objects.get_or_create(title='خنک کننده پردازنده', url='fan-cpu', base_category=main_category, parent_category=category, active=True)

    ChildCategoryModel.objects.get_or_create(title='رم', url='ram', base_category=main_category, parent_category=category, active=True)

    ChildCategoryModel.objects.get_or_create(title='هارد', url='hard', base_category=main_category, parent_category=category, active=True)

    ChildCategoryModel.objects.get_or_create(title='اس اس دی', url='ssd', base_category=main_category, parent_category=category, active=True)

    ChildCategoryModel.objects.get_or_create(title='پاور', url='power', base_category=main_category, parent_category=category, active=True)

    ChildCategoryModel.objects.get_or_create(title='کیس', url='case', base_category=main_category, parent_category=category, active=True)

