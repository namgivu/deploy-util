Context
=======
We have current application running successfully on localhost.

Goal
====
How to get `pip packages list` file, called `requirements.txt`, 
that can be used to run and succeed on all other Linux distros 
e.g. localhost, AWS EC2 host?

The problem?
============
Calling `pip freeze > requirements.txt` will list *all packages* and 
their *dependency packages* with their SPECIFIC VERSIONS.

Simply take the file to pip install i.e.
```
pip install -r requirements.txt
```
will often fail; this is caused by the fact that 
some packages behave abnormally against different Linux distros, 
against different Python versions, and against their dependent packages.

Solution
========
- Make PIP_FREEZE file via `pip freeze > requirements.txt`
- Set up and activate a new empty venv

- a Run the app to get the error e.g. `APP_HOME/deploy/dev/run.sh` aka. `./run.sh`
- b Find error keywords in PIP_FREEZE to get the package name called ERROR_PACKAGE
- c Install ERROR_PACKAGE named p1 for example
```
pip install p1 ; ./run.sh
```

- Repeat abc until we can run the app successfully i.e. we will have the final command
```
pip install p1 p2 p3 ... pN ; ./run.sh
```

- Save the list p1, p2, ..., pN called PACKAGE_LIST to `requirementsFIX.txt`
Of course you need to follow pip syntax using the list

- (optional) 
Refer to `requirements.txt` and fill in the version numbers for packages in PACKAGE_LIST
We just need to enter the version for packages which have deprecated warning 
i.e. latest Flask package when used by old-time code/syntax often raises 
`deprecation warnings`


- It's done i.e. `requirements.txt` is ready to install elsewhere
```
pip install -r requirementsFIX.txt
```

Note on updating requirements.txt 201610.12
===========================================
When `pip install NEW_PACKAGE`, we update `requirements file` as below steps

- update package version
```
pip freeze util/deploy/pip/pip-freeze.txt
```

- append `NEW_PACKAGE==version` to file 
```
util/deploy/pip/requirements_ubuntu-16-onEC2.txt
```

THE END