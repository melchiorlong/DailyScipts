create schema public;

comment on schema public is 'Standard public schema';

alter schema public owner to rdsdb;

grant create, usage on schema public to public;

