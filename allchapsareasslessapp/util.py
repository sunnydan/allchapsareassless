from PIL import Image
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
import os

def handleAvatarUpdate(requestfile, requestuser):
    for filename in os.listdir(settings.MEDIA_ROOT+"/avatars"):
                if(filename.split(".")[0] == "avatar" + str(requestuser.id)):
                    os.remove(os.path.join(
                        settings.MEDIA_ROOT+"\\avatars", filename))

                filetype = requestfile.name.split(".")[-1]
                if(filetype == "gif"):
                    requestfile.name = "avatar" + \
                        str(requestuser.id) + ".gif"
                    requestuser.avatar = requestfile
                    requestuser.save()
                else:
                    image = Image.open(requestfile)
                    filetype = filetype.lower()

                    if(filetype.lower() == "jpg"):
                        filetype = "jpeg"

                    image = image.resize(
                        (settings.AVATAR_IMAGE_SIZE, settings.AVATAR_IMAGE_SIZE), Image.ANTIALIAS)

                    tempfile = BytesIO()
                    image.save(tempfile, filetype.lower())

                    image = InMemoryUploadedFile(
                        tempfile, None, "avatar" +
                        str(requestuser.id) + "." + filetype, tempfile.__sizeof__, None, None)
                    requestuser.avatar = image
                    requestuser.save()
                    tempfile.close()