from django.db import models
from django.urls import reverse
from parler.models import TranslatableModel, TranslatedFields
from django.core.exceptions import ValidationError

class Category(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length=200),
        slug = models.SlugField(max_length=200, unique=True),
    )
    class Meta:
        #ordering = ['name']
        #indexes = [
        #    models.Index(fields=['name']),
        #]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse(
            'shop:product_list_by_category', args=[self.slug]
        )

def validate_pdf(file):
    if not file.name.endswith('.pdf'):
        raise ValidationError("Solo se permiten archivos PDF.")

class Product(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length=200),
        slug = models.SlugField(max_length=200),
        description = models.TextField(blank=True)
    )
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE
    )
    image = models.ImageField(
        upload_to='products/%Y/%m/%d',
        blank=True
    )
    pdf_file = models.FileField(
        upload_to='products/pdfs/%Y/%m/%d/',  # Define el directorio donde se almacenarán los PDFs
        blank=True,
        null=True,
        validators=[validate_pdf],  # Agregamos la validación
        help_text="Sube el archivo PDF del producto"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        #ordering = ['name']
        indexes = [
            #models.Index(fields=['id', 'slug']),
            #models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])