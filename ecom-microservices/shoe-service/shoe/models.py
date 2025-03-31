from djongo import models

class Shoe(models.Model):
    """Model giày cho hệ thống eCommerce"""

    product_id = models.CharField(max_length=100, unique=True)  # Liên kết với Product Service
    size = models.CharField(max_length=10)  # 42, 43 hoặc US 10, UK 9
    color = models.CharField(max_length=50)
    material = models.CharField(max_length=100)  # Leather, Mesh
    gender = models.CharField(max_length=10, choices=[
        ("M", "Men"),
        ("W", "Women"),
        ("U", "Unisex")
    ])
    sport_type = models.CharField(max_length=50, blank=True, null=True)  # Running, Basketball
    style = models.CharField(max_length=50, blank=True, null=True)  # Sneakers, Boots
    closure_type = models.CharField(max_length=50, blank=True, null=True)  # Laces, Slip-on
    sole_material = models.CharField(max_length=100, blank=True, null=True)  # Rubber, Foam
    upper_material = models.CharField(max_length=100, blank=True, null=True)  # Leather, Flyknit
    waterproof = models.BooleanField(default=False)
    breathability = models.CharField(max_length=10, choices=[
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High")
    ], blank=True, null=True)
    recommended_terrain = models.CharField(max_length=50, blank=True, null=True)  # Road, Trail
    warranty_period = models.IntegerField(default=12)  # Bảo hành (tháng)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "shoes"
        indexes = [
            models.Index(fields=["product_id"]),
            models.Index(fields=["size"]),
            models.Index(fields=["color"]),
            models.Index(fields=["sport_type"]),
        ]

    def __str__(self):
        return f"Shoe - {self.style} - Size {self.size} - {self.color}"