create external schema spectrum
from
database 'spectrumdb'
iam_role 'arn:aws:iam::462744805499:role/redshift-spectrum-role';

alter schema spectrum owner to gv_offline_rw;

grant usage on spectrum to gv_offline_ro;

grant usage on spectrum to metabase;

grant usage on spectrum to gv_developer;

