from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from django.utils import timezone
from .models import Paint


class PaintSerializer(serializers.Serializer):
    # class Meta:
    #     model = Paint
    #     fields = ('data', 'describe', 'pub_date')
    data = serializers.CharField()
    describe = serializers.CharField()
    pub_date = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        # 创建一个新的对象
        print('create')
        return self.create(self, validated_data)

    def update(self, instance, validated_data):
        # 更新一个对象时
        print('update')

        return super.update(self, instance, validated_data)
