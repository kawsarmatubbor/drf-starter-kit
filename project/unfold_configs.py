from django.urls import reverse_lazy


def get_site_title(request):
    from apps.system_setting.models import Identity

    identity = Identity.objects.filter(is_active=True).last()

    if identity:
        return identity.title

    return "DRF Starter Kit"


def get_site_favicon(request):
    from apps.system_setting.models import Identity

    identity = Identity.objects.filter(is_active=True).last()

    if identity and identity.fav_icon:
        return identity.fav_icon.url

    return None


def get_site_favicons(request):
    favicon = get_site_favicon(request)

    if not favicon:
        return []

    return [
        {
            "href": favicon,
            "rel": "icon",
        }
    ]


def add_months(value, months):
    month = value.month - 1 + months
    year = value.year + month // 12
    month = month % 12 + 1
    return value.replace(year=year, month=month)


def dashboard_callback(request, context):
    import json
    from calendar import Calendar, month_abbr, month_name

    from django.contrib.auth import get_user_model
    from django.contrib.admin.models import LogEntry
    from django.db.models import Count
    from django.db.models.functions import TruncMonth
    from django.utils import timezone
    from apps.page.models import ContactMessage
    from apps.page.models import OtherPage

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
    context["other_page_count"] = OtherPage.objects.filter(is_active=True).count()
    context["contact_message_count"] = ContactMessage.objects.filter(is_active=True).count()
    context["user_changelist_url"] = reverse_lazy("admin:user_user_changelist")
    context["recent_users"] = [
        {
            "email": user.email,
            "is_active": user.is_active,
            "created_at": user.created_at,
            "url": reverse_lazy("admin:user_user_change", args=[user.pk]),
        }
        for user in User.objects.order_by("-created_at")[:5]
    ]
    context["recent_pages"] = [
        {
            "title": page.title,
            "is_active": page.is_active,
            "created_at": page.created_at,
            "url": reverse_lazy("admin:page_otherpage_change", args=[page.pk]),
        }
        for page in OtherPage.objects.order_by("-created_at")[:5]
    ]
    context["recent_activities"] = [
        {
            "user": activity.user,
            "object_repr": activity.object_repr,
            "action": activity.get_action_flag_display(),
            "created_at": activity.action_time,
        }
        for activity in LogEntry.objects.select_related("user").order_by("-action_time")[:5]
    ]
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
    "SITE_TITLE": get_site_title,
    "SITE_HEADER": get_site_title,
    "SITE_SUBHEADER": "Administration",
    "SITE_URL": "/api/",
    "SITE_ICON": get_site_favicon,
    "SITE_FAVICONS": get_site_favicons,
    "SITE_SYMBOL": "shield_person",
    "DASHBOARD_CALLBACK": "project.unfold_configs.dashboard_callback",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": False,
    "COLORS": {
        "primary": {
            "50": "oklch(98.2% .018 155)",
            "100": "oklch(96.2% .044 156)",
            "200": "oklch(92.5% .084 155)",
            "300": "oklch(87.1% .15 154)",
            "400": "oklch(79.2% .209 151)",
            "500": "oklch(72.3% .219 149)",
            "600": "oklch(62.7% .194 149)",
            "700": "oklch(52.7% .154 150)",
            "800": "oklch(44.8% .119 151)",
            "900": "oklch(39.3% .095 152)",
            "950": "oklch(26.6% .065 153)",
        },
    },
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
            {
                "title": "System Setting",
                "collapsible": True,
                "items": [
                    {
                        "title": "Identity",
                        "icon": "settings",
                        "link": reverse_lazy("admin:system_setting_identity_changelist"),
                    },
                    {
                        "title": "Social Media",
                        "icon": "public",
                        "link": reverse_lazy("admin:system_setting_socialmedia_changelist"),
                    },
                ],
            },
        ],
    },
}
