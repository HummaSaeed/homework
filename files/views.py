from rest_framework import viewsets, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import UploadedFile
from .serializers import UploadedFileSerializer

ALLOWED_EXTENSIONS = ['.pdf', '.docx', '.doc', '.pptx', '.ppt', '.png', '.jpg', '.jpeg', '.gif', '.zip']
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB


class FileViewSet(viewsets.ModelViewSet):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return super().get_queryset()
        return super().get_queryset().filter(uploaded_by=user)

    def create(self, request, *args, **kwargs):
        uploaded = request.FILES.get('file')
        if not uploaded:
            return Response({'error': 'No file provided.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate extension
        import os
        _, ext = os.path.splitext(uploaded.name)
        if ext.lower() not in ALLOWED_EXTENSIONS:
            return Response(
                {'error': f'File type not allowed. Allowed: {", ".join(ALLOWED_EXTENSIONS)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Validate size
        if uploaded.size > MAX_FILE_SIZE:
            return Response(
                {'error': 'File size exceeds 20MB limit.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().create(request, *args, **kwargs)

    def perform_destroy(self, instance):
        # Remove actual file from disk before deleting DB record
        if instance.file:
            import os
            if os.path.isfile(instance.file.path):
                os.remove(instance.file.path)
        instance.delete()
