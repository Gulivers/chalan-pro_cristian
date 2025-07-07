from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework import serializers, viewsets
from .models import WorkPrice, Contract, ContractDetails, Builder, Job, HouseModel
from crewsapp.models import Crew

import logging

logger = logging.getLogger(__name__)

# Serializer for the Builder model
# Serializador para el modelo Builder
class BuilderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Builder
        fields = ['id', 'name', 'trim_amount', 'rough_amount', 'travel_price_amount']

# Serializer for the Job model, including the builder
# Serializador para el modelo Job, incluyendo el builder
class JobSerializer(serializers.ModelSerializer):
    builder = serializers.PrimaryKeyRelatedField(queryset=Builder.objects.all())
    crew_leaders = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = ['id', 'name', 'builder', 'address', 'latitude', 'longitude', 'crew_leaders']

    def get_crew_leaders(self, obj):
        # Importación diferida para evitar referencias circulares
        crews = Crew.objects.filter(jobs=obj)
        return [crew.name for crew in crews]

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


# Serializer for the HouseModel model, including related jobs
class HouseModelSerializer(serializers.ModelSerializer):
    jobs = serializers.PrimaryKeyRelatedField(queryset=Job.objects.all(), many=True)

    class Meta:
        model = HouseModel
        fields = ['id', 'name', 'jobs']

    def create(self, validated_data):
        # Extract jobs from validated data
        jobs = validated_data.pop('jobs', [])
        # Create the HouseModel instance
        house_model = HouseModel.objects.create(**validated_data)
        # Add the jobs to the ManyToMany field
        house_model.jobs.set(jobs)
        return house_model

    def update(self, instance, validated_data):
        # Extract jobs from validated data
        jobs = validated_data.pop('jobs', [])
        # Update the HouseModel instance
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        # Update the ManyToMany field
        instance.jobs.set(jobs)
        return instance

# Serializer for the ContractDetails model
# Serializador para el modelo ContractDetails
class ContractDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractDetails
        fields = ['id', 'cdname', 'cdtrim', 'cdrough', 'cdunit_price', 'cdwork_price', 'contract_details', 'cdtrim_qty', 'cdrough_qty']

# Serializer for the WorkPrice model
# Serializador para el modelo WorkPrice
class WorkPriceSerializer(serializers.ModelSerializer):
    builders = serializers.PrimaryKeyRelatedField(many=True, queryset=Builder.objects.all())

    class Meta:
        model = WorkPrice
        fields = ['id', 'name', 'trim', 'rough', 'unit_price', 'builders']

    # Create a new WorkPrice instance and set its builders
    # Crear una nueva instancia de WorkPrice y asignar sus builders
    def create(self, validated_data):
        builders_data = validated_data.pop('builders')
        work_price = WorkPrice.objects.create(**validated_data)
        work_price.builders.set(builders_data)
        return work_price

    # Update an existing WorkPrice instance and set its builders
    # Actualizar una instancia existente de WorkPrice y asignar sus builders
    def update(self, instance, validated_data):
        builders_data = validated_data.pop('builders', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if builders_data is not None:
            instance.builders.set(builders_data)
        return instance

# Serializer for the Contract model
# Serializador para el modelo Contract
class ContractSerializer(serializers.ModelSerializer):
    contract_details = ContractDetailsSerializer(many=True)
    house_model = HouseModelSerializer(read_only=True)
    builder = BuilderSerializer(read_only=True)
    job = JobSerializer(read_only=True)
    house_model_id = serializers.PrimaryKeyRelatedField(queryset=HouseModel.objects.all(), source='house_model', write_only=True)
    builder_id = serializers.PrimaryKeyRelatedField(queryset=Builder.objects.all(), source='builder', write_only=True)
    job_id = serializers.PrimaryKeyRelatedField(queryset=Job.objects.all(), source='job', write_only=True)

    class Meta:
        model = Contract
        fields = [
            'id', 'created_by', 'date_created', 'last_updated', 'type', 'builder', 'builder_id',
            'job', 'job_id', 'house_model', 'house_model_id', 'lot', 'sqft', 'address', 'job_price', 'travel_price', 
            'total_options', 'total', 'comment', 'file', 'contract_details', 'needs_reprint', 'doc_type',
        ]
        read_only_fields = ['id', 'date_created', 'last_updated']

    # Create a new Contract instance with validated data
    # Crear una nueva instancia de Contract con datos validados
    def create(self, validated_data):
        contract_details_data = validated_data.pop('contract_details')
        builder = validated_data.pop('builder')
        job = validated_data.pop('job')
        house_model = validated_data.pop('house_model')

        validated_data['travel_price'] = builder.travel_price_amount  # Usa el travel_price_amount del builder

        with transaction.atomic():
            # Create the contract with validated data
            # Crear el contrato con los datos validados
            contract = Contract.objects.create(
                **validated_data,
                builder=builder,
                job=job,
                house_model=house_model
            )

            for detail_data in contract_details_data:
                detail_data['contract_details_id'] = contract.id

                ContractDetails.objects.create(**detail_data)

        return contract

    # Update an existing Contract instance with validated data
    # Actualizar una instancia existente de Contract con datos validados
    def update(self, instance, validated_data):
        # Extract nested data
        # Extraer datos anidados
        contract_details_data = validated_data.pop('contract_details', None)
        builder_id = validated_data.pop('builder_id', None)
        job_id = validated_data.pop('job_id', None)
        house_model_id = validated_data.pop('house_model_id', None)

        with transaction.atomic():
            # Update foreign key relationships if they exist
            # Actualizar relaciones de clave foránea si existen
            if builder_id:
                instance.builder = Builder.objects.get(id=builder_id)
                instance.travel_price = instance.builder.travel_price_amount  # Usa el travel_price_amount del builder

            if job_id:
                instance.job = Job.objects.get(id=job_id)

            if house_model_id:
                instance.house_model = HouseModel.objects.get(id=house_model_id)

            # Update other contract fields
            # Actualizar otros campos del contrato
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

            # Handle contract details
            # Manejar los detalles del contrato
            if contract_details_data is not None:
                # Delete existing details
                # Eliminar detalles existentes
                ContractDetails.objects.filter(contract_details=instance).delete()
                # Create new details
                # Crear nuevos detalles
                for detail_data in contract_details_data:
                    # Ensure the 'contract_details' field is not passed twice
                    # Asegúrate de no pasar el campo 'contract_details' dos veces
                    ContractDetails.objects.create(contract_details=instance, **detail_data)

        return instance

# Serializer for the Job model filtered by builder
# Serializador para el modelo Job filtrado por builder
class JobFilteredByBuilderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'name', 'builder', 'address', 'latitude', 'longitude']

# Serializer for the HouseModel model filtered by job
# Serializador para el modelo HouseModel filtrado por job
class HouseModelFilteredByJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseModel
        fields = ['id', 'name', 'jobs']


# Serializers for list options
class BuilderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Builder
        fields = ['id', 'name']


class JobListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'name', 'address', 'builder']


class HouseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseModel
        fields = ['id', 'name', 'jobs']

class ContractListSerializer(serializers.ModelSerializer):
    builder = BuilderSerializer()
    job = JobSerializer()
    house_model = HouseModelSerializer()

    class Meta:
        model = Contract
        fields = ['id', 'type', 'builder', 'job', 'house_model', 'lot', 'address', 'sqft', 'job_price', 'total_options', 'total', 'needs_reprint', 'doc_type', 'date_created']
