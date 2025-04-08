from dataclasses import dataclass

from django.db.models import Model


@dataclass
class Breadcrumb:
    name: str
    url: str
    ignore_seo_parameter: bool = False


def build_breadcrumbs(data: list) -> list[Breadcrumb]:
    result = [Breadcrumb(name="Главная", url="/")]
    for item in data:
        if isinstance(item, Model):
            try:
                if hasattr(item, "title"):
                    name = item.title
                elif hasattr(item, "name"):
                    name = item.name
                else:
                    name = str(item)
                result.append(Breadcrumb(name=name, url=item.get_absolute_url()))
            except AttributeError:
                continue
        elif isinstance(item, dict):
            try:
                result.append(
                    Breadcrumb(
                        name=item["name"],
                        url=item.get("url", ""),
                        ignore_seo_parameter=item.get("ignore_seo_parameter", False),
                    )
                )
            except KeyError:
                continue
    return result
