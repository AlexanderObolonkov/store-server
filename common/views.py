from typing import Any, Protocol


class TitleMixin(Protocol):
    title = None

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context
