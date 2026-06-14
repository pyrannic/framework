from app.services.multimedia import PhotosService, VideosService, UploadService
from app.services.filesystems import FilesystemInterface, LocalFilesystem, S3Filesystem

from pyrannic import ServiceProvider


class AppServiceProvider(ServiceProvider):
    def register(self):
        self.container.when(PhotosService).needs(FilesystemInterface).give(
            LocalFilesystem
        )
        self.container.when([VideosService, UploadService]).needs(
            FilesystemInterface
        ).give(S3Filesystem)
