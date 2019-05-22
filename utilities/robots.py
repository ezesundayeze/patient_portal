from io import StringIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import HttpResponse
from cgi import escape


def render_to_pdf(template_src, context_dict):
    """
    This function renders django template to pdf
    :param template_src:
    :param context_dict:
    :return:
    """
    template = get_template(template_src)
    context = context_dict
    html = template.render(context)
    result = StringIO()

    pdf = pisa.pisaDocument(StringIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))
