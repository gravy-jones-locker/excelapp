from __future__ import annotations

from django.db import models
import config
import subprocess

class TaskManager(models.Manager):

    def rm_surplus(self):
        """Remove any files/records over the specified limit"""
        while self.count() > config.FILE_LIMIT:
            self.first().delete()
    
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
        return subprocess.check_output([
            config.PYTHON_PATH,
            config.SCRIPT_PATH,
            *self.uploadfile_set.get_byte_args()])

class UploadFileManager(models.Model):

    def get_byte_args(self) -> list:
        """Get the contents of all files attached to task as byte arguments"""
        return [self.get(ftype=x).content for x in ['adserver', 'adobe']]

class UploadFile(models.Model):
    """Corresponds to individual uploaded files"""

    content = models.FileField(upload_to='webapp/static/input/')
    ftype = models.CharField(max_length=255)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)