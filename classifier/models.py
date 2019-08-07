from django.conf import settings
from django.db import models
from django.utils import timezone


class Classifier(models.Model):
    feedback = models.CharField(max_length=200)

    def set_val(self):
        self.save()

    def tokenizer(text):
        return text.split(' ')
        
    def preprocessor(text):
        """ Return a cleaned version of text
        """
        text = re.sub('<[^>]*>', '', text)
        emoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)', text)
        text = (re.sub('[\W]+', ' ', text.lower()) + ' ' + ' '.join(emoticons).replace('-', ''))
        return text

    




