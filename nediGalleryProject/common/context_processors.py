from nediGalleryProject.common.models import AboutInnerContentLeft, AboutInnerContentRight, InstagramPics, ArtDescription


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

def about_inner_content_left(request):
    content = AboutInnerContentLeft.objects.first()

    return {
        'about_inner_content_left': content
    }

def about_inner_content_right(request):
    content = AboutInnerContentRight.objects.first()

    return {
        'about_inner_content_right': content
    }