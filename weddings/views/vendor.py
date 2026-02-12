from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from weddings.models import WeddingProfile
from vendors.models import Vendor, VendorCategory, UserVendorSelection

@login_required
def vendor_main(request):
    try:
        profile = request.user.wedding_profile
        group = profile.group
        # if not group: pass
    except WeddingProfile.DoesNotExist:
        pass

    context = {
        'my_selected_vendors': UserVendorSelection.objects.filter(profile=profile, status='final').select_related('vendor', 'vendor__category'),
        'vendor_categories': VendorCategory.objects.all(),
        'recommended_vendors': Vendor.objects.all()[:4],
    }
    return render(request, 'weddings/vendor_main.html', context)
