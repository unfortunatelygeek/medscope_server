from django.db import models

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
