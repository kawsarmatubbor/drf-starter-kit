from django.urls import reverse_lazy

def get_unfold_settings():
    return {
    # Branding
    "SITE_TITLE": "DRF Starter Kit",
    "SITE_HEADER": "Admin Dashboard",
    "SITE_URL": "/",

    # Features 
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,

    # Colors
    "COLORS": {
        "primary": {
            "50":  "239 246 255",
            "100": "219 234 254",
            "200": "191 219 254",
            "300": "147 197 253",
            "400": "96  165 250",
            "500": "59  130 246",
            "600": "37  99  235",
            "700": "29  78  216",
            "800": "30  64  175",
            "900": "30  58  138",
            "950": "23  37  84",
        },
    },

    # Sidebar
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "collapsible": False,
                "items": [
                    {
                        "title": "Dashboard",
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                ],
            },
            {
                "title": "Users",
                "collapsible": True,
                "items": [
                    {
                        "title": "All Users",
                        "icon": "group",
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