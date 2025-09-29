# from django.shortcuts import render
# from rest_framework import viewsets
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

# Tạo bình luận mới
class CommentCreateView(APIView):
    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_day=datetime.now())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailView(APIView):
    def get(self, request, id):
        # Lấy chi tiết bình luận
        comment = get_object_or_404(Comment, id=id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        # Cập nhật bình luận
        comment = get_object_or_404(Comment, id=id)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        # Xóa bình luận
        comment = get_object_or_404(Comment, id=id)
        comment.delete()
        return Response({"message": "Bình luận đã được xoá."}, status=status.HTTP_204_NO_CONTENT)


# Trả lời bình luận
class CommentReplyView(APIView):
    def post(self, request, id):
        parent_comment = get_object_or_404(Comment, id=id)
        data = request.data.copy()
        # data['parent_id'] = parent_comment.id
        data['session_id'] = parent_comment.session_id
        data['created_day'] = datetime.now()

        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Mention người dùng khác
class CommentMentionView(APIView):
    def post(self, request, id):
        comment = get_object_or_404(Comment, id=id) 
        mentioned_user= request.data.get('user')

        if not mentioned_user:
            return Response({'error': 'Thiếu user_id để mention'}, status=status.HTTP_400_BAD_REQUEST)

        # Ở đây bạn có thể thêm logic gửi thông báo cho người được mention
        return Response({'message': f'Đã mention user {mentioned_user} trong comment {id}'}, status=status.HTTP_200_OK)


# Lấy tất cả bình luận của một phiên
class SessionCommentListView(APIView):
    def get(self, request, id):
        comments = Comment.objects.filter(session_id=id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)