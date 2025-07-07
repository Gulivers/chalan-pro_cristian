from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Crew, Truck, TruckAssignment, Category
from .serializers import CrewSerializer, TruckSerializer, TruckAssignmentSerializer
from rest_framework.views import APIView
from django.db import connection

# ViewSet para Truck
class TruckViewSet(viewsets.ModelViewSet):
    queryset = Truck.objects.all()
    serializer_class = TruckSerializer
    permission_classes = [IsAuthenticated]


# ViewSet para Crew
# Filtrado para los Resources del schedule.
class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.filter(category__isnull=False).order_by('id')
    serializer_class = CrewSerializer
    permission_classes = [IsAuthenticated]


# ViewSet para TruckAssignment
class TruckAssignmentViewSet(viewsets.ModelViewSet):
    queryset = TruckAssignment.objects.all()
    serializer_class = TruckAssignmentSerializer
    
    
class CategoryListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = Category.objects.values('id', 'name')
        return Response(categories)


class SupervisorCommunitiesView(APIView):
    def get(self, request):
        query = """
        SELECT
            au.username AS supervisor,
            j.name AS community_job
        FROM crewsapp_crew_members crm
        JOIN auth_user au ON crm.user_id = au.id
        JOIN crewsapp_crew_jobs crj ON crm.crew_id = crj.crew_id
        JOIN ctrctsapp_job j ON crj.job_id = j.id
        GROUP BY au.username, j.name
        ORDER BY au.username, j.name;
        """

        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        result = {}
        for supervisor, community in rows:
            result.setdefault(supervisor, []).append(community)

        return Response(result)