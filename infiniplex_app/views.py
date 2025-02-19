import csv
import datetime

import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render

from infiniplex_app.forms import CSVUploadForm, PatientIDForm
from infiniplex_app.models import Patient
from infiniplex_app.serializers import PatientSerializer

PATIENT_ID = 'patient_id'
OUTCOME = 'outcome'

def upload_csv(request):
    form = CSVUploadForm()
    # patient_id_form = PatientIDForm
    error = None
    success_message = None

    if request.method == 'POST' and request.FILES['csv_file']:
        outcomes_file = request.FILES['csv_file']
        try:
            df = pd.read_csv(outcomes_file)
            df.columns = df.columns.str.replace(' ', '_').str.lower()
            if PATIENT_ID not in df.columns:
                error = f'Error in Input File : Patient ID column is Missing.'
            elif OUTCOME not in df.columns:
                error = f'Error in Input File : Outcome column is Missing.'
        except Exception as e:
            error = f"Please Enter a Valid CSV file."

        if error is None:
            start_time  = datetime.datetime.now()
            for row in df.itertuples():
                Patient(patient_id=row.patient_id, outcome=row.outcome).save()
            success_message = f'{df.shape[0]} rows were successfully uploaded !'
            form = None
            print(datetime.datetime.now() - start_time)

    # patients = Patient.objects.values('patient_id', 'outcome', 'updated_at', 'last_updated').order_by('patient_id', '-updated_at')
    patients = Patient.objects.all().order_by('patient_id', '-updated_at')
    serialized_patients = PatientSerializer(patients, many=True).data
    return render(request, 'upload_csv.html',
                  {'form': form, 'patients': serialized_patients,
                            'error_message': error, 'success_message': success_message})