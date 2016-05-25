# -*- coding: utf-8 -*-
from apiclient import errors


class File(object):

    def fields_from_dict(self, *args, **kwargs):
        if args and kwargs:
            raise Warning('Use keyword args or a dict not both at the same '
                          'time.')
        if args:
            for d in args:
                for k, v in d.iteritems():
                    setattr(self, k, v)
        if kwargs:
            for key, val in kwargs.iteritems():
                setattr(self, key, val)

    # TODO check that fields exist and if they are of the correct type of data
    def __init__(self, ac, *args, **kwargs):
        self.ac = ac
        self.fields_from_dict(*args, **kwargs)

    @classmethod
    def _callback(cls, request_id, response, exception):
        if exception:
            # Handle error
            print exception
        else:
            print "Permission Id: %s" % response.get('id')

    def _create(self, data):
        self.fields_from_dict(data)
        print self.__dict__

    def create(self, data):
        try:
            new_file = self.ac.service.files().create(
                body=data, fields='id').execute()
            return new_file['id']
        except errors.HttpError as error:
            print 'An error occurred: %s' % error

    def change_owner(self, g_file, email, callback=None):
            if isinstance(g_file, File):
                file_id = g_file.id
            else:
                file_id = g_file
            batch = self.ac.service.new_batch_http_request(
                callback=callback or self._callback)
            user_permission = {'type': 'user', 'role': 'owner',
                               'emailAddress': email}
            batch.add(
                self.ac.service.permissions().create(
                    fileId=file_id,
                    body=user_permission,
                    fields='id',
                    transferOwnership=True))
            batch.execute()

    def get(self, key):
        try:
            g_file = self.ac.service.files().get(
                fileId=key).execute()
            print g_file
            return self._create(g_file)
        except errors.HttpError as error:
            print 'An error occurred getting file: %s' % error

    def list(self, corpus=None, order_by=None, page_size=100, page_token=None,
             q=None, spaces=None):
        next_token = True
        while next_token:
            next_token = page_token
            try:
                g_file = self.ac.service.files().list(corpus=corpus,
                                                      orderBy=order_by,
                                                      pageSize=page_size,
                                                      pageToken=next_token,
                                                      q=q, spaces=spaces
                                                      ).execute()
                next_token = g_file.get('nextPageToken')
                print g_file
            except errors.HttpError as error:
                print 'An error occurred getting file: %s' % error
# {
#   "kind": "drive#file",
#   "id": string,
#   "name": string,
#   "mimeType": string,
#   "description": string,
#   "starred": boolean,
#   "trashed": boolean,
#   "explicitlyTrashed": boolean,
#   "parents": [
#     string
#   ],
#   "properties": {
#     (key): string
#   },
#   "appProperties": {
#     (key): string
#   },
#   "spaces": [
#     string
#   ],
#   "version": long,
#   "webContentLink": string,
#   "webViewLink": string,
#   "iconLink": string,
#   "thumbnailLink": string,
#   "viewedByMe": boolean,
#   "viewedByMeTime": datetime,
#   "createdTime": datetime,
#   "modifiedTime": datetime,
#   "modifiedByMeTime": datetime,
#   "sharedWithMeTime": datetime,
#   "sharingUser": {
#     "kind": "drive#user",
#     "displayName": string,
#     "photoLink": string,
#     "me": boolean,
#     "permissionId": string,
#     "emailAddress": string
#   },
#   "owners": [
#     {
#       "kind": "drive#user",
#       "displayName": string,
#       "photoLink": string,
#       "me": boolean,
#       "permissionId": string,
#       "emailAddress": string
#     }
#   ],
#   "lastModifyingUser": {
#     "kind": "drive#user",
#     "displayName": string,
#     "photoLink": string,
#     "me": boolean,
#     "permissionId": string,
#     "emailAddress": string
#   },
#   "shared": boolean,
#   "ownedByMe": boolean,
#   "capabilities": {
#     "canEdit": boolean,
#     "canComment": boolean,
#     "canShare": boolean,
#     "canCopy": boolean,
#     "canReadRevisions": boolean
#   },
#   "viewersCanCopyContent": boolean,
#   "writersCanShare": boolean,
#   "permissions": [
#     permissions Resource
#   ],
#   "folderColorRgb": string,
#   "originalFilename": string,
#   "fullFileExtension": string,
#   "fileExtension": string,
#   "md5Checksum": string,
#   "size": long,
#   "quotaBytesUsed": long,
#   "headRevisionId": string,
#   "contentHints": {
#     "thumbnail": {
#       "image": bytes,
#       "mimeType": string
#     },
#     "indexableText": string
#   },
#   "imageMediaMetadata": {
#     "width": integer,
#     "height": integer,
#     "rotation": integer,
#     "location": {
#       "latitude": double,
#       "longitude": double,
#       "altitude": double
#     },
#     "time": string,
#     "cameraMake": string,
#     "cameraModel": string,
#     "exposureTime": float,
#     "aperture": float,
#     "flashUsed": boolean,
#     "focalLength": float,
#     "isoSpeed": integer,
#     "meteringMode": string,
#     "sensor": string,
#     "exposureMode": string,
#     "colorSpace": string,
#     "whiteBalance": string,
#     "exposureBias": float,
#     "maxApertureValue": float,
#     "subjectDistance": integer,
#     "lens": string
#   },
#   "videoMediaMetadata": {
#     "width": integer,
#     "height": integer,
#     "durationMillis": long
#   }
# }