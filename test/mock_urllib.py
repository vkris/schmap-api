
class MockURLlib():
  """ Mocks a function, can be enquired on how many calls it received """
  def __init__(self, url):
    self.url  = url
    self._calls  = []

  def __call__(self, *arguments):
    """Mock callable"""
    self._calls.append(arguments)
    return self.url

  def called(self):
    """docstring for called"""
    return self._calls
  
  def read(self):
      if (self.url.find("google.com") >= 0):          
          return "<!doctype html>"
      else:
          return "test"
