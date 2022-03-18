create table public.temp_puzzle_log
(
	muid varchar(64),
	user_segment varchar(64),
	action_date date encode az64
);

alter table public.temp_puzzle_log owner to awsuser;

grant select on public.temp_puzzle_log to gv_ro;

grant select on public.temp_puzzle_log to gv_online_ro;

grant delete, insert, references, select, trigger, update on public.temp_puzzle_log to gv_online_rw;

grant select on public.temp_puzzle_log to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.temp_puzzle_log to gv_offline_rw;

grant select on public.temp_puzzle_log to gv_alert;

grant select on public.temp_puzzle_log to dev_user;

