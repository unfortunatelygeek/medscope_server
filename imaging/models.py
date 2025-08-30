from django.db import models


class BaseImage(models.Model):
    """
    Abstract base model for all scan images.
    Includes common fields: image, category, uploaded_at, processed
    """
    image = models.ImageField(upload_to="scans/")
    category = models.CharField(max_length=100, default="default")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)

    class Meta:
        abstract = True


class DermatoImage(BaseImage):
    """
    Dermatoscopy images with region-specific categories
    """
    CATEGORY_CHOICES = [
        ("total_body", "Total Body Mapping"),
        ("head_neck", "Head & Neck"),
        ("torso", "Torso"),
        ("upper_ext", "Upper Extremities"),
        ("lower_ext", "Lower Extremities"),
        ("global", "Global View"),
        ("regional", "Regional View"),
        ("closeup", "Close-up Dermoscopy"),
    ]

    # override category with specific choices
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)


class OtoImage(BaseImage):
    """
    Otoscopy images with ear side metadata
    """
    EAR_CHOICES = [
        ("left", "Left"),
        ("right", "Right"),
    ]
    ear_side = models.CharField(max_length=5, choices=EAR_CHOICES, null=True, blank=True)


class PharyngoImage(BaseImage):
    """
    Pharyngoscopy images with optional region metadata
    """
    region = models.CharField(max_length=50, null=True, blank=True)
