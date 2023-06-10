from django.db import models
from django.utils.text import slugify
from autoslug import AutoSlugField
from django.core.files.storage import FileSystemStorage
from django.conf import settings
# Create your models here.
upload_storage = FileSystemStorage(location=settings.UPLOAD_ROOT, base_url='/images/')

class Category(models.Model):
    id = models.AutoField(primary_key=True, unique=True, editable=False)
    title = models.CharField(max_length=500, blank=False, null=False)
    description = models.CharField(max_length=1000, blank=False, null=False)
    slug = AutoSlugField(populate_from='title',null=True, default=None, unique=True)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name_plural = "Category"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)    

class Product(models.Model):
    SIZE = (
        ("S", "Small"),
        ("M", "Medium"),
        ("L", "Large"),
        ("XL", "Extra Large"),
    )
    COLOR = (
        ("RD", "Red"),
        ("BK", "Black"),
        ("BL", "Blue"),
        ("WT", "White"),
        ("YL", "Yellow"),
    )
    id = models.AutoField(primary_key=True, unique=True, editable=False)
    category=models.ForeignKey(Category, on_delete=models.CASCADE, related_name="product")    
    name = models.CharField(max_length=100, blank=False, null=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=False, null=False)
    quantity = models.IntegerField(blank=False, null=False)
    description = models.CharField(max_length=1000, blank=False, null=False)  
    size_variant = models.CharField(max_length=10, default="L", choices=SIZE ,blank=False)
    color_variant = models.CharField(max_length=10, default="Blue", choices=COLOR, blank=False) 
    slug = AutoSlugField(populate_from='name', null=True, default=None, unique=True) 
      

    def __str__(self) -> str:
        return self.name
    class Meta:
        verbose_name_plural = "Product"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)  

class ProductImage(models.Model):    
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image1 = models.ImageField(upload_to='product-images', storage=upload_storage, blank=False, null=False)
    image2 = models.ImageField(upload_to='product-images', storage=upload_storage, blank=False, null=False)    
    def __str__(self) -> str:
        return self.product.name  