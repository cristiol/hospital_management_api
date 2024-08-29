from rest_framework import status
from rest_framework.views import APIView
from doctors.models import Doctor
from patients.models import Patient
from rest_framework.response import Response
from doctors.permissions import IsDoctor
from users.permissions import IsGeneralManager
from treatments.serializers import TreatmentSerializer


class DoctorPatientReportView(APIView):
    permission_classes = [IsGeneralManager]

    def get(self, request):
        doctors = Doctor.objects.prefetch_related('patient_set').all()

        report_data = [
            {
                'doctor': doctor.name,  # Accessing the `name` property directly
                'patients': list(
                    doctor.patient_set.filter(user__full_name__isnull=False)  # Adjusting the filter
                    .values_list('user__full_name', flat=True)  # Assuming Patient links to User
                )
            }
            for doctor in doctors
        ]
        return Response(report_data)


class PatientTreatmentReportView(APIView):
    permission_classes = [IsGeneralManager | IsDoctor]

    def get(self, request, pk):
        try:
            patient = Patient.objects.get(pk=pk)
        except Patient.DoesNotExist:
            return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)

        applied_treatments = []
        if patient.applied_treatment:
            serializer = TreatmentSerializer(patient.applied_treatment)
            applied_treatments.append(serializer.data)

        return Response({"patient": patient.name, "applied_treatments": applied_treatments})
