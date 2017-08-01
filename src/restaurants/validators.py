from django.core.exceptions import ValidationError

CATEGORIES = ['Asian','American','Mexican','Azerbaijanian']
def validate_category(value):
	cat = value.capitalize()
	if not value in CATEGORIES and not cat in CATEGORIES:
		raise ValidationError(f"{value} not a valid category")