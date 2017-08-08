

def test_DockerUtil_getContainerImage():
  from util.python_util.docker_util import DockerUtil
  containerName='autotest'
  image = DockerUtil.getContainerImage(containerName)
  print image


def test_DockerUtil_isValidEnujImage(imageName):
  from ENUJ_CLOUD.common import isValidEnujImage
  return isValidEnujImage(imageName)


pass


#test_DockerUtil_getContainerImage()
print test_DockerUtil_isValidEnujImage('ubuntu:16.04')
