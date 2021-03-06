import base64
import random
from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import render, redirect

from jigsaw.models import Picture


def make_image_data(im, format):
    bio = BytesIO()
    im.save(bio, format)
    bio.seek(0)
    b = bio.read()
    s = base64.b64encode(b).decode()
    return 'data:image;base64,%s' % s


def index(request):
    id = request.GET.get('id', 0)
    p = Picture.objects.filter(id__gte=id).order_by('id').first()

    if not p:
        p = Picture.objects.order_by('id').first()

    im = Image.open(p.pic)
    w, h = im.size

    # 把图片变成高度 400
    w = int(400 * w / h)
    h = 400
    im0 = im.resize((w, h), 1)

    # 水平垂直切两刀，n 为垂直切点位于图片宽度的百分比，m 为水平切点位于图片高度的百分比
    # x 为垂直切点坐标，y 为水平切点坐标
    n = random.randint(20, 80)
    m = random.randint(20, 80)
    x = int(w * n / 100)
    y = int(h * m / 100)

    im1 = im0.crop((0, 0, x, y))
    im2 = im0.crop((x, 0, w, y))
    im3 = im0.crop((0, y, x, h))
    im4 = im0.crop((x, y, w, h))

    p1 = make_image_data(im1, im.format)
    p2 = make_image_data(im2, im.format)
    p3 = make_image_data(im3, im.format)
    p4 = make_image_data(im4, im.format)

    next_id = p.id + 1

    zan = 'imgs/z0%d.jpg' % random.randint(1, 7)

    pos = [
        "top: %dpx; left: %dpx" % (random.randint(10, 100), random.randint(10, 100)),
        "top: %dpx; right: %dpx" % (random.randint(10, 100), random.randint(10, 100)),
        "bottom: %dpx; left: %dpx" % (random.randint(10, 100), random.randint(10, 100)),
        "bottom: %dpx; right: %dpx" % (random.randint(10, 100), random.randint(10, 100)),
    ]
    random.shuffle(pos)

    return render(request, 'index.html', locals())


def media(request, path):
    return redirect('/static/media/' + path)


