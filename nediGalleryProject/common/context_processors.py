from nediGalleryProject.common.models import InstagramPics


def instagram_pics(request):
    pics = InstagramPics.objects.order_by('-id')[:6]

    return {
        'instagram_pics': pics
    }
