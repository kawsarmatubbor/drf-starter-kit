from django.urls import reverse_lazy


def add_months(value, months):
    month = value.month - 1 + months
    year = value.year + month // 12
    month = month % 12 + 1
    return value.replace(year=year, month=month)


def dashboard_callback(request, context):
    import json
    from calendar import Calendar, month_abbr, month_name

    from django.contrib.auth import get_user_model
    from django.db.models import Count
    from django.db.models.functions import TruncMonth
    from django.utils import timezone

    User = get_user_model()
    first_month = add_months(timezone.localdate().replace(day=1), -11)
    registrations = (
        User.objects.filter(created_at__date__gte=first_month)
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(total=Count("id"))
        .order_by("month")
    )
    registrations_by_month = {
        item["month"].date().replace(day=1): item["total"] for item in registrations
    }

    months = [add_months(first_month, index) for index in range(12)]
    labels = [f"{month_abbr[month.month]} {month.year}" for month in months]
    totals = [registrations_by_month.get(month, 0) for month in months]
    today = timezone.localdate()
    calendar_weeks = Calendar(firstweekday=6).monthdayscalendar(today.year, today.month)

    context["user_count"] = User.objects.count()
    context["active_user_count"] = User.objects.filter(is_active=True).count()
    context["user_changelist_url"] = reverse_lazy("admin:user_user_changelist")
    context["calendar_month"] = f"{month_name[today.month]} {today.year}"
    context["calendar_today"] = today.day
    context["calendar_weekdays"] = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    context["calendar_weeks"] = calendar_weeks
    context["user_registration_chart"] = json.dumps(
        {
            "labels": labels,
            "datasets": [
                {
                    "label": "Registrations",
                    "data": totals,
                    "borderColor": "var(--color-primary-600)",
                    "backgroundColor": "var(--color-primary-100)",
                    "fill": True,
                    "tension": 0.35,
                },
            ],
        }
    )
    context["user_registration_chart_options"] = json.dumps(
        {
            "maintainAspectRatio": False,
            "plugins": {
                "legend": {
                    "display": False,
                },
            },
            "scales": {
                "y": {
                    "beginAtZero": True,
                    "ticks": {
                        "precision": 0,
                    },
                },
            },
        }
    )
    return context


UNFOLD = {
    "SITE_TITLE": "DRF Starter Kit Admin",
    "SITE_HEADER": "DRF Starter Kit",
    "SITE_SUBHEADER": "Administration",
    "SITE_URL": "/api/",
    "SITE_SYMBOL": "shield_person",
    "DASHBOARD_CALLBACK": "project.unfold_configs.dashboard_callback",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": False,
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "items": [
                    {
                        "title": "Dashboard",
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    }
                ],
            },
            {
                "title": "Landing page",
                "collapsible": True,
                "items": [
                    {
                        "title": "Hero Sections",
                        "icon": "view_carousel",
                        "link": reverse_lazy("admin:page_herosection_changelist"),
                    },
                ],
            },
            {
                "title": "Contact page",
                "collapsible": True,
                "items": [
                    {
                        "title": "Contact Section",
                        "icon": "contact_mail",
                        "link": reverse_lazy("admin:page_contactsection_changelist"),
                    },
                    {
                        "title": "Contact Messages",
                        "icon": "message",
                        "link": reverse_lazy("admin:page_contactmessage_changelist"),
                    },
                ],
            },
            {
                "title": "FAQ page",
                "collapsible": True,
                "items": [
                    {
                        "title": "FAQ Section",
                        "icon": "quiz",
                        "link": reverse_lazy("admin:page_faqsection_changelist"),
                    },
                    {
                        "title": "FAQ Questions",
                        "icon": "help",
                        "link": reverse_lazy("admin:page_faqquestion_changelist"),
                    }
                ],
            },
            {
                "items": [
                    {
                        "title": "Other Pages",
                        "icon": "description",
                        "link": reverse_lazy("admin:page_otherpage_changelist"),
                    },
                ],
            },
            {
                "title": "Authentication",
                "collapsible": True,
                "items": [
                    {
                        "title": "Users",
                        "icon": "person",
                        "link": reverse_lazy("admin:user_user_changelist"),
                    },
                    {
                        "title": "My Profile",
                        "icon": "account_circle",
                        "link": lambda request: reverse_lazy(
                            "admin:user_user_change",
                            args=[request.user.pk]
                        ),
                    },
                ],
            },
        ],
    },
}
