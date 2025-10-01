create or replace function refresh_update_time_column()
returns trigger as $$
begin
   new.update_time = now();
   return new;
end;
$$ language plpgsql;


create table bank (
	id serial primary key,
	name_ua text not null,
	name_en text,
	site_url text,
    is_active boolean not null default false ,
	create_time timestamp default now(),
	update_time timestamp default now()
);

create or replace trigger bank_update_time_modified 
before update on bank 
for each row 
execute procedure refresh_update_time_column();

create table bank_api (
	id serial primary key,
	bank_id integer not null,
	url text,
    module_name text,
	class_name text,
	create_time timestamp default now(),
	update_time timestamp default now(),
	constraint fk_bank foreign key (bank_id) references bank (id)
);


create or replace trigger bank_api_update_time_modified 
before update on bank_api
for each row 
execute procedure refresh_update_time_column();


create table currency (
	id serial primary key,
	currency_code integer not null,
	bank_currency_name text not null,
	international_currency_name text not null,
    is_active boolean not null default false,
	create_time timestamp default now(),
	update_time timestamp default now()
);

create or replace trigger currency_update_time_modified 
before update on currency
for each row 
execute procedure refresh_update_time_column();

create table currency_rate (
	id serial primary key,
	bank_id integer not null,
	currency_id integer not null,
	sale integer,
	pay integer,
	create_time timestamp default now(),
	update_time timestamp default now(),
	constraint fk_currency_rate_to_bank foreign key (bank_id) references bank (id),
	constraint fk_currency_rate_to_currency foreign key (currency_id) references currency (id)
);

create or replace trigger currency_rate_update_time_modified 
before update on currency_rate
for each row 
execute procedure refresh_update_time_column();













------------------------------------------------------------------------------
/*
DROP TRIGGER IF EXISTS BANK_UPDATE_TIME_MODIFIED ON PUBLIC.BANK;

SELECT *
FROM PG_TRIGGER;

SELECT TRIGGER_NAME,
       EVENT_MANIPULATION AS EVENT,
       EVENT_OBJECT_TABLE AS TABLE_NAME,
       ACTION_STATEMENT AS FUNCTION_CALL,
       TRIGGER_SCHEMA
FROM INFORMATION_SCHEMA.TRIGGERS
WHERE TRIGGER_SCHEMA = 'public'; 
*/