# Udaan Red Carpet API

It is written in python, using redis as in memory key value data store.
Configuration is saved in mongodb document. Refer sampleApi.config for details

Images Directory Structure
--------------------------

* root (path-to-this-folder will go in image host FQDN)
    * desktop
        * categories-named-folders-hyphen-separated
            * nominee-names-hyphen-separated-with-extension
    * phone
        * categories-named-folders-hyphen-separated
            * nominee-names-hyphen-separated-with-extension