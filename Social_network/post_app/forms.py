from .models import *


from django import forms
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile




class MultipleFilesInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFilesField(forms.FileField):
    def clean(self, data, initial = True):
        single_file_clean = super().clean
        
        if isinstance(data, (list, tuple)):
            return [single_file_clean(file, initial) for file in data]

        return single_file_clean(data, initial)
    

class PostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        label = None,
        required = False,
        queryset = Tag.objects.all(),
        widget = forms.CheckboxSelectMultiple()
    )

    images = MultipleFilesField(
        label = 'Зображення',
        required= False,
        widget= MultipleFilesInput(attrs={'multiple': True, 'accept': 'images/*'})
    )

    
    class Meta:
        model = Post
        fields = ['title', 'topic', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                "id": 'input-form',
                'placeholder': 'Напишіть назву публікації'
            }),
            'topic': forms.TextInput(attrs={
                "id": 'input-form',
                'placeholder': 'Напишіть тему публікації'
            }),
            'content': forms.Textarea(attrs={
                "id": 'input-form',
                'placeholder': 'Напишіть контент публікації',
                'class': 'content-area'
            }),
        }

        labels = {
            'title': 'Назви публікації',
            'topic': 'Тема публікації',
            'content': 'Текст публікації'
        }

        

    def __init__(self, *args, links= None, images = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].queryset = Tag.objects.all()
        self.links_list = []
        
        if links is None:
            links = []
        
        for link in links:
            clean_link = link.strip()
            if clean_link:
                self.links_list.append(clean_link)

        self.images_list = []
        if images is not None:
            self.images_list = list(images)

    
    def clean(self):
        clean_data = super().clean()
        urls_fields = forms.URLField()
        for link in self.links_list:
            try:
                urls_fields.clean(value=link)
            except forms.ValidationError:
                self.add_error(field=None, error="Некоректне посилання")

        image_fields = forms.ImageField()

        for image in self.images_list:
            try:
                image_fields.clean(image)
            except forms.ValidationError:
                self.add_error('images', 'Завантажте , будь ласка, коректне зображення')

        clean_data['images'] = self.images_list

        return clean_data
    
    def save(self, author, commit = True):
        post = super().save(commit=False)
        post.author = author
        if commit:
            post.save()

            post.tags.set(self.cleaned_data["tags"])

            custom_tags = self.data.getlist("custom_tags")
            
            for tag in custom_tags:
                clean_name = tag.strip()
                if clean_name:
                    #get_or_create шукає тег у базі даних, якщо його нема, то створює новий тег
                    tag_object, created = Tag.objects.get_or_create(name = clean_name)
                    post.tags.add(tag_object)

            for url in self.links_list:
                PostLink.objects.create(post=post, url=url)

            uploaded_images = self.cleaned_data.get('images')

            for image in uploaded_images:
                PostImage.objects.create(
                    post=post,
                    original_image = image,
                    compressed_image = self.compress_image(image)
                )

                
        return post
    
    def compress_image(self, original_image):
        original_image.seek(0)
        image = Image.open(original_image)
        image = image.convert('RGB')

        quality = 85
        width, height = image.size
        MAX_COMPRESSED_IMAGE_SIZE = 2 * 1024 * 1024
        
        while True:
            buffer = BytesIO()
            image.save(buffer, format='jpeg', quality = quality, optimize = True)
            
            if buffer.tell() <= MAX_COMPRESSED_IMAGE_SIZE:
                break     
            
            if quality > 35:
                quality -= 10
            else:
                if width <= 50 or height <= 50:
                    break

                width = int(width * 0.9)
                height = int(height * 0.9)
                image = image.resize((width, height), Image.Resampling.LANCZOS)

        original_image.seek(0)
        compressed_name = f'compressed_{original_image.name.rsplit('.',1)[0]}.jpg'
        compressed_image = ContentFile(buffer.getvalue(), name= compressed_name)
        return compressed_image
                

              