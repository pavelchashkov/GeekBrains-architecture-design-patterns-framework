from ..templates import render


class TemplateView:
    template_name = 'template.html'
    folder_templates = 'templates'

    def get_template(self) -> str:
        return self.template_name

    def get_folder_templates(self) -> str:
        return self.folder_templates

    def get_context_data(self) -> dict:
        return {}

    def render_template(self):
        context = self.get_context_data()
        template = self.get_template()
        folder_templates = self.get_folder_templates()
        return '200 OK', render(template, folder_templates, **context)

    def __call__(self, request):
        return self.render_template()


class ListView(TemplateView):
    queryset = []
    template_name = 'list.html'
    context_object_name = 'list_objects'

    def get_queryset(self):
        return self.queryset

    def get_context_object_name(self):
        return self.context_object_name

    def get_context_data(self):
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        return {context_object_name: queryset}
