from django import forms
from .models import *
from apps.user.models import UserModel
from apps.product.models import *

# admins = ((i, i.fullname) for i in UserModel.objects.all())


class SiteDetailForm(forms.ModelForm):
    class Meta:
        model = SiteDetailModel
        fields = '__all__'


class ChatForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    chat_room_id = forms.IntegerField(required=False)
    replay_id = forms.IntegerField(required=False)


class DailyWorksForm(forms.ModelForm):
    class Meta:
        model = DailyWorksModel
        fields = '__all__'


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUsModel
        fields = '__all__'


class MainCategoryForm(forms.ModelForm):
    image = forms.ImageField()
    description = forms.CharField(widget=forms.TextInput())

    class Meta:
        model = MainCategoryModel
        fields = '__all__'
        extra_fields = ['image', 'description']


class ChildCategoryForm(forms.ModelForm):
    image = forms.ImageField()
    description = forms.CharField(widget=forms.TextInput())

    class Meta:
        model = ChildCategoryModel
        fields = '__all__'
        extra_fields = ['image', 'description']


class ProductForm(forms.ModelForm):
    class Meta:
        model = ProductModel
        fields = '__all__'


class CpuPlatformForm(forms.ModelForm):
    class Meta:
        model = CpuPlatformModel
        fields = '__all__'


class GpuPlatformForm(forms.ModelForm):
    class Meta:
        model = GpuPlatformModel
        fields = '__all__'


class FanCpuPlatformForm(forms.ModelForm):
    class Meta:
        model = FanCpuPlatformModel
        fields = '__all__'


class SocketTypeForm(forms.ModelForm):
    class Meta:
        model = SocketTypeModel
        fields = '__all__'


class DDrForm(forms.ModelForm):
    class Meta:
        model = DDRModel
        fields = '__all__'


class GpuDDrForm(forms.ModelForm):
    class Meta:
        model = GpuDDRModel
        fields = '__all__'


class SeriesForm(forms.ModelForm):
    class Meta:
        model = SeriesModel
        fields = '__all__'


class BiteTypeForm(forms.ModelForm):
    class Meta:
        model = BitTypeModel
        fields = '__all__'


class CpuCoreForm(forms.ModelForm):
    class Meta:
        model = CpuCoreModel
        fields = '__all__'


class OnBoardGpuForm(forms.ModelForm):
    class Meta:
        model = OnBoardGpuModel
        fields = '__all__'


class FormFactorForm(forms.ModelForm):
    class Meta:
        model = FormFactorModel
        fields = '__all__'


class MainBoardChipSetForm(forms.ModelForm):
    class Meta:
        model = MainBoardChipSetModel
        fields = '__all__'


class RamFrequencyForm(forms.ModelForm):
    class Meta:
        model = RamFrequencyModel
        fields = '__all__'


class RamPlatformForm(forms.ModelForm):
    class Meta:
        model = RamPlatformModel
        fields = '__all__'


class HardTypeForm(forms.ModelForm):
    class Meta:
        model = HardTypeModel
        fields = '__all__'

class SSDTypeForm(forms.ModelForm):
    class Meta:
        model = SSDTypeModel
        fields = '__all__'


class SataTypeForm(forms.ModelForm):
    class Meta:
        model = SataTypeModel
        fields = '__all__'


class PowerFormFactorForm(forms.ModelForm):
    class Meta:
        model = PowerFormFactorModel
        fields = '__all__'


class CpuForm(forms.ModelForm):
    class Meta:
        model = CpuModel
        exclude = ['main_category', 'child_category', 'price_after_off']



class MainBoardForm(forms.ModelForm):
    class Meta:
        model = MainBoardModel
        exclude = ['main_category', 'child_category', 'price_after_off']


class GpuForm(forms.ModelForm):
    class Meta:
        model = GpuModel
        exclude = ['main_category', 'child_category', 'price_after_off']


class FanCpuForm(forms.ModelForm):
    class Meta:
        model = FanCpuModel
        exclude = ['main_category', 'child_category', 'price_after_off']


class RamForm(forms.ModelForm):
    class Meta:
        model = RamModel
        exclude = ['main_category', 'child_category', 'price_after_off']


class HardForm(forms.ModelForm):
    class Meta:
        model = HardModel
        exclude = ['main_category', 'child_category', 'price_after_off']


class SSDForm(forms.ModelForm):
    class Meta:
        model = SSDModel
        exclude = ['main_category', 'child_category', 'price_after_off']


class PowerForm(forms.ModelForm):
    class Meta:
        model = PowerModel
        exclude = ['main_category', 'child_category', 'price_after_off']


class CaseForm(forms.ModelForm):
    class Meta:
        model = CaseModel
        exclude = ['main_category', 'child_category', 'price_after_off']


class KeyBoardForm(forms.ModelForm):
    class Meta:
        model = KeyBoardModel
        exclude = ['main_category', 'child_category', 'price_after_off']


class MouseForm(forms.ModelForm):
    class Meta:
        model = MouseModel
        exclude = ['main_category', 'child_category', 'price_after_off']


class SpeakerForm(forms.ModelForm):
    class Meta:
        model = SpeakerModel
        exclude = ['main_category', 'child_category', 'price_after_off']


class MonitorForm(forms.ModelForm):
    class Meta:
        model = MonitorModel
        exclude = ['main_category', 'child_category', 'price_after_off']


class OpticalDriveForm(forms.ModelForm):
    class Meta:
        model = OpticalDriveModel
        exclude = ['main_category', 'child_category', 'price_after_off']


class FaqQuestionForm(forms.ModelForm):
    class Meta:
        model = FaqQuestionModel
        fields = '__all__'
