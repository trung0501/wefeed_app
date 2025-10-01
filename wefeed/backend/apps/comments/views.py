# from django.shortcuts import render
# from rest_framework import viewsets
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from datetime import datetime
from .models import Comment
from .serializers import CommentSerializer

# Create your views here.
# class CommentViewSet(viewsets.ModelViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer

logger = logging.getLogger(__name__)

# Tạo bình luận mới
class CommentCreateView(APIView):
    def post(self, request):
        logger.info("[COMMENT CREATE] Bắt đầu tạo bình luận")
        try:
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                comment = serializer.save(created_day=datetime.now())
                logger.info("[COMMENT CREATE] Bình luận(id=%s) đã được tạo thành công",
                            comment.id)
                return Response(
                    {
                        "message": f"Bình luận id={comment.id} đã được tạo thành công",
                        **serializer.data
                    },
                    status=status.HTTP_201_CREATED
                )

            logger.warning("[COMMENT CREATE] Dữ liệu không hợp lệ: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.exception("[COMMENT CREATE] Lỗi khi tạo bình luận: %s", str(e))
            return Response({"error": f"Lỗi khi tạo bình luận: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CommentDetailView(APIView):
    # Lấy chi tiết bình luận
    def get(self, request, id):
        logger.info("[COMMENT DETAIL] Yêu cầu lấy thông tin bình luận id=%s", id)
        try:
            comment = get_object_or_404(Comment, id=id)
            serializer = CommentSerializer(comment, context={"request": request})
            logger.info("[COMMENT DETAIL] Bình luận(id=%s) lấy thành công", comment.id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception("[COMMENT DETAIL] Lỗi khi lấy bình luận id=%s: %s", id, str(e))
            return Response({"error": f"Lỗi khi lấy bình luận: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Cập nhật bình luận
    def put(self, request, id):
        logger.info("[COMMENT UPDATE] Yêu cầu cập nhật bình luận id=%s", id)
        try:
            comment = get_object_or_404(Comment, id=id)
            serializer = CommentSerializer(comment, data=request.data, partial=True)
            if serializer.is_valid():
                updated = serializer.save()
                logger.info("[COMMENT UPDATE] Bình luận(id=%s) đã cập nhật thành công", updated.id)
                return Response(
                    {"message": "Bình luận đã được cập nhật thành công", **serializer.data},
                    status=status.HTTP_200_OK
                )
            logger.warning("[COMMENT UPDATE] Dữ liệu không hợp lệ: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("[COMMENT UPDATE] Lỗi khi cập nhật bình luận id=%s: %s", id, str(e))
            return Response({"error": f"Lỗi khi cập nhật bình luận: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Xóa bình luận
    def delete(self, request, id):
        logger.info("[COMMENT DELETE] Yêu cầu xóa bình luận id=%s", id)
        try:
            comment = get_object_or_404(Comment, id=id)
            comment.delete()
            logger.info("[COMMENT DELETE] Bình luận(id=%s) đã được xóa thành công", id)
            return Response({"message": f"Bình luận id={id} đã được xóa thành công"},
                            status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.exception("[COMMENT DELETE] Lỗi khi xóa bình luận id=%s: %s", id, str(e))
            return Response({"error": f"Lỗi khi xóa bình luận: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Trả lời bình luận
class CommentReplyView(APIView):
    def post(self, request, id):
        logger.info("[COMMENT REPLY] Yêu cầu trả lời bình luận cha id=%s", id)
        try:
            parent_comment = get_object_or_404(Comment, id=id)
            data = request.data.copy()

            # Gán session từ bình luận cha
            data["session_id"] = parent_comment.session_id
            data["created_day"] = datetime.now()
            # lưu quan hệ cha-con:
            data["parent_id"] = parent_comment.id  

            serializer = CommentSerializer(data=data)
            if serializer.is_valid():
                reply = serializer.save()
                logger.info("[COMMENT REPLY] Bình luận con(id=%s) đã được tạo thành công, thuộc bình luận cha id=%s",
                            reply.id, parent_comment.id)
                return Response(
                    {
                        "message": f"Trả lời bình luận id={parent_comment.id} thành công",
                        **serializer.data
                    },
                    status=status.HTTP_201_CREATED
                )
            
            logger.warning("[COMMENT REPLY] Dữ liệu không hợp lệ khi trả lời bình luận id=%s: %s",
                           id, serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.exception("[COMMENT REPLY] Lỗi khi trả lời bình luận id=%s: %s", id, str(e))
            return Response({"error": f"Lỗi khi trả lời bình luận: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Mention người dùng khác
class CommentMentionView(APIView):
    def post(self, request, id):
        logger.info("[COMMENT MENTION] Yêu cầu mention user trong bình luận id=%s", id)
        try:
            comment = get_object_or_404(Comment, id=id)
            mentioned_user = request.data.get("user")

            if not mentioned_user:
                logger.warning("[COMMENT MENTION] Thiếu user_id khi mention trong comment id=%s", id)
                return Response(
                    {"error": "Thiếu user_id để mention"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            logger.info("[COMMENT MENTION] User id=%s đã được mention trong comment id=%s",
                        mentioned_user, comment.id)

            return Response(
                {"message": f"Đã mention user {mentioned_user} trong comment {comment.id}"},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            logger.exception("[COMMENT MENTION] Lỗi khi mention user trong comment id=%s: %s", id, str(e))
            return Response(
                {"error": f"Lỗi khi mention user: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# Lấy tất cả bình luận của một phiên
class SessionCommentListView(APIView):
    def get(self, request, id):
        logger.info("[SESSION COMMENTS] Yêu cầu lấy tất cả bình luận của session id=%s", id)
        try:
            # Kiểm tra session tồn tại
            session = get_object_or_404(Comment, id=id)
            logger.info("[SESSION COMMENTS] Session(id=%s, title='%s') tồn tại",
                        session.id, getattr(session, "title", ""))

            # Lấy tất cả comment thuộc session
            comments = Comment.objects.filter(session_id=id).order_by("-created_day")
            logger.info("[SESSION COMMENTS] Tìm thấy %s bình luận trong session id=%s",
                        comments.count(), id)

            serializer = CommentSerializer(comments, many=True, context={"request": request})
            logger.info("[SESSION COMMENTS] Trả về danh sách bình luận cho session id=%s", id)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.exception("[SESSION COMMENTS] Lỗi khi lấy bình luận của session id=%s: %s", id, str(e))
            return Response(
                {"error": f"Lỗi khi lấy bình luận: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )