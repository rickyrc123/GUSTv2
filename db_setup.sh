#!/bin/bash

pg_ctlcluster 14 main start
su -c "createuser GUSTv2 -s" postgres

echo 'created user'

su -c "createdb GUSTv2 -O GUSTv2" postgres

echo 'created db'

su -c "psql GUSTv2 << EOF
  alter user \"GUSTv2\" WITH PASSWORD  'password';
EOF" postgres