from django.db import models

class IMAGEM_MIX(models.Model):
    imagem = models.FileField(upload_to='.')
