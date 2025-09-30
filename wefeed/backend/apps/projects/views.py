# from django.shortcuts import render
# from rest_framework import viewsets
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from datetime import datetime
from .models import Project
from .serializers import ProjectSerializer

# Create your views here.
# class ProjectViewSet(viewsets.ModelViewSet):
#     queryset = Project.objects.all()
#     serializer_class = ProjectSerializer

logger = logging.getLogger(__name__)

class ProjectCreateView(APIView):
    # Tạo project mới
    def post(self, request):
        logger.info("[PROJECT CREATE] Request received at %s", request.path)
        try:
            serializer = ProjectSerializer(data=request.data)
            if serializer.is_valid():
                project = serializer.save(created_day=datetime.now())
                logger.info("Project created successfully: id=%s, name=%s",
                            project.id, getattr(project, "name", None))
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            logger.warning("Project creation failed. Errors: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.exception("Error creating project")
            return Response({"error": f"Lỗi khi tạo project: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProjectDetailView(APIView):
    # Lấy thông tin project
    def get(self, request, pk):
        logger.info("[PROJECT DETAIL] Request received at %s for project_id=%s", request.path, pk)
        try:
            project = get_object_or_404(Project, pk=pk)
            logger.info("Project found: id=%s, name=%s", project.id, project.name)
            serializer = ProjectSerializer(project)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception("Error retrieving project id=%s", pk)
            return Response({"error": f"Lỗi khi lấy project: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Cập nhật project
    def put(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        serializer = ProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Xóa project
    def delete(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        project.delete()
        return Response({'message': 'Đã xóa project'}, status=status.HTTP_204_NO_CONTENT)


# Phân trang
class ProjectListView(APIView):
    def get(self, request):
        projects = Project.objects.all().order_by('-created_day')

        if not projects.exists():
            return Response({"detail": "Không có project nào."}, status=status.HTTP_404_NOT_FOUND)

        paginator = PageNumberPagination()
        paginator.page_size = 5  
        result_page = paginator.paginate_queryset(projects, request)
        serializer = ProjectSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)