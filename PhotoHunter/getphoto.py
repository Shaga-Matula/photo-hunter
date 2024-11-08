import os
from django.views.generic import TemplateView
from django.http import JsonResponse

class PhotoListView(TemplateView):
    template_name = 'photo_finder.html'

    def post(self, request, *args, **kwargs):
        directory = request.POST.get('directory')
        if not directory:
            return JsonResponse({"error": "No directory provided"}, status=400)

        if not os.path.isdir(directory):
            return JsonResponse({"error": f"Invalid directory: {directory}"}, status=400)

        try:
            files = self.list_files(directory)
            return JsonResponse({'files': files})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def list_files(self, directory):
        files = []
        for root, _, filenames in os.walk(directory):
            for filename in filenames:
                files.append(os.path.join(root, filename))
        return files

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)