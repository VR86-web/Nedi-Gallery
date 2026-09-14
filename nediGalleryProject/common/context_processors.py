from nediGalleryProject.common.models import InstagramPics, ArtDescription


def instagram_pics(request):
    pics = InstagramPics.objects.order_by('-id')[:6]

    return {
        'instagram_pics': pics
    }

def art_description(request):
    description = ArtDescription.objects.first()

    return {
        'art_description': description
    }
