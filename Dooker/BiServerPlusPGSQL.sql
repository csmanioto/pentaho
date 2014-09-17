CREATE USER hibuser PASSWORD 'password';
CREATE USER pentaho_user PASSWORD 'password';
CREATE USER jcr_user PASSWORD 'password';



CREATE DATABASE hibernate ENCODING = 'UTF8' CONNECTION LIMIT = -1;
CREATE DATABASE jackrabbit ENCODING = 'UTF8' CONNECTION LIMIT = -1;
CREATE DATABASE quartz ENCODING = 'UTF8' CONNECTION LIMIT = -1;

\connect quartz 

CREATE TABLE "QRTZ"
(
  name character varying(200) NOT NULL,
  CONSTRAINT "QRTZ_pkey" PRIMARY KEY (name)
);

CREATE TABLE qrtz5_blob_triggers
(
  trigger_name character varying(200) NOT NULL,
  trigger_group character varying(200) NOT NULL,
  blob_data bytea,
  CONSTRAINT qrtz5_blob_triggers_pkey PRIMARY KEY (trigger_name, trigger_group),
  CONSTRAINT qrtz5_blob_triggers_trigger_name_fkey FOREIGN KEY (trigger_name, trigger_group)
      REFERENCES qrtz5_triggers (trigger_name, trigger_group) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE qrtz5_calendars
(
  calendar_name character varying(200) NOT NULL,
  calendar bytea NOT NULL,
  CONSTRAINT qrtz5_calendars_pkey PRIMARY KEY (calendar_name)
);

CREATE TABLE qrtz5_cron_triggers
(
  trigger_name character varying(200) NOT NULL,
  trigger_group character varying(200) NOT NULL,
  cron_expression character varying(120) NOT NULL,
  time_zone_id character varying(80),
  CONSTRAINT qrtz5_cron_triggers_pkey PRIMARY KEY (trigger_name, trigger_group),
  CONSTRAINT qrtz5_cron_triggers_trigger_name_fkey FOREIGN KEY (trigger_name, trigger_group)
      REFERENCES qrtz5_triggers (trigger_name, trigger_group) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE qrtz5_fired_triggers
(
  entry_id character varying(95) NOT NULL,
  trigger_name character varying(200) NOT NULL,
  trigger_group character varying(200) NOT NULL,
  is_volatile boolean NOT NULL,
  instance_name character varying(200) NOT NULL,
  fired_time bigint NOT NULL,
  priority integer NOT NULL,
  state character varying(16) NOT NULL,
  job_name character varying(200),
  job_group character varying(200),
  is_stateful boolean,
  requests_recovery boolean,
  CONSTRAINT qrtz5_fired_triggers_pkey PRIMARY KEY (entry_id)
);

CREATE TABLE qrtz5_job_details
(
  job_name character varying(200) NOT NULL,
  job_group character varying(200) NOT NULL,
  description character varying(250),
  job_class_name character varying(250) NOT NULL,
  is_durable boolean NOT NULL,
  is_volatile boolean NOT NULL,
  is_stateful boolean NOT NULL,
  requests_recovery boolean NOT NULL,
  job_data bytea,
  CONSTRAINT qrtz5_job_details_pkey PRIMARY KEY (job_name, job_group)
);


CREATE TABLE qrtz5_job_listeners
(
  job_name character varying(200) NOT NULL,
  job_group character varying(200) NOT NULL,
  job_listener character varying(200) NOT NULL,
  CONSTRAINT qrtz5_job_listeners_pkey PRIMARY KEY (job_name, job_group, job_listener),
  CONSTRAINT qrtz5_job_listeners_job_name_fkey FOREIGN KEY (job_name, job_group)
      REFERENCES qrtz5_job_details (job_name, job_group) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE qrtz5_locks
(
  lock_name character varying(40) NOT NULL,
  CONSTRAINT qrtz5_locks_pkey PRIMARY KEY (lock_name)
);


CREATE TABLE qrtz5_paused_trigger_grps
(
  trigger_group character varying(200) NOT NULL,
  CONSTRAINT qrtz5_paused_trigger_grps_pkey PRIMARY KEY (trigger_group)
);

CREATE TABLE qrtz5_scheduler_state
(
  instance_name character varying(200) NOT NULL,
  last_checkin_time bigint NOT NULL,
  checkin_interval bigint NOT NULL,
  CONSTRAINT qrtz5_scheduler_state_pkey PRIMARY KEY (instance_name)
);

CREATE TABLE qrtz5_simple_triggers
(
  trigger_name character varying(200) NOT NULL,
  trigger_group character varying(200) NOT NULL,
  repeat_count bigint NOT NULL,
  repeat_interval bigint NOT NULL,
  times_triggered bigint NOT NULL,
  CONSTRAINT qrtz5_simple_triggers_pkey PRIMARY KEY (trigger_name, trigger_group),
  CONSTRAINT qrtz5_simple_triggers_trigger_name_fkey FOREIGN KEY (trigger_name, trigger_group)
      REFERENCES qrtz5_triggers (trigger_name, trigger_group) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE qrtz5_trigger_listeners
(
  trigger_name character varying(200) NOT NULL,
  trigger_group character varying(200) NOT NULL,
  trigger_listener character varying(200) NOT NULL,
  CONSTRAINT qrtz5_trigger_listeners_pkey PRIMARY KEY (trigger_name, trigger_group, trigger_listener),
  CONSTRAINT qrtz5_trigger_listeners_trigger_name_fkey FOREIGN KEY (trigger_name, trigger_group)
      REFERENCES qrtz5_triggers (trigger_name, trigger_group) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE qrtz5_triggers
(
  trigger_name character varying(200) NOT NULL,
  trigger_group character varying(200) NOT NULL,
  job_name character varying(200) NOT NULL,
  job_group character varying(200) NOT NULL,
  is_volatile boolean NOT NULL,
  description character varying(250),
  next_fire_time bigint,
  prev_fire_time bigint,
  priority integer,
  trigger_state character varying(16) NOT NULL,
  trigger_type character varying(8) NOT NULL,
  start_time bigint NOT NULL,
  end_time bigint,
  calendar_name character varying(200),
  misfire_instr smallint,
  job_data bytea,
  CONSTRAINT qrtz5_triggers_pkey PRIMARY KEY (trigger_name, trigger_group),
  CONSTRAINT qrtz5_triggers_job_name_fkey FOREIGN KEY (job_name, job_group)
      REFERENCES qrtz5_job_details (job_name, job_group) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE qrtz_blob_triggers
(
  trigger_name character varying(80) NOT NULL,
  trigger_group character varying(80) NOT NULL,
  blob_data bytea,
  CONSTRAINT qrtz_blob_triggers_pkey PRIMARY KEY (trigger_name, trigger_group),
  CONSTRAINT qrtz_blob_triggers_trigger_name_fkey FOREIGN KEY (trigger_name, trigger_group)
      REFERENCES qrtz_triggers (trigger_name, trigger_group) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE qrtz_calendars
(
  calendar_name character varying(80) NOT NULL,
  calendar bytea NOT NULL,
  CONSTRAINT qrtz_calendars_pkey PRIMARY KEY (calendar_name)
);

CREATE TABLE qrtz_cron_triggers
(
  trigger_name character varying(80) NOT NULL,
  trigger_group character varying(80) NOT NULL,
  cron_expression character varying(80) NOT NULL,
  time_zone_id character varying(80),
  CONSTRAINT qrtz_cron_triggers_pkey PRIMARY KEY (trigger_name, trigger_group),
  CONSTRAINT qrtz_cron_triggers_trigger_name_fkey FOREIGN KEY (trigger_name, trigger_group)
      REFERENCES qrtz_triggers (trigger_name, trigger_group) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
);



CREATE TABLE qrtz_dummy
(
  id bigint
);

CREATE TABLE qrtz_fired_triggers
(
  entry_id character varying(95) NOT NULL,
  trigger_name character varying(80) NOT NULL,
  trigger_group character varying(80) NOT NULL,
  is_volatile boolean NOT NULL,
  instance_name character varying(80) NOT NULL,
  fired_time bigint NOT NULL,
  state character varying(16) NOT NULL,
  job_name character varying(80),
  job_group character varying(80),
  is_stateful boolean,
  requests_recovery boolean,
  CONSTRAINT qrtz_fired_triggers_pkey PRIMARY KEY (entry_id)
);

CREATE TABLE qrtz_job_details
(
  job_name character varying(80) NOT NULL,
  job_group character varying(80) NOT NULL,
  description character varying(120),
  job_class_name character varying(128) NOT NULL,
  is_durable boolean NOT NULL,
  is_volatile boolean NOT NULL,
  is_stateful boolean NOT NULL,
  requests_recovery boolean NOT NULL,
  job_data bytea,
  CONSTRAINT qrtz_job_details_pkey PRIMARY KEY (job_name, job_group)
);

CREATE TABLE qrtz_job_listeners
(
  job_name character varying(80) NOT NULL,
  job_group character varying(80) NOT NULL,
  job_listener character varying(80) NOT NULL,
  CONSTRAINT qrtz_job_listeners_pkey PRIMARY KEY (job_name, job_group, job_listener),
  CONSTRAINT qrtz_job_listeners_job_name_fkey FOREIGN KEY (job_name, job_group)
      REFERENCES qrtz_job_details (job_name, job_group) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
);



CREATE TABLE qrtz_locks
(
  lock_name character varying(40) NOT NULL,
  CONSTRAINT qrtz_locks_pkey PRIMARY KEY (lock_name)
);

CREATE TABLE qrtz_paused_trigger_grps
(
  trigger_group character varying(80) NOT NULL,
  CONSTRAINT qrtz_paused_trigger_grps_pkey PRIMARY KEY (trigger_group)
);

CREATE TABLE qrtz_scheduler_state
(
  instance_name character varying(80) NOT NULL,
  last_checkin_time bigint NOT NULL,
  checkin_interval bigint NOT NULL,
  recoverer character varying(80),
  CONSTRAINT qrtz_scheduler_state_pkey PRIMARY KEY (instance_name)
);

CREATE TABLE qrtz_simple_triggers
(
  trigger_name character varying(80) NOT NULL,
  trigger_group character varying(80) NOT NULL,
  repeat_count bigint NOT NULL,
  repeat_interval bigint NOT NULL,
  times_triggered bigint NOT NULL,
  CONSTRAINT qrtz_simple_triggers_pkey PRIMARY KEY (trigger_name, trigger_group),
  CONSTRAINT qrtz_simple_triggers_trigger_name_fkey FOREIGN KEY (trigger_name, trigger_group)
      REFERENCES qrtz_triggers (trigger_name, trigger_group) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE qrtz_trigger_listeners
(
  trigger_name character varying(80) NOT NULL,
  trigger_group character varying(80) NOT NULL,
  trigger_listener character varying(80) NOT NULL,
  CONSTRAINT qrtz_trigger_listeners_pkey PRIMARY KEY (trigger_name, trigger_group, trigger_listener),
  CONSTRAINT qrtz_trigger_listeners_trigger_name_fkey FOREIGN KEY (trigger_name, trigger_group)
      REFERENCES qrtz_triggers (trigger_name, trigger_group) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE qrtz_triggers
(
  trigger_name character varying(80) NOT NULL,
  trigger_group character varying(80) NOT NULL,
  job_name character varying(80) NOT NULL,
  job_group character varying(80) NOT NULL,
  is_volatile boolean NOT NULL,
  description character varying(120),
  next_fire_time bigint,
  prev_fire_time bigint,
  trigger_state character varying(16) NOT NULL,
  trigger_type character varying(8) NOT NULL,
  start_time bigint NOT NULL,
  end_time bigint,
  calendar_name character varying(80),
  misfire_instr smallint,
  job_data bytea,
  CONSTRAINT qrtz_triggers_pkey PRIMARY KEY (trigger_name, trigger_group),
  CONSTRAINT qrtz_triggers_job_name_fkey FOREIGN KEY (job_name, job_group)
      REFERENCES qrtz_job_details (job_name, job_group) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
);


INSERT INTO qrtz5_locks values('TRIGGER_ACCESS');
INSERT INTO qrtz5_locks values('JOB_ACCESS');
INSERT INTO qrtz5_locks values('CALENDAR_ACCESS');
INSERT INTO qrtz5_locks values('STATE_ACCESS');
INSERT INTO qrtz5_locks values('MISFIRE_ACCESS');

