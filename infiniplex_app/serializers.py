from rest_framework import serializers
from infiniplex_app.models import Patient
from django.template.defaultfilters import date as date_filter

class PatientSerializer(serializers.ModelSerializer):
    formatted_date = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = ['patient_id', 'outcome', 'formatted_date', 'last_updated']

    def get_formatted_date(self, obj):
        return date_filter(obj.updated_at, "d/m/Y H:i:s")
