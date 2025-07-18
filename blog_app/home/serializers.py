from rest_framework import serializers
from .models import Blog

class BlogSerializer(serializers.ModelSerializer):
    main_image = serializers.ImageField(required=False, allow_null = True)
    class Meta:
        model = Blog
        exclude = ['created_at', 'updated_at']