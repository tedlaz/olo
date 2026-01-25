from django import forms

from .models import Category, Dapanes, Diamerisma, Diaxeiristis, Koinoxrista, Xiliosta


class TailwindFormMixin:
    """Mixin to add Tailwind CSS classes to form fields"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Base classes for all inputs
            base_classes = (
                "block w-full rounded-lg border border-gray-300 bg-gray-50 "
                "p-2.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500 "
                "dark:border-gray-600 dark:bg-gray-700 dark:text-white "
                "dark:placeholder-gray-400 dark:focus:border-blue-500 dark:focus:ring-blue-500"
            )

            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs["class"] = base_classes + " min-h-[100px]"
                field.widget.attrs["rows"] = 4
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs["class"] = base_classes
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = (
                    "w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded "
                    "focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 "
                    "focus:ring-2 dark:bg-gray-700 dark:border-gray-600"
                )
            elif isinstance(field.widget, forms.DateInput):
                field.widget.attrs["class"] = base_classes
                field.widget.attrs["type"] = "date"
            else:
                field.widget.attrs["class"] = base_classes

            # Add placeholder
            if field.label:
                field.widget.attrs["placeholder"] = field.label


class CategoryForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = ["category"]
        labels = {"category": "Κατηγορία"}


class DiamerismaForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = Diamerisma
        fields = ["name", "num", "orofos", "sizesm", "owner", "guest"]
        widgets = {
            "sizesm": forms.NumberInput(attrs={"step": "0.01"}),
        }


class DiaxeiristisForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = Diaxeiristis
        fields = ["name", "date_from", "sex"]
        widgets = {
            "date_from": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure date field uses the correct format for HTML5 date input
        if self.instance and self.instance.pk:
            self.fields["date_from"].widget.attrs["value"] = (
                self.instance.date_from.strftime("%Y-%m-%d")
                if self.instance.date_from
                else ""
            )


class KoinoxristaForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = Koinoxrista
        fields = ["ekdosi", "diaxeiristis", "sxolia", "url", "published"]
        widgets = {
            "ekdosi": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "sxolia": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure date field uses the correct format for HTML5 date input
        if self.instance and self.instance.pk:
            self.fields["ekdosi"].widget.attrs["value"] = (
                self.instance.ekdosi.strftime("%Y-%m-%d")
                if self.instance.ekdosi
                else ""
            )


class XiliostaForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = Xiliosta
        fields = ["diamerisma", "category", "xiliosta"]


class DapanesForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = Dapanes
        fields = ["koinoxrista", "category", "par_date", "par_num", "par_per", "value"]
        widgets = {
            "par_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "value": forms.NumberInput(attrs={"step": "0.01"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure date field uses the correct format for HTML5 date input
        if self.instance and self.instance.pk and self.instance.par_date:
            self.fields["par_date"].widget.attrs["value"] = (
                self.instance.par_date.strftime("%Y-%m-%d")
            )


# Inline formset for Dapanes within Koinoxrista
DapanesFormSet = forms.inlineformset_factory(
    Koinoxrista, Dapanes, form=DapanesForm, extra=1, can_delete=True
)
