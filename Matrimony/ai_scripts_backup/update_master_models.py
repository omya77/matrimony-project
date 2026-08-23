import os

filepath = r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\profiles_app\models.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

models_code = '''
class Religion(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    def __str__(self): return self.name

class Caste(models.Model):
    religion = models.ForeignKey(Religion, on_delete=models.CASCADE, related_name='castes')
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    def __str__(self): return f"{self.name} ({self.religion.name})"
    class Meta:
        unique_together = ('religion', 'name')

class MotherTongue(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    def __str__(self): return self.name
'''
if 'class Religion' not in content:
    with open(filepath, 'a', encoding='utf-8') as f:
        f.write(models_code)
        print('Added Master Data models.')
else:
    print('Models already exist.')
