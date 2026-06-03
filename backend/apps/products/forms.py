import json
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


class ColorsField(forms.CharField):
    """Приймає кольори через кому: «Білий, Чорний, Синій» → ['Білий','Чорний','Синій']"""

    PRESET_COLORS = [
        'Білий', 'Чорний', 'Синій', 'Темно-синій', 'Блакитний',
        'Бежевий', 'Молочний', 'Сірий', 'Графіт', 'Хакі',
        'Зелений', 'Червоний', 'Бордовий', 'Коричневий',
    ]

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('required', False)
        kwargs.setdefault('widget', forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Білий, Чорний, Синій  (через кому)\nАбо залишіть порожнім',
            'style': 'width:100%;font-family:monospace;',
        }))
        kwargs.setdefault('help_text',
            'Введіть кольори через кому або по одному на рядку. '
            'Доступні: Білий, Чорний, Синій, Темно-синій, Блакитний, Бежевий, Молочний, Сірий…'
        )
        super().__init__(*args, **kwargs)

    def prepare_value(self, value):
        """Показуємо список як зручний рядок через кому."""
        if isinstance(value, list):
            return ', '.join(value)
        if isinstance(value, str):
            try:
                parsed = json.loads(value)
                if isinstance(parsed, list):
                    return ', '.join(parsed)
            except (json.JSONDecodeError, TypeError):
                pass
        return value or ''

    def to_python(self, value):
        if not value:
            return []
        # Підтримуємо і кому, і новий рядок як роздільник
        raw = value.replace('\n', ',').replace('\r', '')
        parts = [c.strip() for c in raw.split(',') if c.strip()]
        return parts


class ProductAdminForm(_EmojiAdminFormMixin, forms.ModelForm):
    emoji  = forms.ChoiceField(choices=EMOJI_CHOICES, label='Emoji (fallback без фото)')
    colors = ColorsField(label='Кольори')

    class Meta:
        model  = Product
        fields = '__all__'

