from django.db import models

# Create your models here.
class Patient(models.Model):
    patient_id = models.IntegerField()
    outcome = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    last_updated = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        existing_patient = Patient.objects.filter(patient_id=self.patient_id, last_updated=True)
        if existing_patient:
            existing_patient.update(last_updated=False)
            # existing_patient_instance = existing_patient.first()
            # PatientHistory.objects.create(patient_id=self.patient_id,
            #                               outcome=existing_patient_instance.outcome,
            #                               created_at=existing_patient_instance.updated_at)
            # existing_patient.update(outcome=self.outcome)
        super().save(*args, **kwargs)


# class PatientHistory(models.Model):
#     patient_id = models.IntegerField()
#     outcome = models.CharField(max_length=255)
#     created_at = models.DateTimeField(auto_now=True)
