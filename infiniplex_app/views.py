import concurrent.futures
import pandas as pd
from django.core.paginator import Paginator
from django.shortcuts import render

from infiniplex_app.forms import CSVUploadForm, SortForm, RowsPerPageForm
from infiniplex_app.models import Patient
from infiniplex_app.serializers import PatientSerializer

PATIENT_ID = 'patient_id'
OUTCOME = 'outcome'


def get_ordered_patients(request):
    """
    Order Patients :
    First Check if the user chooses order options in dropdown menu
    Then check if the user clicked on a table header
    Return by default ID, then last update.
    """
    sort_field, sort_order = None, None
    if 'primary_sort' in request.POST:
        order = [request.POST.get('primary_sort', 'patient_id'), request.POST.get('secondary_sort', '-updated_at')]
    elif 'sort' in request.GET:
        sort_field = request.GET['sort']
        sort_order = request.GET['order']
        order = [f"{'-' if sort_order == 'desc' else ''}{sort_field}"]
    else:
        order = ['patient_id', '-updated_at']
    patients = Patient.objects.all()
    if request.GET.get('patient_id_search'):
        patients = patients.filter(patient_id=request.GET.get('patient_id_search'))
    return patients.order_by(*order), sort_field, sort_order


def process_csv_file(request):
    """
    Check if the file is a valid CSV file, and process data.
    return : tuple : (Error, Success Message)
    """
    outcomes_file = request.FILES['csv_file']
    try:
        df = pd.read_csv(outcomes_file)
        df.columns = df.columns.str.replace(' ', '_').str.lower()
        if PATIENT_ID not in df.columns:
            return f'Error in Input File : Patient ID column is Missing.', None
        if OUTCOME not in df.columns:
            return f'Error in Input File : Outcome column is Missing.', None
    except Exception as e:
        return f"Please Enter a Valid CSV file.", None

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(save_patient, df.itertuples(index=False))

    return None, f'{df.shape[0]} rows were successfully uploaded !'


def save_patient(row):
    """Function to create and save a Patient instance."""
    Patient(patient_id=row.patient_id, outcome=row.outcome).save()

def upload_csv(request):
    csv_form = CSVUploadForm(request.POST)
    sort_form = SortForm(request.POST)
    rows_form = RowsPerPageForm(request.POST or None, initial={'rows_cnt': str(request.session['rows_per_page'])})
    error = None
    success_message = None

    if rows_form.data.get('rows_cnt'):
        request.session['rows_per_page'] = int(rows_form.data.get('rows_cnt'))

    if request.method == 'POST' and request.FILES.get('csv_file'):
        error, success_message = process_csv_file(request)
        if error is not None:
            csv_form = None

    patients, sort_field, sort_order = get_ordered_patients(request)

    paginator = Paginator(patients, request.session.get('rows_per_page', 100))
    page_number = request.GET.get('page', 1)
    patients_page = paginator.get_page(page_number)
    serialized_patients = PatientSerializer(patients_page, many=True).data

    return render(request, 'upload_csv.html',
                  {'form': csv_form, 'patients': serialized_patients,
                            'patients_page': patients_page,
                            'error_message': error, 'success_message': success_message,
                            'sort_field': sort_field, 'sort_order': sort_order,
                            'sort_form': sort_form, 'rows_form': rows_form})