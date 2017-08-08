#!/usr/bin/env python2.7


##region common paths
import os
upuSCRIPT_HOME  = os.path.abspath(os.path.dirname(__file__))
UTILITY_ROOT    = os.path.abspath('%s/../..' % upuSCRIPT_HOME)
##endregion common paths


##region echo with color ref. http://stackoverflow.com/a/5947802/248616

#color code
HL='\033[1;33m' #high-lighted color
CM='\033[0;32m' #comment color
ER='\033[1;31m' #error color
DK='\033[0;30m' #dark grey color
EC='\033[0m'    #end coloring

#escape color code
eHL='\\033[1;33m' #high-lighted color
eCM='\\033[0;32m' #comment color
eER='\\033[1;31m' #error color
eDK='\\033[0;30m' #dark grey color
eEC='\\033[0m'    #end coloring

##endregion echo with color
