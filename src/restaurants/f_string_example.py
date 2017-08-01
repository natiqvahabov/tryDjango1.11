# f_string example on python3
def home_old(request):
	html_var = 'f strings'
	html_ = f"""
			<!DOCTYPE html>
		   	<html lang=en>
		   	<head>
		   		<title>asdf</title>
		   	</head>
		   	<body>
		   		<h1>Welcome</h1>
		   		<p>It is example of '{html_var} ' </p>
		   	</body>
		   	</html>
		   	"""
	return HttpResponse(html_)
	#return render(request, "home.html", {})
