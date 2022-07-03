from django.db import models
from django.urls import reverse


# Create your models here.

class MedicineBase(models.Model):
    """A typical class defining a model, derived from the Model class."""

    # Fields
    # medicine_weight = models.CharField(max_length=20, help_text='Enter field documentation')
    m_id = models.AutoField(primary_key=True)
    medicine_weight = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)
    ...

    # Metadata
    class Meta:
        ordering = ['created_at']

    # Methods
    # def get_absolute_url(self):
    #     """Returns the URL to access a particular instance of MyModelName."""
    #     return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.medicine_weight
    # def __str__(self):
    #     """String for representing the Model object."""
    #     return f'{self.id} ({self.book.title})'
#sample data
# record = MedicineBase(m_id=1,medicine_weight="30")
# record.save()    
