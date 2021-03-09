--
-- PostgreSQL database dump
--

-- Dumped from database version 10.13
-- Dumped by pg_dump version 10.13

-- Started on 2021-02-09 08:17:27 CET

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 5659 (class 0 OID 0)
-- Dependencies: 5658
-- Name: DATABASE "metacatalog-dev"; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON DATABASE "metacatalog-dev" IS 'Latest version. Managed by Mirko.';


--
-- TOC entry 1 (class 3079 OID 13794)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner:
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 5662 (class 0 OID 0)
-- Dependencies: 1
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner:
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- TOC entry 3 (class 3079 OID 86187)
-- Name: postgis; Type: EXTENSION; Schema: -; Owner:
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- TOC entry 5663 (class 0 OID 0)
-- Dependencies: 3
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner:
--

COMMENT ON EXTENSION postgis IS 'PostGIS geometry, geography, and raster spatial types and functions';


--
-- TOC entry 2 (class 3079 OID 132681)
-- Name: postgis_raster; Type: EXTENSION; Schema: -; Owner:
--

CREATE EXTENSION IF NOT EXISTS postgis_raster WITH SCHEMA public;


--
-- TOC entry 5664 (class 0 OID 0)
-- Dependencies: 2
-- Name: EXTENSION postgis_raster; Type: COMMENT; Schema: -; Owner:
--

COMMENT ON EXTENSION postgis_raster IS 'PostGIS raster types and functions';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 236 (class 1259 OID 87441)
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO testuser;

--
-- TOC entry 275 (class 1259 OID 134101)
-- Name: auth_group; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO testuser;

--
-- TOC entry 274 (class 1259 OID 134099)
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO testuser;

--
-- TOC entry 5665 (class 0 OID 0)
-- Dependencies: 274
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- TOC entry 277 (class 1259 OID 134111)
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO testuser;

--
-- TOC entry 276 (class 1259 OID 134109)
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO testuser;

--
-- TOC entry 5666 (class 0 OID 0)
-- Dependencies: 276
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- TOC entry 273 (class 1259 OID 134093)
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO testuser;

--
-- TOC entry 272 (class 1259 OID 134091)
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO testuser;

--
-- TOC entry 5667 (class 0 OID 0)
-- Dependencies: 272
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- TOC entry 279 (class 1259 OID 134119)
-- Name: auth_user; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO testuser;

--
-- TOC entry 281 (class 1259 OID 134129)
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO testuser;

--
-- TOC entry 280 (class 1259 OID 134127)
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.auth_user_groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO testuser;

--
-- TOC entry 5668 (class 0 OID 0)
-- Dependencies: 280
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.auth_user_groups_id_seq OWNED BY public.auth_user_groups.id;


--
-- TOC entry 257 (class 1259 OID 133352)
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.auth_user_id_seq
    START WITH 3
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO testuser;

--
-- TOC entry 278 (class 1259 OID 134117)
-- Name: auth_user_id_seq1; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.auth_user_id_seq1
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq1 OWNER TO testuser;

--
-- TOC entry 5669 (class 0 OID 0)
-- Dependencies: 278
-- Name: auth_user_id_seq1; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.auth_user_id_seq1 OWNED BY public.auth_user.id;


--
-- TOC entry 283 (class 1259 OID 134137)
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO testuser;

--
-- TOC entry 282 (class 1259 OID 134135)
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.auth_user_user_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO testuser;

--
-- TOC entry 5670 (class 0 OID 0)
-- Dependencies: 282
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.auth_user_user_permissions_id_seq OWNED BY public.auth_user_user_permissions.id;


--
-- TOC entry 297 (class 1259 OID 134274)
-- Name: author_manage_accessrequest; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.author_manage_accessrequest (
    id integer NOT NULL,
    "creationDate" timestamp with time zone NOT NULL,
    description character varying(250) NOT NULL,
    resource_id integer NOT NULL,
    sender_id integer NOT NULL
);


ALTER TABLE public.author_manage_accessrequest OWNER TO testuser;

--
-- TOC entry 296 (class 1259 OID 134272)
-- Name: author_manage_accessrequest_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.author_manage_accessrequest_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.author_manage_accessrequest_id_seq OWNER TO testuser;

--
-- TOC entry 5671 (class 0 OID 0)
-- Dependencies: 296
-- Name: author_manage_accessrequest_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.author_manage_accessrequest_id_seq OWNED BY public.author_manage_accessrequest.id;


--
-- TOC entry 295 (class 1259 OID 134264)
-- Name: author_manage_deletionrequest; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.author_manage_deletionrequest (
    id integer NOT NULL,
    "creationDate" timestamp with time zone NOT NULL,
    description character varying(250) NOT NULL,
    resource_id integer NOT NULL,
    sender_id integer NOT NULL
);


ALTER TABLE public.author_manage_deletionrequest OWNER TO testuser;

--
-- TOC entry 294 (class 1259 OID 134262)
-- Name: author_manage_deletionrequest_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.author_manage_deletionrequest_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.author_manage_deletionrequest_id_seq OWNER TO testuser;

--
-- TOC entry 5672 (class 0 OID 0)
-- Dependencies: 294
-- Name: author_manage_deletionrequest_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.author_manage_deletionrequest_id_seq OWNED BY public.author_manage_deletionrequest.id;


--
-- TOC entry 287 (class 1259 OID 134230)
-- Name: author_manage_profile; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.author_manage_profile (
    id integer NOT NULL,
    "checkedAssociation" boolean NOT NULL,
    "metacatalogPerson_id" integer,
    user_id integer NOT NULL
);


ALTER TABLE public.author_manage_profile OWNER TO testuser;

--
-- TOC entry 286 (class 1259 OID 134228)
-- Name: author_manage_profile_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.author_manage_profile_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.author_manage_profile_id_seq OWNER TO testuser;

--
-- TOC entry 5673 (class 0 OID 0)
-- Dependencies: 286
-- Name: author_manage_profile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.author_manage_profile_id_seq OWNED BY public.author_manage_profile.id;


--
-- TOC entry 289 (class 1259 OID 134240)
-- Name: author_manage_resource; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.author_manage_resource (
    id integer NOT NULL,
    type character varying(50) NOT NULL,
    link character varying(100),
    "dataEntry_id" integer
);


ALTER TABLE public.author_manage_resource OWNER TO testuser;

--
-- TOC entry 288 (class 1259 OID 134238)
-- Name: author_manage_resource_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.author_manage_resource_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.author_manage_resource_id_seq OWNER TO testuser;

--
-- TOC entry 5674 (class 0 OID 0)
-- Dependencies: 288
-- Name: author_manage_resource_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.author_manage_resource_id_seq OWNED BY public.author_manage_resource.id;


--
-- TOC entry 293 (class 1259 OID 134256)
-- Name: author_manage_resource_maintainers; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.author_manage_resource_maintainers (
    id integer NOT NULL,
    resource_id integer NOT NULL,
    maintainer_id integer NOT NULL
);


ALTER TABLE public.author_manage_resource_maintainers OWNER TO testuser;

--
-- TOC entry 292 (class 1259 OID 134254)
-- Name: author_manage_resource_maintainers_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.author_manage_resource_maintainers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.author_manage_resource_maintainers_id_seq OWNER TO testuser;

--
-- TOC entry 5675 (class 0 OID 0)
-- Dependencies: 292
-- Name: author_manage_resource_maintainers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.author_manage_resource_maintainers_id_seq OWNED BY public.author_manage_resource_maintainers.id;


--
-- TOC entry 299 (class 1259 OID 134284)
-- Name: author_manage_resource_owners; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.author_manage_resource_owners (
    id integer NOT NULL,
    resource_id integer NOT NULL,
    owner_id integer NOT NULL
);


ALTER TABLE public.author_manage_resource_owners OWNER TO testuser;

--
-- TOC entry 298 (class 1259 OID 134282)
-- Name: author_manage_resource_owners_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.author_manage_resource_owners_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.author_manage_resource_owners_id_seq OWNER TO testuser;

--
-- TOC entry 5676 (class 0 OID 0)
-- Dependencies: 298
-- Name: author_manage_resource_owners_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.author_manage_resource_owners_id_seq OWNED BY public.author_manage_resource_owners.id;


--
-- TOC entry 291 (class 1259 OID 134248)
-- Name: author_manage_resource_readers; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.author_manage_resource_readers (
    id integer NOT NULL,
    resource_id integer NOT NULL,
    customuser_id integer NOT NULL
);


ALTER TABLE public.author_manage_resource_readers OWNER TO testuser;

--
-- TOC entry 290 (class 1259 OID 134246)
-- Name: author_manage_resource_readers_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.author_manage_resource_readers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.author_manage_resource_readers_id_seq OWNER TO testuser;

--
-- TOC entry 5677 (class 0 OID 0)
-- Dependencies: 290
-- Name: author_manage_resource_readers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.author_manage_resource_readers_id_seq OWNED BY public.author_manage_resource_readers.id;


--
-- TOC entry 216 (class 1259 OID 87177)
-- Name: datasource_types; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.datasource_types (
    id integer NOT NULL,
    name character varying(64) NOT NULL,
    title character varying NOT NULL,
    description character varying
);


ALTER TABLE public.datasource_types OWNER TO testuser;

--
-- TOC entry 215 (class 1259 OID 87175)
-- Name: datasource_types_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.datasource_types_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.datasource_types_id_seq OWNER TO testuser;

--
-- TOC entry 5678 (class 0 OID 0)
-- Dependencies: 215
-- Name: datasource_types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.datasource_types_id_seq OWNED BY public.datasource_types.id;


--
-- TOC entry 222 (class 1259 OID 87222)
-- Name: datasources; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.datasources (
    id integer NOT NULL,
    type_id integer NOT NULL,
    path character varying NOT NULL,
    args character varying,
    creation timestamp without time zone,
    "lastUpdate" timestamp without time zone,
    encoding character varying(64),
    datatype_id integer NOT NULL,
    temporal_scale_id integer,
    spatial_scale_id integer
);


ALTER TABLE public.datasources OWNER TO testuser;

--
-- TOC entry 221 (class 1259 OID 87220)
-- Name: datasources_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.datasources_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.datasources_id_seq OWNER TO testuser;

--
-- TOC entry 5679 (class 0 OID 0)
-- Dependencies: 221
-- Name: datasources_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.datasources_id_seq OWNED BY public.datasources.id;


--
-- TOC entry 240 (class 1259 OID 87468)
-- Name: datatypes; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.datatypes (
    id integer NOT NULL,
    parent_id integer,
    name character varying(64) NOT NULL,
    title character varying NOT NULL,
    description character varying
);


ALTER TABLE public.datatypes OWNER TO testuser;

--
-- TOC entry 239 (class 1259 OID 87466)
-- Name: datatypes_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.datatypes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.datatypes_id_seq OWNER TO testuser;

--
-- TOC entry 5680 (class 0 OID 0)
-- Dependencies: 239
-- Name: datatypes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.datatypes_id_seq OWNED BY public.datatypes.id;


--
-- TOC entry 227 (class 1259 OID 87286)
-- Name: details; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.details (
    id integer NOT NULL,
    entry_id integer,
    key character varying(20) NOT NULL,
    stem character varying(20) NOT NULL,
    value text NOT NULL,
    description character varying,
    thesaurus_id integer
);


ALTER TABLE public.details OWNER TO testuser;

--
-- TOC entry 226 (class 1259 OID 87284)
-- Name: details_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.details_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.details_id_seq OWNER TO testuser;

--
-- TOC entry 5681 (class 0 OID 0)
-- Dependencies: 226
-- Name: details_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.details_id_seq OWNED BY public.details.id;


--
-- TOC entry 285 (class 1259 OID 134197)
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO testuser;

--
-- TOC entry 258 (class 1259 OID 133367)
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.django_admin_log_id_seq
    START WITH 5
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO testuser;

--
-- TOC entry 284 (class 1259 OID 134195)
-- Name: django_admin_log_id_seq1; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.django_admin_log_id_seq1
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq1 OWNER TO testuser;

--
-- TOC entry 5682 (class 0 OID 0)
-- Dependencies: 284
-- Name: django_admin_log_id_seq1; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.django_admin_log_id_seq1 OWNED BY public.django_admin_log.id;


--
-- TOC entry 271 (class 1259 OID 134055)
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO testuser;

--
-- TOC entry 259 (class 1259 OID 133380)
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.django_content_type_id_seq
    START WITH 48
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO testuser;

--
-- TOC entry 270 (class 1259 OID 134053)
-- Name: django_content_type_id_seq1; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.django_content_type_id_seq1
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq1 OWNER TO testuser;

--
-- TOC entry 5683 (class 0 OID 0)
-- Dependencies: 270
-- Name: django_content_type_id_seq1; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.django_content_type_id_seq1 OWNED BY public.django_content_type.id;


--
-- TOC entry 269 (class 1259 OID 134044)
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO testuser;

--
-- TOC entry 268 (class 1259 OID 134042)
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.django_migrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO testuser;

--
-- TOC entry 5684 (class 0 OID 0)
-- Dependencies: 268
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- TOC entry 300 (class 1259 OID 134375)
-- Name: django_session; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO testuser;

--
-- TOC entry 224 (class 1259 OID 87238)
-- Name: entries; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.entries (
    id integer NOT NULL,
    title character varying(512) NOT NULL,
    abstract character varying,
    external_id character varying,
    location public.geometry(Point,4326) NOT NULL,
    geom public.geometry,
    version integer NOT NULL,
    latest_version_id integer,
    comment character varying,
    license_id integer,
    variable_id integer NOT NULL,
    datasource_id integer,
    embargo boolean NOT NULL,
    embargo_end timestamp without time zone,
    publication timestamp without time zone,
    "lastUpdate" timestamp without time zone,
    is_partial boolean NOT NULL,
    uuid character varying(36) NOT NULL,
    citation character varying(2048)
);


ALTER TABLE public.entries OWNER TO testuser;

--
-- TOC entry 223 (class 1259 OID 87236)
-- Name: entries_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.entries_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.entries_id_seq OWNER TO testuser;

--
-- TOC entry 5685 (class 0 OID 0)
-- Dependencies: 223
-- Name: entries_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.entries_id_seq OWNED BY public.entries.id;


--
-- TOC entry 204 (class 1259 OID 87104)
-- Name: entrygroup_types; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.entrygroup_types (
    id integer NOT NULL,
    name character varying(40) NOT NULL,
    description character varying NOT NULL
);


ALTER TABLE public.entrygroup_types OWNER TO testuser;

--
-- TOC entry 203 (class 1259 OID 87102)
-- Name: entrygroup_types_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.entrygroup_types_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.entrygroup_types_id_seq OWNER TO testuser;

--
-- TOC entry 5686 (class 0 OID 0)
-- Dependencies: 203
-- Name: entrygroup_types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.entrygroup_types_id_seq OWNED BY public.entrygroup_types.id;


--
-- TOC entry 218 (class 1259 OID 87188)
-- Name: entrygroups; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.entrygroups (
    id integer NOT NULL,
    type_id integer NOT NULL,
    title character varying(40),
    description character varying,
    uuid character varying(36) NOT NULL,
    publication timestamp without time zone,
    "lastUpdate" timestamp without time zone
);


ALTER TABLE public.entrygroups OWNER TO testuser;

--
-- TOC entry 217 (class 1259 OID 87186)
-- Name: entrygroups_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.entrygroups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.entrygroups_id_seq OWNER TO testuser;

--
-- TOC entry 5687 (class 0 OID 0)
-- Dependencies: 217
-- Name: entrygroups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.entrygroups_id_seq OWNED BY public.entrygroups.id;


--
-- TOC entry 232 (class 1259 OID 87366)
-- Name: generic_1d_data; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.generic_1d_data (
    entry_id integer NOT NULL,
    index numeric NOT NULL,
    value numeric NOT NULL,
    "precision" numeric
);


ALTER TABLE public.generic_1d_data OWNER TO testuser;

--
-- TOC entry 233 (class 1259 OID 87379)
-- Name: generic_2d_data; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.generic_2d_data (
    entry_id integer NOT NULL,
    index numeric NOT NULL,
    value1 numeric NOT NULL,
    value2 numeric NOT NULL,
    precision1 numeric,
    precision2 numeric
);


ALTER TABLE public.generic_2d_data OWNER TO testuser;

--
-- TOC entry 235 (class 1259 OID 87406)
-- Name: generic_geometry_data; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.generic_geometry_data (
    entry_id integer NOT NULL,
    index integer NOT NULL,
    geom public.geometry NOT NULL,
    srid integer
);


ALTER TABLE public.generic_geometry_data OWNER TO testuser;

--
-- TOC entry 234 (class 1259 OID 87392)
-- Name: geom_timeseries; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.geom_timeseries (
    entry_id integer NOT NULL,
    tstamp timestamp without time zone NOT NULL,
    geom public.geometry NOT NULL,
    srid integer
);


ALTER TABLE public.geom_timeseries OWNER TO testuser;

--
-- TOC entry 260 (class 1259 OID 133396)
-- Name: heron_upload_uploadedfile; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.heron_upload_uploadedfile (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    file character varying(100) NOT NULL,
    uploaded_at timestamp with time zone NOT NULL
);


ALTER TABLE public.heron_upload_uploadedfile OWNER TO testuser;

--
-- TOC entry 261 (class 1259 OID 133399)
-- Name: heron_upload_uploadedfile_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.heron_upload_uploadedfile_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.heron_upload_uploadedfile_id_seq OWNER TO testuser;

--
-- TOC entry 5688 (class 0 OID 0)
-- Dependencies: 261
-- Name: heron_upload_uploadedfile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.heron_upload_uploadedfile_id_seq OWNED BY public.heron_upload_uploadedfile.id;


--
-- TOC entry 206 (class 1259 OID 87115)
-- Name: keywords; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.keywords (
    id integer NOT NULL,
    parent_id integer,
    value character varying(1024) NOT NULL,
    uuid character varying(64),
    full_path character varying,
    thesaurus_id integer
);


ALTER TABLE public.keywords OWNER TO testuser;

--
-- TOC entry 205 (class 1259 OID 87113)
-- Name: keywords_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.keywords_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.keywords_id_seq OWNER TO testuser;

--
-- TOC entry 5689 (class 0 OID 0)
-- Dependencies: 205
-- Name: keywords_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.keywords_id_seq OWNED BY public.keywords.id;


--
-- TOC entry 212 (class 1259 OID 87155)
-- Name: licenses; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.licenses (
    id integer NOT NULL,
    short_title character varying(40) NOT NULL,
    title character varying NOT NULL,
    summary character varying,
    full_text character varying,
    link character varying,
    by_attribution boolean NOT NULL,
    share_alike boolean NOT NULL,
    commercial_use boolean NOT NULL
);


ALTER TABLE public.licenses OWNER TO testuser;

--
-- TOC entry 211 (class 1259 OID 87153)
-- Name: licenses_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.licenses_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.licenses_id_seq OWNER TO testuser;

--
-- TOC entry 5690 (class 0 OID 0)
-- Dependencies: 211
-- Name: licenses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.licenses_id_seq OWNED BY public.licenses.id;


--
-- TOC entry 246 (class 1259 OID 87544)
-- Name: logs; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.logs (
    id integer NOT NULL,
    tstamp timestamp without time zone NOT NULL,
    code integer NOT NULL,
    description character varying NOT NULL,
    migration_head integer
);


ALTER TABLE public.logs OWNER TO testuser;

--
-- TOC entry 245 (class 1259 OID 87542)
-- Name: logs_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.logs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.logs_id_seq OWNER TO testuser;

--
-- TOC entry 5691 (class 0 OID 0)
-- Dependencies: 245
-- Name: logs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.logs_id_seq OWNED BY public.logs.id;


--
-- TOC entry 225 (class 1259 OID 87269)
-- Name: nm_entrygroups; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.nm_entrygroups (
    entry_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.nm_entrygroups OWNER TO testuser;

--
-- TOC entry 228 (class 1259 OID 87302)
-- Name: nm_keywords_entries; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.nm_keywords_entries (
    keyword_id integer NOT NULL,
    entry_id integer NOT NULL
);


ALTER TABLE public.nm_keywords_entries OWNER TO testuser;

--
-- TOC entry 229 (class 1259 OID 87320)
-- Name: nm_persons_entries; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.nm_persons_entries (
    person_id integer NOT NULL,
    entry_id integer NOT NULL,
    relationship_type_id integer NOT NULL,
    "order" integer NOT NULL
);


ALTER TABLE public.nm_persons_entries OWNER TO testuser;

--
-- TOC entry 210 (class 1259 OID 87144)
-- Name: person_roles; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.person_roles (
    id integer NOT NULL,
    name character varying(64) NOT NULL,
    description character varying
);


ALTER TABLE public.person_roles OWNER TO testuser;

--
-- TOC entry 209 (class 1259 OID 87142)
-- Name: person_roles_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.person_roles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.person_roles_id_seq OWNER TO testuser;

--
-- TOC entry 5692 (class 0 OID 0)
-- Dependencies: 209
-- Name: person_roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.person_roles_id_seq OWNED BY public.person_roles.id;


--
-- TOC entry 208 (class 1259 OID 87133)
-- Name: persons; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.persons (
    id integer NOT NULL,
    first_name character varying(128),
    last_name character varying(128),
    affiliation character varying(1024),
    organisation_name character varying(1024),
    attribution character varying(1024),
    is_organisation boolean NOT NULL,
    organisation_abbrev character varying(64),
    CONSTRAINT check_names CHECK ((NOT ((last_name IS NULL) AND (organisation_name IS NULL))))
);


ALTER TABLE public.persons OWNER TO testuser;

--
-- TOC entry 207 (class 1259 OID 87131)
-- Name: persons_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.persons_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.persons_id_seq OWNER TO testuser;

--
-- TOC entry 5693 (class 0 OID 0)
-- Dependencies: 207
-- Name: persons_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.persons_id_seq OWNED BY public.persons.id;


--
-- TOC entry 244 (class 1259 OID 87501)
-- Name: spatial_scales; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.spatial_scales (
    id integer NOT NULL,
    resolution integer NOT NULL,
    extent public.geometry(Polygon,4326) NOT NULL,
    support numeric NOT NULL,
    CONSTRAINT spatial_scales_support_check CHECK ((support >= (0)::numeric))
);


ALTER TABLE public.spatial_scales OWNER TO testuser;

--
-- TOC entry 243 (class 1259 OID 87499)
-- Name: spatial_scales_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.spatial_scales_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.spatial_scales_id_seq OWNER TO testuser;

--
-- TOC entry 5695 (class 0 OID 0)
-- Dependencies: 243
-- Name: spatial_scales_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.spatial_scales_id_seq OWNED BY public.spatial_scales.id;


--
-- TOC entry 242 (class 1259 OID 87489)
-- Name: temporal_scales; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.temporal_scales (
    id integer NOT NULL,
    resolution character varying NOT NULL,
    observation_start timestamp without time zone NOT NULL,
    observation_end timestamp without time zone NOT NULL,
    support numeric NOT NULL,
    CONSTRAINT temporal_scales_support_check CHECK ((support >= (0)::numeric))
);


ALTER TABLE public.temporal_scales OWNER TO testuser;

--
-- TOC entry 241 (class 1259 OID 87487)
-- Name: temporal_scales_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.temporal_scales_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.temporal_scales_id_seq OWNER TO testuser;

--
-- TOC entry 5696 (class 0 OID 0)
-- Dependencies: 241
-- Name: temporal_scales_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.temporal_scales_id_seq OWNED BY public.temporal_scales.id;


--
-- TOC entry 238 (class 1259 OID 87448)
-- Name: thesaurus; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.thesaurus (
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    name character varying(1024) NOT NULL,
    title character varying NOT NULL,
    organisation character varying NOT NULL,
    description character varying,
    url character varying NOT NULL
);


ALTER TABLE public.thesaurus OWNER TO testuser;

--
-- TOC entry 237 (class 1259 OID 87446)
-- Name: thesaurus_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.thesaurus_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.thesaurus_id_seq OWNER TO testuser;

--
-- TOC entry 5697 (class 0 OID 0)
-- Dependencies: 237
-- Name: thesaurus_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.thesaurus_id_seq OWNED BY public.thesaurus.id;


--
-- TOC entry 230 (class 1259 OID 87340)
-- Name: timeseries; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.timeseries (
    entry_id integer NOT NULL,
    tstamp timestamp without time zone NOT NULL,
    value numeric NOT NULL,
    "precision" numeric
);


ALTER TABLE public.timeseries OWNER TO testuser;

--
-- TOC entry 231 (class 1259 OID 87353)
-- Name: timeseries_2d; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.timeseries_2d (
    entry_id integer NOT NULL,
    tstamp timestamp without time zone NOT NULL,
    value1 numeric NOT NULL,
    value2 numeric NOT NULL,
    precision1 numeric,
    precision2 numeric
);


ALTER TABLE public.timeseries_2d OWNER TO testuser;

--
-- TOC entry 214 (class 1259 OID 87166)
-- Name: units; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.units (
    id integer NOT NULL,
    name character varying(64) NOT NULL,
    symbol character varying(12) NOT NULL,
    si character varying
);


ALTER TABLE public.units OWNER TO testuser;

--
-- TOC entry 213 (class 1259 OID 87164)
-- Name: units_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.units_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.units_id_seq OWNER TO testuser;

--
-- TOC entry 5698 (class 0 OID 0)
-- Dependencies: 213
-- Name: units_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.units_id_seq OWNED BY public.units.id;


--
-- TOC entry 262 (class 1259 OID 133533)
-- Name: upload_temp; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.upload_temp (
    tstamp text,
    value numeric,
    meta_id integer
);


ALTER TABLE public.upload_temp OWNER TO testuser;

--
-- TOC entry 220 (class 1259 OID 87204)
-- Name: variables; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.variables (
    id integer NOT NULL,
    name character varying(64) NOT NULL,
    symbol character varying(12) NOT NULL,
    unit_id integer NOT NULL,
    keyword_id integer
);


ALTER TABLE public.variables OWNER TO testuser;

--
-- TOC entry 219 (class 1259 OID 87202)
-- Name: variables_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.variables_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.variables_id_seq OWNER TO testuser;

--
-- TOC entry 5699 (class 0 OID 0)
-- Dependencies: 219
-- Name: variables_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.variables_id_seq OWNED BY public.variables.id;


--
-- TOC entry 263 (class 1259 OID 133551)
-- Name: watts_rsp_authfailureresponse; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.watts_rsp_authfailureresponse (
    id integer NOT NULL,
    watts_ref character varying(32) NOT NULL,
    "time" timestamp with time zone NOT NULL,
    msg text
);


ALTER TABLE public.watts_rsp_authfailureresponse OWNER TO testuser;

--
-- TOC entry 264 (class 1259 OID 133557)
-- Name: watts_rsp_authfailureresponse_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.watts_rsp_authfailureresponse_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.watts_rsp_authfailureresponse_id_seq OWNER TO testuser;

--
-- TOC entry 5700 (class 0 OID 0)
-- Dependencies: 264
-- Name: watts_rsp_authfailureresponse_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.watts_rsp_authfailureresponse_id_seq OWNED BY public.watts_rsp_authfailureresponse.id;


--
-- TOC entry 265 (class 1259 OID 133559)
-- Name: watts_rsp_authsuccessresponse; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.watts_rsp_authsuccessresponse (
    id integer NOT NULL,
    watts_ref character varying(32) NOT NULL,
    "time" timestamp with time zone NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.watts_rsp_authsuccessresponse OWNER TO testuser;

--
-- TOC entry 266 (class 1259 OID 133562)
-- Name: watts_rsp_authsuccessresponse_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.watts_rsp_authsuccessresponse_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.watts_rsp_authsuccessresponse_id_seq OWNER TO testuser;

--
-- TOC entry 5701 (class 0 OID 0)
-- Dependencies: 266
-- Name: watts_rsp_authsuccessresponse_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.watts_rsp_authsuccessresponse_id_seq OWNED BY public.watts_rsp_authsuccessresponse.id;


--
-- TOC entry 267 (class 1259 OID 133564)
-- Name: watts_rsp_rsakey; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.watts_rsp_rsakey (
    key_id character varying(200) NOT NULL,
    intended_usage character varying(3) NOT NULL,
    sha_size integer NOT NULL,
    pem text NOT NULL,
    CONSTRAINT watts_rsp_rsakey_sha_size_check CHECK ((sha_size >= 0))
);


ALTER TABLE public.watts_rsp_rsakey OWNER TO testuser;

--
-- TOC entry 302 (class 1259 OID 134390)
-- Name: wps_gui_webprocessingservice; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.wps_gui_webprocessingservice (
    id integer NOT NULL,
    name character varying(30) NOT NULL,
    endpoint character varying(1024) NOT NULL,
    username character varying(100) NOT NULL,
    password character varying(100) NOT NULL
);


ALTER TABLE public.wps_gui_webprocessingservice OWNER TO testuser;

--
-- TOC entry 301 (class 1259 OID 134388)
-- Name: wps_gui_webprocessingservice_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.wps_gui_webprocessingservice_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.wps_gui_webprocessingservice_id_seq OWNER TO testuser;

--
-- TOC entry 5702 (class 0 OID 0)
-- Dependencies: 301
-- Name: wps_gui_webprocessingservice_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.wps_gui_webprocessingservice_id_seq OWNED BY public.wps_gui_webprocessingservice.id;


--
-- TOC entry 304 (class 1259 OID 134403)
-- Name: wps_gui_wpsresults; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.wps_gui_wpsresults (
    id integer NOT NULL,
    creation timestamp with time zone,
    access timestamp with time zone,
    open boolean NOT NULL,
    outputs character varying(1024) NOT NULL,
    wps character varying(255) NOT NULL,
    inputs character varying(2048) NOT NULL
);


ALTER TABLE public.wps_gui_wpsresults OWNER TO testuser;

--
-- TOC entry 303 (class 1259 OID 134401)
-- Name: wps_gui_wpsresults_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.wps_gui_wpsresults_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.wps_gui_wpsresults_id_seq OWNER TO testuser;

--
-- TOC entry 5703 (class 0 OID 0)
-- Dependencies: 303
-- Name: wps_gui_wpsresults_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.wps_gui_wpsresults_id_seq OWNED BY public.wps_gui_wpsresults.id;


--
-- TOC entry 5287 (class 2604 OID 134104)
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- TOC entry 5288 (class 2604 OID 134114)
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- TOC entry 5286 (class 2604 OID 134096)
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- TOC entry 5289 (class 2604 OID 134122)
-- Name: auth_user id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.auth_user ALTER COLUMN id SET DEFAULT nextval('public.auth_user_id_seq1'::regclass);


--
-- TOC entry 5290 (class 2604 OID 134132)
-- Name: auth_user_groups id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.auth_user_groups ALTER COLUMN id SET DEFAULT nextval('public.auth_user_groups_id_seq'::regclass);


--
-- TOC entry 5291 (class 2604 OID 134140)
-- Name: auth_user_user_permissions id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_user_user_permissions_id_seq'::regclass);


--
-- TOC entry 5299 (class 2604 OID 134277)
-- Name: author_manage_accessrequest id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.author_manage_accessrequest ALTER COLUMN id SET DEFAULT nextval('public.author_manage_accessrequest_id_seq'::regclass);


--
-- TOC entry 5298 (class 2604 OID 134267)
-- Name: author_manage_deletionrequest id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.author_manage_deletionrequest ALTER COLUMN id SET DEFAULT nextval('public.author_manage_deletionrequest_id_seq'::regclass);


--
-- TOC entry 5294 (class 2604 OID 134233)
-- Name: author_manage_profile id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.author_manage_profile ALTER COLUMN id SET DEFAULT nextval('public.author_manage_profile_id_seq'::regclass);


--
-- TOC entry 5295 (class 2604 OID 134243)
-- Name: author_manage_resource id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.author_manage_resource ALTER COLUMN id SET DEFAULT nextval('public.author_manage_resource_id_seq'::regclass);


--
-- TOC entry 5297 (class 2604 OID 134259)
-- Name: author_manage_resource_maintainers id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.author_manage_resource_maintainers ALTER COLUMN id SET DEFAULT nextval('public.author_manage_resource_maintainers_id_seq'::regclass);


--
-- TOC entry 5300 (class 2604 OID 134287)
-- Name: author_manage_resource_owners id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.author_manage_resource_owners ALTER COLUMN id SET DEFAULT nextval('public.author_manage_resource_owners_id_seq'::regclass);


--
-- TOC entry 5296 (class 2604 OID 134251)
-- Name: author_manage_resource_readers id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.author_manage_resource_readers ALTER COLUMN id SET DEFAULT nextval('public.author_manage_resource_readers_id_seq'::regclass);


--
-- TOC entry 5267 (class 2604 OID 87180)
-- Name: datasource_types id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.datasource_types ALTER COLUMN id SET DEFAULT nextval('public.datasource_types_id_seq'::regclass);


--
-- TOC entry 5270 (class 2604 OID 87225)
-- Name: datasources id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.datasources ALTER COLUMN id SET DEFAULT nextval('public.datasources_id_seq'::regclass);


--
-- TOC entry 5274 (class 2604 OID 87471)
-- Name: datatypes id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.datatypes ALTER COLUMN id SET DEFAULT nextval('public.datatypes_id_seq'::regclass);


--
-- TOC entry 5272 (class 2604 OID 87289)
-- Name: details id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.details ALTER COLUMN id SET DEFAULT nextval('public.details_id_seq'::regclass);


--
-- TOC entry 5292 (class 2604 OID 134200)
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq1'::regclass);


--
-- TOC entry 5285 (class 2604 OID 134058)
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq1'::regclass);


--
-- TOC entry 5284 (class 2604 OID 134047)
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- TOC entry 5271 (class 2604 OID 87241)
-- Name: entries id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.entries ALTER COLUMN id SET DEFAULT nextval('public.entries_id_seq'::regclass);


--
-- TOC entry 5260 (class 2604 OID 87107)
-- Name: entrygroup_types id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.entrygroup_types ALTER COLUMN id SET DEFAULT nextval('public.entrygroup_types_id_seq'::regclass);


--
-- TOC entry 5268 (class 2604 OID 87191)
-- Name: entrygroups id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.entrygroups ALTER COLUMN id SET DEFAULT nextval('public.entrygroups_id_seq'::regclass);


--
-- TOC entry 5280 (class 2604 OID 133599)
-- Name: heron_upload_uploadedfile id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.heron_upload_uploadedfile ALTER COLUMN id SET DEFAULT nextval('public.heron_upload_uploadedfile_id_seq'::regclass);


--
-- TOC entry 5261 (class 2604 OID 87118)
-- Name: keywords id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.keywords ALTER COLUMN id SET DEFAULT nextval('public.keywords_id_seq'::regclass);


--
-- TOC entry 5265 (class 2604 OID 87158)
-- Name: licenses id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.licenses ALTER COLUMN id SET DEFAULT nextval('public.licenses_id_seq'::regclass);


--
-- TOC entry 5279 (class 2604 OID 87547)
-- Name: logs id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.logs ALTER COLUMN id SET DEFAULT nextval('public.logs_id_seq'::regclass);


--
-- TOC entry 5264 (class 2604 OID 87147)
-- Name: person_roles id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.person_roles ALTER COLUMN id SET DEFAULT nextval('public.person_roles_id_seq'::regclass);


--
-- TOC entry 5262 (class 2604 OID 87136)
-- Name: persons id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.persons ALTER COLUMN id SET DEFAULT nextval('public.persons_id_seq'::regclass);


--
-- TOC entry 5277 (class 2604 OID 87504)
-- Name: spatial_scales id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.spatial_scales ALTER COLUMN id SET DEFAULT nextval('public.spatial_scales_id_seq'::regclass);


--
-- TOC entry 5275 (class 2604 OID 87492)
-- Name: temporal_scales id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.temporal_scales ALTER COLUMN id SET DEFAULT nextval('public.temporal_scales_id_seq'::regclass);


--
-- TOC entry 5273 (class 2604 OID 87451)
-- Name: thesaurus id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.thesaurus ALTER COLUMN id SET DEFAULT nextval('public.thesaurus_id_seq'::regclass);


--
-- TOC entry 5266 (class 2604 OID 87169)
-- Name: units id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.units ALTER COLUMN id SET DEFAULT nextval('public.units_id_seq'::regclass);


--
-- TOC entry 5269 (class 2604 OID 87207)
-- Name: variables id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.variables ALTER COLUMN id SET DEFAULT nextval('public.variables_id_seq'::regclass);


--
-- TOC entry 5281 (class 2604 OID 133999)
-- Name: watts_rsp_authfailureresponse id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.watts_rsp_authfailureresponse ALTER COLUMN id SET DEFAULT nextval('public.watts_rsp_authfailureresponse_id_seq'::regclass);


--
-- TOC entry 5282 (class 2604 OID 134000)
-- Name: watts_rsp_authsuccessresponse id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.watts_rsp_authsuccessresponse ALTER COLUMN id SET DEFAULT nextval('public.watts_rsp_authsuccessresponse_id_seq'::regclass);


--
-- TOC entry 5301 (class 2604 OID 134393)
-- Name: wps_gui_webprocessingservice id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.wps_gui_webprocessingservice ALTER COLUMN id SET DEFAULT nextval('public.wps_gui_webprocessingservice_id_seq'::regclass);


--
-- TOC entry 5302 (class 2604 OID 134406)
-- Name: wps_gui_wpsresults id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.wps_gui_wpsresults ALTER COLUMN id SET DEFAULT nextval('public.wps_gui_wpsresults_id_seq'::regclass);


--
-- TOC entry 5354 (class 2606 OID 87445)
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- TOC entry 5393 (class 2606 OID 134226)
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- TOC entry 5398 (class 2606 OID 134163)
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- TOC entry 5401 (class 2606 OID 134116)
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- TOC entry 5395 (class 2606 OID 134106)
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- TOC entry 5388 (class 2606 OID 134149)
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- TOC entry 5390 (class 2606 OID 134098)
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- TOC entry 5409 (class 2606 OID 134134)
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- TOC entry 5412 (class 2606 OID 134178)
-- Name: auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- TOC entry 5403 (class 2606 OID 134124)
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- TOC entry 5415 (class 2606 OID 134142)
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- TOC entry 5418 (class 2606 OID 134192)
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- TOC entry 5406 (class 2606 OID 134220)
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- TOC entry 5451 (class 2606 OID 134279)
-- Name: author_manage_accessrequest author_manage_accessrequest_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.author_manage_accessrequest
    ADD CONSTRAINT author_manage_accessrequest_pkey PRIMARY KEY (id);


--
-- TOC entry 5454 (class 2606 OID 134281)
-- Name: author_manage_accessrequest author_manage_accessrequest_sender_id_key; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.author_manage_accessrequest
    ADD CONSTRAINT author_manage_accessrequest_sender_id_key UNIQUE (sender_id);


--
-- TOC entry 5456 (class 2606 OID 134359)
-- Name: author_manage_accessrequest author_manage_accessrequest_sender_id_resource_id_40a63d6e_uniq; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.author_manage_accessrequest
    ADD CONSTRAINT author_manage_accessrequest_sender_id_resource_id_40a63d6e_uniq UNIQUE (sender_id, resource_id);


--
-- TOC entry 5444 (class 2606 OID 134346)
-- Name: author_manage_deletionrequest author_manage_deletionre_sender_id_resource_id_35ddc071_uniq; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.author_manage_deletionrequest
    ADD CONSTRAINT author_manage_deletionre_sender_id_resource_id_35ddc071_uniq UNIQUE (sender_id, resource_id);


--
-- TOC entry 5446 (class 2606 OID 134269)
-- Name: author_manage_deletionrequest author_manage_deletionrequest_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.author_manage_deletionrequest
    ADD CONSTRAINT author_manage_deletionrequest_pkey PRIMARY KEY (id);


--
-- TOC entry 5449 (class 2606 OID 134271)
-- Name: author_manage_deletionrequest author_manage_deletionrequest_sender_id_key; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.author_manage_deletionrequest
    ADD CONSTRAINT author_manage_deletionrequest_sender_id_key UNIQUE (sender_id);


--
-- TOC entry 5425 (class 2606 OID 134235)
-- Name: author_manage_profile author_manage_profile_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.author_manage_profile
    ADD CONSTRAINT author_manage_profile_pkey PRIMARY KEY (id);


--
-- TOC entry 5427 (class 2606 OID 134237)
-- Name: author_manage_profile author_manage_profile_user_id_key; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.author_manage_profile
    ADD CONSTRAINT author_manage_profile_user_id_key UNIQUE (user_id);


--
-- TOC entry 5438 (class 2606 OID 134332)
-- Name: author_manage_resource_maintainers author_manage_resource_m_resource_id_maintainer_i_a1321db8_uniq; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.author_manage_resource_maintainers
    ADD CONSTRAINT author_manage_resource_m_resource_id_maintainer_i_a1321db8_uniq UNIQUE (resource_id, maintainer_id);


--
-- TOC entry 5441 (class 2606 OID 134261)
-- Name: author_manage_resource_maintainers author_manage_resource_maintainers_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.author_manage_resource_maintainers
    ADD CONSTRAINT author_manage_resource_maintainers_pkey PRIMARY KEY (id);


--
-- TOC entry 5458 (class 2606 OID 134372)
-- Name: author_manage_resource_owners author_manage_resource_o_resource_id_owner_id_73e5d69f_uniq; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.author_manage_resource_owners
    ADD CONSTRAINT author_manage_resource_o_resource_id_owner_id_73e5d69f_uniq UNIQUE (resource_id, owner_id);


--
-- TOC entry 5461 (class 2606 OID 134289)
-- Name: author_manage_resource_owners author_manage_resource_owners_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.author_manage_resource_owners
    ADD CONSTRAINT author_manage_resource_owners_pkey PRIMARY KEY (id);


--
-- TOC entry 5430 (class 2606 OID 134245)
-- Name: author_manage_resource author_manage_resource_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.author_manage_resource
    ADD CONSTRAINT author_manage_resource_pkey PRIMARY KEY (id);


--
-- TOC entry 5432 (class 2606 OID 134318)
-- Name: author_manage_resource_readers author_manage_resource_r_resource_id_customuser_i_8102fb68_uniq; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.author_manage_resource_readers
    ADD CONSTRAINT author_manage_resource_r_resource_id_customuser_i_8102fb68_uniq UNIQUE (resource_id, customuser_id);


--
-- TOC entry 5435 (class 2606 OID 134253)
-- Name: author_manage_resource_readers author_manage_resource_readers_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.author_manage_resource_readers
    ADD CONSTRAINT author_manage_resource_readers_pkey PRIMARY KEY (id);


--
-- TOC entry 5318 (class 2606 OID 87185)
-- Name: datasource_types datasource_types_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.datasource_types
    ADD CONSTRAINT datasource_types_pkey PRIMARY KEY (id);


--
-- TOC entry 5324 (class 2606 OID 87230)
-- Name: datasources datasources_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.datasources
    ADD CONSTRAINT datasources_pkey PRIMARY KEY (id);


--
-- TOC entry 5362 (class 2606 OID 87476)
-- Name: datatypes datatypes_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.datatypes
    ADD CONSTRAINT datatypes_pkey PRIMARY KEY (id);


--
-- TOC entry 5332 (class 2606 OID 87296)
-- Name: details details_entry_id_stem_key; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.details
    ADD CONSTRAINT details_entry_id_stem_key UNIQUE (entry_id, stem);


--
-- TOC entry 5334 (class 2606 OID 87294)
-- Name: details details_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.details
    ADD CONSTRAINT details_pkey PRIMARY KEY (id);


--
-- TOC entry 5421 (class 2606 OID 134206)
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- TOC entry 5383 (class 2606 OID 134062)
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- TOC entry 5385 (class 2606 OID 134060)
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- TOC entry 5381 (class 2606 OID 134052)
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- TOC entry 5465 (class 2606 OID 134382)
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- TOC entry 5326 (class 2606 OID 87246)
-- Name: entries entries_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.entries
    ADD CONSTRAINT entries_pkey PRIMARY KEY (id);


--
-- TOC entry 5304 (class 2606 OID 87112)
-- Name: entrygroup_types entrygroup_types_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.entrygroup_types
    ADD CONSTRAINT entrygroup_types_pkey PRIMARY KEY (id);


--
-- TOC entry 5320 (class 2606 OID 87196)
-- Name: entrygroups entrygroups_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.entrygroups
    ADD CONSTRAINT entrygroups_pkey PRIMARY KEY (id);


--
-- TOC entry 5351 (class 2606 OID 87413)
-- Name: generic_geometry_data geneic_geometry_data_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.generic_geometry_data
    ADD CONSTRAINT geneic_geometry_data_pkey PRIMARY KEY (entry_id, index);


--
-- TOC entry 5344 (class 2606 OID 87373)
-- Name: generic_1d_data generic_1d_data_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.generic_1d_data
    ADD CONSTRAINT generic_1d_data_pkey PRIMARY KEY (entry_id, index);


--
-- TOC entry 5346 (class 2606 OID 87386)
-- Name: generic_2d_data generic_2d_data_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.generic_2d_data
    ADD CONSTRAINT generic_2d_data_pkey PRIMARY KEY (entry_id, index);


--
-- TOC entry 5348 (class 2606 OID 87399)
-- Name: geom_timeseries geom_timeseries_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.geom_timeseries
    ADD CONSTRAINT geom_timeseries_pkey PRIMARY KEY (entry_id, tstamp);


--
-- TOC entry 5371 (class 2606 OID 133689)
-- Name: heron_upload_uploadedfile heron_upload_uploadedfile_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.heron_upload_uploadedfile
    ADD CONSTRAINT heron_upload_uploadedfile_pkey PRIMARY KEY (id);


--
-- TOC entry 5306 (class 2606 OID 87123)
-- Name: keywords keywords_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.keywords
    ADD CONSTRAINT keywords_pkey PRIMARY KEY (id);


--
-- TOC entry 5308 (class 2606 OID 87125)
-- Name: keywords keywords_uuid_key; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.keywords
    ADD CONSTRAINT keywords_uuid_key UNIQUE (uuid);


--
-- TOC entry 5314 (class 2606 OID 87163)
-- Name: licenses licenses_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.licenses
    ADD CONSTRAINT licenses_pkey PRIMARY KEY (id);


--
-- TOC entry 5369 (class 2606 OID 87552)
-- Name: logs logs_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.logs
    ADD CONSTRAINT logs_pkey PRIMARY KEY (id);


--
-- TOC entry 5330 (class 2606 OID 87273)
-- Name: nm_entrygroups nm_entrygroups_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.nm_entrygroups
    ADD CONSTRAINT nm_entrygroups_pkey PRIMARY KEY (entry_id, group_id);


--
-- TOC entry 5336 (class 2606 OID 87309)
-- Name: nm_keywords_entries nm_keywords_entries_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.nm_keywords_entries
    ADD CONSTRAINT nm_keywords_entries_pkey PRIMARY KEY (keyword_id, entry_id);


--
-- TOC entry 5338 (class 2606 OID 87324)
-- Name: nm_persons_entries nm_persons_entries_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.nm_persons_entries
    ADD CONSTRAINT nm_persons_entries_pkey PRIMARY KEY (person_id, entry_id);


--
-- TOC entry 5312 (class 2606 OID 87152)
-- Name: person_roles person_roles_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.person_roles
    ADD CONSTRAINT person_roles_pkey PRIMARY KEY (id);


--
-- TOC entry 5310 (class 2606 OID 87141)
-- Name: persons persons_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.persons
    ADD CONSTRAINT persons_pkey PRIMARY KEY (id);


--
-- TOC entry 5367 (class 2606 OID 87510)
-- Name: spatial_scales spatial_scales_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.spatial_scales
    ADD CONSTRAINT spatial_scales_pkey PRIMARY KEY (id);


--
-- TOC entry 5364 (class 2606 OID 87498)
-- Name: temporal_scales temporal_scales_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.temporal_scales
    ADD CONSTRAINT temporal_scales_pkey PRIMARY KEY (id);


--
-- TOC entry 5356 (class 2606 OID 87460)
-- Name: thesaurus thesaurus_name_key; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.thesaurus
    ADD CONSTRAINT thesaurus_name_key UNIQUE (name);


--
-- TOC entry 5358 (class 2606 OID 87456)
-- Name: thesaurus thesaurus_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.thesaurus
    ADD CONSTRAINT thesaurus_pkey PRIMARY KEY (id);


--
-- TOC entry 5360 (class 2606 OID 87458)
-- Name: thesaurus thesaurus_uuid_key; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.thesaurus
    ADD CONSTRAINT thesaurus_uuid_key UNIQUE (uuid);


--
-- TOC entry 5342 (class 2606 OID 87360)
-- Name: timeseries_2d timeseries_2d_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.timeseries_2d
    ADD CONSTRAINT timeseries_2d_pkey PRIMARY KEY (entry_id, tstamp);


--
-- TOC entry 5340 (class 2606 OID 87347)
-- Name: timeseries timeseries_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.timeseries
    ADD CONSTRAINT timeseries_pkey PRIMARY KEY (entry_id, tstamp);


--
-- TOC entry 5316 (class 2606 OID 87174)
-- Name: units units_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.units
    ADD CONSTRAINT units_pkey PRIMARY KEY (id);


--
-- TOC entry 5322 (class 2606 OID 87209)
-- Name: variables variables_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.variables
    ADD CONSTRAINT variables_pkey PRIMARY KEY (id);


--
-- TOC entry 5373 (class 2606 OID 133737)
-- Name: watts_rsp_authfailureresponse watts_rsp_authfailureresponse_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.watts_rsp_authfailureresponse
    ADD CONSTRAINT watts_rsp_authfailureresponse_pkey PRIMARY KEY (id);


--
-- TOC entry 5375 (class 2606 OID 133739)
-- Name: watts_rsp_authsuccessresponse watts_rsp_authsuccessresponse_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.watts_rsp_authsuccessresponse
    ADD CONSTRAINT watts_rsp_authsuccessresponse_pkey PRIMARY KEY (id);


--
-- TOC entry 5379 (class 2606 OID 133741)
-- Name: watts_rsp_rsakey watts_rsp_rsakey_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.watts_rsp_rsakey
    ADD CONSTRAINT watts_rsp_rsakey_pkey PRIMARY KEY (key_id);


--
-- TOC entry 5469 (class 2606 OID 134400)
-- Name: wps_gui_webprocessingservice wps_gui_webprocessingservice_name_key; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.wps_gui_webprocessingservice
    ADD CONSTRAINT wps_gui_webprocessingservice_name_key UNIQUE (name);


--
-- TOC entry 5471 (class 2606 OID 134398)
-- Name: wps_gui_webprocessingservice wps_gui_webprocessingservice_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.wps_gui_webprocessingservice
    ADD CONSTRAINT wps_gui_webprocessingservice_pkey PRIMARY KEY (id);


--
-- TOC entry 5473 (class 2606 OID 134411)
-- Name: wps_gui_wpsresults wps_gui_wpsresults_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.wps_gui_wpsresults
    ADD CONSTRAINT wps_gui_wpsresults_pkey PRIMARY KEY (id);


--
-- TOC entry 5391 (class 1259 OID 134227)
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: testuser
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- TOC entry 5396 (class 1259 OID 134164)
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: testuser
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- TOC entry 5399 (class 1259 OID 134165)
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: testuser
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- TOC entry 5386 (class 1259 OID 134150)
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: testuser
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- TOC entry 5407 (class 1259 OID 134180)
-- Name: auth_user_groups_group_id_97559544; Type: INDEX; Schema: public; Owner: testuser
--

CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);


--
-- TOC entry 5410 (class 1259 OID 134179)
-- Name: auth_user_groups_user_id_6a12ed8b; Type: INDEX; Schema: public; Owner: testuser
--

CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);


--
-- TOC entry 5413 (class 1259 OID 134194)
-- Name: auth_user_user_permissions_permission_id_1fbb5f2c; Type: INDEX; Schema: public; Owner: testuser
--

CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);


--
-- TOC entry 5416 (class 1259 OID 134193)
-- Name: auth_user_user_permissions_user_id_a95ead1b; Type: INDEX; Schema: public; Owner: testuser
--

CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);


--
-- TOC entry 5404 (class 1259 OID 134221)
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: testuser
--

CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);


--
-- TOC entry 5452 (class 1259 OID 134360)
-- Name: author_manage_accessrequest_resource_id_ebff19e3; Type: INDEX; Schema: public; Owner: testuser
--

CREATE INDEX author_manage_accessrequest_resource_id_ebff19e3 ON public.author_manage_accessrequest USING btree (resource_id);


--
-- TOC entry 5447 (class 1259 OID 134347)
-- Name: author_manage_deletionrequest_resource_id_bbd36a01; Type: INDEX; Schema: public; Owner: testuser
--

CREATE INDEX author_manage_deletionrequest_resource_id_bbd36a01 ON public.author_manage_deletionrequest USING btree (resource_id);


--
-- TOC entry 5423 (class 1259 OID 134300)
-- Name: author_manage_profile_metacatalogPerson_id_c3544139; Type: INDEX; Schema: public; Owner: testuser
--

CREATE INDEX "author_manage_profile_metacatalogPerson_id_c3544139" ON public.author_manage_profile USING btree ("metacatalogPerson_id");


--
-- TOC entry 5428 (class 1259 OID 134306)
-- Name: author_manage_resource_dataEntry_id_7631c6c9; Type: INDEX; Schema: public; Owner: testuser
--

CREATE INDEX "author_manage_resource_dataEntry_id_7631c6c9" ON public.author_manage_resource USING btree ("dataEntry_id");


--
-- TOC entry 5439 (class 1259 OID 134334)
-- Name: author_manage_resource_maintainers_maintainer_id_819092da; Type: INDEX; Schema: public; Owner: testuser
--

CREATE INDEX author_manage_resource_maintainers_maintainer_id_819092da ON public.author_manage_resource_maintainers USING btree (maintainer_id);


--
-- TOC entry 5442 (class 1259 OID 134333)
-- Name: author_manage_resource_maintainers_resource_id_96b7c96f; Type: INDEX; Schema: public; Owner: testuser
--

CREATE INDEX author_manage_resource_maintainers_resource_id_96b7c96f ON public.author_manage_resource_maintainers USING btree (resource_id);


--
-- TOC entry 5459 (class 1259 OID 134374)
-- Name: author_manage_resource_owners_owner_id_32e02247; Type: INDEX; Schema: public; Owner: testuser
--

CREATE INDEX author_manage_resource_owners_owner_id_32e02247 ON public.author_manage_resource_owners USING btree (owner_id);


--
-- TOC entry 5462 (class 1259 OID 134373)
-- Name: author_manage_resource_owners_resource_id_b0933f5e; Type: INDEX; Schema: public; Owner: testuser
--

CREATE INDEX author_manage_resource_owners_resource_id_b0933f5e ON public.author_manage_resource_owners USING btree (resource_id);


--
-- TOC entry 5433 (class 1259 OID 134320)
-- Name: author_manage_resource_readers_customuser_id_daf81cec; Type: INDEX; Schema: public; Owner: testuser
--

CREATE INDEX author_manage_resource_readers_customuser_id_daf81cec ON public.author_manage_resource_readers USING btree (customuser_id);


--
-- TOC entry 5436 (class 1259 OID 134319)
-- Name: author_manage_resource_readers_resource_id_6de33a32; Type: INDEX; Schema: public; Owner: testuser
--

CREATE INDEX author_manage_resource_readers_resource_id_6de33a32 ON public.author_manage_resource_readers USING btree (resource_id);


--
-- TOC entry 5419 (class 1259 OID 134217)
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: testuser
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- TOC entry 5422 (class 1259 OID 134218)
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: testuser
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- TOC entry 5463 (class 1259 OID 134384)
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: testuser
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- TOC entry 5466 (class 1259 OID 134383)
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: testuser
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- TOC entry 5327 (class 1259 OID 87268)
-- Name: idx_entries_geom; Type: INDEX; Schema: public; Owner: testuser
--

CREATE INDEX idx_entries_geom ON public.entries USING gist (geom);


--
-- TOC entry 5328 (class 1259 OID 87522)
-- Name: idx_entries_location; Type: INDEX; Schema: public; Owner: testuser
--

CREATE INDEX idx_entries_location ON public.entries USING gist (location);


--
-- TOC entry 5352 (class 1259 OID 87419)
-- Name: idx_geneic_geometry_data_geom; Type: INDEX; Schema: public; Owner: testuser
--

CREATE INDEX idx_geneic_geometry_data_geom ON public.generic_geometry_data USING gist (geom);


--
-- TOC entry 5349 (class 1259 OID 87405)
-- Name: idx_geom_timeseries_geom; Type: INDEX; Schema: public; Owner: testuser
--

CREATE INDEX idx_geom_timeseries_geom ON public.geom_timeseries USING gist (geom);


--
-- TOC entry 5365 (class 1259 OID 87511)
-- Name: idx_spatial_scales_extent; Type: INDEX; Schema: public; Owner: testuser
--

CREATE INDEX idx_spatial_scales_extent ON public.spatial_scales USING gist (extent);


--
-- TOC entry 5376 (class 1259 OID 133781)
-- Name: watts_rsp_authsuccessresponse_user_id_a77eab8f; Type: INDEX; Schema: public; Owner: testuser
--

CREATE INDEX watts_rsp_authsuccessresponse_user_id_a77eab8f ON public.watts_rsp_authsuccessresponse USING btree (user_id);


--
-- TOC entry 5377 (class 1259 OID 133782)
-- Name: watts_rsp_rsakey_key_id_c7e3dff1_like; Type: INDEX; Schema: public; Owner: testuser
--

CREATE INDEX watts_rsp_rsakey_key_id_c7e3dff1_like ON public.watts_rsp_rsakey USING btree (key_id varchar_pattern_ops);


--
-- TOC entry 5467 (class 1259 OID 134412)
-- Name: wps_gui_webprocessingservice_name_1e5801c8_like; Type: INDEX; Schema: public; Owner: testuser
--

CREATE INDEX wps_gui_webprocessingservice_name_1e5801c8_like ON public.wps_gui_webprocessingservice USING btree (name varchar_pattern_ops);


--
-- TOC entry 5505 (class 2606 OID 134157)
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5504 (class 2606 OID 134152)
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5503 (class 2606 OID 134143)
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5507 (class 2606 OID 134172)
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5506 (class 2606 OID 134167)
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5509 (class 2606 OID 134186)
-- Name: auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5508 (class 2606 OID 134181)
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5521 (class 2606 OID 134348)
-- Name: author_manage_accessrequest author_manage_access_resource_id_ebff19e3_fk_author_ma; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.author_manage_accessrequest
    ADD CONSTRAINT author_manage_access_resource_id_ebff19e3_fk_author_ma FOREIGN KEY (resource_id) REFERENCES public.author_manage_resource(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5522 (class 2606 OID 134353)
-- Name: author_manage_accessrequest author_manage_accessrequest_sender_id_bc9a3e8d_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.author_manage_accessrequest
    ADD CONSTRAINT author_manage_accessrequest_sender_id_bc9a3e8d_fk_auth_user_id FOREIGN KEY (sender_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5519 (class 2606 OID 134335)
-- Name: author_manage_deletionrequest author_manage_deleti_resource_id_bbd36a01_fk_author_ma; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.author_manage_deletionrequest
    ADD CONSTRAINT author_manage_deleti_resource_id_bbd36a01_fk_author_ma FOREIGN KEY (resource_id) REFERENCES public.author_manage_resource(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5520 (class 2606 OID 134340)
-- Name: author_manage_deletionrequest author_manage_deleti_sender_id_82f7815a_fk_auth_user; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.author_manage_deletionrequest
    ADD CONSTRAINT author_manage_deleti_sender_id_82f7815a_fk_auth_user FOREIGN KEY (sender_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5512 (class 2606 OID 134290)
-- Name: author_manage_profile author_manage_profil_metacatalogPerson_id_c3544139_fk_persons_i; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.author_manage_profile
    ADD CONSTRAINT "author_manage_profil_metacatalogPerson_id_c3544139_fk_persons_i" FOREIGN KEY ("metacatalogPerson_id") REFERENCES public.persons(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5513 (class 2606 OID 134295)
-- Name: author_manage_profile author_manage_profile_user_id_662226ec_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.author_manage_profile
    ADD CONSTRAINT author_manage_profile_user_id_662226ec_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5516 (class 2606 OID 134312)
-- Name: author_manage_resource_readers author_manage_resour_customuser_id_daf81cec_fk_auth_user; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.author_manage_resource_readers
    ADD CONSTRAINT author_manage_resour_customuser_id_daf81cec_fk_auth_user FOREIGN KEY (customuser_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5518 (class 2606 OID 134326)
-- Name: author_manage_resource_maintainers author_manage_resour_maintainer_id_819092da_fk_auth_user; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.author_manage_resource_maintainers
    ADD CONSTRAINT author_manage_resour_maintainer_id_819092da_fk_auth_user FOREIGN KEY (maintainer_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5515 (class 2606 OID 134307)
-- Name: author_manage_resource_readers author_manage_resour_resource_id_6de33a32_fk_author_ma; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.author_manage_resource_readers
    ADD CONSTRAINT author_manage_resour_resource_id_6de33a32_fk_author_ma FOREIGN KEY (resource_id) REFERENCES public.author_manage_resource(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5517 (class 2606 OID 134321)
-- Name: author_manage_resource_maintainers author_manage_resour_resource_id_96b7c96f_fk_author_ma; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.author_manage_resource_maintainers
    ADD CONSTRAINT author_manage_resour_resource_id_96b7c96f_fk_author_ma FOREIGN KEY (resource_id) REFERENCES public.author_manage_resource(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5523 (class 2606 OID 134361)
-- Name: author_manage_resource_owners author_manage_resour_resource_id_b0933f5e_fk_author_ma; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.author_manage_resource_owners
    ADD CONSTRAINT author_manage_resour_resource_id_b0933f5e_fk_author_ma FOREIGN KEY (resource_id) REFERENCES public.author_manage_resource(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5514 (class 2606 OID 134301)
-- Name: author_manage_resource author_manage_resource_dataEntry_id_7631c6c9_fk_entries_id; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.author_manage_resource
    ADD CONSTRAINT "author_manage_resource_dataEntry_id_7631c6c9_fk_entries_id" FOREIGN KEY ("dataEntry_id") REFERENCES public.entries(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5524 (class 2606 OID 134366)
-- Name: author_manage_resource_owners author_manage_resource_owners_owner_id_32e02247_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.author_manage_resource_owners
    ADD CONSTRAINT author_manage_resource_owners_owner_id_32e02247_fk_auth_user_id FOREIGN KEY (owner_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5480 (class 2606 OID 87482)
-- Name: datasources datasources_datatype_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.datasources
    ADD CONSTRAINT datasources_datatype_id_fkey FOREIGN KEY (datatype_id) REFERENCES public.datatypes(id);


--
-- TOC entry 5482 (class 2606 OID 87517)
-- Name: datasources datasources_spatial_scale_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.datasources
    ADD CONSTRAINT datasources_spatial_scale_id_fkey FOREIGN KEY (spatial_scale_id) REFERENCES public.spatial_scales(id);


--
-- TOC entry 5481 (class 2606 OID 87512)
-- Name: datasources datasources_temporal_scale_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.datasources
    ADD CONSTRAINT datasources_temporal_scale_id_fkey FOREIGN KEY (temporal_scale_id) REFERENCES public.temporal_scales(id);


--
-- TOC entry 5479 (class 2606 OID 87231)
-- Name: datasources datasources_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.datasources
    ADD CONSTRAINT datasources_type_id_fkey FOREIGN KEY (type_id) REFERENCES public.datasource_types(id);


--
-- TOC entry 5502 (class 2606 OID 87477)
-- Name: datatypes datatypes_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.datatypes
    ADD CONSTRAINT datatypes_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES public.datatypes(id);


--
-- TOC entry 5489 (class 2606 OID 87297)
-- Name: details details_entry_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.details
    ADD CONSTRAINT details_entry_id_fkey FOREIGN KEY (entry_id) REFERENCES public.entries(id);


--
-- TOC entry 5490 (class 2606 OID 87537)
-- Name: details details_thesaurus_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.details
    ADD CONSTRAINT details_thesaurus_id_fkey FOREIGN KEY (thesaurus_id) REFERENCES public.thesaurus(id);


--
-- TOC entry 5510 (class 2606 OID 134207)
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5511 (class 2606 OID 134212)
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5486 (class 2606 OID 87262)
-- Name: entries entries_datasource_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.entries
    ADD CONSTRAINT entries_datasource_id_fkey FOREIGN KEY (datasource_id) REFERENCES public.datasources(id);


--
-- TOC entry 5483 (class 2606 OID 87247)
-- Name: entries entries_latest_version_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.entries
    ADD CONSTRAINT entries_latest_version_id_fkey FOREIGN KEY (latest_version_id) REFERENCES public.entries(id);


--
-- TOC entry 5484 (class 2606 OID 87252)
-- Name: entries entries_license_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.entries
    ADD CONSTRAINT entries_license_id_fkey FOREIGN KEY (license_id) REFERENCES public.licenses(id);


--
-- TOC entry 5485 (class 2606 OID 87257)
-- Name: entries entries_variable_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.entries
    ADD CONSTRAINT entries_variable_id_fkey FOREIGN KEY (variable_id) REFERENCES public.variables(id);


--
-- TOC entry 5476 (class 2606 OID 87197)
-- Name: entrygroups entrygroups_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.entrygroups
    ADD CONSTRAINT entrygroups_type_id_fkey FOREIGN KEY (type_id) REFERENCES public.entrygroup_types(id);


--
-- TOC entry 5501 (class 2606 OID 87414)
-- Name: generic_geometry_data geneic_geometry_data_entry_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.generic_geometry_data
    ADD CONSTRAINT geneic_geometry_data_entry_id_fkey FOREIGN KEY (entry_id) REFERENCES public.entries(id);


--
-- TOC entry 5498 (class 2606 OID 87374)
-- Name: generic_1d_data generic_1d_data_entry_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.generic_1d_data
    ADD CONSTRAINT generic_1d_data_entry_id_fkey FOREIGN KEY (entry_id) REFERENCES public.entries(id);


--
-- TOC entry 5499 (class 2606 OID 87387)
-- Name: generic_2d_data generic_2d_data_entry_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.generic_2d_data
    ADD CONSTRAINT generic_2d_data_entry_id_fkey FOREIGN KEY (entry_id) REFERENCES public.entries(id);


--
-- TOC entry 5500 (class 2606 OID 87400)
-- Name: geom_timeseries geom_timeseries_entry_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.geom_timeseries
    ADD CONSTRAINT geom_timeseries_entry_id_fkey FOREIGN KEY (entry_id) REFERENCES public.entries(id);


--
-- TOC entry 5474 (class 2606 OID 87126)
-- Name: keywords keywords_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.keywords
    ADD CONSTRAINT keywords_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES public.keywords(id);


--
-- TOC entry 5475 (class 2606 OID 87461)
-- Name: keywords keywords_thesaurus_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.keywords
    ADD CONSTRAINT keywords_thesaurus_id_fkey FOREIGN KEY (thesaurus_id) REFERENCES public.thesaurus(id);


--
-- TOC entry 5487 (class 2606 OID 87274)
-- Name: nm_entrygroups nm_entrygroups_entry_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.nm_entrygroups
    ADD CONSTRAINT nm_entrygroups_entry_id_fkey FOREIGN KEY (entry_id) REFERENCES public.entries(id);


--
-- TOC entry 5488 (class 2606 OID 87279)
-- Name: nm_entrygroups nm_entrygroups_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.nm_entrygroups
    ADD CONSTRAINT nm_entrygroups_group_id_fkey FOREIGN KEY (group_id) REFERENCES public.entrygroups(id);


--
-- TOC entry 5492 (class 2606 OID 87315)
-- Name: nm_keywords_entries nm_keywords_entries_entry_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.nm_keywords_entries
    ADD CONSTRAINT nm_keywords_entries_entry_id_fkey FOREIGN KEY (entry_id) REFERENCES public.entries(id);


--
-- TOC entry 5491 (class 2606 OID 87310)
-- Name: nm_keywords_entries nm_keywords_entries_keyword_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.nm_keywords_entries
    ADD CONSTRAINT nm_keywords_entries_keyword_id_fkey FOREIGN KEY (keyword_id) REFERENCES public.keywords(id);


--
-- TOC entry 5494 (class 2606 OID 87330)
-- Name: nm_persons_entries nm_persons_entries_entry_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.nm_persons_entries
    ADD CONSTRAINT nm_persons_entries_entry_id_fkey FOREIGN KEY (entry_id) REFERENCES public.entries(id);


--
-- TOC entry 5493 (class 2606 OID 87325)
-- Name: nm_persons_entries nm_persons_entries_person_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.nm_persons_entries
    ADD CONSTRAINT nm_persons_entries_person_id_fkey FOREIGN KEY (person_id) REFERENCES public.persons(id);


--
-- TOC entry 5495 (class 2606 OID 87335)
-- Name: nm_persons_entries nm_persons_entries_relationship_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.nm_persons_entries
    ADD CONSTRAINT nm_persons_entries_relationship_type_id_fkey FOREIGN KEY (relationship_type_id) REFERENCES public.person_roles(id);


--
-- TOC entry 5497 (class 2606 OID 87361)
-- Name: timeseries_2d timeseries_2d_entry_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.timeseries_2d
    ADD CONSTRAINT timeseries_2d_entry_id_fkey FOREIGN KEY (entry_id) REFERENCES public.entries(id);


--
-- TOC entry 5496 (class 2606 OID 87348)
-- Name: timeseries timeseries_entry_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.timeseries
    ADD CONSTRAINT timeseries_entry_id_fkey FOREIGN KEY (entry_id) REFERENCES public.entries(id);


--
-- TOC entry 5478 (class 2606 OID 87215)
-- Name: variables variables_keyword_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.variables
    ADD CONSTRAINT variables_keyword_id_fkey FOREIGN KEY (keyword_id) REFERENCES public.keywords(id);


--
-- TOC entry 5477 (class 2606 OID 87210)
-- Name: variables variables_unit_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.variables
    ADD CONSTRAINT variables_unit_id_fkey FOREIGN KEY (unit_id) REFERENCES public.units(id);


--
-- TOC entry 5661 (class 0 OID 0)
-- Dependencies: 5
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

-- GRANT USAGE ON SCHEMA public TO grafanareader;
GRANT USAGE ON SCHEMA public TO testuser;


--
-- TOC entry 5694 (class 0 OID 0)
-- Dependencies: 199
-- Name: TABLE spatial_ref_sys; Type: ACL; Schema: public; Owner: testuser
--

REVOKE ALL ON TABLE public.spatial_ref_sys FROM postgres;
REVOKE SELECT ON TABLE public.spatial_ref_sys FROM PUBLIC;
GRANT SELECT ON TABLE public.spatial_ref_sys TO PUBLIC;
GRANT ALL ON TABLE public.spatial_ref_sys TO testuser;


-- Completed on 2021-02-09 08:17:28 CET

--
-- PostgreSQL database dump complete
--

