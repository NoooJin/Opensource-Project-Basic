from djongo import models
from django import forms

from .models import Review, LatestReviews


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = (
            'content',
            'author_name',
            'rating'
        )
