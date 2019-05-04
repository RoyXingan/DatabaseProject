from django import forms


class CurriculumForm(forms.Form):
    Extensive = 'EX'
    Inclusive = 'IN'
    BasicPlus = 'BP'
    Basic = 'BC'
    Unsatisfactory = 'US'
    Substandard = 'SB'
    TOPIC_COVERAGE = (
        (Extensive, 'Extensive'),
        (Inclusive, 'Inclusive'),
        (BasicPlus, 'BasicPlus'),
        (Basic, 'Basic'),
        (Unsatisfactory, 'Unsatisfactory'),
        (Substandard, 'Substandard'),
    )
    curriculum_name = forms.CharField(max_length=50)
    admin_name = forms.CharField(max_length=100)
    admin_id = forms.IntegerField()
    min_credits = forms.IntegerField()
    topic_coverage = forms.ChoiceField(
        choices=TOPIC_COVERAGE,
    )
    goal_valid_credits = forms.IntegerField()
    goal_valid = forms.BooleanField()

    def clean(self):
        cleaned_data = super(CurriculumForm, self).clean()
        curriculum_name = cleaned_data.get('curriculum_name')
        admin_name = cleaned_data.get('admin_name')
        admin_id = cleaned_data.get('admin_id')
        min_credits = cleaned_data.get('min_credits')
        topic_coverage = cleaned_data.get('topic_coverage')
        goal_valid_credits = cleaned_data.get('goal_valid_credits')
        goal_valid = cleaned_data.get('goal_valid')
        if not curriculum_name and not admin_name and not admin_id and not min_credits and not topic_coverage and not goal_valid_credits and not goal_valid:
            raise forms.ValidationError('You have to write something!')