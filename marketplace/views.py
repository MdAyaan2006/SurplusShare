from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail 
from django.db.models import Q
from django.core.paginator import Paginator 
from .models import Item, Profile, Review, Conversation, Message
from .forms import ItemForm, ProfileForm, MessageForm

def home(request):
    category_query = request.GET.get('category')
    search_query = request.GET.get('q')
    all_items = Item.objects.filter(status='Available').order_by('-created_at') 
    
    if category_query:
        all_items = all_items.filter(category=category_query)
    if search_query:
        all_items = all_items.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))
    
    paginator = Paginator(all_items, 12) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'index.html', {'items': page_obj, 'current_category': category_query, 'search_query': search_query})

@login_required(login_url='/login/')
def post_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False) 
            item.owner = request.user 
            item.save() 
            return redirect('home')
    else:
        form = ItemForm()
    return render(request, 'post_item.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() 
            Profile.objects.create(user=user)
            login(request, user) 
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required(login_url='/login/')
def profile(request):
    my_items = Item.objects.filter(owner=request.user).order_by('-created_at')
    profile_obj, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile_obj)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')
    else:
        profile_form = ProfileForm(instance=profile_obj)

    return render(request, 'profile.html', {'my_items': my_items, 'profile_form': profile_form, 'profile': profile_obj})

@login_required(login_url='/login/')
def mark_claimed(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if item.owner == request.user:
        item.status = 'Claimed'
        item.save()
    return redirect('profile')

def item_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login') 
        if 'rating' in request.POST:
            rating = int(request.POST.get('rating'))
            text = request.POST.get('review_text', '')
            if item.owner and request.user != item.owner:
                Review.objects.create(reviewee=item.owner, reviewer=request.user, rating=rating, text=text)
            return redirect('item_detail', item_id=item.id)
    return render(request, 'item_detail.html', {'item': item})

@login_required(login_url='/login/')
def edit_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if item.owner != request.user:
        return redirect('home')
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_detail', item_id=item.id)
    else:
        form = ItemForm(instance=item)
    return render(request, 'edit_item.html', {'form': form, 'item': item})

@login_required(login_url='/login/')
def inbox(request):
    my_conversations = Conversation.objects.filter(
        Q(buyer=request.user) | Q(item__owner=request.user)
    ).order_by('-created_at')
    return render(request, 'inbox.html', {'conversations': my_conversations})

@login_required(login_url='/login/')
def start_chat(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.user == item.owner:
        return redirect('item_detail', item_id=item.id)
    convo, created = Conversation.objects.get_or_create(item=item, buyer=request.user)
    return redirect('chat_room', convo_id=convo.id)

@login_required(login_url='/login/')
def chat_room(request, convo_id):
    convo = get_object_or_404(Conversation, id=convo_id)
    
    if request.user != convo.buyer and request.user != convo.item.owner:
        return redirect('home')
        
    # --- NEW: MARK MESSAGES AS READ ---
    # Find any unread messages sent by the OTHER person, and mark them read
    convo.messages.exclude(sender=request.user).filter(is_read=False).update(is_read=True)
    
    messages = convo.messages.all().order_by('created_at')
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.conversation = convo
            msg.sender = request.user
            msg.save()
            return redirect('chat_room', convo_id=convo.id)
    else:
        form = MessageForm()
        
    return render(request, 'chat_room.html', {'convo': convo, 'messages': messages, 'form': form})