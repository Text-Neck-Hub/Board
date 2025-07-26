class BoardViewSet(viewsets.ModelViewSet):
    """
    게시판(카테고리) 리소스에 대한 CRUD API 뷰셋.
    게시판 생성, 수정, 삭제는 관리자만 가능하도록 설정.
    """
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
