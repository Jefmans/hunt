from django.template.defaultfilters import slugify
from hashlib import sha256
import random




def random_str_generator(size= 10):
	numbers = str(sha256().hexdigest())
	return ''.join(random.choice(numbers) for _ in range(size))



def unique_slug_generator(instance, new_slug = None):
	if new_slug is not None:
		slug = new_slug
	else:
		slug = slugify(instance.title)

	Klass = instance.__class__
	qs_exists = Klass.objects.filter(slug=slug).exists()

	if qs_exists:
		random_number = random_str_generator(size=4)
		new_slug = f"{slug}--{random_number}"

		return unique_slug_generator(instance, new_slug=new_slug)
	return slug

def pre_save_receiver_slugify(sender, instance, *args, **kwargs):
	if slugify(instance.title) not in instance.slug:
		instance.slug = unique_slug_generator(instance)

	if not instance.slug:
		Klass = instance.__class__
		slug = slugify(instance.title)
		qs_exists = Klass.objects.filter(slug=slug).exists()

		if qs_exists: 
			instance.slug = unique_slug_generator(instance, new_slug=slug)
		else:
			instance.slug = unique_slug_generator(instance)


