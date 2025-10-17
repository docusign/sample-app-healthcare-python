from rest_framework.serializers import Serializer, CharField, EmailField, URLField, BooleanField

class RequestMedicalRecordsSerializer(Serializer):
    name=CharField()
    email=EmailField()

class Covid19ConsentFormSerializer(Serializer):
    first_name=CharField()
    last_name=CharField()
    country_code=CharField(
        max_length=5, min_length=1, allow_blank=False, trim_whitespace=True
    )
    phone_number=CharField(
        max_length=15, min_length=2, allow_blank=False, trim_whitespace=True
    )

class ApplyForPatientAssistanceSerializer(Serializer):
    first_name=CharField()
    last_name=CharField()
    email=EmailField()
    useWithoutExtension=BooleanField()
    return_url=URLField(
        max_length=200, min_length=None, allow_blank=False
    )
