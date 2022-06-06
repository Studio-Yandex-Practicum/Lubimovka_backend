from django.contrib import admin


class AdminPlayMixin:
    """Mixin add festival year and program of Play.

    Need to add parameters in admin class
        readonly_fields = ("play_festival_year", "play_program",)
    """

    @admin.display(description="Год участия в фестивале")
    def play_festival_year(self, obj):
        if obj:
            return f"{obj.play.festival.year}"
        return None

    @admin.display(description="Программа")
    def play_program(self, obj):
        if obj:
            return f"{obj.play.program}"
        return None
