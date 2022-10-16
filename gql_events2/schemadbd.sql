CREATE TABLE "Event" (
  "id" UUID,
  "name" string,
  "start" datetime,
  "end" datetime,
  "capacity" int,
  "eventtype_id" UUID,
  "subject_id" UUID,
  "lesson_id" UUID,
  "location_id" UUID,
  "groups" list,
  "participants" list,
  "organizers" list,
  "comment" string
);

CREATE TABLE "EventType" (
  "id" UUID,
  "name" string
);

CREATE TABLE "Location" (
  "id" UUID,
  "name" string
);

CREATE TABLE "Role" (
  "id" UUID,
  "name" string
);

CREATE TABLE "User" (
  "id" UUID,
  "name" string
);

CREATE TABLE "Group" (
  "id" UUID,
  "name" string
);

CREATE TABLE "Subject" (
  "id" UUID,
  "name" string
);

CREATE TABLE "Lesson" (
  "id" UUID,
  "name" string
);

CREATE TABLE "Event_Participant" (
  "event_id" UUID,
  "user_id" UUID
);

CREATE TABLE "Event_Organizer" (
  "event_id" UUID,
  "user_id" UUID
);

CREATE TABLE "Event_Group" (
  "event_id" UUID,
  "group_id" UUID
);

ALTER TABLE "Event" ADD FOREIGN KEY ("eventtype_id") REFERENCES "EventType" ("id");

ALTER TABLE "Event" ADD FOREIGN KEY ("subject_id") REFERENCES "Subject" ("id");

ALTER TABLE "Event" ADD FOREIGN KEY ("lesson_id") REFERENCES "Lesson" ("id");

ALTER TABLE "Event" ADD FOREIGN KEY ("location_id") REFERENCES "Location" ("id");

ALTER TABLE "Event_Participant" ADD FOREIGN KEY ("user_id") REFERENCES "User" ("id");

ALTER TABLE "Event_Participant" ADD FOREIGN KEY ("event_id") REFERENCES "Event" ("participants");

ALTER TABLE "Event_Organizer" ADD FOREIGN KEY ("user_id") REFERENCES "User" ("id");

ALTER TABLE "Event_Organizer" ADD FOREIGN KEY ("event_id") REFERENCES "Event" ("organizers");

ALTER TABLE "Event_Group" ADD FOREIGN KEY ("group_id") REFERENCES "Group" ("id");

ALTER TABLE "Event_Group" ADD FOREIGN KEY ("event_id") REFERENCES "Event" ("groups");
