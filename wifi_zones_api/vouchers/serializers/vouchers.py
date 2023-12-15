"""Vouchers serializers"""

# Utils
import random
from datetime import date

from django.core.exceptions import ObjectDoesNotExist
# Django
from django.utils.translation import gettext_lazy as _
# Django REST Framework
from rest_framework import serializers

# Api Caller
from wifi_zones_api.external_apis import ruijie
# Models
from wifi_zones_api.locations.models import Location
from wifi_zones_api.subscriptions.models import Subscription
from wifi_zones_api.users.models import User
from wifi_zones_api.vouchers.models import Voucher


class VoucherCreateModelSerializer(serializers.Serializer):
    """Subscription create model serializer."""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    long = serializers.DecimalField(max_digits=7, decimal_places=5)
    lat = serializers.DecimalField(max_digits=7, decimal_places=5)

    def validate(self, data):
        long = data.get("long")
        lat = data.get("lat")

        all_locations = Location.objects.all()
        threshold = 200  # meters

        location_found = False

        for location in all_locations:
            distance = location.distance_to(lat, long)
            if distance <= threshold:
                self.context["location"] = location
                location_found = True

        if not location_found:
            raise serializers.ValidationError(_("No internet access point near you."))

        try:
            subscription = Subscription.objects.get(user=data["user"], status="active")
            self.context["subscription"] = subscription
        except ObjectDoesNotExist:
            raise serializers.ValidationError(_("You have no active subscription."))

        return data

    def create(self, validated_data):
        try:
            code = str(random.random)[:16]
            location: Location = self.context["location"]
            subscription: Subscription = self.context["subscription"]
            user: User = validated_data["user"]
            voucher, created = Voucher.objects.get_or_create(user=user,
                                                             location=location, date=date.today(),
                                                             defaults={"connection_code": code})
            if created:
                if location.brand == "RU":
                    plans = ruijie.get_plans(location.external_id)
                    for plan in plans:
                        if plan["name"] == subscription.plan.slug_name:
                            data = {
                                "quantity": 1,
                                "profile": plan["authProfileId"],
                                "userGroupId": plan["id"],
                                "firstName": user.first_name,
                                "lastName": user.last_name,
                                "email": user.email,
                                "phone": user.phone_number,
                                "comment": ""
                            }

                            ruijie_voucher = ruijie.generate_voucher(data, location.external_id)
                            if not ruijie_voucher:
                                raise serializers.ValidationError(_("Error generating connection code."))

                            voucher.connection_code = ruijie_voucher.get("codeNo")
                            voucher.save()

                            return {
                                "location": location.name,
                                "connection_code": ruijie_voucher.get("codeNo")
                            }

                    raise serializers.ValidationError(_("Error fetching plan data from AP."))

            else:
                return {
                    "location": location.name,
                    "connection_code": voucher.connection_code
                }
        except:
            raise serializers.ValidationError(_("Error generating voucher."))


class VoucherResponseSerializer(serializers.Serializer):
    location = serializers.CharField()
    connection_code = serializers.CharField()
