from rest_framework import serializers
from learner.models.payments import Payments

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = ['id', 'amount', 'transaction_code', 'paymentMode', 'enrollement', 'payed_on', 'created_by']
        read_only_fields = ['created_by', 'payed_on']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
