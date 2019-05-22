from django_messages.models import *
from rest_framework import serializers

from mobiles.models import *


class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDemograph


class DoctorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffDirectory


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffSpecialization


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class MobileMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientAttachment

class PatientBillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bills