from django.shortcuts import render


def register_user(request):
    submitted = None
    errors = {}

    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip()
        city = request.POST.get("city", "").strip()
        program = request.POST.get("program", "").strip()

        if not full_name:
            errors["full_name"] = "Full name is required."
        if not email:
            errors["email"] = "Email is required."

        if not errors:
            submitted = {
                "full_name": full_name,
                "email": email,
                "city": city or "Not provided",
                "program": program or "CS471",
            }

    return render(
        request,
        "usermodule/register.html",
        {"submitted": submitted, "errors": errors},
    )
