# from django.shortcuts import render
# from rest_framework import viewsets
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from datetime import datetime
from .models import Canvas
from .serializers import CanvasSerializer

# Create your views here.
# class CanvasViewSet(viewsets.ModelViewSet):
#     queryset = Canvas.objects.all()
#     serializer_class = CanvasSerializer

logger = logging.getLogger(__name__)

class CanvasCreateView(APIView):
    # Tạo canvas mới
    def post(self, request):
        logger.info("[CANVAS CREATE] Request received at %s", request.path)
        try:
            serializer = CanvasSerializer(data=request.data)
            if serializer.is_valid():
                canvas = serializer.save(created_day=datetime.now())
                success_message = f"Canvas '{getattr(canvas, 'name', '')}' đã được tạo thành công"
                
                # Logging thành công
                logger.info("%s (id=%s)", success_message, canvas.id)

                return Response(
                    {
                        "message": success_message,
                        **serializer.data
                    },
                    status=status.HTTP_201_CREATED
                )

            logger.warning("Canvas creation failed. Errors: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.exception("Error creating canvas")
            return Response({"error": f"Lỗi khi tạo canvas: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CanvasDetailView(APIView):
    # Lấy thông tin canvas
    def get(self, request, id):
        logger.info("[CANVAS DETAIL] Yêu cầu lấy thông tin canvas id=%s", id)
        try:
            canvas = get_object_or_404(Canvas, id=id)
            serializer = CanvasSerializer(canvas)
            logger.info("[CANVAS DETAIL] Canvas(id=%s, name='%s') lấy thành công",
                        canvas.id, getattr(canvas, "name", ""))
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception("[CANVAS DETAIL] Lỗi khi lấy canvas id=%s: %s", id, str(e))
            return Response({"error": f"Lỗi khi lấy canvas: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Cập nhật canvas
    def put(self, request, id):
        logger.info("[CANVAS UPDATE] Yêu cầu cập nhật canvas id=%s", id)
        try:
            canvas = get_object_or_404(Canvas, id=id)
            serializer = CanvasSerializer(canvas, data=request.data, partial=True)
            if serializer.is_valid():
                updated = serializer.save()
                logger.info("[CANVAS UPDATE] Canvas(id=%s, name='%s') đã cập nhật thành công",
                            updated.id, getattr(updated, "name", ""))
                return Response(
                    {"message": "Canvas đã được cập nhật thành công", **serializer.data},
                    status=status.HTTP_200_OK
                )
            logger.warning("[CANVAS UPDATE] Dữ liệu không hợp lệ: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("[CANVAS UPDATE] Lỗi khi cập nhật canvas id=%s: %s", id, str(e))
            return Response({"error": f"Lỗi khi cập nhật canvas: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Xóa canvas
    def delete(self, request, id):
        logger.info("[CANVAS DELETE] Yêu cầu xóa canvas id=%s", id)
        try:
            canvas = get_object_or_404(Canvas, id=id)
            canvas_name = getattr(canvas, "name", "")
            canvas.delete()
            logger.info("[CANVAS DELETE] Canvas(id=%s, name='%s') đã được xóa thành công",
                        id, canvas_name)
            return Response({"message": f"Canvas '{canvas_name}' đã được xóa thành công"},
                            status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.exception("[CANVAS DELETE] Lỗi khi xóa canvas id=%s: %s", id, str(e))
            return Response({"error": f"Lỗi khi xóa canvas: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)