from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import sekolah, jenjang, kelas, mata_pelajaran
from .serializers import (
    SekolahSerializer, 
    JenjangSerializer, 
    KelasSerializer, 
    MataPelajaranSerializer
)
from rest_framework.decorators import action

class BaseAtributViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='bulk-delete')
    def bulk_delete(self, request):
        try:
            ids = request.data.get('ids', [])
            if not ids:
                return Response(
                    {'error': 'Tidak ada ID yang diberikan'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            self.get_queryset().filter(id__in=ids).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class SekolahViewSet(BaseAtributViewSet):
    queryset = sekolah.objects.all()
    serializer_class = SekolahSerializer

class JenjangViewSet(BaseAtributViewSet):
    queryset = jenjang.objects.all()
    serializer_class = JenjangSerializer

class KelasViewSet(BaseAtributViewSet):
    queryset = kelas.objects.all()
    serializer_class = KelasSerializer
    
    def get_queryset(self):
        return self.queryset.select_related('jenjang')

    @action(detail=False, methods=['get'])
    def by_jenjang(self, request):
        jenjang_id = request.query_params.get('jenjang_id')
        if jenjang_id:
            kelas_list = kelas.objects.filter(jenjang_id=jenjang_id)
            serializer = self.get_serializer(kelas_list, many=True)
            return Response(serializer.data)
        return Response({'error': 'jenjang_id parameter diperlukan'}, status=400)

class MataPelajaranViewSet(BaseAtributViewSet):
    queryset = mata_pelajaran.objects.all()
    serializer_class = MataPelajaranSerializer
    

