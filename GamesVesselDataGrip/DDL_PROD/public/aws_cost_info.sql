create table public.aws_cost_info
(
	time_period date not null,
	service varchar(256) not null,
	amount double precision not null,
	unit varchar(30),
	estimated boolean,
	create_time timestamp default ('now'::character varying)::timestamp without time zone not null encode az64,
	update_time timestamp not null encode az64,
	linked_account varchar(20) default ''::character varying not null,
	amount_usd double precision default (0)::double precision not null,
	constraint aws_cost_info_pkey
		primary key (linked_account, time_period, service)
)
sortkey(linked_account, time_period, service);

comment on table public.aws_cost_info is 'aws花费信息表';

comment on column public.aws_cost_info.time_period is '日期';

comment on column public.aws_cost_info.service is '服务名称';

comment on column public.aws_cost_info.amount is '金额值';

comment on column public.aws_cost_info.unit is '金额单位';

comment on column public.aws_cost_info.estimated is '是否估值';

comment on column public.aws_cost_info.create_time is '此条记录创建时间，系统默认值
';

comment on column public.aws_cost_info.update_time is '记录更新时间，语句更新';

comment on column public.aws_cost_info.linked_account is '账户信息';

comment on column public.aws_cost_info.amount_usd is '金额值(美元), amount 字段的美元表示';

alter table public.aws_cost_info owner to gv_offline_rw;

grant select on public.aws_cost_info to gv_ro;

grant insert, select, update on public.aws_cost_info to gv_online_ro;

grant select on public.aws_cost_info to gv_offline_ro;

grant delete, insert, references, select, trigger, update on public.aws_cost_info to gv_online_rw;

grant select on public.aws_cost_info to metabase;

grant select on public.aws_cost_info to gv_developer;

