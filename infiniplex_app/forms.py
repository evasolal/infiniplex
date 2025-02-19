from django import forms

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(label='Upload a New Outcome File', required=False)


class SortForm(forms.Form):
    primary_sort = forms.ChoiceField(
        choices=[('patient_id', 'Patient ID'), ('updated_at', 'Date/Time'), ('outcome', 'Outcome')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Sort by",
        initial=None,
        required=False
    )

    secondary_sort = forms.ChoiceField(
        choices=[('patient_id', 'Patient ID'), ('updated_at', 'Date/Time'), ('outcome', 'Outcome')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Then by",
        required=False
    )


class RowsPerPageForm(forms.Form):
    rows_cnt = forms.ChoiceField(
        choices=[('10', '10'), ('25', '25'), ('50', '50'), ('100', '100'), ('200', '200')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Rows Per Page",
        initial='100',
        required=False)