class NoFileError(Exception):
  "No file found in the request!"
  pass

class FileTypeNotSupported(Exception):
  "File type not supported! Please choose an mp4 file."
  pass

class InternalServerError(Exception):
  "Internal Server Error!!!"
  pass