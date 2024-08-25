from .models import *
from django.db.models import Q


def filter_category(category):
    brands = BrandModel.objects.filter(category__url=category)
    if category == 'cpu':
        list_platform = CpuPlatformModel.objects.all()
        list_socket = SocketTypeModel.objects.all()
        list_ddr = DDRModel.objects.all()
        list_series = SeriesModel.objects.all()
        list_bit = BitTypeModel.objects.all()
        list_core = CpuCoreModel.objects.all()
        list_gpu = OnBoardGpuModel.objects.all()

        filter_dict = [
            {'name': 'برند', 'list': brands, 'title': 'brand'},
            {'name': 'مبتنی', 'list': list_platform, 'title': 'platform'},
            {'name': 'سوکت', 'list': list_socket, 'title': 'socket'},
            {'name': 'ddr', 'list': list_ddr, 'title': 'ddr'},
            {'name': 'سری', 'list': list_series, 'title': 'series'},
            {'name': 'bit', 'list': list_bit, 'title': 'bit'},
            {'name': 'تعداد هسته', 'list': list_core, 'title': 'core'},
            {'name': 'گرافیک', 'list': list_gpu, 'title': 'gpu'},
        ]

        return filter_dict

    elif category == 'main-board':
        list_platform = CpuPlatformModel.objects.all()
        list_socket = SocketTypeModel.objects.all()
        list_ddr = DDRModel.objects.all()
        list_chipset = MainBoardChipSetModel.objects.all()
        list_ram_frequency = RamFrequencyModel.objects.all()
        filter_dict = [
            {'name': 'برند', 'list': brands, 'title': 'brand'},
            {'name': 'پلتفرم', 'list': list_platform, 'title': 'platform'},
            {'name': 'سوکت', 'list': list_socket, 'title': 'socket'},
            {'name': 'ddr', 'list': list_ddr, 'title': 'ddr'},
            {'name': 'دارای wifi', 'list': '', 'title': 'has_wifi'},
            {'name': 'دارای بلوتوث', 'list': '', 'title': 'has_bluetooth'},
            {'name': 'چیپست', 'list': list_chipset, 'title': 'chipset'},
            {'name': 'دارای پورت hdmi', 'list': '', 'title': 'has_hdmi_port'},
            {'name': 'داری پورت vga', 'list': '', 'title': 'has_vga_port'},
            {'name': 'دارای پورت display', 'list': '', 'title': 'has_display_port'},
            {'name': 'فرکانس رم', 'list': list_ram_frequency, 'title': 'ram_frequency'},
        ]

        return filter_dict

    elif category == 'gpu':
        list_platform = GpuPlatformModel.objects.all()
        list_ddr = DDRModel.objects.all()

        filter_dict = [
            {'name': 'برند', 'list': brands, 'title': 'brand'},
            {'name': 'پلتفرم', 'list': list_platform, 'title': 'platform'},
            {'name': 'ddr', 'list': list_ddr, 'title': 'ddr'},
        ]

        return filter_dict

    elif category == 'fan-cpu':
        list_platform = FanCpuPlatformModel.objects.all()
        list_sockets = SocketTypeModel.objects.all()

        filter_dict = [
            {'name': 'برند', 'list': brands, 'title': 'brand'},
            {'name': 'پلتفرم', 'list': list_platform, 'title': 'platform'},
            {'name': 'سوکت', 'list': list_sockets, 'title': 'sockets'},
        ]

        return filter_dict

    elif category == 'ram':
        list_platform = FanCpuPlatformModel.objects.all()
        list_ram_frequency = RamFrequencyModel.objects.all()

        filter_dict = [
            {'name': 'برند', 'list': brands, 'title': 'brand'},
            {'name': 'پلتفرم', 'list': list_platform, 'title': 'platform'},
            {'name': 'فرکانس', 'list': list_ram_frequency},
        ]

        return filter_dict

    elif category == 'hard':
        list_type = HardTypeModel.objects.all()
        list_sata = SataTypeModel.objects.all()

        filter_dict = [
            {'name': 'برند', 'list': brands, 'title': 'brand'},
            {'name': 'نوع', 'list': list_type, 'title': 'type'},
            {'name': 'ساتا', 'list': list_sata, 'title': 'sata'},
            {'name': 'ضد آب', 'list': '', 'title': 'water_proof'},
        ]

        return filter_dict

    elif category == 'ssd':
        list_type = SataTypeModel.objects.all()

        filter_dict = [
            {'name': 'برند', 'list': brands, 'title': 'brand'},
            {'name': 'نوع', 'list': list_type, 'title': 'type'},
        ]

        return filter_dict

    elif category == 'power':
        list_form_factor = PowerFormFactorModel.objects.all()
        modular = ['true', 'false']

        filter_dict = [
            {'name': 'برند', 'list': brands, 'title': 'brand'},
            {'name': 'فرم فاکتور', 'list': list_form_factor, 'title': 'form_factor'},
            {'name': 'ماژولار', 'list': modular, 'title': 'modular'},
        ]

        return filter_dict
    elif category == 'case':
        list_form_factor = FormFactorModel.objects.all()
        list_power_form_factor = PowerFormFactorModel.objects.all()

        filter_dict = [
            {'name': 'برند', 'list': brands, 'title': 'brand'},
            {'name': 'فرم فاکتور', 'list': list_form_factor, 'title': 'main_board_form_factor'},
            {'name': 'پاور فرم فاکتور', 'list': list_power_form_factor, 'title': 'power_form_factor'},
        ]

        return filter_dict


def get_category_products(category):
    if category == 'cpu':
        products = CpuModel.objects.filter(active=True)

    elif category == 'main-board':
        products = MainBoardModel.objects.filter(active=True)

    elif category == 'gpu':
        products = GpuModel.objects.filter(active=True)

    elif category == 'fan-cpu':
        products = FanCpuModel.objects.filter(active=True)

    elif category == 'ram':
        products = RamModel.objects.filter(active=True)

    elif category == 'hard':
        products = HardModel.objects.filter(active=True)

    elif category == 'ssd':
        products = SSDModel.objects.filter(active=True)

    elif category == 'power':
        products = PowerModel.objects.filter(active=True)

    elif category == 'case':
        products = CaseModel.objects.filter(active=True)

    else:
        products = ProductModel.objects.filter(Q(child_category__url=category)
                                               | Q(child_category__parent_category__url=category))

    return products


def compare_products(category, id):
    if category == 'cpu':
        product = CpuModel.objects.get(id=id)

    elif category == 'main-board':
        product = MainBoardModel.objects.get(id=id)

    elif category == 'gpu':
        product = GpuModel.objects.get(id=id)

    elif category == 'fan-cpu':
        product = FanCpuModel.objects.get(id=id)

    elif category == 'ram':
        product = RamModel.objects.get(id=id)

    elif category == 'hard':
        product = HardModel.objects.get(id=id)

    elif category == 'ssd':
        product = SSDModel.objects.get(id=id)

    elif category == 'power':
        product = PowerModel.objects.get(id=id)

    elif category == 'case':
        product = CaseModel.objects.get(id=id)

    else:
        product = ProductModel.objects.filter(id=id).first()
        fields = [{'name': i.field.title, 'amount': i.amount} for i in ProductFieldModel.objects.filter(product=product)]
        return [product, fields]

    fields = [{'name': i.verbose_name, 'amount': '' if str(product.__getattribute__(i.name)).endswith('None')else product.__getattribute__(i.name)} for i in product._meta.get_fields()[25:]]

    return [product, fields]
