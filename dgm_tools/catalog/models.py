from django.db import models
from django.contrib.auth.models import User
from slugify import slugify


class Post(models.Model):
    """
    Modelo de las entradas
    del CMS
    """
    title = models.CharField(null=False, max_length=110, verbose_name='Titulo', db_index=True)
    description = models.TextField(blank=True, verbose_name='Encabezado')
    slug = models.SlugField(max_length=210, unique=True)
    text = models.TextField(blank=True, verbose_name='Texto')
    # Categorization
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name="Categoria")
    level = models.IntegerField('Nivel', blank=True, null=True, db_index=True, choices=((1, 'Principiante'),(2, 'Intermedio'), (3, 'Avanzado')))
    tags = models.ManyToManyField('Tag')
    link_external_tool = models.URLField(verbose_name="Link de le Herramienta", blank=True)
    # State
    public = models.BooleanField(default=False, verbose_name='Publicado', db_index=True)
    # Periodicity
    created = models.DateTimeField(auto_now_add=True, verbose_name='Creado')
    modified = models.DateTimeField(auto_now=True, verbose_name='Modificado')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Autor')

    def __str__(self):
        """
        Verbose de una instancia
        entrada en la base de datos
        """
        return 'Post: {}'.format(self.title)

    def get_absolute_url(self):
        """
        Url relativa de la entrada
        dentro del CMS
        """
        from django.urls import reverse
        return reverse('catalog_post', kwargs={'slug': self.slug})

    def save(self):
        """
        Crea un nuevo registro entrada
        en la base de datos. Genera el slug
        automaticamente a patir del
        del titulo
        """
        if not self.id:
            self.slug = slugify(self.title)

        super(Post, self).save()

    class Meta:
        index_together = ['slug', 'public']
        verbose_name = 'Solucion'
        verbose_name_plural = 'Soluciones'


class Category(models.Model):
    """
    Modelo de categoria
    para el CMS
    """
    name = models.CharField(null=False, max_length=110, verbose_name='Nombre', unique=True)
    slug = models.SlugField(db_index=True, editable=False)
    description = models.TextField(blank=True, verbose_name='Descripcion')
    # Periodicity
    created = models.DateTimeField(auto_now_add=True, verbose_name='Creado')
    public = models.BooleanField(default=False, verbose_name='Publicado', db_index=True)

    def __str__(self):
        """
        Verbose de una instancia
        categoria en la base de datos
        """
        return '{}'.format(self.name)

    def save(self):
        """
        Crea un nuevo registro categoria
        en la base de datos. Genera el slug
        automaticamente a patir del
        del nombre
        """
        if not self.id:
            self.slug = slugify(self.name)
        
        super(Category, self).save()

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'


class Tag(models.Model):
    """
    Modelo de tag
    para el CMS
    """
    tag = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(db_index=True, editable=False)
    # Periodicity
    created = models.DateTimeField(auto_now_add=True, verbose_name='Creado')
    public = models.BooleanField(default=False, verbose_name='Publicado', db_index=True)

    def __str__(self):
        """
        Verbose de una instancia
        tag en la base de datos
        """
        return '{}'.format(self.tag)

    def save(self):
        """
        Crea un nuevo registro categoria
        en la base de datos. Genera el slug
        automaticamente a patir del
        del tag
        """
        if not self.id:
            self.slug = slugify(self.tag)
        
        super(Tag, self).save()
