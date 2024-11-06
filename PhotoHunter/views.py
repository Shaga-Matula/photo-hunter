import os
from django.views.generic import TemplateView
from django.http import JsonResponse

class PhotoListView(TemplateView):
    template_name = 'photo_finder.html'  # This will look for the template in the root templates directory

    def post(self, request, *args, **kwargs):
        # Get the directory path from the POST request
        directory = request.POST.get('directory')
        
        # Check if the directory is provided
        if not directory:
            return JsonResponse({"error": "No directory provided"}, status=400)

        # Check if the provided path is a valid directory
        if not os.path.isdir(directory):
            return JsonResponse({"error": f"Invalid directory: {directory}"}, status=400)

        try:
            # List all files in the specified directory
            files = self.list_files(directory)
            return JsonResponse({'files': files})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def list_files(self, directory):
        # Initialize an empty list to hold file paths
        files = []
        
        # Walk through the directory and its subdirectories
        for root, _, filenames in os.walk(directory):
            for filename in filenames:
                # Append the full file path to the list
                files.append(os.path.join(root, filename))
        
        return files

    def get(self, request, *args, **kwargs):
        # Render the template for GET requests
        return super().get(request, *args, **kwargs)