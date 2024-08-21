from django.db import models

# Create your models here.
from django.contrib.auth.models import User

from django.db import models

class ComponentChoices(models.TextChoices):
    BATTERY = 'BA', 'Battery'
    MCU = 'MU', 'Microcontroller'
    PORT = 'PT', 'Charging Port'
    LED = 'LE', 'LED'
    SCREEN = 'SC', 'Screen'
    VIBRATOR = 'VB', 'Vibrator'
    PCB = 'PB', 'PCB'
    MIC = 'MP', 'Microphone'
    SWITCH = 'SW', 'Switch'
    BUTTON = 'BN', 'Button'
    
class DeviceChoices(models.TextChoices):
    VAPE = 'VP', 'Vaporizer'

class LogChoices(models.TextChoices):
    HACK = 'HA', 'Hack'
    TEARDOWN = 'TD', 'Teardown'

# Extending User model with a profile picture and saved logs
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='static/profile_pics/', blank=True, null=True)
    saved_logs = models.ManyToManyField('Log', related_name='saved_by_users', blank=True)

    def __str__(self):
        return self.user.username

class Device(models.Model):
    name = models.CharField(max_length=255)
    model = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    sales_links = models.URLField(max_length=200, blank=True, null=True)
    retailer = models.CharField(max_length=255, blank=True, null=True)
    manufacturer = models.CharField(max_length=255, blank=True, null=True)
    components = models.ManyToManyField('Component', related_name='devices')
    type = models.CharField(
        max_length=2,
        choices=DeviceChoices.choices,
        default=DeviceChoices.VAPE,
    )
    refillable = models.BooleanField(default=False)
    rechargeable = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.model}"

class UserDevice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    purchase_date = models.DateField(blank=True, null=True)
    purchase_location = models.CharField(max_length=255, blank=True, null=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    purchase_link = models.URLField(max_length=200, blank=True, null=True)
    notes = models.ManyToManyField('Note', related_name='device_notes', blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.device.name}"

class Component(models.Model):
    manufacturer = models.CharField(max_length=255, blank=True, null=True)
    data_sheet = models.URLField(max_length=200, blank=True, null=True)
    notes = models.ManyToManyField('Note', related_name='component_notes', blank=True)
    type = models.CharField(
        max_length=2,
        choices=ComponentChoices.choices,
        default=ComponentChoices.BATTERY,
    )

    dimensions = models.CharField(max_length=255)
    capacity = models.IntegerField()
    dimensions = models.CharField(max_length=255)
    voltage = models.DecimalField(max_digits=5, decimal_places=2)
    model = models.CharField(max_length=255)
    core = models.CharField(max_length=255)
    clock_speed = models.CharField(max_length=255)
    memory_flash = models.IntegerField()
    memory_sram = models.IntegerField()
    subtype = models.CharField(max_length=255)
    pins = models.IntegerField()
    size = models.CharField(max_length=255)

    def __str__(self):
        return self.type

class Tool(models.Model):
    subtype = models.CharField(max_length=255)
    size = models.CharField(max_length=255, blank=True, null=True)
    notes = models.ManyToManyField('Note', related_name='tool_notes', blank=True)

    def __str__(self):
        return f"{self.type} - {self.size if self.size else 'N/A'}"

class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, blank=True, null=True)
    user_device = models.ForeignKey(UserDevice, on_delete=models.CASCADE, blank=True, null=True)
    tools_used = models.ManyToManyField(Tool, related_name='tools')
    entries = models.ManyToManyField('Note', related_name='entries', blank=True)
    components = models.ManyToManyField(Component, related_name='components', blank=True)
    type = models.CharField(
        max_length=2,
        choices=LogChoices.choices,
        default=LogChoices.TEARDOWN,
    )
    destructive = models.BooleanField(default=False)
    goal = models.CharField(max_length=1024)
    approach = models.TextField()
    hackable = models.BooleanField(default=False)

    def __str__(self):
        return f"Log by {self.user.username} on {self.device.name if self.device else 'User Device'}"

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    photos = models.ImageField(upload_to='static/note_photos/', blank=True, null=True)
    posted_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now=True)

