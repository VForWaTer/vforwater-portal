--
-- PostgreSQL database dump
--

-- Dumped from database version 10.6
-- Dumped by pg_dump version 10.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner:
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner:
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: postgis; Type: EXTENSION; Schema: -; Owner:
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner:
--

COMMENT ON EXTENSION postgis IS 'PostGIS geometry, geography, and raster spatial types and functions';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: lt_domain; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.lt_domain (
    id integer NOT NULL,
    pid integer,
    domain_name character varying(65) NOT NULL,
    project_id integer,
    created_on timestamp without time zone,
    updated_on timestamp without time zone
);


ALTER TABLE public.lt_domain OWNER TO testuser;

--
-- Name: lt_domain_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.lt_domain_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.lt_domain_id_seq OWNER TO testuser;

--
-- Name: lt_domain_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.lt_domain_id_seq OWNED BY public.lt_domain.id;


--
-- Name: lt_license; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.lt_license (
    id integer NOT NULL,
    license_abbrev character varying(20) NOT NULL,
    license_name character varying(255) NOT NULL,
    legal_text character varying,
    text_url character varying(255),
    access boolean NOT NULL,
    share boolean NOT NULL,
    edit boolean NOT NULL,
    commercial boolean NOT NULL,
    created_on timestamp without time zone,
    updated_on timestamp without time zone,
    CONSTRAINT lt_license_check CHECK (((legal_text IS NOT NULL) OR (text_url IS NOT NULL)))
);


ALTER TABLE public.lt_license OWNER TO testuser;

--
-- Name: lt_license_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.lt_license_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.lt_license_id_seq OWNER TO testuser;

--
-- Name: lt_license_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.lt_license_id_seq OWNED BY public.lt_license.id;


--
-- Name: lt_location; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.lt_location (
    id integer NOT NULL,
    centroid_x numeric,
    centroid_y numeric,
    srid integer,
    geometry_type character varying(15),
    created_on timestamp without time zone,
    updated_on timestamp without time zone,
    geom public.geometry NOT NULL
);


ALTER TABLE public.lt_location OWNER TO testuser;

--
-- Name: lt_location_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.lt_location_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.lt_location_id_seq OWNER TO testuser;

--
-- Name: lt_location_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.lt_location_id_seq OWNED BY public.lt_location.id;


--
-- Name: lt_project; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.lt_project (
    id integer NOT NULL,
    project_name character varying(65) NOT NULL,
    user_id integer,
    created_on timestamp without time zone,
    updated_on timestamp without time zone
);


ALTER TABLE public.lt_project OWNER TO testuser;

--
-- Name: lt_project_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.lt_project_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.lt_project_id_seq OWNER TO testuser;

--
-- Name: lt_project_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.lt_project_id_seq OWNED BY public.lt_project.id;


--
-- Name: lt_quality; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.lt_quality (
    id integer NOT NULL,
    flag_name character varying(25) NOT NULL,
    flag_weight integer,
    created_on timestamp without time zone,
    updated_on timestamp without time zone,
    CONSTRAINT lt_quality_flag_weight_check CHECK ((flag_weight >= 0)),
    CONSTRAINT lt_quality_flag_weight_check1 CHECK ((flag_weight <= 100))
);


ALTER TABLE public.lt_quality OWNER TO testuser;

--
-- Name: lt_quality_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.lt_quality_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.lt_quality_id_seq OWNER TO testuser;

--
-- Name: lt_quality_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.lt_quality_id_seq OWNED BY public.lt_quality.id;


--
-- Name: lt_site; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.lt_site (
    id integer NOT NULL,
    site_name character varying(65),
    elevation numeric,
    rel_height numeric,
    orientation_degree integer,
    slope numeric,
    landuse character varying(65),
    site_comment character varying,
    created_on timestamp without time zone,
    updated_on timestamp without time zone,
    CONSTRAINT lt_site_orientation_degree_check CHECK ((orientation_degree >= 0)),
    CONSTRAINT lt_site_orientation_degree_check1 CHECK ((orientation_degree <= 360)),
    CONSTRAINT lt_site_slope_check CHECK ((slope >= (0)::numeric)),
    CONSTRAINT lt_site_slope_check1 CHECK ((slope < (1)::numeric))
);


ALTER TABLE public.lt_site OWNER TO testuser;

--
-- Name: lt_site_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.lt_site_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.lt_site_id_seq OWNER TO testuser;

--
-- Name: lt_site_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.lt_site_id_seq OWNED BY public.lt_site.id;


--
-- Name: lt_soil; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.lt_soil (
    id integer NOT NULL,
    geology character varying(65),
    soil_type character varying(65),
    porosity numeric,
    field_capacity numeric,
    residual_moisture numeric,
    created_on timestamp without time zone,
    updated_on timestamp without time zone,
    CONSTRAINT lt_soil_check CHECK ((field_capacity > residual_moisture)),
    CONSTRAINT lt_soil_check1 CHECK ((field_capacity < porosity)),
    CONSTRAINT lt_soil_check2 CHECK ((residual_moisture < porosity)),
    CONSTRAINT lt_soil_field_capacity_check CHECK (((field_capacity < (1)::numeric) AND (field_capacity > (0)::numeric))),
    CONSTRAINT lt_soil_porosity_check CHECK (((porosity < (1)::numeric) AND (porosity > (0)::numeric))),
    CONSTRAINT lt_soil_residual_moisture_check CHECK (((residual_moisture < (1)::numeric) AND (residual_moisture > (0)::numeric)))
);


ALTER TABLE public.lt_soil OWNER TO testuser;

--
-- Name: lt_soil_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.lt_soil_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.lt_soil_id_seq OWNER TO testuser;

--
-- Name: lt_soil_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.lt_soil_id_seq OWNED BY public.lt_soil.id;


--
-- Name: lt_source_type; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.lt_source_type (
    id integer NOT NULL,
    type_name character varying(65) NOT NULL,
    created_on timestamp without time zone,
    updated_on timestamp without time zone
);


ALTER TABLE public.lt_source_type OWNER TO testuser;

--
-- Name: lt_source_type_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.lt_source_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.lt_source_type_id_seq OWNER TO testuser;

--
-- Name: lt_source_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.lt_source_type_id_seq OWNED BY public.lt_source_type.id;


--
-- Name: lt_unit; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.lt_unit (
    id integer NOT NULL,
    unit_name character varying(65) NOT NULL,
    unit_abbrev character varying(15) NOT NULL,
    unit_symbol character varying(5) NOT NULL,
    derived_si boolean,
    to_derived_si character varying,
    created_on timestamp without time zone,
    updated_on timestamp without time zone
);


ALTER TABLE public.lt_unit OWNER TO testuser;

--
-- Name: lt_unit_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.lt_unit_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.lt_unit_id_seq OWNER TO testuser;

--
-- Name: lt_unit_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.lt_unit_id_seq OWNED BY public.lt_unit.id;


--
-- Name: lt_user; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.lt_user (
    id integer NOT NULL,
    is_institution boolean NOT NULL,
    first_name character varying(65),
    last_name character varying(65),
    institution_name character varying(255),
    department character varying(255),
    email character varying(60),
    comment character varying,
    created_on timestamp without time zone,
    updated_on timestamp without time zone
);


ALTER TABLE public.lt_user OWNER TO testuser;

--
-- Name: lt_user_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.lt_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.lt_user_id_seq OWNER TO testuser;

--
-- Name: lt_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.lt_user_id_seq OWNED BY public.lt_user.id;


--
-- Name: nm_meta_domain; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.nm_meta_domain (
    meta_id integer,
    domain_id integer
);


ALTER TABLE public.nm_meta_domain OWNER TO testuser;

--
-- Name: tbl_data; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.tbl_data (
    tstamp timestamp without time zone NOT NULL,
    meta_id integer NOT NULL,
    value numeric NOT NULL
);


ALTER TABLE public.tbl_data OWNER TO testuser;

--
-- Name: tbl_data_source; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.tbl_data_source (
    id integer NOT NULL,
    source_type_id integer,
    source_path character varying NOT NULL,
    settings character varying,
    created_on timestamp without time zone,
    updated_on timestamp without time zone
);


ALTER TABLE public.tbl_data_source OWNER TO testuser;

--
-- Name: tbl_data_source_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.tbl_data_source_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tbl_data_source_id_seq OWNER TO testuser;

--
-- Name: tbl_data_source_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.tbl_data_source_id_seq OWNED BY public.tbl_data_source.id;


--
-- Name: tbl_meta; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.tbl_meta (
    id integer NOT NULL,
    ts_start timestamp without time zone,
    ts_stop timestamp without time zone,
    external_id character varying(255),
    support character varying(255),
    spacing character varying(255),
    creator_id integer,
    publisher_id integer,
    geometry_id integer,
    license_id integer,
    quality_id integer,
    site_id integer,
    soil_id integer,
    variable_id integer,
    sensor_id integer,
    source_id integer,
    comment character varying,
    created_on timestamp without time zone,
    updated_on timestamp without time zone
);


ALTER TABLE public.tbl_meta OWNER TO testuser;

--
-- Name: tbl_meta_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.tbl_meta_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tbl_meta_id_seq OWNER TO testuser;

--
-- Name: tbl_meta_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.tbl_meta_id_seq OWNED BY public.tbl_meta.id;


--
-- Name: tbl_sensor; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.tbl_sensor (
    id integer NOT NULL,
    sensor_name character varying(65),
    manufacturer character varying(255),
    documentation_url character varying,
    last_configured timestamp without time zone,
    valid_until timestamp without time zone,
    sensor_comment character varying,
    created_on timestamp without time zone,
    updated_on timestamp without time zone
);


ALTER TABLE public.tbl_sensor OWNER TO testuser;

--
-- Name: tbl_variable; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.tbl_variable (
    id integer NOT NULL,
    variable_name character varying(65) NOT NULL,
    variable_abbrev character varying(15) NOT NULL,
    variable_symbol character varying(5) NOT NULL,
    unit_id integer NOT NULL,
    created_on timestamp without time zone,
    updated_on timestamp without time zone
);


ALTER TABLE public.tbl_variable OWNER TO testuser;

--
-- Name: tbl_variable_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.tbl_variable_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tbl_variable_id_seq OWNER TO testuser;

--
-- Name: tbl_variable_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.tbl_variable_id_seq OWNED BY public.tbl_variable.id;


--
-- Name: lt_domain id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.lt_domain ALTER COLUMN id SET DEFAULT nextval('public.lt_domain_id_seq'::regclass);


--
-- Name: lt_license id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.lt_license ALTER COLUMN id SET DEFAULT nextval('public.lt_license_id_seq'::regclass);


--
-- Name: lt_location id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.lt_location ALTER COLUMN id SET DEFAULT nextval('public.lt_location_id_seq'::regclass);


--
-- Name: lt_project id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.lt_project ALTER COLUMN id SET DEFAULT nextval('public.lt_project_id_seq'::regclass);


--
-- Name: lt_quality id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.lt_quality ALTER COLUMN id SET DEFAULT nextval('public.lt_quality_id_seq'::regclass);


--
-- Name: lt_site id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.lt_site ALTER COLUMN id SET DEFAULT nextval('public.lt_site_id_seq'::regclass);


--
-- Name: lt_soil id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.lt_soil ALTER COLUMN id SET DEFAULT nextval('public.lt_soil_id_seq'::regclass);


--
-- Name: lt_source_type id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.lt_source_type ALTER COLUMN id SET DEFAULT nextval('public.lt_source_type_id_seq'::regclass);


--
-- Name: lt_unit id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.lt_unit ALTER COLUMN id SET DEFAULT nextval('public.lt_unit_id_seq'::regclass);


--
-- Name: lt_user id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.lt_user ALTER COLUMN id SET DEFAULT nextval('public.lt_user_id_seq'::regclass);


--
-- Name: tbl_data_source id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.tbl_data_source ALTER COLUMN id SET DEFAULT nextval('public.tbl_data_source_id_seq'::regclass);


--
-- Name: tbl_meta id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.tbl_meta ALTER COLUMN id SET DEFAULT nextval('public.tbl_meta_id_seq'::regclass);


--
-- Name: tbl_variable id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.tbl_variable ALTER COLUMN id SET DEFAULT nextval('public.tbl_variable_id_seq'::regclass);


--
-- Data for Name: lt_domain; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.lt_domain (id, pid, domain_name, project_id, created_on, updated_on) FROM stdin;
\.


--
-- Data for Name: lt_license; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.lt_license (id, license_abbrev, license_name, legal_text, text_url, access, share, edit, commercial, created_on, updated_on) FROM stdin;
1	GNU AGPLv3	GNU Affero General Public License v3.0	 GNU AFFERO GENERAL PUBLIC LICENSE Version 3, 19 November 2007 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/> Everyone is permitted to copy and distribute verbatim copies of this license document, but changing it is not allowed....	https://www.gnu.org/licenses/agpl-3.0.de.html	t	t	t	f	\N	\N
2	MIT License 	MIT License	MIT License Copyright (c) [year] [fullname] Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction,....	http://gamelab.mit.edu/eula/slower_eula_win.php	t	t	t	f	\N	\N
3	Beerware	THE BEER-WARE LICENSE	"THE BEER-WARE LICENSE" (Revision 42): * <phk@FreeBSD.ORG> wrote this file. As long as you retain this notice you * can do whatever you want with this stuff. If we meet some day, and you think * this stuff is worth it, you can buy me a beer in return Poul-Henning Kamp	https://people.freebsd.org/~phk/	t	t	t	f	\N	\N
\.


--
-- Data for Name: lt_location; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.lt_location (id, centroid_x, centroid_y, srid, geometry_type, created_on, updated_on, geom) FROM stdin;
1	-71.060316	48.432044	4326	POINT	2018-12-11 13:23:22.550301	2018-12-11 13:23:22.550301	0101000020E61000003CDBA337DCC351C06D37C1374D374840
2	-72.06	48.432	4326	POINT	2018-12-11 13:33:54.875212	2018-12-11 13:33:54.875212	0101000020E6100000A4703D0AD70352C09EEFA7C64B374840
3	-71.06	48.432	3857	POINT	2018-12-11 13:33:54.875212	2018-12-11 13:33:54.875212	0101000020110F0000A4703D0AD7C351C09EEFA7C64B374840
4	-74	46	4326	POINT	2018-12-11 13:33:54.875212	2018-12-11 13:33:54.875212	0101000020E610000000000000008052C00000000000004740
\.


--
-- Data for Name: lt_project; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.lt_project (id, project_name, user_id, created_on, updated_on) FROM stdin;
1	Vforwater	1	2018-12-11 13:50:24.417176	2018-12-11 13:50:24.417176
2	polariq	2	2018-12-11 13:50:24.417176	2018-12-11 13:50:24.417176
3	schnuffel	2	2018-12-11 13:50:24.417176	2018-12-11 13:50:24.417176
\.


--
-- Data for Name: lt_quality; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.lt_quality (id, flag_name, flag_weight, created_on, updated_on) FROM stdin;
1	bad	1	2018-12-12 10:09:20.580699	2018-12-12 10:09:20.580699
2	not bad	2	2018-12-12 10:09:20.580699	2018-12-12 10:09:20.580699
3	well	2	2018-12-12 10:09:20.580699	2018-12-12 10:09:20.580699
\.


--
-- Data for Name: lt_site; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.lt_site (id, site_name, elevation, rel_height, orientation_degree, slope, landuse, site_comment, created_on, updated_on) FROM stdin;
1	Mt Eddie	3501.2	78.74	\N	0.4	grasland	The place to be for getting samples	2018-12-12 10:29:12.289096	2018-12-12 10:29:12.289096
2	the cave	\N	-222	34	\N	0	you might need a torch	2018-12-12 10:29:12.289096	2018-12-12 10:29:12.289096
3	zuse-z3	2	\N	\N	0.01	treeland	sample temple	2018-12-12 10:29:12.289096	2018-12-12 10:29:12.289096
\.


--
-- Data for Name: lt_soil; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.lt_soil (id, geology, soil_type, porosity, field_capacity, residual_moisture, created_on, updated_on) FROM stdin;
1	marl	\N	\N	\N	\N	2018-12-12 10:32:32.17681	2018-12-12 10:32:32.17681
2	gneiss	volcanic soil	\N	\N	\N	2018-12-12 10:32:32.17681	2018-12-12 10:32:32.17681
3	sand	peat	\N	\N	\N	2018-12-12 10:32:32.17681	2018-12-12 10:32:32.17681
\.


--
-- Data for Name: lt_source_type; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.lt_source_type (id, type_name, created_on, updated_on) FROM stdin;
1	file path	2018-12-12 14:00:57.008317	2018-12-12 14:00:57.008317
2	file url	2018-12-12 14:00:57.008317	2018-12-12 14:00:57.008317
3	wms	2018-12-12 14:00:57.008317	2018-12-12 14:00:57.008317
\.


--
-- Data for Name: lt_unit; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.lt_unit (id, unit_name, unit_abbrev, unit_symbol, derived_si, to_derived_si, created_on, updated_on) FROM stdin;
1	centigrade	deg. C	C	f	\N	\N	\N
2	percent	pct	%	f	\N	\N	\N
3	milibar	mbar	mbar	f	\N	\N	\N
4	meter	m	m	f	\N	\N	\N
5	velocity	m/s	m/s	f	\N	\N	\N
6	hour	hr	h	f	\N	\N	\N
\.


--
-- Data for Name: lt_user; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.lt_user (id, is_institution, first_name, last_name, institution_name, department, email, comment, created_on, updated_on) FROM stdin;
1	t	Hanna	Froh	school of waldorf	tree class	hanna@hat.se	the cutest flower in the pond	2018-12-11 13:50:24.417176	2018-12-11 13:50:24.417176
2	f	Elvis	Jackson			elvis@hea.vy	Likes no music	2018-12-11 13:50:24.417176	2018-12-11 13:50:24.417176
3	t	Will	ma	Paris school of arts	wodka drawing	blue@mad.gov		2018-12-11 13:50:24.417176	2018-12-11 13:50:24.417176
4	f	nerd	lily	\N	\N	red@hat.nw	\N	2018-12-11 13:53:49.404942	2018-12-11 13:53:49.404942
\.


--
-- Data for Name: nm_meta_domain; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.nm_meta_domain (meta_id, domain_id) FROM stdin;
\.


--
-- Data for Name: spatial_ref_sys; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.spatial_ref_sys (srid, auth_name, auth_srid, srtext, proj4text) FROM stdin;
\.


--
-- Data for Name: tbl_data_source; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.tbl_data_source (id, source_type_id, source_path, settings, created_on, updated_on) FROM stdin;
1	1	tbl_data	\N	\N	\N
\.


--
-- Data for Name: tbl_meta; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.tbl_meta (id, ts_start, ts_stop, external_id, support, spacing, creator_id, publisher_id, geometry_id, license_id, quality_id, site_id, soil_id, variable_id, sensor_id, source_id, comment, created_on, updated_on) FROM stdin;
1	\N	\N	\N	\N	5min	1	2	\N	\N	\N	1	1	2	3	\N	Sap flow velocity measured	2017-06-28 15:05:52	2017-06-28 15:05:52
2	\N	\N	\N	\N	5min	2	3	1	2	3	1	2	7	4	\N	dnd - deep nose drilling	2017-06-28 15:05:52	2017-06-28 15:05:52
3	\N	\N	\N	\N	5min	3	4	2	1	2	1	2	3	2	\N	wiedavor	2017-06-28 15:05:52	2017-06-28 15:05:52
4	\N	\N	\N	\N	5min	4	1	3	1	3	3	1	4	1	\N	bigerva	2017-06-28 15:05:52	2017-06-28 15:05:52
5	\N	\N	\N	\N	5min	1	2	4	2	1	2	1	5	1	\N	nunima	2017-06-28 15:05:52	2017-06-28 15:05:52
6	\N	\N	\N	\N	5min	2	3	1	3	2	1	2	6	2	\N	hrxxxwl	2017-06-28 15:05:52	2017-06-28 15:05:52
7	\N	\N	\N	\N	5min	3	4	2	3	3	3	3	7	3	\N	diedeldiedüb	2017-06-28 15:05:52	2017-06-28 15:05:52
8	\N	\N	\N	\N	5min	4	1	3	2	1	2	2	8	4	\N	yxdocknf	2017-06-28 15:05:52	2017-06-28 15:05:52
9	\N	\N	\N	\N	15min	4	1	3	2	1	2	2	9	3	\N	txt here	2017-06-28 15:05:52	2017-06-28 15:05:52
10	\N	\N	\N	\N	5min	4	1	3	2	1	2	2	10	2	\N	fil smth in	2017-06-28 15:05:52	2017-06-28 15:05:52
11	\N	\N	\N	\N	15min	4	1	3	2	1	2	2	7	1	\N	need input	2017-06-28 15:05:52	2017-06-28 15:05:52
\.


--
-- Data for Name: tbl_sensor; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.tbl_sensor (id, sensor_name, manufacturer, documentation_url, last_configured, valid_until, sensor_comment, created_on, updated_on) FROM stdin;
1	Ddect	pauling	www.Dp.de	\N	\N	\N	\N	\N
2	bob	blop	www.Dp.bb	\N	\N	\N	\N	\N
3	fjodr	fjeul	www.wan.se	\N	\N	\N	\N	\N
4	speedo	Airhus	www.Ah.com	\N	\N	\N	\N	\N
\.


--
-- Data for Name: tbl_variable; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.tbl_variable (id, variable_name, variable_abbrev, variable_symbol, unit_id, created_on, updated_on) FROM stdin;
1	air temperature	T	T	1	\N	\N
2	realtive humidity	rel. rH	rH	2	\N	\N
3	air pressure	p	p	3	\N	\N
4	precipitation	R	R	4	\N	\N
5	terrain height	H.ü. NN	H	4	\N	\N
6	water content	Theta	Th	2	\N	\N
7	saturation	Sw	Sw	2	\N	\N
8	wind direction	D	D	1	\N	\N
9	soil temperature	T	T	1	\N	\N
10	water temperature	T	T	1	\N	\N
\.


--
-- Name: lt_domain_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.lt_domain_id_seq', 1, false);


--
-- Name: lt_license_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.lt_license_id_seq', 1, false);


--
-- Name: lt_location_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.lt_location_id_seq', 1, false);


--
-- Name: lt_project_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.lt_project_id_seq', 1, false);


--
-- Name: lt_quality_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.lt_quality_id_seq', 1, false);


--
-- Name: lt_site_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.lt_site_id_seq', 1, false);


--
-- Name: lt_soil_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.lt_soil_id_seq', 1, false);


--
-- Name: lt_source_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.lt_source_type_id_seq', 1, false);


--
-- Name: lt_unit_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.lt_unit_id_seq', 1, false);


--
-- Name: lt_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.lt_user_id_seq', 1, false);


--
-- Name: tbl_data_source_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.tbl_data_source_id_seq', 1, false);


--
-- Name: tbl_meta_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.tbl_meta_id_seq', 1, false);


--
-- Name: tbl_variable_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.tbl_variable_id_seq', 1, false);


--
-- Name: lt_domain lt_domain_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.lt_domain
    ADD CONSTRAINT lt_domain_pkey PRIMARY KEY (id);


--
-- Name: lt_license lt_license_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.lt_license
    ADD CONSTRAINT lt_license_pkey PRIMARY KEY (id);


--
-- Name: lt_location lt_location_geom_key; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.lt_location
    ADD CONSTRAINT lt_location_geom_key UNIQUE (geom);


--
-- Name: lt_location lt_location_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.lt_location
    ADD CONSTRAINT lt_location_pkey PRIMARY KEY (id);


--
-- Name: lt_project lt_project_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.lt_project
    ADD CONSTRAINT lt_project_pkey PRIMARY KEY (id);


--
-- Name: lt_quality lt_quality_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.lt_quality
    ADD CONSTRAINT lt_quality_pkey PRIMARY KEY (id);


--
-- Name: lt_site lt_site_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.lt_site
    ADD CONSTRAINT lt_site_pkey PRIMARY KEY (id);


--
-- Name: lt_soil lt_soil_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.lt_soil
    ADD CONSTRAINT lt_soil_pkey PRIMARY KEY (id);


--
-- Name: lt_source_type lt_source_type_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.lt_source_type
    ADD CONSTRAINT lt_source_type_pkey PRIMARY KEY (id);


--
-- Name: lt_source_type lt_source_type_type_name_key; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.lt_source_type
    ADD CONSTRAINT lt_source_type_type_name_key UNIQUE (type_name);


--
-- Name: lt_unit lt_unit_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.lt_unit
    ADD CONSTRAINT lt_unit_pkey PRIMARY KEY (id);


--
-- Name: lt_unit lt_unit_unit_name_key; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.lt_unit
    ADD CONSTRAINT lt_unit_unit_name_key UNIQUE (unit_name);


--
-- Name: lt_user lt_user_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.lt_user
    ADD CONSTRAINT lt_user_pkey PRIMARY KEY (id);


--
-- Name: tbl_data tbl_data_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.tbl_data
    ADD CONSTRAINT tbl_data_pkey PRIMARY KEY (tstamp, meta_id);


--
-- Name: tbl_data_source tbl_data_source_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.tbl_data_source
    ADD CONSTRAINT tbl_data_source_pkey PRIMARY KEY (id);


--
-- Name: tbl_meta tbl_meta_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.tbl_meta
    ADD CONSTRAINT tbl_meta_pkey PRIMARY KEY (id);


--
-- Name: tbl_sensor tbl_sensor_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.tbl_sensor
    ADD CONSTRAINT tbl_sensor_pkey PRIMARY KEY (id);


--
-- Name: tbl_variable tbl_variable_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.tbl_variable
    ADD CONSTRAINT tbl_variable_pkey PRIMARY KEY (id);


--
-- Name: tbl_variable tbl_variable_variable_name_key; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.tbl_variable
    ADD CONSTRAINT tbl_variable_variable_name_key UNIQUE (variable_name);


--
-- Name: idx_lt_location_geom; Type: INDEX; Schema: public; Owner: testuser
--

CREATE INDEX idx_lt_location_geom ON public.lt_location USING gist (geom);


--
-- Name: ix_lt_project_project_name; Type: INDEX; Schema: public; Owner: testuser
--

CREATE UNIQUE INDEX ix_lt_project_project_name ON public.lt_project USING btree (project_name);


--
-- Name: lt_domain lt_domain_pid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.lt_domain
    ADD CONSTRAINT lt_domain_pid_fkey FOREIGN KEY (pid) REFERENCES public.lt_domain(id);


--
-- Name: lt_domain lt_domain_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.lt_domain
    ADD CONSTRAINT lt_domain_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.lt_project(id);


--
-- Name: lt_location lt_location_srid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.lt_location
    ADD CONSTRAINT lt_location_srid_fkey FOREIGN KEY (srid) REFERENCES public.spatial_ref_sys(srid);


--
-- Name: lt_project lt_project_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.lt_project
    ADD CONSTRAINT lt_project_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.lt_user(id);


--
-- Name: nm_meta_domain nm_meta_domain_domain_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.nm_meta_domain
    ADD CONSTRAINT nm_meta_domain_domain_id_fkey FOREIGN KEY (domain_id) REFERENCES public.lt_domain(id);


--
-- Name: nm_meta_domain nm_meta_domain_meta_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.nm_meta_domain
    ADD CONSTRAINT nm_meta_domain_meta_id_fkey FOREIGN KEY (meta_id) REFERENCES public.tbl_meta(id);


--
-- Name: tbl_data tbl_data_meta_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.tbl_data
    ADD CONSTRAINT tbl_data_meta_id_fkey FOREIGN KEY (meta_id) REFERENCES public.tbl_meta(id);


--
-- Name: tbl_data_source tbl_data_source_source_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.tbl_data_source
    ADD CONSTRAINT tbl_data_source_source_type_id_fkey FOREIGN KEY (source_type_id) REFERENCES public.lt_source_type(id);


--
-- Name: tbl_meta tbl_meta_creator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.tbl_meta
    ADD CONSTRAINT tbl_meta_creator_id_fkey FOREIGN KEY (creator_id) REFERENCES public.lt_user(id);


--
-- Name: tbl_meta tbl_meta_geometry_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.tbl_meta
    ADD CONSTRAINT tbl_meta_geometry_id_fkey FOREIGN KEY (geometry_id) REFERENCES public.lt_location(id);


--
-- Name: tbl_meta tbl_meta_license_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.tbl_meta
    ADD CONSTRAINT tbl_meta_license_id_fkey FOREIGN KEY (license_id) REFERENCES public.lt_license(id);


--
-- Name: tbl_meta tbl_meta_publisher_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.tbl_meta
    ADD CONSTRAINT tbl_meta_publisher_id_fkey FOREIGN KEY (publisher_id) REFERENCES public.lt_user(id);


--
-- Name: tbl_meta tbl_meta_quality_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.tbl_meta
    ADD CONSTRAINT tbl_meta_quality_id_fkey FOREIGN KEY (quality_id) REFERENCES public.lt_quality(id);


--
-- Name: tbl_meta tbl_meta_sensor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.tbl_meta
    ADD CONSTRAINT tbl_meta_sensor_id_fkey FOREIGN KEY (sensor_id) REFERENCES public.tbl_sensor(id);


--
-- Name: tbl_meta tbl_meta_site_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.tbl_meta
    ADD CONSTRAINT tbl_meta_site_id_fkey FOREIGN KEY (site_id) REFERENCES public.lt_site(id);


--
-- Name: tbl_meta tbl_meta_soil_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.tbl_meta
    ADD CONSTRAINT tbl_meta_soil_id_fkey FOREIGN KEY (soil_id) REFERENCES public.lt_soil(id);


--
-- Name: tbl_meta tbl_meta_source_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.tbl_meta
    ADD CONSTRAINT tbl_meta_source_id_fkey FOREIGN KEY (source_id) REFERENCES public.tbl_data_source(id);


--
-- Name: tbl_meta tbl_meta_variable_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.tbl_meta
    ADD CONSTRAINT tbl_meta_variable_id_fkey FOREIGN KEY (variable_id) REFERENCES public.tbl_variable(id);


--
-- Name: tbl_variable tbl_variable_unit_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.tbl_variable
    ADD CONSTRAINT tbl_variable_unit_id_fkey FOREIGN KEY (unit_id) REFERENCES public.lt_unit(id);


--
-- PostgreSQL database dump complete
--
