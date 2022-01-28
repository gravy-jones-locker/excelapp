from __future__ import annotations

from django.db import models
import config
import os
import subprocess

from .utils import ConversionError

class TaskManager(models.Manager):

    def rm_surplus(self):
        """Remove any files/records over the specified limit"""
        while self.count() > config.FILE_LIMIT * 2:
            task = self.first()
            for file in task.uploadfile_set.all():
                print(file)
                os.remove(file.content.file.name)
            task.delete()
    
    def goc_from_form(self, id: int, ftype: str, fstream: bytes) -> Task:
        """Get or create a task from a form id and file bytes stream"""
        task, _ = self.get_or_create(id=id)
        file = UploadFile(content=fstream, ftype=ftype, task=task)
        file.save()
        return task

class Task(models.Model):
    """Corresponds to an individual upload/process/download task"""

    objects = TaskManager()

    def process(self):
        """Run the external command to generate the combined data"""
        try:
            return subprocess.check_output([
                config.PYTHON_PATH,
                config.SCRIPT_PATH,
                *self.uploadfile_set.get_path_args()])
        except:
            raise ConversionError
        
    def get_ftypes(self) -> list:
        """Return field types which are present in the record"""
        return list(self.uploadfile_set.values_list('ftype', flat=True))

class UploadFileManager(models.Manager):

    def get_path_args(self) -> list:
        """Get the contents of all files attached to task as byte arguments"""
        return [self.get(ftype=x).content.file.name for x in ['adserver', 'adobe']]

class UploadFile(models.Model):
    """Corresponds to individual uploaded files"""

    objects = UploadFileManager()

    content = models.FileField(upload_to='webapp/static/input/')
    ftype = models.CharField(max_length=255)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)