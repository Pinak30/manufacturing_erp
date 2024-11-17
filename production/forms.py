from django import forms
from .models import BOM, Sku, RawMaterial, Designation

class BOMForm(forms.Form):
    bom_id = forms.IntegerField(required=False, widget=forms.HiddenInput())  # Hidden for updates

    sku_id = forms.ChoiceField(
        label="SKU",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    raw_material_id = forms.MultipleChoiceField(
        label="Raw Materials",
        widget=forms.CheckboxSelectMultiple(),
    )

    qty_required = forms.CharField(
        label="Quantities Required (comma-separated)",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    machine_required = forms.CharField(
        label="Machines Required (comma-separated)",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    designation_id = forms.MultipleChoiceField(
        label="Designations",
        widget=forms.CheckboxSelectMultiple(),
    )

    required_worker = forms.CharField(
        label="Workers Required (comma-separated)",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    by_product = forms.CharField(
        label="By-products (comma-separated)",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
    )

    qty_to_be_produced = forms.IntegerField(
        label="Quantity to Be Produced",
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate choices dynamically
        self.fields['sku_id'].choices = [(sku.sku_id, sku.sku_name) for sku in Sku.objects.all()]
        self.fields['raw_material_id'].choices = [
            (rm.raw_material_id, rm.raw_material_name) for rm in RawMaterial.objects.all()
        ]
        self.fields['designation_id'].choices = [
            (des.designation_id, des.designation_name) for des in Designation.objects.all()
        ]

    def save(self, instance=None):
        data = self.cleaned_data
        raw_material_ids = list(map(int, data['raw_material_id']))
        qty_required = list(map(float, data['qty_required'].split(',')))
        machine_required = data['machine_required'].split(',')
        designation_ids = list(map(int, data['designation_id']))
        required_worker = list(map(int, data['required_worker'].split(',')))
        by_product = (
            list(map(int, data['by_product'].split(','))) if data['by_product'] else []
        )

        if instance:  # Update existing BOM
            b_o_m = instance
        else:  # Create new BOM
            b_o_m = BOM()

        b_o_m.sku_id = int(data['sku_id'])
        b_o_m.raw_material_id = raw_material_ids
        b_o_m.qty_required = qty_required
        b_o_m.machine_required = machine_required
        b_o_m.designation_id = designation_ids
        b_o_m.required_worker = required_worker
        b_o_m.by_product = by_product
        b_o_m.qty_to_be_produced = data['qty_to_be_produced']
        b_o_m.save()
        return b_o_m
