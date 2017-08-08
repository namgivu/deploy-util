#!/usr/bin/env python2.7

from common   import * #initiate common asset
from input    import * #load the inputs

#region parse params
options = dict(
  shortOpts = 'a:',
  longOpts  = ['autorun='],
)

isAutorun = getArg('-a', options)
#endregion parse params

HOST_URL = '%s://localhost:%s' % (DEPLOY_HTTP, DEPLOY_PORT)
curlSSL = '-k' if isSSL(DEPLOY_PORT) else '' #curl's turning off SSL option

##region Making test @ Flask web with REACT frontend
stepsFRONTEND = []

#define testcases
testCasesFE = [
  #used when web not run yet
  dict(url=HOST_URL, grep='title|h1'),

  #TODO add more testcase to test REACT frontend rendered outcome
  #dict(url=HOST_URL, grep='favicon.png'),
  #dict(url=HOST_URL/path/to/static/README.md, grep=''),
]

#region run test cases
for i,testCase in enumerate(testCasesFE): #foreach with index ref. http://stackoverflow.com/a/28072982/248616
  url  = testCase['url']
  grep = testCase['grep']

  #test run #1
  fe01  = 'curl {curlSSL} -s {url} | grep --color -Ei "{grep}"'.format(
    curlSSL=curlSSL, url=url, grep=grep,
  )

  #test run #2
  """
  opt       -s silence  -o output to file  -w format output result  ref. http://superuser.com/a/442395/34893
  e.g. curl -s          -o /dev/null       -w "%{http_code}"        http://localhost:5000/
  """
  optHttpCode = '-w "%{http_code}"'
  fe02 = 'curl {curlSSL} -s -o /dev/null {optHttpCode} {url}'.format(
    curlSSL=curlSSL, optHttpCode=optHttpCode, url=url
  )

  #record a running step
  stepsFRONTEND.append('echo "{eCM}Testcase #FE{i} START{eEC}"'.format(eCM=eCM, eEC=eEC, i=i))

  stepsFRONTEND.append('echo "grep \'%s\'" ' % grep)
  stepsFRONTEND.append(fe01)

  stepsFRONTEND.append('echo "status_code" ')
  stepsFRONTEND.append(fe02)

  stepsFRONTEND.append('echo')
  stepsFRONTEND.append('echo "{eCM}Testcase #FE{i} END{eEC}"'.format(eCM=eCM, eEC=eEC, i=i))

#endregion run test cases

##endregion Making test @ Flask web with REACT frontend

##region Making test @ Flask web as API backend
stepsAPI = []

#make a POST request ref. http://stackoverflow.com/a/14978657/248616
api01 = 'curl {curlSSL} -s --data "{data}" {url} | grep -E "status|message|succeed" '.format(
  curlSSL=curlSSL,
  url  = '%s/v2/auth' % HOST_URL,
  data = 'email=%s&password=%s' % ('testmaya3@gmail.com', '123456'),
)

testCasesAPI = [
  dict(sh=api01, desc='Test API @ /v2/auth')
]

stepsAPI.append('echo ; echo')
for i,testCase in enumerate(testCasesAPI):
  sh   = testCase['sh']
  desc = testCase['desc']

  stepsAPI.append('echo "{eCM}Testcase #API{i} START{eEC}"'.format(eCM=eCM, eEC=eEC, i=i))
  stepsAPI.append('echo "desc: %s" ' % desc)
  stepsAPI.append(sh)
  stepsAPI.append('echo "{eCM}Testcase #API{i} END{eEC}"'.format(eCM=eCM, eEC=eEC, i=i))

##endregion Making test @ Flask web as API backend

#region print infos & steps
infos = FLASK_DEPLOY_INFO

##region steps
steps = ''

#aftermath info check
steps += '''
{HL}#Hosted aftermath check {EC}
  echo '{eHL}Hosted aftermath check {eEC}'

  echo ; echo '{eCM}DEPLOY_WWWROOT {eEC}'
  ls -lad {DEPLOY_WWWROOT}

  echo ; echo '{eCM}PUBLIC_PATHS {eEC}'
  ls -lad {printedDEPLOYED_PUBLIC_PATHS}

  echo ; echo '{eCM}Apache site {eEC}'
  export f={SITES_AVAILABLE}/{SITE_ID}.conf
  ls -la $f

    echo '{eCM}View deploy id, deploy wwwroot, deploy port {eEC}'
      export f={SITES_AVAILABLE}/{DEPLOY_ID}.{SITECONF_MASTER}
      cat $f | grep -E 'Define[ ]+DEPLOY_ID'
      cat $f | grep -E '^[ ]*SSLCertificateFile'    | {trimGrep}
      cat $f | grep -E '^[ ]*SSLCertificateKeyFile' | {trimGrep}

      export f={SITES_AVAILABLE}/{DEPLOY_ID}.{SITECONF_SUB00}
      cat $f | grep -E 'Define[ ]+DEPLOY_WWWROOT'
      cat $f | grep -E 'Define[ ]+DEPLOY_PORT'

  echo ; echo '{eCM}RBS local config {eEC}'
  export f={DEPLOYED_LOCAL_CONFIG}
  ls -la $f
    echo ; echo '  {eCM}View active local config {eEC}'
    printf '  ' ; cat $f | grep -E 'ACTIVE_LOCAL_CONFIG[ ]*='

    echo ; echo '  {eCM}View active mysql connection string {eEC}'
    printf '  ' ; cat $f | grep -E 'SQLALCHEMY_DATABASE_URI[ ]*='
'''.format(
  HL=HL,CM=CM,EC=EC,
  eHL=eHL,eCM=eCM,eEC=eEC,

  DEPLOY_WWWROOT=DEPLOY_WWWROOT,
  printedDEPLOYED_PUBLIC_PATHS=' '.join(DEPLOYED_PUBLIC_PATHS),
  SITES_AVAILABLE=SITES_AVAILABLE,
  SITE_ID=SITE_ID,
  DEPLOY_ID=DEPLOY_ID,
  SITECONF_SUB00=SITECONF_SUB00,
  SITECONF_MASTER=SITECONF_MASTER,
  DEPLOYED_LOCAL_CONFIG=RBS_LOCAL_CONFIG.replace(CODE_HOME, DEPLOY_WWWROOT),

  trimGrep="awk '{$1=$1;print}' ", #trim leading & trailing spaces when grep ref. http://unix.stackexchange.com/a/205854/17671
)

#run functional testing
steps += '''
{HL}#Functional testing {EC}
echo
echo '{eHL}Functional testing {eEC}'
echo

  {CM}#Run real Flask app; it must succeed{EC}
  {testStepsFRONTEND}

  {CM}#Run real React frontend web; it must succeed{EC}
  {testStepsAPI}


{HL}#Functional testing {EC}
echo
tail /var/log/apache2/{DEPLOY_ID}.error.log
'''.format(
  HL=HL,CM=CM,EC=EC,
  eHL=eHL,eCM=eCM,eEC=eEC,

  testStepsFRONTEND = '\n  '.join(stepsFRONTEND),
  testStepsAPI      = '\n  '.join(stepsAPI),

  DEPLOY_ID = DEPLOY_ID,
)

##endregion steps

print(infos)
print(steps)

#endregion print infos & steps

#autorun if required
if isAutorun: runPrintedSteps(
  steps, headline='Autorun deploy-aftermath check'
)
