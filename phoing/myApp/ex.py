
###################### reference section ######################
@csrf_exempt
def reference_save(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        reference_id = data["reference_id"]
        reference = get_object_or_404(Reference, pk=reference_id)
        is_saved = request.user in reference.save_users.all()
        if(is_saved):
            reference.save_users.remove(
                get_object_or_404(User, pk=request.user.pk))
        else:
            reference.save_users.add(get_object_or_404(User, pk=request.user.pk))
        is_saved = not is_saved
        reference.save()
        return JsonResponse({'reference_id': reference_id, 'is_saved': is_saved})


def reference_list(request):
    references = Reference.objects.all()

    # infinite scroll
    references_per_page = 3
    page = request.GET.get('page', 1)
    paginator = Paginator(references, references_per_page)
    try:
        references = paginator.page(page)
    except PageNotAnInteger:
        references = paginator.page(1)
    except EmptyPage:
        references = paginator.page(paginator.num_pages)

    context = {
        'references': references,
        'request_user': request.user,
    }
    return render(request, 'myApp/reference/reference_list.html', context=context)


def reference_detail(request, pk):
    reference = get_object_or_404(Reference, pk=pk)
    ctx = {
        'reference': reference,
        'request_user': request.user,
    }
    return render(request, 'myApp/reference/reference_detail.html', context=ctx)


@login_required
def reference_delete(request, pk):
    reference = get_object_or_404(Reference, pk=pk)
    if request.method == 'POST':
        reference.delete()
        messages.success(request, "탈퇴되었습니다.")
        return redirect('myApp:reference_list')
    else:
        ctx = {'reference': reference}
        return render(request, 'myApp/reference/reference_delete.html', context=ctx)


@login_required
def reference_update(request, pk):
    reference = get_object_or_404(Reference, pk=pk)
    if request.method == 'POST':
        form = ReferenceForm(request.POST, request.FILES, instance=reference)
        if form.is_valid():
            reference.image = request.FILES.get('image')
            reference = form.save()
            return redirect('myApp:reference_detail', reference.pk)
    else:
        form = ReferenceForm(instance=reference)
        ctx = {'form': form}
        return render(request, 'myApp/reference/reference_update.html', ctx)


@login_required
def reference_create(request):
    # if request.user.is_authenticated:
    #     return redirect('myApp:profile_detail')

    if request.method == 'POST':
        reference_form = ReferenceForm(request.POST, request.FILES)
        if reference_form.is_valid():
            reference = reference_form.save(commit=False)
            reference.user = request.user
            reference.is_closed = False
            reference.save()
            reference.image = request.FILES.get('image')
            return redirect('myApp:reference_detail', reference.pk)

    else:
        reference_form = ReferenceForm()

    return render(request, 'myApp/reference/reference_create.html', {'form': reference_form})
