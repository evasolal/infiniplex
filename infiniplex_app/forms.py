from django import forms

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()

class PatientIDForm(forms.Form):
    patient_id = forms.IntegerField()