\echo GO!

\echo creating the database...
create database paperlims;

\echo create base user...
create user paperplane with password 'nodeadtrees';

\echo granting privileges...
grant all privileges on database paperlims to paperplane;

\echo install additional extensions...
\connect paperlims;
create extension citext;
create extension tablefunc;

\echo done!
