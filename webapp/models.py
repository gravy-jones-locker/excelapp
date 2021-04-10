from django.db import models
import config
import shutil
import os
import subprocess

# Create your models here.

class CustomManager(models.Manager):

    """Class for managing table-level operations"""

    def rm_surplus(self):

        """Remove any files/records over the specified limit"""
        
        while self.count() > config.FILE_LIMIT:
            self.first().full_delete()

class UploadFile(models.Model):

    """One line db table to store file upload/download"""

    objects = CustomManager()

    content = models.FileField(upload_to='webapp/static/input/')
    
    out_path = models.CharField(max_length=255)
    fname = models.CharField(max_length=255)

    def process(self):

        """Pass the input file to the script and save output"""

        self.out_path = self.content.name.replace('input', 'output')

        # Run script - check_output waits for completion
        cmd = [config.PYTHON_PATH,
               config.SCRIPT_PATH,
               self.content.name,
               self.out_path]

        res = subprocess.check_output(cmd)

        self.fname = os.path.split(self.content.name)[1]
        self.save()  # Commits new fname/out_path to db
        
        return self

    def full_delete(self):

        """Delete db record and saved files associated with record"""

        os.remove(self.out_path)
        os.remove(self.content.name)

        self.delete()