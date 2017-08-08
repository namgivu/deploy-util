'''
This config allows personal/local dev config to be loaded
e.g. SQLALCHEMY_DATABASE_URI differs on dev local machines
'''


config_local = {}
config_local.update(ACTIVE_LOCAL_CONFIG='YOUR_ACTIVE_LOCAL_CONFIG')  # name of config set activated

##region config entries
config_local.update(DEBUG=True)  # show full error detail when error occurs

#region database

#region connection
config_local.update(SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://YOUR_DB_USER:YOUR_DB_PASS@YOUR_DB_HOST/YOUR_DB_NAME?charset=utf8')

'''
Info
  format = dialect+driver://username:password@host:port/database
  ref. http://flask-sqlalchemy.pocoo.org/2.1/config/
'''
#endregion connection

config_local.update(SQLALCHEMY_ECHO=False) #True to log all the statements issued to stderr which can be useful for debugging ref. http://flask-sqlalchemy.pocoo.org/2.1/config/
#endregion database

#region whitelist ip
config_local.update(WHITELIST_LIST_IP = [
                                         #'127.0.0.1'  #localhost
                                        ])
#endregion whitelist ip

##endregion config entries