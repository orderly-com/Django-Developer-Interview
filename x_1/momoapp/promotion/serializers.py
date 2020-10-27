from rest_framework import serializers
from promotion.models import PromotionFramework

class PromotionFrameworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionFramework
        fields = (
            'id',
            'cnid',
            'title',
            'title_hash',
            'slug',
            'publish_date',
            'url',
            'content',
            'read')

    # @property
    # def data(self):
    #     # call the super() to get the default serialized data
    #     serialized_data = super(PromotionFrameworkSerializer, self).data
    #     custom_representation = {'data': serialized_data}  # insert the above response in a dictionary
    #     return custom_representation

class RawStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionFramework
        fields = ['title','title_hash']