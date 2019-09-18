import random

from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Image, ImageVote



# Create your views here.


def index(request):
    template = loader.get_template('image_voter/index.html')
    context = {}
    return HttpResponse(template.render(context, request))

def choice(request):
    template = loader.get_template('image_voter/choice.html')

    image_1_id = 1
    image_2_id = 2
    image_1_name_for_display = 'charade'
    image_1_image_filename = 'image_voter/images/step_a_hepburn_2019090712541567850049_133.png'
    image_2_name_for_display = 'seatbelts'
    image_2_image_filename = 'image_voter/images/step_bette_davis_2019090810401567928452_158.png'

    request.session.modified = True

    image_pair = get_fresh_image_pair(request)

    if image_pair[0].is_portrait:
        image_1_portrait_or_landscape = "portrait"
    else:
        image_1_portrait_or_landscape = "landscape"

    if image_pair[1].is_portrait:
        image_2_portrait_or_landscape = "portrait"
    else:
        image_2_portrait_or_landscape = "landscape"

    context = {'image_1_name_for_display': image_pair[0].name_for_display,
               'image_2_name_for_display': image_pair[1].name_for_display,
               'image_1_image_filename': "/image_voter/images/%s" % image_pair[0].image_filename,
               'image_2_image_filename': "/image_voter/images/%s" % image_pair[1].image_filename,
               'image_1_id' : image_pair[0].id,
               'image_2_id' : image_pair[1].id,
               'image_1_portrait_or_landscape': image_1_portrait_or_landscape,
               'image_2_portrait_or_landscape': image_2_portrait_or_landscape

               }
    return HttpResponse(template.render(context, request))

def results(request):
    template = loader.get_template('image_voter/results.html')
    context={}
    return HttpResponse(template.render(context, request))

def get_num_images(request):
    num_images = request.session.get('num_visits', -1)
    if num_images == -1:
        num_images = Image.objects.count
        request.session['num_images'] = num_images


def get_fresh_image_pair(request):
    image_pool_ids = request.session.get('image_pool_ids', [])
    print(image_pool_ids)
    if len(image_pool_ids) == 0:
        image_pool_ids = list(Image.objects.values_list('id', flat=True))
        print(image_pool_ids)

    request.session['image_pool_ids'] = image_pool_ids


    image_pair=[]
    image_id_pair = []
    first_choice = random.choice(image_pool_ids)
    image_id_pair.append(first_choice)
    print("mark A, image_pool_ids is", image_pool_ids)
    print("mark A, first_choice is", first_choice)
    image_pool_ids.remove(first_choice)
    print("mark B", image_pool_ids is", image_pool_ids")

    if len(image_pool_ids) == 0:
        image_pool_ids = list(Image.objects.values_list('id', flat=True))
        image_pool_ids.remove(first_choice)
    second_choice = random.choice(image_pool_ids)
    image_pool_ids.remove(second_choice)
    image_id_pair.append(second_choice)
    request.session['image_pool_ids'] = image_pool_ids

    previous_pairs = request.session.get('previous_pairs',[])
    previous_pairs.append(image_id_pair)
    request.session["previous_pairs"] = previous_pairs

    for image_id in image_id_pair:
        image = Image.objects.get(pk=image_id)
        image_pair.append(image)


    print("image_pair is", image_pair)
    request.session["current_id_pair"] = image_id_pair
    request.session.modified = True


    return image_pair


def vote(request):
    image_id_pair = request.session["current_id_pair"]

    for image_id in image_id_pair:
        try:
            image = Image.objects.get(pk=image_id)
        except (KeyError, Image.DoesNotExist):
            return render(request, 'image/choice.html', {
                'error_message': "There was an unexpected issue, and your choice was not saved.  Here's a different pair",
            })
        is_preferred = False
        if image_id == request.POST['choice']:
            is_preferred = True

        vote_record = ImageVote(image=image, is_preferred=is_preferred)
        vote_record.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
    return HttpResponseRedirect(reverse('results', #args=(selected_choice.id,)
         ))






