from collections import defaultdict

from django import template
from django.utils.safestring import mark_safe

from specs.models import ProductFeatures

register = template.Library()


@register.filter
def product_spec(category):

    product_features = ProductFeatures.objects.filter(product__category=category)
    feature_and_values = defaultdict(list)

    for product_feature in product_features:
        if product_feature.value not in feature_and_values[(product_feature.feature.feature_name, product_feature.feature.feature_filter_name)]:
            feature_and_values[
                (product_feature.feature.feature_name, product_feature.feature.feature_filter_name)
            ].append(product_feature.value)

    search_filter_body = """<div class="col-md-12">{}</div>"""
    mid_res = ""

    for (feature_name, feature_filter_name), feature_values in feature_and_values.items():
        feature_name_html = f"""<p>{feature_name}</p>"""
        feature_values_res = ""

        for f_v in feature_values:
            mid_feature_values_res = \
                "<input type='checkbox' name='{f_f_name}' value='{feature_name}'> <span>{feature_name}</span></br>".format(
                    feature_name=f_v, f_f_name=feature_filter_name
                )
            feature_values_res += "<div class='checkbox'>" + mid_feature_values_res + '</div>'

        feature_name_html += feature_values_res
        mid_res += feature_name_html

    res = search_filter_body.format(mid_res)

    return mark_safe(res)
