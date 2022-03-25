select
    distinct
    campaign_id, status
from dim_poseidon_campaign_info
;

'15017500968'

select
    status,
    count(1)
from mid_dh_ua_new_data
group by status
;



select
    status,
    count(1)
from mid_dh_ua_data
group by status
;
