from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BlogSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Blog
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination

class PublicBlog(APIView):
    def get(self, request):
        try:
            
            blogs = Blog.objects.all().order_by('?')

            if request.GET.get('uid'):
                uid = request.GET.get('uid')
                blogs = blogs.filter(uid = uid)

            if request.GET.get('search'):
                search = request.GET.get('search')
                blogs = blogs.filter(Q(title__icontains = search) | Q(blog_text__icontains = search))


            paginator = PageNumberPagination()
            paginator.page_size = 4                     # <-- how many per page

        # 4. Let paginator slice the queryset according to ?page=
            page = paginator.paginate_queryset(blogs, request)

        # 5. Serialize just that page of objects
            serializer = BlogSerializer(page, many=True)

        # 6. Return a fully paginated response
            return paginator.get_paginated_response(serializer.data)
        
        except Exception as e:
            return Response({
                'data': {}, 
                       'message': 'something went wrong or invalid page'}, status= status.HTTP_400_BAD_REQUEST
                       )

class BlogView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            
            blogs = Blog.objects.filter(user = request.user)

            if request.GET.get('search'):
                search = request.GET.get('search')
                blogs = blogs.filter(Q(title__icontains = search) | Q(blog_text__icontains = search))

            if request.GET.get('uid'):
                uid = request.GET.get('uid')
                blogs = blogs.filter(uid = uid)
               


            serializer = BlogSerializer(blogs, many = True)

            return Response({'data': serializer.data,
                                 'message': 'Blog fetched successfully'}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({
                'data': {}, 
                       'message': 'something went wrong'}, status= status.HTTP_400_BAD_REQUEST
                       )



    def post(self, request):
        try:
            data = request.data
            data['user'] = request.user.id


            serializer = BlogSerializer(data = data)

            if not serializer.is_valid():
                return Response({'data': serializer.errors,
                                 'message': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()

            return Response({'data': serializer.data,
                                 'message': 'Blog created successfully'}, status=status.HTTP_201_CREATED)
          

        except Exception as e:
            return Response({
                'data': {}, 
                       'message': 'something went wrong'}, status= status.HTTP_400_BAD_REQUEST
                       )


    def patch(self, request):
        try:
            data = request.data
            
            blog = Blog.objects.filter(uid = data.get('uid'))

            if not blog.exists():
                return Response({
                    'data': {},
                    'message': 'Invalid blog uid'
                }, status= status.HTTP_400_BAD_REQUEST)
            

            if request.user != blog[0].user:
                return Response({
                    'data': {},
                    'message': 'You are not authorized to do this'
                }, status= status.HTTP_400_BAD_REQUEST)
            
            serializer = BlogSerializer(blog[0], data = data, partial = True) 
            
            if not serializer.is_valid():
                return Response({'data': serializer.errors,
                                 'message': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()

            return Response({'data': serializer.data,
                                 'message': 'Blog updated successfully'}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({
                'data': {}, 
                       'message': 'something went wrong'}, status= status.HTTP_400_BAD_REQUEST
                       )


    def delete(self, request):
        try:
            data = request.data
            
            blog = Blog.objects.filter(uid = data.get('uid'))

            if not blog.exists():
                return Response({
                    'data': {},
                    'message': 'Invalid blog uid'
                }, status= status.HTTP_400_BAD_REQUEST)
            

            if request.user != blog[0].user:
                return Response({
                    'data': {},
                    'message': 'You are not authorized to do this'
                }, status= status.HTTP_400_BAD_REQUEST)
            
            blog[0].delete()

            return Response({'data': {},
                                 'message': 'Blog deleted successfully'}, status=status.HTTP_204_NO_CONTENT)    
            
        
        except Exception as e:
            return Response({
                'data': {}, 
                       'message': 'something went wrong'}, status= status.HTTP_400_BAD_REQUEST
                       )                 