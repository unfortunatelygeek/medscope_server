from django.db import models

class BaseImage(models.Model):
    image = models.ImageField(upload_to='scans/')
    category = models.CharField(max_length=100, default='default')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    
    class Meta:
        abstract = True

class DermatoImage(models.Model):
    CATEGORY_CHOICES = [
        ('total_body', 'Total Body Mapping'),
        ('head_neck', 'Head & Neck'),
        ('torso', 'Torso'),
        ('upper_ext', 'Upper Extremities'),
        ('lower_ext', 'Lower Extremities'),
        ('global', 'Global View'),
        ('regional', 'Regional View'),
        ('closeup', 'Close-up Dermoscopy'),
    ]

    image = models.ImageField(upload_to='uploads/')
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    uploaded_at = models.DateTimeField(auto_now_add=True)


#dummy for now
class OtoImage(BaseImage):
    ear_side = models.CharField(max_length=5, choices=[('left', 'Left'), ('right', 'Right')], null=True, blank=True)

class PharyngoImage(BaseImage):
    region = models.CharField(max_length=50, null=True, blank=True)
