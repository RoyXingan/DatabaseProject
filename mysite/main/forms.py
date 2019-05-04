from django import forms


class CurriculumForm(forms.Form):
    curriculum_name = forms.CharField()
    admin_name = forms.CharField()
    admin_id = forms.IntegerField()
    min_credits = forms.IntegerField()
    topic_coverage = forms.CharField()
    goal_valid_credits = forms.IntegerField()
    goal_valid = forms.BooleanField()
