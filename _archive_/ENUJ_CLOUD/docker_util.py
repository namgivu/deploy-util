#!/usr/bin/env python2.7
import docker
DOCKER_CLIENT = docker.from_env()


class DockerUtil:

  def __init__(self): pass


  #region docker identity i.e. id/name
  pass


  @staticmethod
  def getShortId(container):
    return container.id[0:12]


  @staticmethod
  def validateId(shortId):
    """Check to see if `containerIP` is a valid container id"""
    return shortId in [DockerUtil.getShortId(container) for container in DOCKER_CLIENT.containers.list()]


  @staticmethod
  def validateName(name):
    """Check to see if `name` is a valid container name"""
    return name in [container.name for container in DOCKER_CLIENT.containers.list()]


  @staticmethod
  def getName(shortId):
    """Get container name from id `shortId` """
    container = DOCKER_CLIENT.containers.get(shortId)
    return container.name if container else None


  @staticmethod
  def getNameOrFail(identity):
    """Ensure we can get container name from id/name `identity` """

    #must be name or id
    notOK = not DockerUtil.validateId(identity)
    notOK = notOK and not DockerUtil.validateName(identity)
    if notOK: raise Exception('Invalid container name/id %s' % identity)

    #convert ip to container name if any
    if DockerUtil.validateId(identity):
      name = DockerUtil.getName(identity)
    else:
      name = identity

    return name


  pass
  #endregion docker identity i.e. id/name


  @staticmethod
  def getContainerImage(containerName):
    """From container name `containerName` return its docker image aka. container image"""
    container = DOCKER_CLIENT.containers.get(containerName)
    if not container: return None
    if len(container.image.tags)==0: return None
    return container.image.tags[0]
