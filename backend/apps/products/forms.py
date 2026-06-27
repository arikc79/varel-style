from django import forms

from .models import Category, Product


EMOJI_CHOICES = [
    ('👖', '👖 Джинси'),
    ('👔', '👔 Сорочки'),
    ('🤵', '🤵 Костюми'),
    ('🏃', '🏃 Спорт'),
    ('🧥', '🧥 Куртки'),
    ('👟', '👟 Кросівки'),
]


class _EmojiAdminFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Якщо в БД уже є emoji поза списком, залишаємо його доступним для редагування.
        current_emoji = getattr(self.instance, 'emoji', None)
        if current_emoji and current_emoji not in dict(EMOJI_CHOICES):
            self.fields['emoji'].choices = [(current_emoji, f'{current_emoji} (поточне)')] + EMOJI_CHOICES


class CategoryAdminForm(_EmojiAdminFormMixin, forms.ModelForm):
    emoji = forms.ChoiceField(choices=EMOJI_CHOICES, label='Emoji')

    class Meta:
        model = Category
        fields = '__all__'


class ProductAdminForm(_EmojiAdminFormMixin, forms.ModelForm):
    emoji = forms.ChoiceField(choices=EMOJI_CHOICES, label='Emoji (fallback без фото)')

    class Meta:
        model = Product
        fields = '__all__'

